"""
云端调用大模型api：5个key同时开始（每个key一个worker）
"""

import asyncio
import os
import json
import time
from openai import AsyncOpenAI
import prompts
import shutil
import review_code

# 模型 Qwen/Qwen3-32B deepseek-ai/DeepSeek-V3.2 Qwen/Qwen3-Coder-480B-A35B-Instruct
RESULT_DIR = "cllm-results/qwen3-32b"
DATASET_FILE = "datasets/test.json"
MODEL_NAME = "Qwen/Qwen3-32B"
BASE_URL = "https://api-inference.modelscope.cn/v1"
PER_THREAD_NUMS = 1

with open(DATASET_FILE, "r", encoding="utf-8") as f:
    emergency_situation = json.load(f)

BASE_KEYS = [
    "ms-5c9ec602-3554-4d46-b858-15b4f90756ed",
    "ms-c45ac4c4-65fe-4941-8208-bc8c82e223d8",
    "ms-f5cf8848-e0a7-435a-bd16-3595ef54f8dd",
    "ms-e7515d03-7395-4d88-817a-3b3aa267c948",
    "ms-917a1896-16f9-428f-849a-518a5e35c226",
    "ms-61e45448-b478-49a7-a86f-b52c449b9059",
]
API_KEYS = [key for key in BASE_KEYS for _ in range(1)]

def clean_code_block(text: str) -> str:
    """清理代码无用信息"""
    return text.replace("```python", "").replace("```", "").strip()


async def call_model(index: int, client: AsyncOpenAI):
    """单次调用"""
    print(f"[idx={index}] start")
    resp = await client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.9,
        top_p=0.95,
        messages=[
            {"role": "system", "content": prompts.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": prompts.USER_PROMPT.format(
                    EMERGENCY_SITUATIONS=emergency_situation[index][
                        "emergency_situation"
                    ],
                    ORIGINAL_CODE=prompts.ORIGINAL_CODE,
                ),
            },
        ],
        extra_body={
            "enable_thinking": False,
        }
    )
    out_path = os.path.join(RESULT_DIR, f"result_{index + 1}.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(clean_code_block(resp.choices[0].message.content))

    print(f"[idx={index}] done")


async def key_worker(
    key_id: int, client: AsyncOpenAI, indices: list[int], per_key_concurrency: int = 1
) -> float:
    """
    一个 key 的 worker：启动时立刻跑起来
    per_key_concurrency=1 => 每个key同一时间只跑1个请求
    返回该 worker 的耗时(秒)
    """
    sem = asyncio.Semaphore(per_key_concurrency)

    async def _run_one(idx: int):
        async with sem:
            await call_model(idx, client)

    t0 = time.time()
    await asyncio.gather(*[_run_one(i) for i in indices])
    elapsed = time.time() - t0
    print(f"[key={key_id}] elapsed: {elapsed:.2f}s")
    return elapsed


async def main():
    """主函数"""
    if os.path.exists(RESULT_DIR):
        shutil.rmtree(RESULT_DIR)
    os.makedirs(RESULT_DIR)

    clients = [AsyncOpenAI(base_url=BASE_URL, api_key=k) for k in API_KEYS]

    # round-robin 均分索引给每个 key
    buckets = [[] for _ in API_KEYS]
    for i in range(len(emergency_situation)):
        buckets[i % len(API_KEYS)].append(i)

    # 关键：5个 worker 同时启动 => 5个key同时开始
    per_key_concurrency = PER_THREAD_NUMS
    workers = [
        key_worker(
            kid, clients[kid], buckets[kid], per_key_concurrency=per_key_concurrency
        )
        for kid in range(len(API_KEYS))
    ]
    elapsed_list = await asyncio.gather(*workers)
    total_processing = sum(elapsed_list)
    return total_processing


if __name__ == "__main__":
    start_time = time.time()
    total_processing = asyncio.run(main())
    wall_time = time.time() - start_time
    print(f"Wall time: {wall_time:.2f}s")
    review_code.main(DATASET_FILE, RESULT_DIR)
    print(f"Total processing time: {total_processing:.2f}s")
    
    