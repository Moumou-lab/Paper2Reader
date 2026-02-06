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
    instructions=(
        "你是一个通用型的AI助手，类似团队中的万能人，可以帮助解决各种问题、处理多样化任务。"
        "你擅长分析、建议、执行，能够根据需要调用工具或自主完成任务。"
        "请用专业、简明的方式满足用户的多种需求。"
    ),
    model=base_dpsk_model,
    model_settings=base_dpsk_nothink_setting(),
    output_type=str,
    tool=[],
)