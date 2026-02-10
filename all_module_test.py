from loguru import logger
from p2r_agents import (
    MentorAgent,
    ParserAgent,
)
import asyncio
from agents import Runner

async def main():
    outline_result = await Runner.run(starting_agent=MentorAgent, input="你好, 一句话介绍一下快手")
    logger.success(outline_result)

if __name__ == "__main__":
    asyncio.run(main())