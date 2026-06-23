# mini-SWE-agent 代码编辑对比实验

这个目录用于把 MAFIG 的三个场景数据转换成 mini-SWE-agent 可以执行的代码编辑任务。

## 当前结构

```text
code-editing/
  tasks.jsonl              # 任务清单，不包含答案
  gold.jsonl               # gold function 标签，只用于离线分析
  repos/                   # 每个样本对应一个独立任务仓库
  outputs/mini-swe-agent/  # mini-SWE-agent 输出目录
  scripts/
    build_tasks.py         # 生成任务仓库
    run_swe_agent.py       # 调用 mini-SWE-agent 跑任务
    evaluate.py            # 汇总验证结果
```

每个任务仓库的结构如下：

```text
code-editing/repos/port_001/
  functions.py       # 待修改代码
  _review_code.py    # 从 datasets/<scene>/review_code.py 复制来的验证器
  verify.py          # 当前任务的验证入口
  issue.md           # 给 mini-SWE-agent 的问题描述
```

`repos/` 和 `tasks.jsonl` 都不包含 `gold_functions`，避免把答案泄露给 agent。答案单独保存在 `gold.jsonl`，只用于离线统计或错误分析。

## 1. 生成任务

在仓库根目录运行：

```bash
conda activate llm
python code-editing/scripts/build_tasks.py
```

这会生成：

```text
code-editing/tasks.jsonl
code-editing/gold.jsonl
code-editing/repos/*
```

如果只想生成一小部分样本，修改 [build_tasks.py](/root/code/MAFIG/code-editing/scripts/build_tasks.py:24) 顶部配置：

```python
SCENES = ["port"]
LIMIT_PER_SCENE = 5
```

## 2. 检查单个任务

进入任意任务目录：

```bash
cd code-editing/repos/port_001
python verify.py
```

原始 `functions.py` 通常会返回 `fail`，这是正常的，因为任务还没有被 agent 修改。agent 修改完成后，再运行 `python verify.py`，返回 `pass` 才表示当前任务解决成功。

## 3. 启动 vLLM

mini-SWE-agent 通过 LiteLLM 调用模型。这里默认使用 vLLM 的 OpenAI-compatible 服务。

先启动模型服务：

```bash
conda activate llm
vllm serve /data/huggingface/Qwen2.5-Coder-7B-Instruct \
  --served-model-name Qwen2.5-Coder-7B-Instruct
```

这里要注意两点：

- `--served-model-name` 要和脚本里的模型名后半部分一致
- vLLM 默认地址是 `http://localhost:8000/v1`

如果你的模型路径、服务名或端口不同，需要同步修改 [run_swe_agent.py](/root/code/MAFIG/code-editing/scripts/run_swe_agent.py:39) 顶部配置：

```python
MODEL_NAME = "hosted_vllm/Qwen2.5-Coder-7B-Instruct"
VLLM_BASE_URL = "http://localhost:8000/v1"
VLLM_API_KEY = "EMPTY"
```

`hosted_vllm/...` 是 mini-SWE-agent 官方文档里给 vLLM 的 LiteLLM provider 写法。脚本同时使用 `litellm_textbased`，这样本地 Qwen 不需要返回 OpenAI tool call，只需要按 mini-SWE-agent 的文本格式输出 bash 命令。

## 4. 运行 mini-SWE-agent

在仓库根目录运行：

```bash
conda activate llm
python code-editing/scripts/run_swe_agent.py
```

脚本会：

1. 读取 `tasks.jsonl`
2. 把 `code-editing/repos/<task_id>/` 复制到可修改目录
3. 先检查 `VLLM_BASE_URL/models` 是否能连上
4. 调用 `mini-swe-agent` 包里的 `minisweagent.run.mini.main`
5. 使用 `mini_textbased.yaml` 和 `litellm_textbased` 跑本地模型
6. 让 agent 修改 `functions.py`
7. 在修改后的目录里运行 `python verify.py`
8. 保存轨迹和验证结果

修改后的任务目录在：

```text
code-editing/outputs/mini-swe-agent/workdirs/<task_id>/
```

每个任务的运行记录在：

```text
code-editing/outputs/mini-swe-agent/runs/<task_id>/done.json
```

总记录文件在：

```text
code-editing/outputs/mini-swe-agent/records.jsonl
```

## 5. 汇总评测结果

运行：

```bash
conda activate llm
python code-editing/scripts/evaluate.py
```

默认评测目录是：

```text
code-editing/outputs/mini-swe-agent/workdirs/
```

结果会写入：

```text
code-editing/outputs/mini-swe-agent/evaluation.json
```

评测指标包括：

- 任务成功率：多少个任务完全 `pass`
- 事件成功率：所有突发事件中解决了多少个
- 各场景单独统计：`port`、`warehousing`、`deck`

## 6. 公平性说明

为了和 MAFIG、ReAct 或其他代码编辑方法公平对比，需要保持以下条件一致：

- 使用同一批 `tasks.jsonl`
- 使用同一个模型，例如 `Qwen2.5-Coder-7B-Instruct`
- 使用同一个验证器，也就是任务里的 `verify.py`
- 不给 mini-SWE-agent 提供 `gold_functions`
- 不给 mini-SWE-agent 提供额外关键词表或函数职责表
- 对所有方法使用相同 timeout、步数限制和评测脚本

## 7. 常用配置

如果只想先跑少量任务，修改 [run_swe_agent.py](/root/code/MAFIG/code-editing/scripts/run_swe_agent.py:28)：

```python
LIMIT = 3
```

如果要调整 agent 最大步数：

```python
MAX_AGENT_STEPS = 30
```

如果要调整命令执行超时：

```python
ENV_TIMEOUT = 30
```

如果要重新生成全部任务：

```bash
conda activate llm
python code-editing/scripts/build_tasks.py
```
