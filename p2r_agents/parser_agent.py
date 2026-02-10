# 标准导入
from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
)
from pydantic import BaseModel
# 自定义导入
from .config import (
    base_model,
    base_dpsk_nothink_setting,
    base_dpsk_think_setting,
)
from .prompts.parser_prompt import parser_prompt

ParserAgent = Agent(
    name="论文解析专家",
    instructions=parser_prompt(), # 仅做任务定义, 目标 Section 内容, 需要在 User Message 中传入
    model=base_model,
    model_settings=base_dpsk_nothink_setting(),
    output_type=str,
)