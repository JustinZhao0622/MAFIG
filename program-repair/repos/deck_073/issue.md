
## Task: Emergency Event Code Fix

Scene: deck

Emergency events:
第5辆维修车发生故障不可用;第5个通用移动资源发生故障不可用;第5辆充氧车发生故障不可用;第5辆加氮车初始位置调整为(1,5);第5个固定保障资源初始位置调整为(0,0);站位(7,4)(8,4)(7,5)(8,5)四个点发生故障;第5辆消防车初始位置调整为(1,1)

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
