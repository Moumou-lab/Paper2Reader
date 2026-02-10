# 标准导入
import json
from typing import List, Dict
from pathlib import Path
from loguru import logger
from tqdm import tqdm
# 自定义导入
from p2r_agents import (
    MentorAgent,
    ParserAgent,
)
from p2r_agents.prompts import (
    mentor_outline_prompt, 
    parser_page_update_prompt,
)
from utils.pdf_util import (
    get_pdf_info,
    extract_pdf_text_from_page,
)
from utils.json_util import (
    read_parser_json,
    update_parser_json,
)


async def main_workflow(pdf_path: str) -> Dict:
    pdf_info = get_pdf_info(pdf_path)
    logger.success(f"论文基本信息如下:\n {pdf_info}")
    pdf_text_list = []
    for page in tqdm(range(1, pdf_info['page_count']+1), desc="论文文本提取进度..."):
        text = extract_pdf_text_from_page(pdf_path, page)
        pdf_text_list.append(text)
    logger.success(f"全文页数: {len(pdf_text_list)}")

    # 第一步: MentorAgent 基于全文提取章节骨架（仅标题，其他字段保持空占位）
    outline_prompt = mentor_outline_prompt(pdf_text_list)
    outline_result = MentorAgent().call_response(outline_prompt).content
    section_outline = json.loads(outline_result)
    update_parser_json(pdf_path, section_outline)
    logger.success(f"初始章节骨架: \n{json.dumps(section_outline, ensure_ascii=False, indent=2)}")

    # 第二步: ParserAgent 按页补充骨架中的字段
    for page in tqdm(range(1, pdf_info['page_count'] + 1), desc="论文逐页补充进度..."):
        section_outline = read_parser_json(pdf_path)
        page_text = pdf_text_list[page - 1]
        page_prompt = parser_page_update_prompt(page, page_text, section_outline)
        page_result = ParserAgent().call_response(page_prompt).content
        section_outline = json.loads(page_result)
        update_parser_json(pdf_path, section_outline)
        logger.success(f"第 {page} 页补充后的章节 JSON 已更新")

        if page == 2: break # 调试使用, 后续删除

    final_json = read_parser_json(pdf_path)
    logger.success(f"论文解析结果: \n{json.dumps(final_json, ensure_ascii=False, indent=2)}")