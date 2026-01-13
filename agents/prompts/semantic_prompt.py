"""
Semantic Agent 的提示词
"""

SEMANTIC_PROMPT_TEMPLATE = """你是一个专业的学术论文分析助手。基于以下已解析的论文信息，进行深入的语义分析和理解。

已解析的论文信息：
{parsed_data}

请进行以下分析，并以 JSON 格式返回：

{{
    "core_concepts": ["核心概念1", "核心概念2"],
    "research_questions": ["研究问题1", "研究问题2"],
    "methodology_analysis": "方法论的详细分析",
    "key_insights": ["关键洞察1", "关键洞察2"],
    "related_work_summary": "相关工作总结",
    "technical_details": "技术细节说明",
    "strengths": ["优点1", "优点2"],
    "limitations": ["局限性1", "局限性2"],
    "future_work": "未来工作方向",
    "practical_applications": "实际应用场景"
}}

请提供深入、准确的分析，帮助读者更好地理解论文的核心内容。
"""
