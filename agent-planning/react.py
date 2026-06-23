from __future__ import annotations

import datetime as dt
import importlib.util
import json
import multiprocessing
import random
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


MODEL_PATH = "/data/huggingface/Qwen2.5-Coder-7B-Instruct"
SCENES = ["deck"]  # port, warehousing, deck
LIMIT_PER_SCENE: Optional[int] = None
OFFSET_PER_SCENE = 0
SHUFFLE = False
SEED = 233

MAX_REVIEW_ROUNDS = 3
BATCH_SIZE: Optional[int] = None
VERIFY_TIMEOUT = 5
TEMPERATURE = 0.0
TOP_P = 0.95
MAX_TOKENS = 5000
GPU_MEMORY_UTILIZATION = 0.9
DTYPE = "auto"
DEVICE = "cuda"
VERBOSE = True

OUT_DIR = "./agent-planning/results"


ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = ROOT / "datasets"
RESULTS_DIR = ROOT / "results"

SYSTEM_PROMPT = """你是一名【突发事件应对与调度系统重构专家】，专门负责在给定突发事件约束下，
对既有调度代码进行【最小必要修改】，以恢复系统的可运行性与逻辑一致性。

你必须严格遵守以下所有规则，任何一条违反都视为失败：

【任务目标】
- 基于给定的突发事件描述，仅对现有代码中的逻辑进行必要调整
- 使系统在当前突发条件下可以正确执行，不允许规避问题或简化处理

【修改范围与限制】
1. 只能修改【已有函数的函数体内部逻辑】
   - 严禁新增函数
   - 严禁删除函数
   - 严禁修改函数名、参数列表、返回值形式

2. 严禁修改、删除或新增任何 import 语句
   - 必须从原始代码中原样复制 import 部分

3. 不允许通过以下方式“绕过”问题：
   - 直接 return / pass 跳过核心逻辑
   - 硬编码结果
   - 删除关键调度步骤
   - 捕获异常但不处理真实冲突

【突发事件约束】
4. 突发事件描述是【唯一可信事实来源】
   - 不允许引入任何未明确给出的新故障、新延迟或新假设
   - 不允许“合理推测”额外事件

当你被要求输出代码时：
5. 仅返回【修改后的完整 Python 代码】
   - 必须包含 import 语句
   - 不允许 markdown 代码块
   - 不允许解释、示例、省略号、占位文本或多余文本
"""

INITIAL_THINK_PROMPT = """这是第 1 轮。请先根据突发事件思考自己应该如何修改代码。
本轮只输出修改思路，不要输出 Python 代码。随后系统会要求你基于这个思路再次生成完整解决方案代码。

SCENE:
{SCENE}

EMERGENCY_SITUATIONS:
{EMERGENCY_SITUATIONS}

CODE:
{CODE}
"""

FEEDBACK_THINK_PROMPT = """这是第 {ROUND} 轮修复。上一版代码没有完全通过 review。
请基于突发事件、完整历史对话、上一版代码和 review 反馈，先思考下一步应该如何修改。
本轮只输出修改思路，不要输出 Python 代码。随后系统会要求你再次生成完整解决方案代码。

SCENE:
{SCENE}

EMERGENCY_SITUATIONS:
{EMERGENCY_SITUATIONS}

REVIEW_FEEDBACK:
{REVIEW_FEEDBACK}

CODE:
{CODE}
"""

CODE_USER_PROMPT = """现在请再次根据突发事件、上面的修改思路和完整历史对话，生成解决方案。

只输出修改后的完整 Python 代码：
- 必须包含 import 语句
- 不允许 markdown 代码块
- 不允许解释、示例、省略号、占位文本或多余文本
"""


@dataclass
class CaseState:
    case_no: int
    scene: str
    dataset_index: int
    emergency_situation: str
    gold_functions: List[str]
    original_code: str
    result_path: Path
    started: float
    current_code: str = ""
    feedback: str = ""
    solved: int = 0
    total: int = 0
    verify_status: str = "not_run"
    done: bool = False
    rounds: int = 0
    raw_last: str = ""
    thoughts: List[str] = field(default_factory=list)
    messages: List[Dict[str, str]] = field(default_factory=list)
    stage_logs: List[Dict[str, Any]] = field(default_factory=list)
    attempts: List[Dict[str, Any]] = field(default_factory=list)


class LocalVLLMClient:
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
        self.llm = LLM(
            model=MODEL_PATH,
            device=DEVICE,
            dtype=DTYPE,
            trust_remote_code=True,
            gpu_memory_utilization=GPU_MEMORY_UTILIZATION,
        )

    def generate_many(self, inputs: Sequence[str]) -> List[str]:
        params = SamplingParams(
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_TOKENS,
        )
        outputs = self.llm.generate(list(inputs), params)
        return [output.outputs[0].text for output in outputs]


def load_dataset(scene: str) -> List[Dict[str, Any]]:
    return json.loads((DATASETS_DIR / scene / "test.json").read_text(encoding="utf-8"))


def load_function_code(scene: str) -> str:
    return (DATASETS_DIR / scene / "functions.py").read_text(encoding="utf-8")


def split_events(text: str) -> List[str]:
    return [part.strip() for part in text.strip().split(";") if part.strip()]


def build_inputs(tokenizer: Any, states: Sequence[CaseState]) -> List[str]:
    inputs = []
    for state in states:
        text = tokenizer.apply_chat_template(
            state.messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs.append(text)
    return inputs


def clean_code_output(text: str) -> str:
    stripped = text.strip()
    match = re.search(r"```(?:python)?\s*([\s\S]*?)```", stripped)
    code = match.group(1).strip() if match else stripped
    return code + "\n"


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def verify_worker(scene: str, file_path: str, events: Sequence[str], queue: multiprocessing.Queue) -> None:
    module = load_module(DATASETS_DIR / scene / "review_code.py", f"{scene}_review_code")
    result: Dict[str, Any] = {}
    module.run_verify_case(file_path, list(events), result)
    queue.put(result)


def run_scene_verifier(scene: str, file_path: Path, events: Sequence[str]) -> Dict[str, Any]:
    queue: multiprocessing.Queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=verify_worker,
        args=(scene, str(file_path), list(events), queue),
    )
    process.start()
    process.join(VERIFY_TIMEOUT)
    if process.is_alive():
        process.terminate()
        process.join()
        return {"timeout": True, "result": {"total": len(events), "solved": 0, "unsolved": list(events)}}
    if queue.empty():
        return {"error": "review 子进程没有返回结果"}
    return queue.get()


def verification_counts(result: Dict[str, Any], events: Sequence[str]) -> Tuple[int, int, str]:
    if result.get("timeout"):
        return 0, len(events), "timeout"
    if "error" in result:
        return 0, len(events), "error"
    data = result.get("result", {})
    solved = data.get("solved", 0)
    total = data.get("total", len(events))
    return int(solved) if isinstance(solved, int) else 0, int(total) if isinstance(total, int) else len(events), "ok"


def compact_review_feedback(result: Dict[str, Any], events: Sequence[str]) -> str:
    solved, total, status = verification_counts(result, events)
    if status == "timeout":
        return f"review 超时，当前解决 {solved}/{total} 个事件。请简化代码并继续修复所有突发事件。"
    if status == "error":
        return f"代码运行失败，当前解决 0/{total} 个事件。错误信息：{result['error']}"

    unsolved = result.get("result", {}).get("unsolved", [])
    if not unsolved:
        return f"review 通过 {solved}/{total}"

    rows = []
    for item in unsolved[:8]:
        if isinstance(item, dict):
            rows.append(f"- {item.get('function', 'unknown')}: {item.get('event', '')}")
        elif isinstance(item, (list, tuple)) and item:
            rows.append(f"- {item[0]}")
        else:
            rows.append(f"- {item}")
    return f"review 通过 {solved}/{total}，仍未解决：\n" + "\n".join(rows)


def iter_cases() -> List[Tuple[str, int, Dict[str, Any]]]:
    cases = []
    for scene in SCENES:
        scene_cases = [(scene, idx, item) for idx, item in enumerate(load_dataset(scene))]
        if SHUFFLE:
            scene_offset = sum((i + 1) * ord(ch) for i, ch in enumerate(scene))
            random.Random(SEED + scene_offset).shuffle(scene_cases)
        scene_cases = scene_cases[OFFSET_PER_SCENE:]
        if LIMIT_PER_SCENE is not None:
            scene_cases = scene_cases[:LIMIT_PER_SCENE]
        cases.extend(scene_cases)
    return cases


def batch_items(items: Sequence[CaseState]) -> List[Sequence[CaseState]]:
    if BATCH_SIZE is None or BATCH_SIZE <= 0:
        return [items] if items else []
    return [items[idx:idx + BATCH_SIZE] for idx in range(0, len(items), BATCH_SIZE)]


def output_run_dir() -> Path:
    if OUT_DIR:
        path = Path(OUT_DIR)
        return path if path.is_absolute() else ROOT / path
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    return RESULTS_DIR / f"react_review_loop_{timestamp}"


def build_states(run_dir: Path) -> List[CaseState]:
    source_cache = {scene: load_function_code(scene) for scene in SCENES}
    states = []
    for case_no, (scene, idx, item) in enumerate(iter_cases(), 1):
        state = CaseState(
            case_no=case_no,
            scene=scene,
            dataset_index=idx,
            emergency_situation=item["emergency_situation"],
            gold_functions=[str(name) for name in item["functions"]],
            original_code=source_cache[scene],
            result_path=run_dir / scene / f"result_{idx + 1}.py",
            started=time.time(),
        )
        state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": INITIAL_THINK_PROMPT.format(
                    SCENE=state.scene,
                    EMERGENCY_SITUATIONS=state.emergency_situation,
                    CODE=state.original_code,
                ),
            },
        ]
        states.append(state)
    return states


def append_next_round_prompt(state: CaseState, round_idx: int) -> None:
    state.messages.append(
        {
            "role": "user",
            "content": FEEDBACK_THINK_PROMPT.format(
                ROUND=round_idx,
                SCENE=state.scene,
                EMERGENCY_SITUATIONS=state.emergency_situation,
                REVIEW_FEEDBACK=state.feedback,
                CODE=state.current_code,
            )
        }
    )


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run_round(client: LocalVLLMClient, states: Sequence[CaseState], round_idx: int) -> None:
    active = [state for state in states if not state.done]
    for group in batch_items(active):
        think_inputs = build_inputs(client.tokenizer, group)
        thoughts = client.generate_many(think_inputs)
        for state, model_input, thought in zip(group, think_inputs, thoughts):
            state.thoughts.append(thought)
            state.stage_logs.append(
                {
                    "round": round_idx,
                    "stage": "think",
                    "input": model_input,
                    "output": thought,
                }
            )
            state.messages.append({"role": "assistant", "content": thought})
            state.messages.append({"role": "user", "content": CODE_USER_PROMPT})

        code_inputs = build_inputs(client.tokenizer, group)
        outputs = client.generate_many(code_inputs)
        for state, model_input, raw in zip(group, code_inputs, outputs):
            code = clean_code_output(raw)
            state.current_code = code
            state.raw_last = raw
            state.rounds = round_idx
            state.stage_logs.append(
                {
                    "round": round_idx,
                    "stage": "code",
                    "input": model_input,
                    "output": raw,
                }
            )
            state.messages.append({"role": "assistant", "content": raw})
            state.result_path.parent.mkdir(parents=True, exist_ok=True)
            state.result_path.write_text(code, encoding="utf-8")

            events = split_events(state.emergency_situation)
            verify_result = run_scene_verifier(state.scene, state.result_path, events)
            solved, total, verify_status = verification_counts(verify_result, events)
            state.solved = solved
            state.total = total
            state.verify_status = verify_status
            state.feedback = compact_review_feedback(verify_result, events)
            state.done = solved == total and total > 0
            state.attempts.append(
                {
                    "round": round_idx,
                    "thought": state.thoughts[-1] if state.thoughts else "",
                    "solved": solved,
                    "total": total,
                    "verify_status": verify_status,
                    "feedback": state.feedback,
                }
            )
            if not state.done and round_idx < MAX_REVIEW_ROUNDS:
                append_next_round_prompt(state, round_idx + 1)

            if VERBOSE:
                status = "SOLVED" if state.done else "MISS"
                print(f"[ROUND {round_idx}][{status}] {state.scene}#{state.dataset_index + 1}: solved={solved}/{total}")


def finalize_records(states: Sequence[CaseState]) -> List[Dict[str, Any]]:
    records = []
    for state in states:
        records.append(
            {
                "case_no": state.case_no,
                "scene": state.scene,
                "dataset_index": state.dataset_index,
                "emergency_situation": state.emergency_situation,
                "gold_functions": state.gold_functions,
                "code_path": str(state.result_path),
                "solved": state.solved,
                "total": state.total,
                "solve_rate": state.solved / max(state.total, 1),
                "verify_status": state.verify_status,
                "rounds": state.rounds,
                "feedback": state.feedback,
                "thoughts": state.thoughts,
                "messages": state.messages,
                "stage_logs": state.stage_logs,
                "attempts": state.attempts,
                "raw": state.raw_last,
                "latency_sec": time.time() - state.started,
            }
        )
    return records


def build_model_io(records: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "case_no": record["case_no"],
            "scene": record["scene"],
            "dataset_index": record["dataset_index"],
            "emergency_situation": record["emergency_situation"],
            "stages": record["stage_logs"],
        }
        for record in records
    ]


def summarize(records: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    rows = []
    for scene in ["all"] + sorted({record["scene"] for record in records}):
        items = records if scene == "all" else [record for record in records if record["scene"] == scene]
        if not items:
            continue
        cases = len(items)
        solved = sum(record["solved"] for record in items)
        total = sum(record["total"] for record in items)
        rows.append(
            {
                "scene": scene,
                "cases": cases,
                "case_solve_rate": sum(record["solved"] == record["total"] for record in items) / cases,
                "event_solve_rate": solved / max(total, 1),
                "avg_rounds": sum(record["rounds"] for record in items) / cases,
                "verify_errors": sum(record["verify_status"] != "ok" for record in items),
                "avg_latency_sec": sum(record["latency_sec"] for record in items) / cases,
            }
        )
    return {"react_review_loop": rows}


def print_summary(summary: Dict[str, Any]) -> None:
    print("\nscene         cases  case_solve  event_solve  avg_rounds  verify_err  avg_latency")
    print("------------  -----  ----------  -----------  ----------  ----------  -----------")
    for row in summary["react_review_loop"]:
        print(
            f"{row['scene']:<12}  {row['cases']:>5}  {row['case_solve_rate']:.4f}      "
            f"{row['event_solve_rate']:.4f}       {row['avg_rounds']:>10.2f}  "
            f"{row['verify_errors']:>10}  {row['avg_latency_sec']:>11.2f}"
        )


def main() -> int:
    started = time.time()
    run_dir = output_run_dir()
    states = build_states(run_dir)
    client = LocalVLLMClient()

    for round_idx in range(1, MAX_REVIEW_ROUNDS + 1):
        active_count = sum(not state.done for state in states)
        if active_count == 0:
            break
        if VERBOSE:
            print(f"[ROUND {round_idx}] active={active_count}")
        run_round(client, states, round_idx)

    records = finalize_records(states)
    records_path = run_dir / f"{SCENES[0]}_records.jsonl"
    write_jsonl(records_path, records)
    model_io_path = run_dir / f"{SCENES[0]}_model_io.json"
    write_json(model_io_path, build_model_io(records))
    summary = summarize(records)
    summary_path = run_dir / f"{SCENES[0]}_summary.json"
    write_json(summary_path, summary)
    print_summary(summary)
    print(f"\nrecords: {records_path}")
    print(f"model_io: {model_io_path}")
    print(f"summary: {summary_path}")
    print(f"time_taken_sec: {time.time() - started:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())