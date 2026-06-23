
## Task: Emergency Event Code Fix

Scene: deck

Emergency events:
第1个固定保障资源初始位置调整为(0,10);第1辆加氮车初始位置调整为(3,1);第1辆加油车发生故障不可用;第1辆充氧车发生故障不可用;第1辆牵引车初始位置调整为(2,3)

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
