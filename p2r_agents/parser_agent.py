# 标准导入
import json
from openai import (
    OpenAI,
    AsyncOpenAI,
    )
from pydantic import BaseModel
from typing import Any
from loguru import logger

# 自定义导入
from .config import (
    TEXT_MODEL,
    base_client,
    base_dpsk_settings,
)
from .prompts.parser_prompt import parser_system_prompt
from .tools.tool_schema import TOOL_SCHEMA
from .tools.parser_tool import (
    tool_recall_sections, # 召回 Tool
    tool_update_sections, # 更新 Tool
)

class ParserAgent:
    def __init__(
        self,
        model=TEXT_MODEL,
        client=base_client,
        _base_settings=base_dpsk_settings(thinking=False),
        _tools=TOOL_SCHEMA,
        current_pdf_path: str | None = None,
    ):
        self.model = model
        self.client = client
        self._base_settings = _base_settings
        self._tools = _tools
        self.current_pdf_path = current_pdf_path

    def call_response(self, input: str | list[dict]) -> Any:
        """
        调用 OpenAI 聊天补全接口，自动处理工具调用循环。
        Args:
            input (str | list[dict])
            pdf_path (str | None): 当前论文路径（可选，优先级高于实例默认值）
        Returns:
            Any: OpenAI 返回的最终消息对象（文本回复）
        """
        if isinstance(input, str):
            messages = [
                {"role": "system", "content": parser_system_prompt()},
                {"role": "user", "content": input},
            ]
        elif isinstance(input, list):
            messages = input
        else:
            raise TypeError(f"Invalid input type: {type(input)}")

        max_iterations = 6
        for iteration in range(max_iterations):
            logger.debug(f"ParserAgent 第 {iteration + 1} 轮对话")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._tools,
                **self._base_settings,
            )
            message = response.choices[0].message

            if not message.tool_calls:
                return message

            messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in message.tool_calls
                    ],
                }
            )

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments or "{}")

                # 运行时上下文注入：模型不感知 pdf_path，由宿主代码补齐
                if function_name in {"tool_recall_sections", "tool_update_sections"}:
                    arguments["pdf_path"] = self.current_pdf_path

                tool_func = globals().get(function_name)
                if not callable(tool_func):
                    tool_call_result = {"success": False, "error": f"Unknown tool: {function_name}"}
                else:
                    tool_call_result = tool_func(**arguments)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_call_result, ensure_ascii=False),
                    }
                )

        return message

