from typing import List, Dict
from pathlib import Path
import fitz  # PyMuPDF

# ================================ Internal Functions ================================
def _validate_pdf_path(pdf_path: str) -> Path:
    """验证 PDF 路径"""
    path = Path(pdf_path)
    if not path.exists() or not path.suffix == ".pdf":
        raise ValueError(f"无效的 PDF 路径: {pdf_path}")
    return path

# ================================ Public Functions ================================
def get_pdf_info(pdf_path: str) -> Dict:
    """获取 PDF 信息"""
    try:
        pdf_path = _validate_pdf_path(pdf_path)
    except ValueError as e:
        raise ValueError(f"无效的 PDF 路径: {e}")

    # 获取文件大小（靠文件系统，而不是内部流）
    file_size = pdf_path.stat().st_size

    with fitz.open(pdf_path) as pdf:
        info = {
            "page_count": pdf.page_count,
            "file_size(bytes)": file_size,
            "file_name": pdf_path.name,
        }
    return info

def extract_pdf_text_from_page(pdf_path: str, target_page: int) -> str:
    """
    使用 PyMuPDF (fitz) 对 PDF 目标页进行文本提取。
    Args:
        pdf_path: PDF 文件路径
        target_page: 目标页码（从 1 开始，对用户友好）
    Returns:
        提取的文本字符串
    """

    doc = fitz.open(pdf_path)
    if target_page < 1 or target_page > doc.page_count:
        raise ValueError(f"target_page 超出范围: 1 ~ {doc.page_count}")
    page = doc.load_page(target_page - 1)  # PyMuPDF 页码从 0 开始

    # 尝试先直接提取文本
    text = page.get_text().strip()

    return text