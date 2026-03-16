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
from review_code import run_verify_case

EDIT_START = "<<EDIT_START>>"
EDIT_END = "<<EDIT_END>>"

from zai import ZhipuAiClient

MODEL_NAME = "glm-5"
MAX_RETRIES = 5
RETRY_DELAY = 1
OUT_DIR = "datasets/glm5"

BASE_KEYS = [
    "5c6d3d4312f94fa1a6773b17aa97b75d.w9cZbahrqSsPSeTt",
    "5123fb6446a248648c88a1c20007a5a6.GzwNMUsco0qkbQl1",
    "11724e5a71d24cd9bb1cccd52fe6a29a.DnAUeBnWIte1Nqvm",
    "90bab6b6ce984d46897b139da16fa8df.k3X9o8wUFVCRAamq",
    "893c0081a0df4938b8bb1e2c83a44fab.hchpXHmo65DHBrgX",
]
API_KEYS = [key for key in BASE_KEYS for _ in range(3)]

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
    # if os.path.exists(OUT_DIR):
    #     shutil.rmtree(OUT_DIR)
    # os.makedirs(OUT_DIR, exist_ok=True)

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
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p = multiprocessing.Process(target=run_verify_case, args=(file_path, events, return_dict))
    p.start()
    p.join(VERIFY_TIMEOUT)
    if p.is_alive():
        p.terminate()
        p.join()
        return False
    if 'error' in return_dict:
        return False
    result = return_dict.get('result', {})
    return result.get('solved', 0) == result.get('total', 0)


def _normalize_line(line):
    line = re.sub(r"#.*$", "", line)
    return re.sub(r"\s+", "", line)


def _get_comparable_lines(text):
    result = []
    for idx, raw in enumerate(text.splitlines()):
        norm = _normalize_line(raw)
        if norm:
            result.append((norm, idx))
    return result


def _to_line_ranges(indices):
    if not indices:
        return []
    indices = sorted(set(indices))
    ranges = []
    start = end = indices[0]
    for i in indices[1:]:
        if i == end + 1:
            end = i
        else:
            ranges.append((start, end))
            start = end = i
    ranges.append((start, end))
    return ranges


def _get_edit_line_ranges(original, generated):
    orig_cmp = _get_comparable_lines(original)
    gen_cmp = _get_comparable_lines(generated)
    orig_norm = [x[0] for x in orig_cmp]
    gen_norm = [x[0] for x in gen_cmp]
    gen_line_map = [x[1] for x in gen_cmp]
    matcher = SequenceMatcher(a=orig_norm, b=gen_norm, autojunk=False)
    changed = []
    for tag, _, _, b0, b1 in matcher.get_opcodes():
        if tag != "equal" and b0 < b1:
            changed.extend(gen_line_map[b0:b1])
    return _to_line_ranges(changed)


def _add_edit_markers(text, line_ranges):
    if not line_ranges:
        return text
    lines = text.splitlines(keepends=True)
    offsets = []
    cur = 0
    for ln in lines:
        offsets.append(cur)
        cur += len(ln)
    result = text
    for start_line, end_line in reversed(line_ranges):
        if start_line < 0 or start_line >= len(lines):
            continue
        end_line = max(start_line, min(end_line, len(lines) - 1))
        start_pos = offsets[start_line]
        end_trim_len = len(lines[end_line].rstrip("\r\n"))
        end_pos = offsets[end_line] + end_trim_len
        result = result[:end_pos] + EDIT_END + result[end_pos:]
        result = result[:start_pos] + EDIT_START + result[start_pos:]
    return result


def mark_edits(original_code, generated_code):
    """对比原始代码和生成代码，在差异行上插入 EDIT_START/EDIT_END 标记"""
    line_ranges = _get_edit_line_ranges(original_code, generated_code)
    return _add_edit_markers(generated_code, line_ranges)


def merge_and_format(
    emergency_situations,
    index_offset=0,
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
    index_offset = 0

    # events = generate_grouped_events(num_samples=200, save_path=raw_path)
    # asyncio.run(generate_solutions(events, index_offset=index_offset))
    
    # review code验证glm后，构建训练集
    with open(raw_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    merge_and_format(events, index_offset=index_offset)
