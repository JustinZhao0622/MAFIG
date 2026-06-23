"""
感知智能体
"""

import ast
import json
import time
import re
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import prompts as prompts_mod

import torch
seed = 42
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

def _parse_function_list(raw_text):
    """安全解析模型输出中的函数名列表。支持从解释文本和代码块中提取 [...]。"""
    if not raw_text:
        return []

    text = raw_text.strip()

    # 1. 优先提取 ```python ... ``` 或 ``` ... ``` 代码块中的内容
    code_blocks = re.findall(r"```(?:python)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    candidates = []
    for block in code_blocks:
        candidates.append(block.strip())
    # 2. 同时把全文也作为候选，防止没有代码块
    candidates.append(text)
    for candidate in candidates:
        # 3. 从候选文本中提取第一个 [...] 列表
        match = re.search(r"\[[\s\S]*?\]", candidate)
        if not match:
            continue
        list_text = match.group(0).strip()
        try:
            parsed = ast.literal_eval(list_text)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except Exception:
            pass
        # 4. 兜底解析：适合 ["a", "b"] 这种简单列表
        body = list_text[1:-1].strip()
        if not body:
            return []
        items = []
        for part in body.split(","):
            value = part.strip().strip("'").strip('"').strip()
            if value:
                items.append(value)
        if items:
            return items
    return []


def _normalize_function_list(functions, expected_len):
    """把感知结果修正到与事件数量一致。"""
    valid_names = set(prompts_mod.functions_mapping.keys()) | {"None", "none", ""}
    normalized = []
    for item in functions[:expected_len]:
        value = str(item).strip()
        if value not in valid_names:
            value = "None"
        if value.lower() == "none" or value == "":
            value = "None"
        normalized.append(value)
    while len(normalized) < expected_len:
        normalized.append("None")
    return normalized


def perception_agent(DIR, model_path):
    """
    感知智能体
    通过判断突发事件，给出需要修改的函数名列表
    """
    with open("datasets/test.json", "r", encoding="utf-8") as f:
        emergency_situations = json.load(f)
    start_time = time.time()

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    llm = LLM(
        model=model_path,
        dtype="auto",
        trust_remote_code=True,
        gpu_memory_utilization=0.9,
        seed=seed,
    )
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2560, seed=seed)

    inputs = []
    for _, emergency_situation in enumerate(emergency_situations):
        messages = [
            {"role": "system", "content": prompts_mod.perception_system_prompt},
            {
                "role": "user",
                "content": prompts_mod.perception_user_prompt.format(
                    EMERGENCY_SITUATIONS=emergency_situation["emergency_situation"],
                    nums=len(emergency_situation["emergency_situation"].split(";")),
                ),
            },
        ]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs.append(text)
    
    outputs = llm.generate(inputs, sampling_params)

    # 感知智能体结果的处理和存储
    for i, output in enumerate(outputs):
        expected_len = len(emergency_situations[i]["functions"])
        raw_text = output.outputs[0].text
        text = _parse_function_list(raw_text)
        if len(text) != expected_len:
            print("!!警告，感知智能体输出的函数名列表长度与突发事件数量不一致，已自动补齐/截断!!")
        text = _normalize_function_list(text, expected_len)
        emergency_situations[i]["perception_raw_output"] = raw_text
        emergency_situations[i]["perception_functions"] = text
    with open(f"{DIR}/perception_events.json", "w", encoding="utf-8") as f:
        json.dump(emergency_situations, f, ensure_ascii=False, indent=4)
    return time.time() - start_time

