
## Task: Emergency Event Code Fix

Scene: port

Emergency events:
id为2的船舶任务时长延长至20分钟;站位(8,9)发生故障,以该点为终点的调整为(9,9);站位(6,3)(7,3)(6,4)(7,4)四个点发生故障;第0艘到达的船舶延迟10分钟到达;id为5的资源不可用

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
