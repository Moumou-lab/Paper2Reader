import re
import json
from typing import List, Dict, Any
from pathlib import Path
import fitz  # PyMuPDF

# ================================ Internal Functions ================================
def _validate_pdf_path(pdf_path: str) -> Path:
    """验证 PDF 路径"""
    path = Path(pdf_path)
    if not path.exists() or not path.suffix == ".pdf":
        raise ValueError(f"无效的 PDF 路径: {pdf_path}")
    return path


def _get_image_output_dir(pdf_path: str) -> Path:
    paper_name = Path(pdf_path).stem
    output_dir = Path("outputs") / paper_name / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _horizontal_overlap_ratio(a: fitz.Rect, b: fitz.Rect) -> float:
    overlap = max(0.0, min(a.x1, b.x1) - max(a.x0, b.x0))
    base = max(1.0, min(a.width, b.width))
    return overlap / base


def _find_best_caption_for_image(
    page: fitz.Page,
    image_rect: fitz.Rect,
    search_margin: float = 140.0,
) -> Dict[str, Any]:
    """
    在图片附近搜索最可能的图标题（caption）。
    优先下方文本，其次上方文本；结合关键词、距离和水平重叠评分。
    """
    caption_regex = re.compile(r"(figure|fig\.?|图)\s*[\.:]?\s*\d*", re.IGNORECASE)
    best_text = ""
    best_score = 0.0

    blocks = page.get_text("blocks")
    for block in blocks:
        x0, y0, x1, y1, text = block[:5]
        if not text or not text.strip():
            continue

        block_rect = fitz.Rect(x0, y0, x1, y1)
        overlap_ratio = _horizontal_overlap_ratio(image_rect, block_rect)
        if overlap_ratio < 0.18:
            continue

        position_bonus = 0.0
        distance = 1e9
        # 图片下方（最常见）
        if block_rect.y0 >= image_rect.y1:
            distance = block_rect.y0 - image_rect.y1
            if distance <= search_margin:
                position_bonus = 0.5
        # 图片上方（部分论文会把 caption 放上方）
        elif block_rect.y1 <= image_rect.y0:
            distance = image_rect.y0 - block_rect.y1
            if distance <= search_margin * 0.7:
                position_bonus = 0.25
        else:
            # 与图片有垂直重叠时一般不是 caption
            continue

        if position_bonus <= 0:
            continue

        keyword_bonus = 0.6 if caption_regex.search(text) else 0.0
        proximity_bonus = max(0.0, 0.5 - distance / max(search_margin, 1.0))
        overlap_bonus = min(0.4, overlap_ratio * 0.4)
        length_penalty = 0.0 if len(text.strip()) <= 300 else -0.2
        score = keyword_bonus + proximity_bonus + overlap_bonus + position_bonus + length_penalty

        if score > best_score:
            best_score = score
            best_text = " ".join(text.split())

    confidence = max(0.0, min(1.0, best_score / 1.8))
    return {"caption": best_text, "caption_confidence": round(confidence, 4)}

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

    with fitz.open(pdf_path) as doc:
        if target_page < 1 or target_page > doc.page_count:
            raise ValueError(f"target_page 超出范围: 1 ~ {doc.page_count}")
        page = doc.load_page(target_page - 1)  # PyMuPDF 页码从 0 开始

        # 尝试先直接提取文本
        text = page.get_text().strip()
        return text


def extract_pdf_images_with_captions(
    pdf_path: str,
    search_margin: float = 140.0,
) -> List[Dict[str, Any]]:
    """
    抽取 PDF 中的位图，并为每张图匹配最可能的图标题（caption）。
    返回字段:
    - image_path: 图片绝对路径
    - relative_path: 相对 outputs/<paper>/ 的路径
    - page/index/xref/width/height/bbox
    - caption/caption_confidence
    """
    valid_pdf_path = _validate_pdf_path(pdf_path)
    image_output_dir = _get_image_output_dir(str(valid_pdf_path))
    results: List[Dict[str, Any]] = []

    with fitz.open(valid_pdf_path) as doc:
        for page_idx in range(doc.page_count):
            page = doc.load_page(page_idx)
            page_num = page_idx + 1
            images = page.get_images(full=True)
            for image_idx, image in enumerate(images, start=1):
                xref = image[0]
                image_info = doc.extract_image(xref)
                image_bytes = image_info.get("image")
                if not image_bytes:
                    continue

                ext = image_info.get("ext", "png")
                file_name = f"p{page_num}_i{image_idx}_x{xref}.{ext}"
                file_path = image_output_dir / file_name
                file_path.write_bytes(image_bytes)

                rects = page.get_image_rects(xref)
                rect = rects[0] if rects else fitz.Rect(0, 0, 0, 0)
                caption_info = _find_best_caption_for_image(
                    page=page,
                    image_rect=rect,
                    search_margin=search_margin,
                )

                results.append(
                    {
                        "image_path": str(file_path),
                        "relative_path": f"images/{file_name}",
                        "page": page_num,
                        "index": image_idx,
                        "xref": xref,
                        "width": int(image_info.get("width", rect.width or 0)),
                        "height": int(image_info.get("height", rect.height or 0)),
                        "bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
                        "caption": caption_info["caption"],
                        "caption_confidence": caption_info["caption_confidence"],
                    }
                )

    caption_file = image_output_dir / "captions.json"
    caption_file.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return results