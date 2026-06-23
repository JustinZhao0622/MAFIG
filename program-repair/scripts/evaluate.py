#!/usr/bin/env python3
"""
Evaluate generated code-editing task repos.

By default this evaluates mini-swe-agent workdirs created by run_swe_agent.py. Change
CANDIDATE_ROOT to evaluate another method's edited repos, as long as each task
directory contains functions.py and verify.py.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


ROOT = Path(__file__).resolve().parents[2]
CODE_EDITING_DIR = ROOT / "code-editing"
TASKS_FILE = CODE_EDITING_DIR / "tasks.jsonl"
CANDIDATE_ROOT = CODE_EDITING_DIR / "outputs" / "mini-swe-agent" / "workdirs"
RUNS_ROOT = CODE_EDITING_DIR / "outputs" / "mini-swe-agent" / "runs"
RESULTS_FILE = CODE_EDITING_DIR / "outputs" / "mini-swe-agent" / "evaluation.json"
LIMIT: Optional[int] = None
VERIFY_TIMEOUT = 20
PYTHON_BIN = "python"


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run_verify(repo_dir: Path) -> Dict[str, Any]:
    if not repo_dir.exists():
        return {"status": "missing_repo", "total": 0, "solved": 0}
    try:
        proc = subprocess.run(
            [PYTHON_BIN, "verify.py"],
            cwd=repo_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=VERIFY_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "total": 0,
            "solved": 0,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
        }

    parsed = None
    for line in reversed(proc.stdout.splitlines()):
        try:
            parsed = json.loads(line)
            break
        except json.JSONDecodeError:
            continue

    if not isinstance(parsed, dict):
        return {
            "status": "parse_error",
            "total": 0,
            "solved": 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    parsed["returncode"] = proc.returncode
    parsed["stdout"] = proc.stdout
    parsed["stderr"] = proc.stderr
    return parsed


def load_run_record(task_id: str) -> Dict[str, Any]:
    path = RUNS_ROOT / task_id / "done.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"error": "invalid_done_json", "path": str(path)}


def as_number(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def summarize(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    rows = list(records)
    scene_names = ["all"] + sorted({row["scene"] for row in rows})
    by_scene = []
    for scene in scene_names:
        items = rows if scene == "all" else [row for row in rows if row["scene"] == scene]
        if not items:
            continue
        completed_items = [item for item in items if item["verify"].get("status") != "missing_repo"]
        total_events = sum(item["verify"].get("total", 0) for item in completed_items)
        solved_events = sum(item["verify"].get("solved", 0) for item in completed_items)
        passed = sum(1 for item in completed_items if item["verify"].get("status") == "pass")
        agent_times = [
            value
            for value in (as_number(item.get("agent_latency_sec")) for item in completed_items)
            if value is not None
        ]
        task_times = [
            value
            for value in (as_number(item.get("task_latency_sec")) for item in completed_items)
            if value is not None
        ]
        by_scene.append({
            "scene": scene,
            "tasks": len(items),
            "completed_tasks": len(completed_items),
            "missing_tasks": len(items) - len(completed_items),
            "task_success_rate": passed / len(completed_items) if completed_items else 0,
            "event_success_rate": solved_events / total_events if total_events else 0,
            "solved_events": solved_events,
            "total_events": total_events,
            "agent_total_sec": sum(agent_times),
            "agent_avg_sec": sum(agent_times) / len(agent_times) if agent_times else 0,
            "task_total_sec": sum(task_times),
            "task_avg_sec": sum(task_times) / len(task_times) if task_times else 0,
            "timed_tasks": len(agent_times),
            "status_counts": status_counts(item["verify"].get("status", "unknown") for item in items),
        })
    return {"summary": by_scene, "records": rows}


def status_counts(statuses: Iterable[str]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for status in statuses:
        counts[status] = counts.get(status, 0) + 1
    return counts


def print_summary(summary: Dict[str, Any]) -> None:
    print("\nscene         tasks  done  timed  missing  task_sr  event_sr  solved/total  agent_sec  avg_sec")
    print("------------  -----  ----  -----  -------  -------  --------  ------------  ---------  -------")
    for row in summary["summary"]:
        print(
            f"{row['scene']:<12}  {row['tasks']:>5}  {row['completed_tasks']:>4}  "
            f"{row['timed_tasks']:>5}  {row['missing_tasks']:>7}  {row['task_success_rate']:.4f}   "
            f"{row['event_success_rate']:.4f}    {row['solved_events']}/{row['total_events']:<11}  "
            f"{row['agent_total_sec']:>9.2f}  {row['agent_avg_sec']:>7.2f}"
        )


def main() -> int:
    tasks = read_jsonl(TASKS_FILE)
    if LIMIT is not None:
        tasks = tasks[:LIMIT]

    records = []
    for task in tasks:
        repo_dir = CANDIDATE_ROOT / task["id"]
        run_record = load_run_record(task["id"])
        verify = run_verify(repo_dir)
        agent_result = run_record.get("agent_result", {})
        records.append({
            "id": task["id"],
            "scene": task["scene"],
            "dataset_index": task["dataset_index"],
            "repo": str(repo_dir.relative_to(ROOT)) if repo_dir.exists() else str(repo_dir),
            "run_record": str((RUNS_ROOT / task["id"] / "done.json").relative_to(ROOT))
            if run_record else None,
            "agent_latency_sec": agent_result.get("latency_sec"),
            "verify_latency_sec": run_record.get("verify_latency_sec"),
            "task_latency_sec": run_record.get("task_latency_sec"),
            "verify": verify,
        })

    summary = summarize(records)
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print_summary(summary)
    print(f"\nresults: {RESULTS_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
