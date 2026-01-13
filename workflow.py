"""
多 Agent 工作流协调器
"""
from typing import Dict, Any, Optional
from agents.parser_agent import ParserAgent
from agents.semantic_agent import SemanticAgent
from agents.quality_agent import QualityAgent
from agents.output_agent import OutputAgent
from loguru import logger


class Paper2ReaderWorkflow:
    """论文阅读工作流"""
    
    def __init__(self):
        """初始化工作流和各个 Agent"""
        self.parser_agent = ParserAgent()
        self.semantic_agent = SemanticAgent()
        self.quality_agent = QualityAgent()
        self.output_agent = OutputAgent()
    
    def run(self, paper_content: str) -> Dict[str, Any]:
        """
        运行完整的工作流
        
        Args:
            paper_content: 论文内容（文本）
            
        Returns:
            包含所有处理结果的字典
        """
        logger.info("开始处理论文...")
        
        # 阶段 1: 解析论文
        logger.info("阶段 1: 解析论文结构和提取关键信息...")
        parser_result = self.parser_agent.process({'paper_content': paper_content})
        parsed_data = parser_result.get('parsed_data', {})
        
        if not parsed_data or 'error' in parsed_data:
            logger.error("论文解析失败")
            return {
                'success': False,
                'error': '论文解析失败',
                'parser_result': parser_result
            }
        
        logger.info("论文解析完成")
        
        # 阶段 2: 语义分析
        logger.info("阶段 2: 进行语义分析和理解...")
        semantic_result = self.semantic_agent.process({'parsed_data': parsed_data})
        semantic_analysis = semantic_result.get('semantic_analysis', {})
        
        if not semantic_analysis or 'error' in semantic_analysis:
            logger.warning("语义分析可能存在问题，继续执行...")
        
        logger.info("语义分析完成")
        
        # 阶段 3: 质量检查
        logger.info("阶段 3: 进行质量检查...")
        quality_result = self.quality_agent.process({
            'parsed_data': parsed_data,
            'semantic_analysis': semantic_analysis
        })
        quality_check = quality_result.get('quality_check', {})
        
        logger.info("质量检查完成")
        
        # 阶段 4: 生成笔记
        logger.info("阶段 4: 生成最终笔记文档...")
        output_result = self.output_agent.process({
            'parsed_data': parsed_data,
            'semantic_analysis': semantic_analysis,
            'quality_check': quality_check
        })
        note_content = output_result.get('note_content', '')
        
        logger.info("笔记生成完成")
        
        return {
            'success': True,
            'parsed_data': parsed_data,
            'semantic_analysis': semantic_analysis,
            'quality_check': quality_check,
            'note_content': note_content,
            'parser_result': parser_result,
            'semantic_result': semantic_result,
            'quality_result': quality_result,
            'output_result': output_result
        }
    
    def run_with_retry(self, paper_content: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        运行工作流，支持重试
        
        Args:
            paper_content: 论文内容
            max_retries: 最大重试次数
            
        Returns:
            处理结果
        """
        for attempt in range(max_retries + 1):
            try:
                result = self.run(paper_content)
                if result.get('success', False):
                    return result
                elif attempt < max_retries:
                    logger.warning(f"处理失败，尝试重试 ({attempt + 1}/{max_retries})...")
            except Exception as e:
                logger.error(f"处理过程中出现错误: {str(e)}")
                if attempt < max_retries:
                    logger.warning(f"尝试重试 ({attempt + 1}/{max_retries})...")
                else:
                    return {
                        'success': False,
                        'error': str(e)
                    }
        
        return {
            'success': False,
            'error': '处理失败，已达到最大重试次数'
        }
