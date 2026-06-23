#!/usr/bin/env python3
"""
Build self-contained code-editing tasks for SWE-agent style experiments.

Each task repo contains:
  - functions.py: the file the agent should edit
  - _review_code.py: copied verifier for the scene
  - verify.py: validates this single task
  - issue.md: task description for the agent

Gold function labels are written only to code-editing/tasks.jsonl, not into the
task repos.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


ROOT = Path(__file__).resolve().parents[2]
DATASETS_DIR = ROOT / "datasets"
CODE_EDITING_DIR = ROOT / "code-editing"
REVIEW_CODE_DIR = CODE_EDITING_DIR
REPOS_DIR = CODE_EDITING_DIR / "repos"
TASKS_FILE = CODE_EDITING_DIR / "tasks.jsonl"
GOLD_FILE = CODE_EDITING_DIR / "gold.jsonl"

SCENES = ["deck"]
# "port", "warehousing", "deck"
LIMIT_PER_SCENE: Optional[int] = None
CLEAN_REPOS = True


ISSUE_TEMPLATE = """
## Task: Emergency Event Code Fix

Scene: {scene}

Emergency events:
{emergency_situation}

The current directory contains a `functions.py` file with scheduling functions.
You need to produce a corrected complete `functions.py` that handles the emergency events above.

## Rules

- Only modify the body of existing functions
- Do NOT add or remove functions; do NOT change function names, parameters, or return types
- Do NOT modify, remove, or add any import statements
- Do NOT use bash, shell commands, editors, sed, or file-writing commands
- Do NOT output explanations, markdown fences, snippets, or omitted sections

The runner will show you the current `functions.py`, ask for a full replacement file,
run `verify.py`, and feed any structured review feedback back into the next round.
Use the feedback to fix only the unresolved emergency events.
"""


VERIFY_TEMPLATE = r'''#!/usr/bin/env python3
from __future__ import annotations

import json
import multiprocessing
import sys
from pathlib import Path


sys.dont_write_bytecode = True

EVENTS = {events_json}
TIMEOUT = 10


def _worker(queue) -> None:
    import _review_code
    result = {{}}
    _review_code.run_verify_case(str(Path(__file__).with_name("functions.py")), EVENTS, result)
    queue.put(result)


def main() -> int:
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue()
    process = ctx.Process(target=_worker, args=(queue,))
    process.start()
    process.join(TIMEOUT)

    if process.is_alive():
        process.kill()
        process.join()
        print(json.dumps({{"status": "timeout", "total": len(EVENTS), "solved": 0, "unsolved": [], "feedback": "review 超时"}}, ensure_ascii=False))
        return 1

    if queue.empty():
        print(json.dumps({{"status": "error", "error": "verifier returned no result", "total": len(EVENTS), "solved": 0, "unsolved": [], "feedback": "review 子进程没有返回结果"}}, ensure_ascii=False))
        return 1

    result = queue.get()
    if "error" in result:
        print(json.dumps({{"status": "error", "error": result["error"], "total": len(EVENTS), "solved": 0, "unsolved": [], "feedback": result["error"]}}, ensure_ascii=False))
        return 1

    data = result.get("result", {{"total": len(EVENTS), "solved": 0, "unsolved": EVENTS}})
    total = int(data.get("total", len(EVENTS)))
    solved = int(data.get("solved", 0))
    unsolved = data.get("unsolved", [])
    status = "pass" if solved == total else "fail"
    payload = {{
        "status": status,
        "total": total,
        "solved": solved,
        "solved_events": data.get("solved_events", []),
        "unsolved": unsolved,
        "feedback": data.get("feedback", ""),
    }}
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def load_dataset(scene: str) -> List[Dict[str, Any]]:
    with (DATASETS_DIR / scene / "test.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def split_events(text: str) -> List[str]:
    return [part.strip() for part in text.split(";") if part.strip()]


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def task_id(scene: str, dataset_index: int) -> str:
    return f"{scene}_{dataset_index + 1:03d}"


def build_task_repo(scene: str, dataset_index: int, item: Dict[str, Any]) -> Dict[str, Any]:
    tid = task_id(scene, dataset_index)
    repo_dir = REPOS_DIR / tid
    repo_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(DATASETS_DIR / scene / "functions.py", repo_dir / "functions.py")
    shutil.copyfile(REVIEW_CODE_DIR / f"review_code_{scene}.py", repo_dir / "_review_code.py")

    emergency_situation = item["emergency_situation"]
    events = split_events(emergency_situation)
    (repo_dir / "verify.py").write_text(
        VERIFY_TEMPLATE.format(events_json=json.dumps(events, ensure_ascii=False, indent=2)),
        encoding="utf-8",
    )
    (repo_dir / "issue.md").write_text(
        ISSUE_TEMPLATE.format(scene=scene, emergency_situation=emergency_situation),
        encoding="utf-8",
    )

    return {
        "id": tid,
        "scene": scene,
        "dataset_index": dataset_index,
        "repo": str(repo_dir.relative_to(ROOT)),
        "issue_file": str((repo_dir / "issue.md").relative_to(ROOT)),
        "test_cmd": "python verify.py",
        "emergency_situation": emergency_situation,
        "events": events,
    }


def main() -> int:
    if CLEAN_REPOS and REPOS_DIR.exists():
        shutil.rmtree(REPOS_DIR)
    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    gold_records = []
    for scene in SCENES:
        dataset = load_dataset(scene)
        if LIMIT_PER_SCENE is not None:
            dataset = dataset[:LIMIT_PER_SCENE]
        for dataset_index, item in enumerate(dataset):
            record = build_task_repo(scene, dataset_index, item)
            records.append(record)
            gold_records.append({
                "id": record["id"],
                "scene": scene,
                "dataset_index": dataset_index,
                "gold_functions": item.get("functions", []),
            })

    write_jsonl(TASKS_FILE, records)
    write_jsonl(GOLD_FILE, gold_records)
    print(f"built {len(records)} tasks")
    print(f"tasks: {TASKS_FILE}")
    print(f"gold: {GOLD_FILE}")
    print(f"repos: {REPOS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
