from loguru import logger
from p2r_agents import (
    MentorAgent,
    ParserAgent,
    ComposeAgent,
)
import asyncio



async def main():
    mentor_test = MentorAgent().call_response("你好, 一句话介绍一下快手")
    logger.success(mentor_test)
    parser_test = ParserAgent().call_response("你好, 一句话介绍一下快手")
    logger.success(parser_test)
    compose_test = ComposeAgent().call_response("你好, 一句话介绍一下快手")
    logger.success(compose_test)

if __name__ == "__main__":
    asyncio.run(main())