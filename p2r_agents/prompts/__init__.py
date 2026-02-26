"""
Prompts 模块, 包含所有 Prompt 的定义
"""
from .parser_prompt import parser_system_prompt
from .parser_prompt import parser_page_update_prompt
from .mentor_prompt import mentor_outline_prompt
from .compose_prompt import compose_report_prompt
__all__ = [
    "parser_system_prompt",
    "parser_page_update_prompt",
    "mentor_outline_prompt",
    "compose_report_prompt",
]