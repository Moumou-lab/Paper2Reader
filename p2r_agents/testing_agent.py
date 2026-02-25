# 标准导入
import json
from typing import Any
from loguru import logger
# 自定义导入
from .config import (
    TEXT_MODEL,
    base_client,
    base_dpsk_settings,
)
from .tools.tool_schema import TOOL_SCHEMA
from .tools.parser_tool import tool_recall_sections, tool_update_sections

class TestingAgent:
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
    def call_response(self, input: str|list[dict]) -> Any:
        """
        调用 OpenAI 聊天补全接口，自动处理工具调用循环。
        Args:
            input (str | list[dict])
        Returns:
            Any: OpenAI 返回的最终消息对象（文本回复）
        """
        if isinstance(input, str):
           messages=[
                {"role": "system", "content": "你是一个有用的AI, 可以完成用户的各种需求, 你有工具可以调用."},
                {"role": "user", "content": input},
            ]
        elif isinstance(input, list):
            messages = input
        else:
            raise TypeError(f"Invalid input type: {type(input)}")

        # 工具调用循环
        max_iterations = 5  # 防止无限循环
        for iteration in range(max_iterations):
            logger.debug(f"第 {iteration + 1} 轮对话")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._tools,
                **self._base_settings,
            )
            message = response.choices[0].message
            
            # 如果没有工具调用，直接返回最终结果
            if not message.tool_calls:
                logger.debug(f"完整对话历史: {json.dumps(messages, ensure_ascii=False, indent=2)}")
                logger.debug(f"最终回复全部信息:\n {message}")
                return message
            
            # 把模型的工具调用消息加入对话历史
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in message.tool_calls
                ]
            })
            # 执行每个工具调用
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # 运行时上下文注入：模型不感知 pdf_path，由宿主代码补齐
                if function_name in {"tool_recall_sections", "tool_update_sections"}:
                    arguments["pdf_path"] = self.current_pdf_path

                # 直接用函数名字符串调用全局作用域中该工具函数
                tool_func = globals().get(function_name)
                tool_call_result = tool_func(**arguments)

                # 把工具返回结果加入对话历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_call_result, ensure_ascii=False),
                })
            logger.info(f"对话历史:\n {message}")
        # 达到最大迭代次数，返回最后一条消息
        return message

# python -m p2r_agents.testing_agent
if __name__ == "__main__":
    PDF_PATH = "/Users/zhengjiaqi/Projects/Paper2Reader/papers/testing.pdf"
    testing_agent = TestingAgent(current_pdf_path=PDF_PATH)
    result = testing_agent.call_response(f"""
    请帮我召回 Introduction 和 Related Work 章节的parser数据, 把每一个字段的内容翻译为对应语言(中文->英文, 英文->中文).
    注意事项:
    1. 不要改变原有内容, 只翻译.
    2. 标题不要翻译
    3. 以 list 的格式返回, 每一个元素是一个顶层 section 的 parser数据.
    4. 不要有**多余解释或代码块**.
""")
    print("\n=== 最终回复 ===")
    print(result.content if result.content else result) 