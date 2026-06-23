
## Task: Emergency Event Code Fix

Scene: warehousing

Emergency events:
Forklift_2叉车初始位置调整为(37,21);Zone_2堆积区最大容量缩减至93;Forklift_1叉车发生故障不可用;Zone_2堆积区发生故障不可用;Zone_3堆积区当前库存增加79

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
