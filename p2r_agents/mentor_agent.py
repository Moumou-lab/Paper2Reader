# 标准导入
from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    tool,
)
from pydantic import BaseModel
# 自定义导入
from .config import (
    base_dpsk_model,
    base_dpsk_nothink_setting,
    base_dpsk_think_setting,
)
# from tools
# from .prompts.parser_prompt import parser_prompt

MentorAgent = Agent(
    name="万能专家",
    instructions="""你是一个通用型的AI助手，能够处理多样化任务。
根据用户的具体要求，完成任务需求。
""",
    model=base_dpsk_model,
    # model_settings=base_dpsk_nothink_setting(),
    model_settings=base_dpsk_think_setting(),
    output_type=str,
    # tool=[],
)