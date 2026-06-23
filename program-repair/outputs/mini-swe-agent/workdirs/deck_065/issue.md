
## Task: Emergency Event Code Fix

Scene: deck

Emergency events:
第2辆液压车初始位置调整为(0,5);第2辆加氮车初始位置调整为(3,4);第2辆加油车发生故障不可用;从第4架舰载机开始到达间隔改为8分钟;第2辆维修车发生故障不可用;第2辆牵引车初始位置调整为(1,8);第4个牵引任务目标站位调整为(2,1)

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
