"""
基础 Agent 类，所有 Agent 的基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from openai import OpenAI
from .config import BASE_URL, API_KEY


class BaseAgent(ABC):
    """所有 Agent 的基础类"""
    
    def __init__(self, model: str = 'deepseek-ai/DeepSeek-V3.2'):
        """
        初始化 Agent
        
        Args:
            model: 使用的模型名称
        """
        self.client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
        )
        self.model = model
        self.extra_body = {
            "enable_thinking": False,
        }
    
    def _call_llm(self, messages: list, stream: bool = False) -> Dict[str, Any]:
        """
        调用 LLM API
        
        Args:
            messages: 消息列表
            stream: 是否流式输出
            
        Returns:
            API 响应
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            extra_body=self.extra_body
        )
        
        return {
            'content': response.choices[0].message.content,
            'reasoning': getattr(response.choices[0].message, 'reasoning_content', None)
        }
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理后的数据字典
        """
        pass
