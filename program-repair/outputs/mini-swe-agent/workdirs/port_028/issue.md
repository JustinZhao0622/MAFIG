
## Task: Emergency Event Code Fix

Scene: port

Emergency events:
站位(6,4)(7,4)(6,5)(7,5)四个点发生故障;id为7的资源不可用;站位(9,8)发生故障,以该点为终点的调整为(10,8);id为4的船舶任务时长延长至20分钟;第1艘到达的船舶延迟10分钟到达

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
