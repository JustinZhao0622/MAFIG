"""
特情决策智能体
"""
import os
import json
import time
import textwrap
import ast
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import prompts as prompts_mod

import torch
seed = 42
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

def extract_fenced_code(text: str) -> str | None:
    lines = text.replace("\r\n", "\n").splitlines()
    blocks = []
    in_block = False
    block_lang = ""
    block_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_block:
                blocks.append((block_lang, "\n".join(block_lines).strip()))
                in_block = False
                block_lines = []
            else:
                block_lang = stripped[3:].strip().lower()
                in_block = True
        elif in_block:
            block_lines.append(line)

    for lang, code in blocks:
        if lang in ("", "python", "py"):
            return code
    return blocks[0][1] if blocks else None


def strip_to_code_start(text: str) -> str:
    lines = text.strip().splitlines()
    code_prefixes = ("import ", "from ", "def ", "async def ", "class ", "@")

    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(code_prefixes):
            return "\n".join(lines[idx:]).strip()
        if stripped.startswith(('"""', "'''")):
            lookahead = lines[idx + 1 : idx + 12]
            if any(next_line.lstrip().startswith(code_prefixes) for next_line in lookahead):
                return "\n".join(lines[idx:]).strip()

    return text.strip()


def trim_to_parseable_python(text: str) -> str:
    lines = text.strip().splitlines()
    for end in range(len(lines), 0, -1):
        candidate = "\n".join(lines[:end]).strip()
        if not candidate:
            continue
        try:
            ast.parse(candidate)
        except SyntaxError:
            continue
        return candidate
    return text.strip()


def get_original_function_names() -> set[str]:
    try:
        tree = ast.parse(prompts_mod.ORIGINAL_CODE)
    except SyntaxError:
        return set()
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }



def clean_code_block(text: str) -> str:
    """清理模型输出，仅保留可执行的 Python 代码。"""
    code = extract_fenced_code(text) or text
    code = strip_to_code_start(code)
    code = code.replace("```python", "").replace("```py", "").replace("```", "")
    code = code.replace("import heapq", "").replace("import time", "").replace("import random", "")
    code = trim_to_parseable_python(code)
    return code.strip()


def decision_agent(DIR, model_path):
    """
    特情决策智能体
    通过判断突发事件，给出需要修改的函数名列表
    """
    with open(f"{DIR}/perception_events.json", "r", encoding="utf-8") as f:
        emergency_situations = json.load(f)
    start_time = time.time()

    # 决策智能体
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    llm = LLM(
        model=model_path,
        dtype="auto",
        trust_remote_code=True,
        gpu_memory_utilization=0.9,
        seed=seed,
    )
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2560, seed=seed)

    # 阶段1：遍历所有记录，收集全部 inputs
    all_inputs = []
    record_slices = []  # 记录每条记录对应的 input 数量，用于拆分结果
    for emergency_situation in emergency_situations:
        events = emergency_situation["emergency_situation"].split(";")
        real_events = []
        real_functions = []

        # 去除感知智能体中未识别到的突发事件
        for event_idx, event in enumerate(events):
            if (
                emergency_situation["functions"][event_idx]
                == emergency_situation["perception_functions"][event_idx]
            ):
                real_events.append(event)
                real_functions.append(emergency_situation["functions"][event_idx])
        # 如果突发事件所对应的函数是一样的，那么将相同类型的突发事件合并
        fn_to_events = {}
        fn_order = []
        for event_idx, event in enumerate(real_events):
            fn = real_functions[event_idx]
            if fn not in fn_to_events:
                fn_order.append(fn)
                fn_to_events[fn] = []
            fn_to_events[fn].append(event)
        merged_events = [";".join(fn_to_events[fn]) for fn in fn_order]
        merged_functions = fn_order

        for i in range(len(merged_events)):
            messages = [
                {"role": "system", "content": prompts_mod.SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompts_mod.USER_PROMPT.format(
                        EMERGENCY_SITUATIONS=merged_events[i],
                        ORIGINAL_CODE=prompts_mod.functions_mapping[
                            merged_functions[i]
                        ],
                    ),
                },
            ]
            all_inputs.append(
                tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
            )
        record_slices.append(len(merged_events))

    # 阶段2：一次性批量推理
    all_outputs = llm.generate(all_inputs, sampling_params)

    # 阶段3：按记录拆分结果并写文件
    os.makedirs(f"{DIR}/results", exist_ok=True)
    offset = 0
    for record_idx, count in enumerate(record_slices):
        codes = ""
        for output in all_outputs[offset:offset + count]:
            result = output.outputs[0].text
            result = clean_code_block(result.strip())
            codes += textwrap.dedent(result) + "\n\n"
        offset += count
        res ="import heapq\nimport time\nimport random\n\n" + codes
        with open(f"{DIR}/results/result_{record_idx+1}.py", "w+") as f:
            f.write(res)
    return time.time() - start_time
