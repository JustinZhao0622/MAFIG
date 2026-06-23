
## Task: Emergency Event Code Fix

Scene: warehousing

Emergency events:
Zone_1堆积区发生故障不可用;Zone_1堆积区最大容量缩减至96;Forklift_3叉车发生故障不可用;Forklift_1叉车初始位置调整为(45,45);从第5辆货车开始间隔改为6分钟

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
