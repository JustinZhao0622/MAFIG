"""
本地调用大模型：按 test.json 逐条生成结果文件
"""
import os
import json
import shutil
import time
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import prompts as prompts_mod
import review_code

# Qwen2.5-Coder-7B-Instruct  Meta-Llama-3.1-8B-Instruct  glm-4-9b-chat
OUT_DIR = "local-llm-results/glm-4-9b-chat"
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR)
MODEL_PATH = "/data/huggingface/glm-4-9b-chat"

with open("datasets/test.json", "r", encoding="utf-8") as f:
    emergency_situation = json.load(f)


def clean_code_block(text: str) -> str:
    """清理代码无用信息"""
    return text.replace("```python", "").replace("```", "").strip()


_local_llm = None
_local_tokenizer = None


def call_local_model_batch(out_dir=OUT_DIR):
    global _local_llm, _local_tokenizer

    if _local_llm is None:
        _local_llm = LLM(
            model=MODEL_PATH,
            device="cuda",
            dtype="auto",
            trust_remote_code=True,
            gpu_memory_utilization=0.9,
        )
        _local_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2560)

    inputs = []
    for idx in range(len(emergency_situation)):
        messages = [
            {"role": "system", "content": prompts_mod.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": prompts_mod.USER_PROMPT.format(
                    EMERGENCY_SITUATIONS=emergency_situation[idx]["emergency_situation"],
                    ORIGINAL_CODE=prompts_mod.ORIGINAL_CODE,
                ),
            },
        ]
        text = _local_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs.append(text)

    outputs = _local_llm.generate(inputs, sampling_params)
    raw_texts = [out.outputs[0].text for out in outputs]
    for idx, raw in enumerate(raw_texts):
        code_only = clean_code_block(raw)
        file_path = os.path.join(out_dir, f"result_{idx+1}.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_only + "\n")

    return raw_texts


if __name__ == "__main__":
    start_time = time.time()
    call_local_model_batch()
    end_time = time.time()
    review_code.main("datasets/test.json",OUT_DIR)
    print(f"Time taken: {end_time - start_time:.2f} seconds")