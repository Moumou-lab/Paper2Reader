"""
Quality Agent - 负责质量检查和优化
"""
import json
from typing import Dict, Any
from .base_agent import BaseAgent
from .prompts.quality_prompt import QUALITY_PROMPT_TEMPLATE


class QualityAgent(BaseAgent):
    """质量检查 Agent"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        进行质量检查
        
        Args:
            input_data: 包含 'parsed_data' 和 'semantic_analysis' 的字典
            
        Returns:
            包含质量检查结果的字典
        """
        parsed_data = input_data.get('parsed_data', {})
        semantic_analysis = input_data.get('semantic_analysis', {})
        
        if not parsed_data or not semantic_analysis:
            raise ValueError("解析数据和语义分析结果不能为空")
        
        # 转换为字符串格式
        parsed_data_str = json.dumps(parsed_data, ensure_ascii=False, indent=2)
        semantic_analysis_str = json.dumps(semantic_analysis, ensure_ascii=False, indent=2)
        
        # 构建提示词
        prompt = QUALITY_PROMPT_TEMPLATE.format(
            parsed_data=parsed_data_str,
            semantic_analysis=semantic_analysis_str
        )
        
        # 调用 LLM
        messages = [
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        response = self._call_llm(messages)
        
        # 尝试解析 JSON 响应
        content = response['content']
        try:
            # 尝试提取 JSON 部分
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                content = content[json_start:json_end].strip()
            elif '```' in content:
                json_start = content.find('```') + 3
                json_end = content.find('```', json_start)
                content = content[json_start:json_end].strip()
            
            quality_data = json.loads(content)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始内容
            quality_data = {
                'raw_response': content,
                'error': 'Failed to parse JSON response',
                'needs_revision': True
            }
        
        return {
            'quality_check': quality_data,
            'raw_response': response['content'],
            'reasoning': response.get('reasoning')
        }