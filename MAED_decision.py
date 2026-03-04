"""
特情决策智能体
"""
import os
import json
import time
import textwrap
import sys
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import prompts as prompts_mod


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
        device="cuda",
        dtype="auto",
        trust_remote_code=True,
        gpu_memory_utilization=0.9,
    )
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2560)

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
            result = (
                output.outputs[0]
                .text.replace("```python", "")
                .replace("```", "")
                .replace("import heapq", "")
                .replace("import time", "")
                .replace("import random", "")
                .strip()
            )
            codes += textwrap.dedent(result) + "\n\n"
        offset += count
        res = "import heapq\nimport time\nimport random\n\n" + codes
        with open(f"{DIR}/results/result_{record_idx+1}.py", "w+") as f:
            f.write(res)
    return time.time() - start_time
