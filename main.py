"""
Paper2Reader 主入口文件
"""
import argparse
import sys
from pathlib import Path
from workflow import Paper2ReaderWorkflow
from utils import read_paper, save_note, get_paper_files
from loguru import logger


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Paper2Reader - 多 Agent 论文阅读和笔记生成系统'
    )
    parser.add_argument(
        'input',
        type=str,
        nargs='?',
        default=None,
        help='论文文件名（从 papers/ 目录）或完整文件路径，或论文内容（如果使用 -t 选项）'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='输出笔记文件路径（可选，默认保存在 outputs/ 目录）'
    )
    parser.add_argument(
        '-t', '--text',
        action='store_true',
        help='直接输入论文文本内容（而不是文件路径）'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='列出 papers/ 目录下的所有论文文件'
    )
    
    args = parser.parse_args()
    
    # 列出论文文件
    if args.list or args.input is None:
        paper_files = get_paper_files()
        if paper_files:
            print("可用的论文文件:")
            for i, file_path in enumerate(paper_files, 1):
                file_name = Path(file_path).name
                print(f"  {i}. {file_name}")
            print(f"\n使用方法: python main.py <文件名>")
            print(f"示例: python main.py {Path(paper_files[0]).name}")
        else:
            print("papers/ 目录下没有找到论文文件")
        return
    
    # 获取论文内容
    if args.text:
        paper_content = args.input
    else:
        # 确定论文文件路径
        paper_path = args.input
        paper_path_obj = Path(paper_path)
        
        # 检查文件是否存在
        file_found = False
        
        # 情况1: 绝对路径或相对路径，文件存在
        if paper_path_obj.exists():
            paper_path = str(paper_path_obj.resolve())
            file_found = True
        # 情况2: 尝试在 papers/ 目录中查找
        else:
            papers_dir = Path('papers')
            # 直接拼接路径
            potential_path = papers_dir / paper_path
            if potential_path.exists():
                paper_path = str(potential_path.resolve())
                file_found = True
            else:
                # 尝试模糊匹配文件名（不区分大小写）
                paper_files = get_paper_files()
                matching_files = [
                    f for f in paper_files 
                    if Path(f).name.lower() == paper_path_obj.name.lower() or 
                       Path(f).stem.lower() == paper_path_obj.stem.lower()
                ]
                
                if matching_files:
                    paper_path = matching_files[0]
                    file_found = True
                    logger.info(f"找到匹配的论文文件: {paper_path}")
        
        # 如果文件不存在，提示错误
        if not file_found:
            logger.error(f"❌ 错误：找不到论文文件 '{args.input}'")
            logger.error(f"   在 papers/ 目录中未找到该文件")
            
            # 列出可用的论文文件
            available_files = get_paper_files()
            if available_files:
                print("\n可用的论文文件:")
                for i, file_path in enumerate(available_files, 1):
                    file_name = Path(file_path).name
                    print(f"  {i}. {file_name}")
                print(f"\n提示：可以直接使用文件名，例如: python main.py {Path(available_files[0]).name}")
            else:
                print("\npapers/ 目录下没有找到任何论文文件")
            
            sys.exit(1)
        
        # 读取论文文件
        try:
            # 检查文件扩展名，PDF 文件需要特殊处理
            final_path_obj = Path(paper_path)
            file_ext = final_path_obj.suffix.lower()
            if file_ext == '.pdf':
                logger.warning("⚠️  检测到 PDF 文件，当前版本仅支持文本文件（.md, .txt）")
                logger.warning("   请先将 PDF 转换为文本格式，或使用文本文件")
                sys.exit(1)
            
            paper_content = read_paper(paper_path)
            logger.info(f"✅ 成功读取论文文件: {final_path_obj.name}")
        except Exception as e:
            logger.error(f"❌ 读取论文文件失败: {str(e)}")
            sys.exit(1)
    
    if not paper_content.strip():
        logger.error("论文内容为空")
        sys.exit(1)
    
    # 创建工作流并运行
    logger.info("初始化工作流...")
    workflow = Paper2ReaderWorkflow()
    
    try:
        logger.info("开始处理论文...")
        result = workflow.run_with_retry(paper_content)
        
        if not result.get('success', False):
            logger.error(f"处理失败: {result.get('error', '未知错误')}")
            sys.exit(1)
        
        # 获取生成的笔记内容
        note_content = result.get('note_content', '')
        
        if not note_content:
            logger.warning("生成的笔记内容为空")
            # 尝试使用原始输出
            note_content = result.get('output_result', {}).get('raw_response', '')
        
        # 保存笔记
        try:
            # 尝试从解析数据中获取论文标题
            parsed_data = result.get('parsed_data', {})
            paper_title = parsed_data.get('title') if isinstance(parsed_data, dict) else None
            
            output_path = save_note(note_content, args.output, paper_title)
            logger.info(f"✅ 处理完成！笔记已保存到: {output_path}")
            
            # 显示质量检查结果
            quality_check = result.get('quality_check', {})
            if isinstance(quality_check, dict):
                completeness = quality_check.get('completeness_score', 0)
                accuracy = quality_check.get('accuracy_score', 0)
                clarity = quality_check.get('clarity_score', 0)
                
                if completeness or accuracy or clarity:
                    logger.info(f"质量评分 - 完整性: {completeness:.2f}, 准确性: {accuracy:.2f}, 清晰度: {clarity:.2f}")
            
        except Exception as e:
            logger.error(f"保存笔记失败: {str(e)}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"处理过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
