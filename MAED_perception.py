"""
感知智能体
"""

import os
import json
import shutil
import time
import sys
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import prompts as prompts_mod


def perception_agent(DIR, model_path):
    """
    感知智能体
    通过判断突发事件，给出需要修改的函数名列表
    """
    if os.path.exists(DIR):
        shutil.rmtree(DIR)
    os.makedirs(DIR)
    with open("datasets/test.json", "r", encoding="utf-8") as f:
        emergency_situations = json.load(f)

    start_time = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    llm = LLM(
        model=model_path,
        device="cuda",
        dtype="auto",
        trust_remote_code=True,
        gpu_memory_utilization=0.9,
    )
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2560)

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
        text = eval(
            output.outputs[0].text.replace("```python", "").replace("```", "").strip()
        )
        # 把str转化为list
        if len(text) != len(emergency_situations[i]["functions"]):
            print("!!警告，感知智能体输出的函数名列表长度与突发事件数量不一致!!")
            sys.exit(1)
        emergency_situations[i]["perception_functions"] = text
    with open(f"{DIR}/perception_events.json", "w", encoding="utf-8") as f:
        json.dump(emergency_situations, f, ensure_ascii=False, indent=4)
    return time.time() - start_time


if __name__ == "__main__":
    perception_agent("MAED", "/data/huggingface/Qwen2.5-Coder-7B-Instruct")
