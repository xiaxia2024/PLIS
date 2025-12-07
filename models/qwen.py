import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PLIS_QWEN_API_KEY")
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
DEFAULT_MODEL = os.getenv("QWEN_MODEL", "Qwen-7B")

HEADERS = {
    "Content-type" : "application/json",
    "Authorization": f"Bearer {APT_KEY}" if API_KEY else ""
}

def call_qwen(prompt: str, model: str = None, max_tokens: int = 1500, timeout: int =60) -> str:
    """
    Call Qwen (Bailian) chat completions endpoint and return content text.
    If API fails or key missing, return fallback message.
    """
    if not API_KEY:
        return "[QWEN_API_KEY not set] " + prompt[:300]

    use_model = model or DEfAULT_MODEL
    payload = {
        "model": use_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0
    }

    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Support common response shape: choices[0].message.content
        if isinstance(data, dict):
            choices = data.get("choices") or data.get("result") or []
            if choices and isinstance(choices, list):
                first = choices[0]
                # try nested structures
                if isinstance(first, dict):
                    m = first.get("message") or first.get("delta") or first
                    if isinstance(m, dict):
                        content = m.get("content") or m.get("text") or ""
                        if isinstance(content, dict):
                            # sometimes content may be {"type":"text","parts":[...]}
                            parts = content.get("parts") or content.get("text")
                            if isinstance(parts, list):
                                return "".join(parts)
                            return str(parts)
                        return str(content)
                    return str(m)
                return str(first)
        return json.dumps(data)
    except Exception as e:
        return f"[QWEN call failed: {e}] {prompt[:300]}"

