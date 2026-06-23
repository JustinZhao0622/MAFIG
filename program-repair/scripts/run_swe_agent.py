#!/usr/bin/env python3
"""
Run code-editing tasks with direct local-vLLM code generation.

This runner does not use mini-swe-agent. The model gets three rounds. In each
round it receives the current functions.py plus structured review feedback from
the previous round, returns a complete replacement functions.py, and this script
writes and reviews it.
"""

from __future__ import annotations

import ast
import gc
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


ROOT = Path(__file__).resolve().parents[2]
CODE_EDITING_DIR = ROOT / "code-editing"
TASKS_FILE = CODE_EDITING_DIR / "tasks.jsonl"
OUTPUT_DIR = CODE_EDITING_DIR / "outputs" / "mini-swe-agent"
WORKDIR_ROOT = OUTPUT_DIR / "workdirs"
RUNS_ROOT = OUTPUT_DIR / "runs"
RECORDS_FILE = OUTPUT_DIR / "records.jsonl"
CONFIG_HOME = CODE_EDITING_DIR / ".config"

os.environ.setdefault("XDG_CONFIG_HOME", str(CONFIG_HOME))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

LIMIT: Optional[int] = None
SKIP_EXISTING = False
VERIFY_TIMEOUT = 20
PYTHON_BIN = sys.executable

MODEL_NAME = "Qwen2.5-Coder-7B-Instruct"
MODEL_PATH = "/data/huggingface/Qwen2.5-Coder-7B-Instruct"
DTYPE = "auto"
DEVICE = "cuda"
TRUST_REMOTE_CODE = True
GPU_MEMORY_UTILIZATION = 0.9
TENSOR_PARALLEL_SIZE = 1
MAX_MODEL_LEN: Optional[int] = None

MAX_REPAIR_ROUNDS = 3
BATCH_SIZE: Optional[int] = None
TEMPERATURE = 0.0
TOP_P = 0.95
MAX_MODEL_TOKENS = 8000

SYSTEM_PROMPT = """你是一名代码修复器，专门根据突发事件修改 functions.py。

硬性规则：
1. 只能输出修改后的完整 Python 文件内容。
2. 不允许输出 Markdown 代码块，不允许解释，不允许 bash，不允许省略号。
3. 必须保留原始 import 语句，不能新增、删除或修改 import。
4. 只能修改已有函数的函数体逻辑；不能新增函数，不能删除函数，不能修改函数名、参数列表或返回值形式。
5. 不允许直接 return/pass 跳过核心逻辑，不允许硬编码 verifier 输出。
"""

USER_PROMPT_TEMPLATE = """场景：
{scene}

突发事件：
{emergency_situation}

Review/验证语义：
- review 会逐条检查每个突发事件是否被解决。
- review 反馈中的 function 表示最可能需要继续修改的函数。
- 如果 feedback 里有 unsolved，请只针对这些未解决事件继续修复，不要引入额外事件。
- 路径故障通常需要改 route_planning：故障点不可到达、路径不能经过故障点；终点调整需要把旧终点重定向到新终点。
- 资源不可用通常意味着初始化函数返回列表中不能包含该资源。
- 位置/任务调整通常意味着对应初始化函数返回的目标对象字段必须改为新坐标或优先级。

当前 functions.py：
{code}

{feedback}

请输出新的完整 functions.py。只输出 Python 代码本身。
"""


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def split_batches(items: Sequence[Any]) -> Iterable[Sequence[Any]]:
    if BATCH_SIZE is None or BATCH_SIZE <= 0:
        if items:
            yield items
        return
    for start in range(0, len(items), BATCH_SIZE):
        yield items[start:start + BATCH_SIZE]


def prepare_workdir(task: Dict[str, Any]) -> Path:
    source_repo = ROOT / task["repo"]
    workdir = WORKDIR_ROOT / task["id"]
    if workdir.exists():
        shutil.rmtree(workdir)
    shutil.copytree(source_repo, workdir)
    return workdir


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run_verify(workdir: Path) -> Dict[str, Any]:
    try:
        proc = subprocess.run(
            [PYTHON_BIN, "verify.py"],
            cwd=workdir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=VERIFY_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "parsed": {"status": "timeout", "total": 0, "solved": 0, "unsolved": []},
        }

    parsed = None
    for line in reversed(proc.stdout.splitlines()):
        try:
            parsed = json.loads(line)
            break
        except json.JSONDecodeError:
            continue

    if not isinstance(parsed, dict):
        parsed = {"status": "parse_error", "total": 0, "solved": 0, "unsolved": []}

    return {
        "status": parsed.get("status", "unknown"),
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "parsed": parsed,
    }


def load_local_vllm() -> tuple[Any, Any, Any]:
    from transformers import AutoTokenizer
    from vllm import LLM, SamplingParams

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=TRUST_REMOTE_CODE)
    llm_kwargs = {
        "model": MODEL_PATH,
        "device": DEVICE,
        "dtype": DTYPE,
        "trust_remote_code": TRUST_REMOTE_CODE,
        "gpu_memory_utilization": GPU_MEMORY_UTILIZATION,
    }
    if TENSOR_PARALLEL_SIZE > 1:
        llm_kwargs["tensor_parallel_size"] = TENSOR_PARALLEL_SIZE
    if MAX_MODEL_LEN is not None:
        llm_kwargs["max_model_len"] = MAX_MODEL_LEN
    llm = LLM(**llm_kwargs)
    sampling_params = SamplingParams(
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_MODEL_TOKENS,
    )
    return tokenizer, llm, sampling_params


def generate_batch(llm: Any, prompts: List[str], sampling_params: Any) -> List[Any]:
    try:
        return llm.generate(prompts, sampling_params, use_tqdm=False)
    except TypeError:
        return llm.generate(prompts, sampling_params)


def extract_code(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:python|py)?\s*\n([\s\S]*?)\n```", text, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    starts = [idx for idx in [text.find('"""'), text.find("import "), text.find("from "), text.find("def ")] if idx >= 0]
    if starts:
        text = text[min(starts):].strip()
    return text.rstrip() + "\n"


def import_block(code: str) -> str:
    out = []
    started = False
    for line in code.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            out.append(stripped)
            started = True
        elif started and not stripped:
            continue
        elif started:
            break
    return "\n".join(out)


def function_signatures(code: str) -> List[str]:
    tree = ast.parse(code)
    signatures = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            signatures.append(f"{node.name}/{len(args)}/{len(node.args.defaults)}")
    return signatures


def validate_code(candidate: str, original: str) -> Optional[str]:
    try:
        ast.parse(candidate)
    except SyntaxError as exc:
        return f"生成代码存在语法错误：{exc}"
    if import_block(candidate) != import_block(original):
        return "生成代码修改了 import 区域。必须原样保留原始 import 语句。"
    try:
        if function_signatures(candidate) != function_signatures(original):
            return "生成代码新增/删除函数或修改了函数签名。只能修改已有函数体。"
    except SyntaxError as exc:
        return f"函数结构检查失败：{exc}"
    return None


def compact_feedback(verify: Dict[str, Any], validation_error: Optional[str] = None) -> str:
    if validation_error:
        return f"上一轮代码无效：{validation_error}"

    parsed = verify.get("parsed") or verify
    status = parsed.get("status") or verify.get("status")
    solved = parsed.get("solved", 0)
    total = parsed.get("total", 0)
    if status == "pass":
        return f"上一轮 review 通过：{solved}/{total}。"

    if isinstance(parsed.get("feedback"), str) and parsed["feedback"].strip():
        return "上一轮 review 未通过，精确反馈如下：\n" + parsed["feedback"].strip()

    lines = [f"上一轮 review 未通过：{solved}/{total}。"]
    if parsed.get("error"):
        lines.append(f"运行错误：{parsed['error']}")
    if verify.get("stderr"):
        lines.append("stderr 摘要：\n" + verify["stderr"][-1200:])
    unsolved = parsed.get("unsolved", [])
    if unsolved:
        lines.append("仍未解决的突发事件：")
        for item in unsolved:
            if isinstance(item, dict):
                lines.append(
                    f"- event: {item.get('event', '')}\n"
                    f"  function: {item.get('function', 'unknown')}\n"
                    f"  reason: {item.get('reason', item.get('check', 'review 检查未通过'))}"
                )
            else:
                lines.append(f"- {item}")
    return "\n".join(lines)


@dataclass
class TaskState:
    task: Dict[str, Any]
    workdir: Path
    task_output_dir: Path
    done_file: Path
    trajectory_path: Path
    tokenizer: Any
    original_code: str
    current_code: str
    issue: str
    emergency_situation: str
    started: float
    active: bool = True
    error: Optional[str] = None
    final_verify: Dict[str, Any] = field(default_factory=dict)
    feedback: str = ""
    attempts: List[Dict[str, Any]] = field(default_factory=list)
    stage_logs: List[Dict[str, Any]] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    verify_latency_sec: float = 0.0


def make_task_state(task: Dict[str, Any], tokenizer: Any) -> TaskState:
    started = time.time()
    task_output_dir = RUNS_ROOT / task["id"]
    task_output_dir.mkdir(parents=True, exist_ok=True)
    workdir = prepare_workdir(task)
    code = (workdir / "functions.py").read_text(encoding="utf-8")
    issue = (workdir / "issue.md").read_text(encoding="utf-8")
    return TaskState(
        task=task,
        workdir=workdir,
        task_output_dir=task_output_dir,
        done_file=task_output_dir / "done.json",
        trajectory_path=task_output_dir / "trajectory.json",
        tokenizer=tokenizer,
        original_code=code,
        current_code=code,
        issue=issue,
        emergency_situation=task.get("emergency_situation", issue),
        started=started,
    )


def build_prompt(state: TaskState, round_idx: int) -> str:
    feedback = state.feedback or "这是第 1 轮，还没有上一轮 review 反馈。"
    content = USER_PROMPT_TEMPLATE.format(
        scene=state.task["scene"],
        emergency_situation=state.emergency_situation,
        code=state.current_code,
        feedback=feedback,
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"这是第 {round_idx}/{MAX_REPAIR_ROUNDS} 轮修复。\n\n{content}"},
    ]
    return state.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def save_trajectory(state: TaskState) -> None:
    payload = {
        "id": state.task["id"],
        "scene": state.task["scene"],
        "model_name": MODEL_NAME,
        "model_path": MODEL_PATH,
        "mode": "direct_code_generation",
        "max_repair_rounds": MAX_REPAIR_ROUNDS,
        "active": state.active,
        "error": state.error,
        "feedback": state.feedback,
        "attempts": state.attempts,
        "stage_logs": state.stage_logs,
        "token_stats": {
            "prompt_tokens": state.prompt_tokens,
            "completion_tokens": state.completion_tokens,
        },
    }
    state.trajectory_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def apply_generation(state: TaskState, request_output: Any, round_idx: int, prompt: str) -> None:
    completion = request_output.outputs[0]
    raw = completion.text
    prompt_token_ids = getattr(request_output, "prompt_token_ids", None) or []
    completion_token_ids = getattr(completion, "token_ids", None) or []
    state.prompt_tokens += len(prompt_token_ids)
    state.completion_tokens += len(completion_token_ids)

    candidate = extract_code(raw)
    validation_error = validate_code(candidate, state.original_code)
    verify: Dict[str, Any]
    if validation_error:
        verify = {
            "status": "invalid_code",
            "parsed": {"status": "invalid_code", "total": 0, "solved": 0, "unsolved": []},
            "returncode": None,
            "stdout": "",
            "stderr": "",
        }
    else:
        (state.workdir / "functions.py").write_text(candidate, encoding="utf-8")
        state.current_code = candidate
        verify_started = time.time()
        verify = run_verify(state.workdir)
        state.verify_latency_sec += time.time() - verify_started

    state.final_verify = verify
    state.feedback = compact_feedback(verify, validation_error)
    parsed = verify.get("parsed") or verify
    if parsed.get("status") == "pass":
        state.active = False
    elif round_idx >= MAX_REPAIR_ROUNDS:
        state.active = False
        state.error = f"Reached repair round limit: {MAX_REPAIR_ROUNDS}"

    attempt = {
        "round": round_idx,
        "prompt": prompt,
        "raw_response": raw,
        "generated_code": candidate,
        "validation_error": validation_error,
        "verify": verify,
        "feedback_for_next_round": state.feedback,
        "prompt_tokens": len(prompt_token_ids),
        "completion_tokens": len(completion_token_ids),
        "timestamp": time.time(),
    }
    state.attempts.append(attempt)
    state.stage_logs.append({"round": round_idx, "input": prompt, "output": raw})
    save_trajectory(state)


def run_rounds(states: List[TaskState], llm: Any, sampling_params: Any) -> None:
    for round_idx in range(1, MAX_REPAIR_ROUNDS + 1):
        active = [state for state in states if state.active]
        if not active:
            break
        print(f"round {round_idx}/{MAX_REPAIR_ROUNDS}: generating {len(active)} active tasks")
        for group in split_batches(active):
            prompts = [build_prompt(state, round_idx) for state in group]
            outputs = generate_batch(llm, prompts, sampling_params)
            for state, prompt, request_output in zip(group, prompts, outputs):
                try:
                    apply_generation(state, request_output, round_idx, prompt)
                except BaseException as exc:
                    state.error = f"{type(exc).__name__}: {exc}"
                    state.final_verify = {
                        "status": "error",
                        "parsed": {"status": "error", "total": 0, "solved": 0, "unsolved": [], "error": state.error},
                        "returncode": None,
                        "stdout": "",
                        "stderr": "",
                    }
                    state.active = False
                    save_trajectory(state)
                parsed = state.final_verify.get("parsed", {})
                print(
                    f"{state.task['id']}: status={parsed.get('status')} "
                    f"solved={parsed.get('solved')}/{parsed.get('total')} "
                    f"round={round_idx}"
                )


def finalize_state(state: TaskState) -> Dict[str, Any]:
    if not state.final_verify:
        verify_started = time.time()
        state.final_verify = run_verify(state.workdir)
        state.verify_latency_sec += time.time() - verify_started

    parsed = state.final_verify.get("parsed") or state.final_verify
    exit_status = "Submitted" if parsed.get("status") == "pass" else "LimitsExceeded"
    agent_result = {
        "error": state.error,
        "trajectory_path": display_path(state.trajectory_path),
        "latency_sec": time.time() - state.started,
        "agent": {
            "info": {
                "model_stats": {
                    "instance_cost": 0.0,
                    "api_calls": len(state.attempts),
                    "prompt_tokens": state.prompt_tokens,
                    "completion_tokens": state.completion_tokens,
                },
                "config": {
                    "agent": {
                        "mode": "direct_code_generation",
                        "step_limit": MAX_REPAIR_ROUNDS,
                    },
                    "model": {
                        "model_name": MODEL_NAME,
                        "model_path": MODEL_PATH,
                        "temperature": TEMPERATURE,
                        "top_p": TOP_P,
                        "max_tokens": MAX_MODEL_TOKENS,
                    },
                },
                "exit_status": exit_status,
                "submission": "",
            }
        },
    }
    record = {
        "id": state.task["id"],
        "scene": state.task["scene"],
        "dataset_index": state.task["dataset_index"],
        "repo": display_path(state.workdir),
        "runner_version": "direct-codegen",
        "model_name": MODEL_NAME,
        "model_path": MODEL_PATH,
        "agent_result": agent_result,
        "verify_latency_sec": state.verify_latency_sec,
        "task_latency_sec": time.time() - state.started,
        "verify": state.final_verify,
    }
    state.done_file.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def main() -> int:
    time_start = time.time()
    tasks = read_jsonl(TASKS_FILE)
    if LIMIT is not None:
        tasks = tasks[:LIMIT]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    WORKDIR_ROOT.mkdir(parents=True, exist_ok=True)
    if RECORDS_FILE.exists() and not SKIP_EXISTING:
        RECORDS_FILE.unlink()

    tokenizer, llm, sampling_params = load_local_vllm()
    try:
        states: List[TaskState] = []
        records: List[Dict[str, Any]] = []
        for task in tasks:
            done_file = RUNS_ROOT / task["id"] / "done.json"
            if SKIP_EXISTING and done_file.exists():
                records.append(json.loads(done_file.read_text(encoding="utf-8")))
                continue
            states.append(make_task_state(task, tokenizer))

        run_rounds(states, llm, sampling_params)
        records.extend(finalize_state(state) for state in states)

        for record in records:
            append_jsonl(RECORDS_FILE, [record])
        print(f"time: {time.time() - time_start:.1f}s")
    finally:
        del llm
        del tokenizer
        gc.collect()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
