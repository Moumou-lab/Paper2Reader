# 标准导入
from tempfile import tempdir
from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
)
from typing import List, Dict
from pathlib import Path
from loguru import logger

# 自定义导入
from p2r_agents import (
    mentor_agent,
    ParserAgent,
)
from utils.pdf_util import (
    get_pdf_info,
    extract_pdf_text_from_page,
)



async def main_workflow(pdf_path: str) -> Dict:
    pdf_info = get_pdf_info(pdf_path)
    logger.success(f"论文基本信息如下:\n {pdf_info}")
    parser_messages = []
    for page in range(1, pdf_info['page_count']+1): # index 从 1 开始
        text = extract_pdf_text_from_page(pdf_path, page)
        logger.info(f"第 {page} 页文本如下:\n {text}")
        parser_messages.append({"role": "user", "content": text})
        cur_section_result = await Runner.run(ParserAgent, parser_messages)

        parser_messages[-1] = {"role": "user", "content": f"论文第{page}页的关键信息"}
        parser_messages.append({"role": "assistant", "content": str(cur_section_result.final_output)}) # 这里直接 str 强转, 后续可以考虑优化
        logger.success(parser_messages)


        if page == 10: break # attention一共就10页, 目前测试用, 后续删除
    
    # ToDo: mentor_agent 调用, 总结全文的解析结果
    paper_parser_query = f"""
以页为单位, 论文解析结果如下:
{parser_messages}
你需要把这个汇总, 输出一份整体的论文解析结果, 包括论文的章节信息、关键信息、评价和建议等。
"""
    paper_parser_result = await Runner.run(mentor_agent, paper_parser_query)
    logger.success(f"论文解析结果: \n{paper_parser_result.final_output}")