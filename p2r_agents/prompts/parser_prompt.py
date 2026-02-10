"""
Parser Agent 的提示词
"""


def parser_system_prompt() -> str:
    return """你是一个专业的论文解析助手。
你的输入会包含：
1) 当前页 OCR 文本
2) 一个章节骨架 JSON（顶层 list，含 section_title 和 subsections）

你的任务是：只基于当前页文本，对该 JSON 进行“原地补充”，并返回更新后的完整 JSON。
"""


def parser_page_update_prompt(page: int, page_text: str, current_outline) -> str:
    return f"""
【任务】
根据当前页文本，补充已有章节 JSON（不要丢结构）。

【当前页码】
{page}

【当前页文本】
{page_text}

【当前章节 JSON】
{current_outline}

【补充规则】
1. 只在能匹配到对应章节时补充字段：
   - section_content
   - main_contributions
   - methodology
   - experiments
   - conclusions
2. 章节匹配优先依据 section_title（大小写、标点、编号可做合理归一化）。
3. 保留已有内容，新增内容与已有内容合并并去重，不要覆盖掉已补充信息。
4. 未在本页出现证据的字段不要编造。
5. 公式以 Latex 格式输出
6. 顶层结构必须保持为 list；每个节点字段必须完整保留：
   - section_title
   - section_content
   - main_contributions
   - methodology
   - experiments
   - conclusions
   - subsections
7. 如本页无有效信息，原样返回输入 JSON。
8. 仅输出合法 JSON（顶层 list），不要输出解释和 Markdown 代码块。
"""

