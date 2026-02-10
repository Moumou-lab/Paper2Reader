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
    PDF_PATH = "papers/DSSM.pdf"
    await main_workflow(PDF_PATH)

if __name__ == "__main__":
    asyncio.run(main())