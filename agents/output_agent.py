"""
Output Agent - 负责生成最终的笔记文档
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from .prompts.output_prompt import OUTPUT_PROMPT_TEMPLATE
import json


class OutputAgent(BaseAgent):
    """输出生成 Agent"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成最终的笔记文档
        
        Args:
            input_data: 包含 'parsed_data', 'semantic_analysis', 'quality_check' 的字典
            
        Returns:
            包含生成的笔记文档的字典
        """
        parsed_data = input_data.get('parsed_data', {})
        semantic_analysis = input_data.get('semantic_analysis', {})
        quality_check = input_data.get('quality_check', {})
        
        # 转换为字符串格式
        parsed_data_str = json.dumps(parsed_data, ensure_ascii=False, indent=2)
        semantic_analysis_str = json.dumps(semantic_analysis, ensure_ascii=False, indent=2)
        quality_check_str = json.dumps(quality_check, ensure_ascii=False, indent=2)
        
        # 构建提示词
        prompt = OUTPUT_PROMPT_TEMPLATE.format(
            parsed_data=parsed_data_str,
            semantic_analysis=semantic_analysis_str,
            quality_check=quality_check_str
        )
        
        # 调用 LLM
        messages = [
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        response = self._call_llm(messages)
        
        # 提取 Markdown 内容
        content = response['content']
        if '```markdown' in content:
            md_start = content.find('```markdown') + 11
            md_end = content.find('```', md_start)
            content = content[md_start:md_end].strip()
        elif '```' in content:
            md_start = content.find('```') + 3
            md_end = content.find('```', md_start)
            if md_end > 0:
                content = content[md_start:md_end].strip()
        
        return {
            'note_content': content,
            'raw_response': response['content'],
            'reasoning': response.get('reasoning')
        }
