"""
Tools for recalling and updating sections in parser_paper.json.
"""
from typing import List, Dict, Any
from pydantic import BaseModel

def tool_recall_sections(titles: List[str]) -> List[Dict[str, Any]]:
    """
    召回 section list
    精准匹配section或subsection的标题, 模糊匹配兜底
    """
    results = [
        {
            "section_tittle": "MOCK TiTTLE - 1",
            "section_content": "MOCK CONTENT - 1",
        },
        {
            "section_tittle": "MOCK TiTTLE - 2",
            "section_content": "MOCK CONTENT - 2",
            "subsections": [
                {
                    "section_tittle": "MOCK TiTTLE - 2.1",
                    "section_content": "MOCK CONTENT - 2.1",
                },
            ],
        }
    ]
    return results