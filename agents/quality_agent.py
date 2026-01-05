# semantic_agent.py
from config import *
from openai import OpenAI

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY, 
)
extra_body = {
    "enable_thinking": False,
}

response = client.chat.completions.create(
    model='deepseek-ai/DeepSeek-V3.2', # ModelScope Model-Id, required
    messages=[
        {
          'role': 'user',
          'content': '9.9和9.11谁大'
        }
    ],
    stream=False,
    extra_body=extra_body
)

print(response.choices[0].message.reasoning_content)
print('\n\n === Final Answer ===\n')
print(response.choices[0].message.content)