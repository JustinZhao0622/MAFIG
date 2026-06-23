"""
本地调用大模型：按 test.json 逐条生成结果文件，并记录多模型多轮实验日志
"""
import ast
import gc
import json
import logging
import os
import shutil
import time

from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

import prompts as prompts_mod
import review_code

import torch
seed = 42
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="local-llm-results/local_llm.log",
    filemode="a",
)
logger = logging.getLogger(__name__)


DATASET_FILE = "datasets/test.json"
BASE_OUT_DIR = "local-llm-results"
MODEL_RUNS = 2

MODELS = [
    # {
    #     "name": "Qwen2.5-Coder-7B-Instruct",
    #     "path": "/data/huggingface/Qwen2.5-Coder-7B-Instruct",
    #     "out_dir": "qwen2.5-coder-7b-instruct",
    # },
    # {
    #     "name": "Meta-Llama-3.1-8B-Instruct",
    #     "path": "/data/huggingface/Meta-Llama-3.1-8B-Instruct",
    #     "out_dir": "meta-llama-3.1-8b-instruct",
    # },
    # {
    #     "name": "glm-4-9b-chat",
    #     "path": "/data/huggingface/glm-4-9b-chat",
    #     "out_dir": "glm-4-9b-chat",
    # },
    {
        "name": "Qwen2.5-7B-Instruct",
        "path": "/data/huggingface/Qwen2.5-7B-Instruct",
        "out_dir": "Qwen2.5-7B-Instruct",
    },
    # {
    #     "name": "Qwen3-8B",
    #     "path": "/data/huggingface/Qwen3-8B",
    #     "out_dir": "Qwen3-8B",
    # },
]


with open(DATASET_FILE, "r", encoding="utf-8") as f:
    emergency_situations = json.load(f)


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
    code = "\n\nimport heapq\nimport time\nimport random\n\n" + code
    return code.strip()


def build_plain_prompt(item):
    user_prompt = prompts_mod.USER_PROMPT.format(
        EMERGENCY_SITUATIONS=item["emergency_situation"],
        ORIGINAL_CODE=prompts_mod.ORIGINAL_CODE,
    )
    return (
        f"{prompts_mod.SYSTEM_PROMPT.strip()}\n\n"
        f"{user_prompt.strip()}\n\n"
        "修改后的完整 Python 代码:\n"
    )


def build_inputs(tokenizer):
    inputs = []
    for item in emergency_situations:
        messages = [
            {"role": "system", "content": prompts_mod.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": prompts_mod.USER_PROMPT.format(
                    EMERGENCY_SITUATIONS=item["emergency_situation"],
                    ORIGINAL_CODE=prompts_mod.ORIGINAL_CODE,
                ),
            },
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs.append(text)
    return inputs


def prepare_out_dir(out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)


def call_local_model_batch(model_path, out_dir):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    llm = LLM(
        model=model_path,
        dtype="auto",
        trust_remote_code=True,
        gpu_memory_utilization=0.9,
        seed=seed,
    )
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2560, seed=seed)

    inputs = build_inputs(tokenizer)
    outputs = llm.generate(inputs, sampling_params)

    for idx, out in enumerate(outputs):
        raw_text = out.outputs[0].text
        code_only = clean_code_block(raw_text)
        file_path = os.path.join(out_dir, f"result_{idx+1}.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_only + "\n")

    del llm
    del tokenizer
    gc.collect()


def run_single_experiment(model_cfg, run_idx):
    out_dir = os.path.join(BASE_OUT_DIR, model_cfg["out_dir"], f"run_{run_idx}")
    prepare_out_dir(out_dir)

    start_time = time.time()
    call_local_model_batch(model_cfg["path"], out_dir)
    elapsed = time.time() - start_time
    accuracy = review_code.main(DATASET_FILE, out_dir)

    logger.info(
        "model=%s, run=%s, time=%.2f, accuracy=%s, out_dir=%s",
        model_cfg["name"],
        run_idx,
        elapsed,
        accuracy,
        out_dir,
    )


def main():
    logger.info("=======================================================")
    logger.info("start local llm benchmark: models=%s, runs=%s", len(MODELS), MODEL_RUNS)

    for model_cfg in MODELS:
        for run_idx in range(1, MODEL_RUNS + 1):
            run_single_experiment(model_cfg, run_idx)


if __name__ == "__main__":
    main()
