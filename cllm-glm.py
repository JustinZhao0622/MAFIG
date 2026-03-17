"""
调用智谱AI glm-5：多key并发（asyncio + to_thread），记录每个worker耗时
"""

import asyncio
import os
import json
import time
from zai import ZhipuAiClient
import prompts
import shutil
import review_code

OUT_DIR = "cllm-results/glm-5"
MODEL_NAME = "glm-5"
API_KEYS = [
    "5c6d3d4312f94fa1a6773b17aa97b75d.w9cZbahrqSsPSeTt",
    "5123fb6446a248648c88a1c20007a5a6.GzwNMUsco0qkbQl1",
    "11724e5a71d24cd9bb1cccd52fe6a29a.DnAUeBnWIte1Nqvm",
    "35da9a35c1f149d6905d9accb5218caf.ynVDb5rZfz6RXRsp",
    "90bab6b6ce984d46897b139da16fa8df.k3X9o8wUFVCRAamq",
]

with open("datasets/test.json", "r", encoding="utf-8") as f:
    emergency_situation = json.load(f)


def clean_code_block(text: str) -> str:
    return text.replace("```python", "").replace("```", "").strip()


MAX_RETRIES = 5
RETRY_DELAY = 1


def _sync_call(index: int, client: ZhipuAiClient):
    print(f"[idx={index}] start")
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
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
            )
            out_path = os.path.join(OUT_DIR, f"result_{index + 1}.py")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(clean_code_block(resp.choices[0].message.content))
            print(f"[idx={index}] done")
            return
        except Exception as err:
            last_err = err
            print(f"[idx={index}] error: {err}, retry {attempt + 1}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    print(f"[idx={index}] failed after {MAX_RETRIES} retries, last error: {last_err}")


async def call_model(index: int, client: ZhipuAiClient):
    await asyncio.to_thread(_sync_call, index, client)


async def key_worker(
    key_id: int, client: ZhipuAiClient, indices: list[int], concurrency: int = 1
) -> float:
    sem = asyncio.Semaphore(concurrency)

    async def _run_one(idx: int):
        async with sem:
            await call_model(idx, client)

    t0 = time.time()
    await asyncio.gather(*[_run_one(i) for i in indices])
    elapsed = time.time() - t0
    print(f"[key={key_id}] elapsed: {elapsed:.2f}s")
    return elapsed


async def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    clients = [ZhipuAiClient(api_key=k) for k in API_KEYS]

    buckets = [[] for _ in API_KEYS]
    for i in range(len(emergency_situation)):
        buckets[i % len(API_KEYS)].append(i)

    workers = [
        key_worker(kid, clients[kid], buckets[kid], concurrency=1)
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
    review_code.main("datasets/test.json", OUT_DIR)
    print(f"Total processing time: {total_processing:.2f}s")