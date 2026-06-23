
## Task: Emergency Event Code Fix

Scene: deck

Emergency events:
站位(6,7)(7,7)(6,8)(7,8)四个点发生故障;站位(7,9)发生故障,以该点为终点的调整为(8,9);第3个固定保障资源初始位置调整为(1,3);第3辆消防车初始位置调整为(0,8);第3辆液压车初始位置调整为(1,1)

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
