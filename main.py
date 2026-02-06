# 标准模块导入
import asyncio
from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
)
from loguru import logger

# 自定义模块导入
from p2r_agents.parser_agent import ParserAgent
from workflow import main_workflow


async def main():
    logger.info("开始执行 main 函数")   
    result = await main_workflow("papers/attention.pdf")


if __name__ == "__main__":
    asyncio.run((main()))