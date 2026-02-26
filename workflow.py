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
    ComposeAgent,
)
from p2r_agents.prompts import (
    mentor_outline_prompt, 
    parser_page_update_prompt,
    compose_report_prompt,
)
from utils.pdf_util import (
    get_pdf_info,
    extract_pdf_text_from_page,
    extract_pdf_images_with_captions,
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
    # 图像抽取
    image_output_dir = Path("outputs") / Path(pdf_path).stem / "images"
    captions_file = image_output_dir / "captions.json"
    captions_data = []

    image_items = extract_pdf_images_with_captions(pdf_path)
    logger.success(f"图片抽取完成，共 {len(image_items)} 张，caption 文件: {captions_file}")

    if captions_file.exists():
        try:
            captions_data = json.loads(captions_file.read_text(encoding="utf-8"))
            logger.success(f"已加载 captions.json，共 {len(captions_data)} 条")
        except Exception as e:
            logger.warning(f"读取 captions.json 失败，将按无图模式生成报告: {e}")

    # # 第一步: MentorAgent 基于全文提取章节骨架（仅标题，其他字段保持空占位）
    # outline_prompt = mentor_outline_prompt(pdf_text_list)
    # outline_result = MentorAgent().call_response(outline_prompt).content
    # section_outline = json.loads(outline_result)
    # update_parser_json(pdf_path, section_outline)
    # logger.success(f"初始章节骨架: \n{json.dumps(section_outline, ensure_ascii=False, indent=2)}")

    # # 第二步: ParserAgent 按页补充骨架中的字段
    # parser_agent = ParserAgent(current_pdf_path=pdf_path)
    # for page in tqdm(range(1, pdf_info['page_count']), desc="论文逐页补充进度..."):
    #     page_text = pdf_text_list[page - 1] + pdf_text_list[page] # 每次 Concat 两页文本, 确保上下文连续性
    #     page_prompt = parser_page_update_prompt(page, page_text)
    #     page_result = parser_agent.call_response(page_prompt).content
    #     logger.success(f"第 {page} 页处理完成: {page_result}")
    #     if page == 6: break # 调试使用, 后续删除

    final_json = read_parser_json(pdf_path)
    logger.success(f"论文解析结果: \n{json.dumps(final_json, ensure_ascii=False, indent=2)}")

    # 第三步: ComposeAgent 基于 parser_paper 生成 Markdown 报告
    compose_agent = ComposeAgent(current_pdf_path=pdf_path)
    compose_prompt = compose_report_prompt(final_json, captions_data)
    compose_result = compose_agent.call_response(compose_prompt)
    report_md = compose_result.content if compose_result and compose_result.content else ""

    report_path = Path("outputs") / Path(pdf_path).stem / "report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_md, encoding="utf-8")
    logger.success(f"组会报告已生成, 报告路径: {report_path}")
    