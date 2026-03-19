"""
生成决策智能体的训练数据
三阶段流程：
1. 生成突发事件并按函数分组合并
2. 调用智谱AI glm-5 生成代码解决方案
3. 将结果整理为 LLaMA Factory 训练格式
"""
import sys
import os
import re
import json
import shutil
import time
import asyncio
import multiprocessing
from difflib import SequenceMatcher

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import prompts as prompts_mod
import generate_suitiations
from review_code import verify_file_with_timeout
import add_tokenizers

from zai import ZhipuAiClient

MODEL_NAME = "glm-4.7"
MAX_RETRIES = 5
RETRY_DELAY = 1
OUT_DIR = "datasets/glm4.7"

BASE_KEYS = [
    "a2751098f4ea4114a411860eeae6b8d8.3Hde3xtEWfPm9BCW",
    "0934c41d73ca4466ac275247b59f43ea.a0qXhTM84boG5NXT",
    "dc14be00604846329ab684128ad5af3f.SuYT32up0vDr91TL",
    "0d412435f4f748a1bfc24f0340e2e678.5njc8BCqRle6rsZg",
    "1c7b6776bd294a7c8fc87b84d4858b74.uhJnKdzQNBfPdmwL",
    "7d767b2a5ddc4d428c714a3462285805.S4lBGuUTLchLeJbZ",
    "7ef9c807602c4408b4091e6bd155497e.PePeRElMbqosmngf"
]
API_KEYS = [key for key in BASE_KEYS for _ in range(1)]

def clean_code_block(text):
    return text.replace("```python", "").replace("```", "").strip()


# ======================== 阶段1：生成突发事件并按函数分组 ========================

def generate_grouped_events(num_samples=50, save_path="datasets/decision_raw_train_datas.json"):
    generate_suitiations.generate_dataset(num_samples=num_samples, save_path=save_path)
    with open(save_path, "r", encoding="utf-8") as f:
        emergency_situations = json.load(f)

    results = []
    for emergency_situation in emergency_situations:
        events = emergency_situation["emergency_situation"].split(";")
        functions = emergency_situation["functions"]
        fn_to_events = {}
        fn_order = []
        for event_idx, event in enumerate(events):
            fn = functions[event_idx]
            if fn not in fn_to_events:
                fn_order.append(fn)
                fn_to_events[fn] = []
            fn_to_events[fn].append(event)
        merged_events = [";".join(fn_to_events[fn]) for fn in fn_order]
        for i in range(len(merged_events)):
            results.append({
                "emergency_situation": merged_events[i],
                "functions": fn_order[i],
            })

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"阶段1完成：生成 {len(results)} 条分组事件 -> {save_path}")
    return results


# ======================== 阶段2：调用智谱AI glm-5 生成代码 ========================

def _sync_call(index, client, emergency_situations, index_offset=0):
    out_index = index + index_offset
    print(f"[idx={out_index}] start")
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                temperature=0.9,
                top_p=0.95,
                messages=[
                    {"role": "system", "content": prompts_mod.SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": prompts_mod.USER_PROMPT.format(
                            EMERGENCY_SITUATIONS=emergency_situations[index]["emergency_situation"],
                            ORIGINAL_CODE=prompts_mod.functions_mapping[emergency_situations[index]["functions"]],
                        ),
                    },
                ],
            )
            out_path = os.path.join(OUT_DIR, f"result_{out_index}.py")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(clean_code_block(resp.choices[0].message.content))
            print(f"[idx={out_index}] done")
            return
        except Exception as err:
            last_err = err
            print(f"[idx={out_index}] error: {err}, retry {attempt + 1}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    print(f"[idx={out_index}] failed after {MAX_RETRIES} retries, last error: {last_err}")


async def call_model(index, client, emergency_situations, index_offset=0):
    await asyncio.to_thread(_sync_call, index, client, emergency_situations, index_offset)


async def key_worker(key_id, client, indices, emergency_situations, index_offset=0, concurrency=1):
    sem = asyncio.Semaphore(concurrency)

    async def _run_one(idx):
        async with sem:
            await call_model(idx, client, emergency_situations, index_offset)

    t0 = time.time()
    await asyncio.gather(*[_run_one(i) for i in indices])
    elapsed = time.time() - t0
    print(f"[key={key_id}] elapsed: {elapsed:.2f}s")
    return elapsed


async def generate_solutions(emergency_situations, index_offset=0):
    clients = [ZhipuAiClient(api_key=k) for k in API_KEYS]
    buckets = [[] for _ in API_KEYS]
    for i in range(len(emergency_situations)):
        buckets[i % len(API_KEYS)].append(i)

    workers = [
        key_worker(kid, clients[kid], buckets[kid], emergency_situations, index_offset, concurrency=1)
        for kid in range(len(API_KEYS))
    ]
    elapsed_list = await asyncio.gather(*workers)
    print(f"阶段2完成：生成代码 -> {OUT_DIR}/ (总处理时间: {sum(elapsed_list):.2f}s)")


# ======================== 阶段3：整理为训练数据格式 ========================

VERIFY_TIMEOUT = 5

def _verify_file(file_path, events):
    """验证单个结果文件是否完全解决了所有特情，返回 True/False"""
    result = verify_file_with_timeout(file_path, events, VERIFY_TIMEOUT)
    if result.get("timeout") or "error" in result:
        return False
    verify_result = result.get("result", {})
    return verify_result.get("solved", 0) == verify_result.get("total", 0)

def merge_and_format(
    emergency_situations,
    index_offset=1,
    save_path="datasets/decision_train_datas.json",
):
    results = []
    skipped = 0
    for idx, item in enumerate(emergency_situations):
        file_path = os.path.join(OUT_DIR, f"result_{idx + index_offset}.py")
        if not os.path.exists(file_path):
            print(f"[跳过] 缺少 {file_path}")
            skipped += 1
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read().strip()

        events = [e.strip() for e in item["emergency_situation"].split(";") if e.strip()]
        if not _verify_file(file_path, events):
            print(f"[跳过] result_{idx + index_offset}.py 未通过验证")
            skipped += 1
            continue

        original_code = prompts_mod.functions_mapping[item["functions"]]

        results.append({
            "system": prompts_mod.SYSTEM_PROMPT,
            "instruction": prompts_mod.USER_PROMPT.format(
                EMERGENCY_SITUATIONS=item["emergency_situation"],
                ORIGINAL_CODE=original_code,
            ),
            "input": "",
            "output": code,
        })

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"阶段3完成：{len(results)} 条通过验证加入训练集，{skipped} 条被过滤 -> {save_path}")


# ======================== 主流程 ========================

if __name__ == "__main__":
    raw_path = "datasets/decision_raw_train_datas.json"
    index_offset = 1
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    events = generate_grouped_events(num_samples=50, save_path=raw_path)
    asyncio.run(generate_solutions(events, index_offset=index_offset))
    
    # review code验证glm后，构建训练集
    with open(raw_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    merge_and_format(events, index_offset=index_offset)
    add_tokenizers.main()
