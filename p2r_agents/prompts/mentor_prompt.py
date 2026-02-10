"""
Mentor Agent 的提示词
"""
def mentor_system_prompt() -> str:
    return """你是一个通用型的AI助手，能够处理多样化任务。
根据用户的具体要求，完成任务需求。
"""

def mentor_outline_prompt(pdf_text_list):
    return f"""
你将收到一篇论文按页提取后的全文文本列表。

【任务】
仅根据全文文本，输出论文的章节骨架 JSON（顶层是 list）。

【输出结构】
顶层必须是 JSON 数组，每个元素代表一个大标题章节，字段如下：
{{
  "section_title": "章节标题",
  "section_content": "内容",
  "main_contributions": [],
  "methodology": "方法论",
  "experiments": [],
  "conclusions": [],
  "subsections": [
    {{
      "section_title": "小标题",
      "section_content": "内容",
      "main_contributions": [],
      "methodology": "方法论",
      "experiments": [],
      "conclusions": [],
      "subsections": []
    }}
  ]
}}

【规则】
1. 只填写标题层级：大标题和小标题。
2. 除标题外，其他字段必须保持空占位（"" 或 []），不能填内容。
3. 若某大标题下没有小标题，subsections 必须是 []。
4. 标题命名尽量贴合论文原文，不要编造。
5. 只输出合法 JSON 数组，不要输出 Markdown 代码块，不要输出解释文字。

【输入全文】
{pdf_text_list}
"""