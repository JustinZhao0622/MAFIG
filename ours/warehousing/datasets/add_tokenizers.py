"""
在 juece_train_data.json 中添加 loss 字段：
比较原始代码与 response，忽略换行/空白/注释差异，
在 response 的差异代码段上插入 <<EDIT_START>> 和 <<EDIT_END>>。
"""

import json
import re
from difflib import SequenceMatcher

EDIT_START = "<<EDIT_START>>"
EDIT_END = "<<EDIT_END>>"

INPUT_PATH = "/root/code/MAFIG/ours/warehousing/datasets/decision_train_datas.json"
OUTPUT_PATH = "/root/code/MAFIG/ours/warehousing/datasets/decision_loss_train_datas.json"

_CODE_BLOCK_RE = re.compile(
    r"CODE:\s*(?P<code>.*?)\s*请基于上述突发事件，对代码进行必要修改。\s*$",
    re.DOTALL,
)


def extract_original_code(prompt: str):
    if not isinstance(prompt, str) or not prompt:
        return None
    match = _CODE_BLOCK_RE.search(prompt)
    if not match:
        return None
    return match.group("code").strip()


def normalize_line(line: str) -> str:
    line = re.sub(r"#.*$", "", line)
    return re.sub(r"\s+", "", line)


_DOCSTRING_DELIM = re.compile(r'^\s*("""|\'\'\')')


def _in_docstring(lines: list[str], idx: int) -> bool:
    """判断 lines[idx] 是否处于 docstring 内部"""
    toggle = 0
    for i in range(idx):
        stripped = lines[i].strip()
        count = stripped.count('"""') + stripped.count("'''")
        toggle += count
    return toggle % 2 == 1


def get_comparable_lines(text: str):
    raw_lines = text.splitlines()
    result = []
    in_doc = False
    for idx, raw in enumerate(raw_lines):
        stripped = raw.strip()
        delim_count = stripped.count('"""') + stripped.count("'''")
        if delim_count % 2 == 1:
            in_doc = not in_doc
        if in_doc or delim_count > 0:
            continue
        norm = normalize_line(raw)
        if norm:
            result.append((norm, idx))
    return result


def to_line_ranges(indices):
    """把行号列表压缩为连续区间[(start, end), ...]，end 为包含端。"""
    if not indices:
        return []
    indices = sorted(set(indices))
    ranges = []
    start = indices[0]
    end = indices[0]
    for i in indices[1:]:
        if i == end + 1:
            end = i
        else:
            ranges.append((start, end))
            start = i
            end = i
    ranges.append((start, end))
    return ranges


def get_edit_line_ranges(original: str, generated: str):
    """
    返回 generated 中需要打标的行区间（基于行级对齐，支持多段）。
    """
    orig_cmp = get_comparable_lines(original)
    gen_cmp = get_comparable_lines(generated)

    orig_norm = [x[0] for x in orig_cmp]
    gen_norm = [x[0] for x in gen_cmp]
    gen_line_map = [x[1] for x in gen_cmp]

    matcher = SequenceMatcher(a=orig_norm, b=gen_norm, autojunk=False)
    changed_line_indices = []

    for tag, _, _, b0, b1 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if b0 < b1:
            changed_line_indices.extend(gen_line_map[b0:b1])

    return to_line_ranges(changed_line_indices)


def add_markers_by_line_ranges(text: str, line_ranges):
    if not line_ranges:
        return text

    lines = text.splitlines(keepends=True)
    if not lines:
        return text

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
        end_line_text = lines[end_line]
        end_trim_len = len(end_line_text.rstrip("\r\n"))
        end_pos = offsets[end_line] + end_trim_len

        result = result[:end_pos] + EDIT_END + result[end_pos:]
        result = result[:start_pos] + EDIT_START + result[start_pos:]

    return result


def process_record(record: dict) -> bool:
    if not isinstance(record, dict):
        return False
    prompt = record.get("instruction")
    response = record.get("output")
    if not isinstance(prompt, str) or not isinstance(response, str):
        return False

    original_code = extract_original_code(prompt)
    if not original_code:
        return False

    line_ranges = get_edit_line_ranges(original_code, response)
    record["loss"] = add_markers_by_line_ranges(response, line_ranges)
    return True


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("输入数据格式错误：顶层必须是 list。")

    success = 0
    failed = 0
    for item in data:
        if process_record(item):
            success += 1
        else:
            failed += 1

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"处理完成: success={success}, failed={failed}, output={OUTPUT_PATH}")


if __name__ == "__main__":
    main()
