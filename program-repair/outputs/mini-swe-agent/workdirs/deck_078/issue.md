
## Task: Emergency Event Code Fix

Scene: deck

Emergency events:
第4辆加油车发生故障不可用;站位(4,7)(5,7)(4,8)(5,8)四个点发生故障;第4个固定保障资源初始位置调整为(0,9);第4个牵引任务目标站位调整为(0,7);从第5架舰载机开始到达间隔改为6分钟

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
