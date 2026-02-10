"""
API 与模型配置（SiliconFlow）
建议通过环境变量 SILICONFLOW_API_KEY 设置密钥，避免提交到仓库。
"""
from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
)
from openai import (
    OpenAI,
    AsyncOpenAI,
)

import os

BASE_URL = os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
API_KEY = os.environ.get("SILICONFLOW_API_KEY", "sk-nhnklopejonbklumkchlnsjaluxbetocvqdzevgcrjptjlpj")

# 文本模型（解析 / 语义 / 质量）
TEXT_MODEL = "deepseek-ai/DeepSeek-V3.2"
# TEXT_MODEL = "Qwen/Qwen3-VL-32B-Thinking"

base_client = AsyncOpenAI(
    base_url = BASE_URL,
    api_key = API_KEY
)
base_model = OpenAIChatCompletionsModel(
    model=TEXT_MODEL,
    openai_client = base_client,
)

def base_dpsk_nothink_setting(
    max_tokens: int = 65536,
    temperature: float = 1.0,
    top_p: float = 0.95,
    top_k: int = 20,
):
    return ModelSettings(
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        extra_body={
            "top_k": top_k,
            "chat_template_kwargs": {"thinking": False},
        }
    )

def base_dpsk_think_setting(
    max_tokens: int = 65536,
):
    return ModelSettings(
        max_tokens=max_tokens,
        extra_body={
            "chat_template_kwargs": {"thinking": True},
        }
    )

def base_dpsk_settings(
    max_tokens: int = 65536,
    temperature: float = 1.0,
    top_p: float = 0.95,
    top_k: int = 20,
    thinking: bool = False,
):
    return {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "extra_body": {
            "top_k": top_k,
            "chat_template_kwargs": {"thinking": thinking},
        }
    }