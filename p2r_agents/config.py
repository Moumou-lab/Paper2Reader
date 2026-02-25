"""
API 与模型配置（SiliconFlow）
"""
import os
from openai import (
    OpenAI,
    AsyncOpenAI, # 异步客户端
)

BASE_URL = os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
API_KEY = os.environ.get("SILICONFLOW_API_KEY", "sk-nhnklopejonbklumkchlnsjaluxbetocvqdzevgcrjptjlpj")
TEXT_MODEL = "Pro/deepseek-ai/DeepSeek-V3.2"
# TEXT_MODEL = "Qwen/Qwen3-VL-32B-Thinking"

base_client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

def base_dpsk_settings(
    max_tokens: int = 65536,
    temperature: float = 1.0,
    top_p: float = 0.95,
    top_k: int = 20,
    thinking: bool = False,
):
    think_type = "enabled" if thinking else "disabled"
    return {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "extra_body": {
            "top_k": top_k,
            # "chat_template_kwargs": {"thinking": thinking},
            "thinking": {"type": think_type} 
        }
    }