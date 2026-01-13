"""
Parser Agent - 负责解析论文结构和提取关键信息
"""
import json
from typing import Dict, Any
from .base_agent import BaseAgent
from .prompts.parser_prompt import PARSER_PROMPT_TEMPLATE


class ParserAgent(BaseAgent):
    """论文解析 Agent"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析论文内容
        
        Args:
            input_data: 包含 'paper_content' 的字典
            
        Returns:
            包含解析结果的字典
        """
        paper_content = input_data.get('paper_content', '')
        
        if not paper_content:
            raise ValueError("论文内容不能为空")
        
        # 构建提示词
        prompt = PARSER_PROMPT_TEMPLATE.format(paper_content=paper_content)
        
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
            
            parsed_data = json.loads(content)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始内容
            parsed_data = {
                'raw_response': content,
                'error': 'Failed to parse JSON response'
            }
        
        return {
            'parsed_data': parsed_data,
            'raw_response': response['content'],
            'reasoning': response.get('reasoning')
        }