#!/usr/bin/env python3
from __future__ import annotations

import json
import multiprocessing
import sys
from pathlib import Path


sys.dont_write_bytecode = True

EVENTS = [
  "Zone_1堆积区当前库存增加71",
  "Forklift_1叉车发生故障不可用",
  "站位(6,6)(7,6)(6,7)(7,7)四个点发生故障"
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
