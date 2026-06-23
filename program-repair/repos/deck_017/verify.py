#!/usr/bin/env python3
from __future__ import annotations

import json
import multiprocessing
import sys
from pathlib import Path


sys.dont_write_bytecode = True

EVENTS = [
  "站位(9,12)发生故障,以该点为终点的调整为(10,12)",
  "第5个通用移动资源发生故障不可用",
  "第5个固定保障资源初始位置调整为(2,1)",
  "第5辆加油车发生故障不可用",
  "第5辆供电车初始位置调整为(2,0)",
  "第5辆消防车初始位置调整为(2,2)",
  "第5辆维修车发生故障不可用",
  "站位(6,8)(7,8)(6,9)(7,9)四个点发生故障"
]
TIMEOUT = 10


def _worker(queue) -> None:
    import _review_code
    result = {}
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
        print(json.dumps({"status": "timeout", "total": len(EVENTS), "solved": 0, "unsolved": [], "feedback": "review 超时"}, ensure_ascii=False))
        return 1

    if queue.empty():
        print(json.dumps({"status": "error", "error": "verifier returned no result", "total": len(EVENTS), "solved": 0, "unsolved": [], "feedback": "review 子进程没有返回结果"}, ensure_ascii=False))
        return 1

    result = queue.get()
    if "error" in result:
        print(json.dumps({"status": "error", "error": result["error"], "total": len(EVENTS), "solved": 0, "unsolved": [], "feedback": result["error"]}, ensure_ascii=False))
        return 1

    data = result.get("result", {"total": len(EVENTS), "solved": 0, "unsolved": EVENTS})
    total = int(data.get("total", len(EVENTS)))
    solved = int(data.get("solved", 0))
    unsolved = data.get("unsolved", [])
    status = "pass" if solved == total else "fail"
    payload = {
        "status": status,
        "total": total,
        "solved": solved,
        "solved_events": data.get("solved_events", []),
        "unsolved": unsolved,
        "feedback": data.get("feedback", ""),
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
