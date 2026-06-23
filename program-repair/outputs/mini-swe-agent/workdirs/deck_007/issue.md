
## Task: Emergency Event Code Fix

Scene: deck

Emergency events:
第3辆供电车初始位置调整为(0,8);第3辆气源车发生故障不可用;第3个固定保障资源初始位置调整为(1,7);第3辆维修车发生故障不可用;第3个通用移动资源发生故障不可用;第3辆消防车初始位置调整为(1,6);第3辆充氧车发生故障不可用;站位(9,9)发生故障,以该点为终点的调整为(10,9)

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
