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
from .prompts.mentor_prompt import mentor_system_prompt


class MentorAgent:
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
                {"role": "system", "content": mentor_system_prompt()},
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

# python -m p2r_agents.mentor_agent
if __name__ == "__main__":
    mentor_agent = MentorAgent() # 必须加括号
    response = mentor_agent.call_response("你好，一句话介绍一下华东师范大学")
    print(response)