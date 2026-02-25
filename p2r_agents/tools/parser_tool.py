"""
从 parser_paper.json 按标题召回章节。
返回以顶层 section（大标题）为粒度的完整 parser。
"""
from typing import List, Dict, Any, Optional

from utils.json_util import read_parser_json, update_parser_json

def _norm(s: str) -> str:
    return " ".join((s or "").strip().lower().split())

def tool_recall_sections(
    titles: List[str],
    pdf_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    从 pdf_path 对应的 parser_paper.json 召回顶层 section（完整对象）。
    匹配规则：
    1) 命中顶层 section 标题 -> 返回该顶层 section 的完整 parser；
    2) 命中任意 subsection 标题 -> 也返回其所属顶层 section 的完整 parser。
    """
    try:
        outline = read_parser_json(pdf_path)
    except (FileNotFoundError, OSError, ValueError):
        return []
    if not isinstance(outline, list):
        return []

    def title_matched(s: str, ask_list: List[str]) -> bool:
        s_norm = _norm(s)
        return any(ask in s_norm or s_norm in ask for ask in ask_list)

    def has_match_in_tree(node: Dict[str, Any], ask_list: List[str]) -> bool:
        if title_matched(node.get("section_title", ""), ask_list):
            return True
        for sub in node.get("subsections") or []:
            if has_match_in_tree(sub, ask_list):
                return True
        return False

    results = []
    ask_set = [_norm(t) for t in titles]
    for sec in outline:
        if has_match_in_tree(sec, ask_set):
            results.append(sec)
    return results


def tool_update_sections(
    updated_sections: List[Dict[str, Any]],
    pdf_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    将 LLM 补全后的顶层 section 完整 parser 回写到原 parser_paper.json。

    参数 updated_sections 的每个元素都应是一个顶层 section 的完整对象（含 subsections）。
    回写策略：
    1) 按 section_title（归一化）匹配原始顶层 section，命中则替换；
    2) 未命中的新 section 追加到末尾；
    3) 其他原始 section 保持不变。
    """
    if not pdf_path or not isinstance(updated_sections, list):
        return {"success": False, "updated_count": 0, "appended_count": 0}
    try:
        outline = read_parser_json(pdf_path)
    except (FileNotFoundError, OSError, ValueError):
        return {"success": False, "updated_count": 0, "appended_count": 0}
    if not isinstance(outline, list):
        return {"success": False, "updated_count": 0, "appended_count": 0}

    incoming_map: Dict[str, Dict[str, Any]] = {}
    for sec in updated_sections:
        if isinstance(sec, dict):
            key = _norm(sec.get("section_title", ""))
            if key:
                incoming_map[key] = sec

    updated_count = 0
    new_outline: List[Dict[str, Any]] = []
    used_keys = set()

    for sec in outline:
        key = _norm(sec.get("section_title", ""))
        if key in incoming_map:
            new_outline.append(incoming_map[key])
            used_keys.add(key)
            updated_count += 1
        else:
            new_outline.append(sec)

    appended_sections = [v for k, v in incoming_map.items() if k not in used_keys]
    new_outline.extend(appended_sections)

    update_parser_json(pdf_path, new_outline)
    return {
        "success": True,
        "updated_count": updated_count,
        "appended_count": len(appended_sections),
        "total_sections": len(new_outline),
    }