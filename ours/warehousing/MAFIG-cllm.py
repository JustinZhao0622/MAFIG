"""Run the MAFIG two-stage framework with remote GLM calls."""

import ast
import asyncio
import json
import logging
import os
import re
import shutil
import textwrap
import time

from zai import ZhipuAiClient

import prompts as prompts_mod
import review_code


DATASET_FILE = "datasets/test.json"
BASE_OUT_DIR = "MAFIG-cllm"
MODEL_NAME = "glm-4.7"
TEMPERATURE = 0.9
TOP_P = 0.95
MAX_RETRIES = 5
RETRY_DELAY = 1
REQUEST_COOLDOWN_SECONDS = 10
PER_KEY_CONCURRENCY = 1
COMMON_IMPORTS = "import heapq\nimport time\nimport random"

DEFAULT_API_KEYS = [
    "90c6d629ee25d69f65fb4c0a19181306.5tIohk21Q4JRoQCj",
]


os.makedirs(BASE_OUT_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=os.path.join(BASE_OUT_DIR, "MAFIG-cllm.log"),
    filemode="a+",
)
logger = logging.getLogger(__name__)


def load_api_keys() -> list[str]:
    return DEFAULT_API_KEYS


def read_dataset() -> list[dict]:
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_run_dir(run_dir: str) -> None:
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(os.path.join(run_dir, "results"), exist_ok=True)


def extract_fenced_code(text: str) -> str | None:
    blocks = re.findall(
        r"```(?:python|py)?\s*([\s\S]*?)```",
        text,
        flags=re.IGNORECASE,
    )
    return blocks[0].strip() if blocks else None


def strip_to_code_start(text: str) -> str:
    lines = text.strip().splitlines()
    code_prefixes = ("import ", "from ", "def ", "async def ", "class ", "@")

    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(code_prefixes):
            return "\n".join(lines[idx:]).strip()
        if stripped.startswith(('"""', "'''")):
            lookahead = lines[idx + 1 : idx + 12]
            if any(next_line.lstrip().startswith(code_prefixes) for next_line in lookahead):
                return "\n".join(lines[idx:]).strip()
    return text.strip()


def trim_to_parseable_python(text: str) -> str:
    lines = text.strip().splitlines()
    for end in range(len(lines), 0, -1):
        candidate = "\n".join(lines[:end]).strip()
        if "def " not in candidate:
            continue
        try:
            ast.parse(candidate)
        except SyntaxError:
            continue
        return candidate
    return text.strip()


def clean_code_block(text: str) -> str:
    code = extract_fenced_code(text) or text
    code = code.replace("```python", "").replace("```py", "").replace("```", "")
    code = strip_to_code_start(code)
    code = trim_to_parseable_python(code)
    return code.strip()


def strip_common_imports(code: str) -> str:
    lines = []
    for line in code.splitlines():
        stripped = line.strip()
        if stripped in {"import heapq", "import time", "import random"}:
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def extract_function_code(raw_text: str, function_name: str) -> str:
    code = clean_code_block(raw_text)
    lines = code.splitlines()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return textwrap.dedent(strip_common_imports(code)).strip()

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == function_name and getattr(node, "end_lineno", None):
                start = node.lineno - 1
                end = node.end_lineno
                return textwrap.dedent("\n".join(lines[start:end])).strip()
    return textwrap.dedent(strip_common_imports(code)).strip()


def parse_function_list(raw_text: str) -> list[str]:
    if not raw_text:
        return []

    candidates = []
    fenced = extract_fenced_code(raw_text)
    if fenced:
        candidates.append(fenced)
    candidates.append(raw_text.strip())

    for candidate in candidates:
        match = re.search(r"\[[\s\S]*?\]", candidate)
        if not match:
            continue
        list_text = match.group(0).strip()
        try:
            parsed = ast.literal_eval(list_text)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except Exception:
            pass

        body = list_text[1:-1].strip()
        if not body:
            return []
        items = []
        for part in body.split(","):
            value = part.strip().strip("'").strip('"').strip()
            if value:
                items.append(value)
        if items:
            return items
    return []


def normalize_function_list(functions: list[str], expected_len: int) -> list[str]:
    valid_names = set(prompts_mod.functions_mapping.keys()) | {"None", "none", ""}
    normalized = []
    for item in functions[:expected_len]:
        value = str(item).strip()
        if value not in valid_names:
            value = "None"
        if value.lower() == "none" or value == "":
            value = "None"
        normalized.append(value)
    while len(normalized) < expected_len:
        normalized.append("None")
    return normalized


def split_events(event_text: str) -> list[str]:
    return [event.strip() for event in event_text.split(";") if event.strip()]


def _sync_chat(
    job_id: int,
    client: ZhipuAiClient,
    messages: list[dict],
    stage: str,
) -> tuple[str, float]:
    print(f"[{stage} idx={job_id}] start")
    started_at = time.time()
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                messages=messages,
            )
            print(f"[{stage} idx={job_id}] done")
            return resp.choices[0].message.content or "", time.time() - started_at
        except Exception as err:
            last_err = err
            print(
                f"[{stage} idx={job_id}] error: {err}, "
                f"retry {attempt + 1}/{MAX_RETRIES}"
            )
            if attempt < MAX_RETRIES - 1:
                time.sleep(10)
    print(f"[{stage} idx={job_id}] failed, last error: {last_err}")
    return "", time.time() - started_at


async def _call_model(job_id: int, client: ZhipuAiClient, messages: list[dict], stage: str):
    content, request_elapsed = await asyncio.to_thread(
        _sync_chat,
        job_id,
        client,
        messages,
        stage,
    )
    return job_id, content, request_elapsed


async def _key_worker(
    key_id: int,
    client: ZhipuAiClient,
    jobs: list[tuple[int, list[dict]]],
    stage: str,
    concurrency: int = PER_KEY_CONCURRENCY,
) -> tuple[float, dict[int, str]]:
    sem = asyncio.Semaphore(concurrency)
    results = {}
    processing_elapsed = 0.0

    async def _run_one(job_id: int, messages: list[dict]) -> None:
        nonlocal processing_elapsed
        async with sem:
            result_id, content, request_elapsed = await _call_model(
                job_id,
                client,
                messages,
                stage,
            )
            results[result_id] = content
            processing_elapsed += request_elapsed
            if REQUEST_COOLDOWN_SECONDS > 0:
                print(
                    f"[{stage} idx={job_id}] cooldown "
                    f"{REQUEST_COOLDOWN_SECONDS}s"
                )
                await asyncio.sleep(REQUEST_COOLDOWN_SECONDS)

    wall_started_at = time.time()
    await asyncio.gather(*[_run_one(job_id, messages) for job_id, messages in jobs])
    wall_elapsed = time.time() - wall_started_at
    print(
        f"[{stage} key={key_id}] processing: {processing_elapsed:.2f}s, "
        f"wall: {wall_elapsed:.2f}s"
    )
    return processing_elapsed, results


async def run_glm_batch(
    jobs: list[tuple[int, list[dict]]],
    stage: str,
) -> tuple[float, dict[int, str]]:
    if not jobs:
        return 0.0, {}

    api_keys = load_api_keys()
    clients = [ZhipuAiClient(api_key=key) for key in api_keys]
    buckets = [[] for _ in clients]
    for offset, job in enumerate(jobs):
        buckets[offset % len(clients)].append(job)

    worker_results = await asyncio.gather(
        *[
            _key_worker(key_id, clients[key_id], buckets[key_id], stage)
            for key_id in range(len(clients))
            if buckets[key_id]
        ]
    )

    total_processing = 0.0
    merged_results = {}
    for elapsed, results in worker_results:
        total_processing += elapsed
        merged_results.update(results)
    return total_processing, merged_results


async def perception_agent(run_dir: str) -> float:
    emergency_situations = read_dataset()
    jobs = []

    for idx, emergency_situation in enumerate(emergency_situations):
        events = split_events(emergency_situation["emergency_situation"])
        messages = [
            {"role": "system", "content": prompts_mod.perception_system_prompt},
            {
                "role": "user",
                "content": prompts_mod.perception_user_prompt.format(
                    EMERGENCY_SITUATIONS=emergency_situation["emergency_situation"],
                    nums=len(events),
                ),
            },
        ]
        jobs.append((idx, messages))

    elapsed, raw_outputs = await run_glm_batch(jobs, "perception")

    for idx, emergency_situation in enumerate(emergency_situations):
        expected_len = len(emergency_situation.get("functions", []))
        if expected_len == 0:
            expected_len = len(split_events(emergency_situation["emergency_situation"]))

        raw_text = raw_outputs.get(idx, "")
        parsed = parse_function_list(raw_text)
        if len(parsed) != expected_len:
            print(
                f"[perception idx={idx}] warning: expected {expected_len} functions, "
                f"got {len(parsed)}; normalized"
            )
        emergency_situation["perception_raw_output"] = raw_text
        emergency_situation["perception_functions"] = normalize_function_list(
            parsed,
            expected_len,
        )

    with open(os.path.join(run_dir, "perception_events.json"), "w", encoding="utf-8") as f:
        json.dump(emergency_situations, f, ensure_ascii=False, indent=4)
    return elapsed


def build_decision_jobs(emergency_situations: list[dict]):
    jobs = []
    record_task_ids = [[] for _ in emergency_situations]
    task_meta = {}
    task_id = 0

    for record_idx, emergency_situation in enumerate(emergency_situations):
        events = split_events(emergency_situation["emergency_situation"])
        expected_functions = emergency_situation.get("functions", [])
        perception_functions = emergency_situation.get("perception_functions", [])
        real_events = []
        real_functions = []

        for event_idx, event in enumerate(events):
            expected_fn = (
                expected_functions[event_idx]
                if event_idx < len(expected_functions)
                else "None"
            )
            perceived_fn = (
                perception_functions[event_idx]
                if event_idx < len(perception_functions)
                else "None"
            )
            if expected_fn == perceived_fn and perceived_fn != "None":
                real_events.append(event)
                real_functions.append(perceived_fn)

        fn_to_events = {}
        fn_order = []
        for event, fn in zip(real_events, real_functions):
            if fn not in fn_to_events:
                fn_order.append(fn)
                fn_to_events[fn] = []
            fn_to_events[fn].append(event)

        for fn in fn_order:
            merged_event = ";".join(fn_to_events[fn])
            messages = [
                {"role": "system", "content": prompts_mod.SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompts_mod.USER_PROMPT.format(
                        EMERGENCY_SITUATIONS=merged_event,
                        ORIGINAL_CODE=prompts_mod.functions_mapping[fn],
                    ),
                },
            ]
            jobs.append((task_id, messages))
            record_task_ids[record_idx].append(task_id)
            task_meta[task_id] = {"record_idx": record_idx, "function": fn}
            task_id += 1

    return jobs, record_task_ids, task_meta


async def decision_agent(run_dir: str) -> float:
    with open(os.path.join(run_dir, "perception_events.json"), "r", encoding="utf-8") as f:
        emergency_situations = json.load(f)

    jobs, record_task_ids, task_meta = build_decision_jobs(emergency_situations)
    elapsed, raw_outputs = await run_glm_batch(jobs, "decision")

    result_dir = os.path.join(run_dir, "results")
    os.makedirs(result_dir, exist_ok=True)

    for record_idx, task_ids in enumerate(record_task_ids):
        fragments = []
        for task_id in task_ids:
            fn = task_meta[task_id]["function"]
            raw_text = raw_outputs.get(task_id, "")
            fragment = extract_function_code(raw_text, fn)
            if fragment:
                fragments.append(fragment)

        if fragments:
            result = COMMON_IMPORTS + "\n\n" + "\n\n".join(fragments).strip() + "\n"
        else:
            result = prompts_mod.ORIGINAL_CODE.strip() + "\n"

        with open(
            os.path.join(result_dir, f"result_{record_idx + 1}.py"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(result)

    return elapsed


async def main() -> None:
    run_dir = os.path.join(BASE_OUT_DIR, MODEL_NAME)
    prepare_run_dir(run_dir)

    start_time = time.time()
    perception_time = await perception_agent(run_dir)
    decision_time = await decision_agent(run_dir)
    wall_time = time.time() - start_time
    accuracy = review_code.main(DATASET_FILE, os.path.join(run_dir, "results"))

    logger.info(
        "model=%s, perception_time=%.2fs, decision_time=%.2fs, "
        "wall_time=%.2fs, accuracy=%.4f, out_dir=%s",
        MODEL_NAME,
        perception_time,
        decision_time,
        wall_time,
        accuracy,
        run_dir,
    )
    print(
        f"model={MODEL_NAME}, perception_time={perception_time:.2f}s, "
        f"decision_time={decision_time:.2f}s, wall_time={wall_time:.2f}s, "
        f"accuracy={accuracy:.4f}, out_dir={run_dir}"
    )


if __name__ == "__main__":
    asyncio.run(main())
