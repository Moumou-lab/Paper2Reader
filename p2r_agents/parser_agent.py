# 标准导入
from openai import (
    OpenAI,
    AsyncOpenAI,
    )
from pydantic import BaseModel
from typing import Any

# 自定义导入
from .config import (
    TEXT_MODEL,
    base_client,
    base_dpsk_settings,
)
from .prompts.parser_prompt import parser_system_prompt


class ParserAgent:
    def __init__(
        self,
        model=TEXT_MODEL,
        client=base_client,
        _base_settings=base_dpsk_settings(thinking=False),
    ):
        self.model = model
        self.client = client
        self._base_settings = _base_settings

    def call_response(self, input: str|list[dict]) -> Any:
        """
        调用 OpenAI 聊天补全接口并返回单条消息对象。
        Args:
            input (str | list[dict])
        Returns:
            Any: OpenAI 返回的单条消息对象
        """
        if isinstance(input, str):
           messages=[
                {"role": "system", "content": parser_system_prompt()},
                {"role": "user", "content": input},
            ]
        elif isinstance(input, list):
            messages = input
        else:
            raise TypeError(f"Invalid input type: {type(input)}")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **self._base_settings,  # 展开统一设置
        )
        return response.choices[0].message

