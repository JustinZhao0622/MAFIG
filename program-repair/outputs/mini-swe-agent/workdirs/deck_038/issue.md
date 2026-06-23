
## Task: Emergency Event Code Fix

Scene: deck

Emergency events:
站位(6,6)(7,6)(6,7)(7,7)四个点发生故障;第4辆液压车初始位置调整为(2,5);第4辆牵引车初始位置调整为(2,9);从第7架舰载机开始到达间隔改为8分钟;第4辆供电车初始位置调整为(3,8);第6个牵引任务目标站位调整为(2,5);第4个固定保障资源初始位置调整为(0,5);第4辆气源车发生故障不可用

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
