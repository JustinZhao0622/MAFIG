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

# 模型 Qwen/Qwen3-32B deepseek-ai/DeepSeek-V3.2 Qwen/Qwen3-Coder-480B-A35B-Instruct
OUT_DIR = "cllm-results/deepseek-v3.2"
MODEL_NAME = "deepseek-ai/DeepSeek-V3.2"
BASE_URL = "https://api-inference.modelscope.cn/v1"
PER_THREAD_NUMS = 1

with open("datasets/test.json", "r", encoding="utf-8") as f:
    emergency_situation = json.load(f)

API_KEYS = [
    "ms-92c3238b-15c9-4118-ac1c-57b408b341b0",
    "ms-5c9ec602-3554-4d46-b858-15b4f90756ed",
    "ms-578abbfe-1f6f-4649-8186-0541ba4a1452",
    "ms-f5cf8848-e0a7-435a-bd16-3595ef54f8dd",
    "ms-d1abc073-c66f-4fa2-805c-3b67f7f479c8",
]


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
        ]
    )
    index += 1
    out_path = os.path.join(OUT_DIR, f"result_{index}.py")
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
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

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
    print(f"Total processing time (sum of all workers): {total_processing:.2f}s")


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    wall_time = time.time() - start_time
    print(f"Wall time: {wall_time:.2f}s")
