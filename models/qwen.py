import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PLIS_QWEN_API_KEY")
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

def call_qwen(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "Qwen-7B",   # 可选 Qwen-7B / 14B，根据你账号情况
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post(API_URL, json=data, headers=headers, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    # 百炼返回结果中 content 在 choices[0]['message']['content']
    return result['choices'][0]['message']['content']

