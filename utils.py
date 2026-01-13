"""
工具函数
"""
import os
from pathlib import Path
from typing import Optional
from loguru import logger


def read_paper(file_path: str) -> str:
    """
    读取论文文件
    
    Args:
        file_path: 论文文件路径
        
    Returns:
        论文内容（文本）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"成功读取论文文件: {file_path}")
        return content
    except Exception as e:
        logger.error(f"读取论文文件失败: {str(e)}")
        raise


def save_note(note_content: str, output_path: Optional[str] = None, paper_title: Optional[str] = None) -> str:
    """
    保存笔记到文件
    
    Args:
        note_content: 笔记内容
        output_path: 输出文件路径（可选）
        paper_title: 论文标题（用于生成文件名）
        
    Returns:
        保存的文件路径
    """
    # 如果没有指定输出路径，使用默认路径
    if not output_path:
        output_dir = Path('outputs')
        output_dir.mkdir(exist_ok=True)
        
        if paper_title:
            # 清理标题，用作文件名
            safe_title = "".join(c for c in paper_title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]  # 限制长度
            output_path = output_dir / f"{safe_title}_note.md"
        else:
            output_path = output_dir / "paper_note.md"
    else:
        # 如果指定了输出路径，确保目录存在
        output_path_obj = Path(output_path)
        output_dir = output_path_obj.parent
        if output_dir and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_path_obj
    
    # 保存文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(note_content)
        logger.info(f"笔记已保存到: {output_path}")
        return str(output_path)
    except Exception as e:
        logger.error(f"保存笔记失败: {str(e)}")
        raise


def get_paper_files(papers_dir: str = 'papers') -> list:
    """
    获取论文目录下的所有文件
    
    Args:
        papers_dir: 论文目录路径
        
    Returns:
        文件路径列表
    """
    papers_path = Path(papers_dir)
    if not papers_path.exists():
        return []
    
    # 支持的论文文件格式
    supported_extensions = ['.md', '.txt', '.pdf']
    
    paper_files = []
    for ext in supported_extensions:
        paper_files.extend(papers_path.glob(f'*{ext}'))
    
    return [str(f) for f in paper_files]
