"""
Semantic Agent - 负责进行语义分析和理解
"""
import json
from typing import Dict, Any
from .base_agent import BaseAgent
from .prompts.semantic_prompt import SEMANTIC_PROMPT_TEMPLATE


class SemanticAgent(BaseAgent):
    """语义分析 Agent"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        进行语义分析
        
        Args:
            input_data: 包含 'parsed_data' 的字典
            
        Returns:
            包含语义分析结果的字典
        """
        parsed_data = input_data.get('parsed_data', {})
        
        if not parsed_data:
            raise ValueError("解析数据不能为空")
        
        # 将 parsed_data 转换为字符串格式
        parsed_data_str = json.dumps(parsed_data, ensure_ascii=False, indent=2)
        
        # 构建提示词
        prompt = SEMANTIC_PROMPT_TEMPLATE.format(parsed_data=parsed_data_str)
        
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
            
            semantic_data = json.loads(content)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始内容
            semantic_data = {
                'raw_response': content,
                'error': 'Failed to parse JSON response'
            }
        
        return {
            'semantic_analysis': semantic_data,
            'raw_response': response['content'],
            'reasoning': response.get('reasoning')
        }