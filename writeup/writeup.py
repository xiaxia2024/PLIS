import os
import textwrap
from models.qwen import call_qwen
from datetime import datetime

def generate_writeup(machine_name: str, os_type: str, parsed: dict, classes, path, explanations):
    output_dir = "data/outputs"
    os.makedirs(output_dir, exist_ok=True)

    safe_machine = machine_name.replace(" ", "_")
    safe_os = os_type.replace(" ", "_")
    output_path = f"{output_dir}/{safe_machine}_{safe_os}.md"

    # 自动换行，最多每行80字符
    raw_text = parsed.get("raw","")[:6000]  # 取前8000字符，避免报告太大
    wrapped_text = "\n".join(textwrap.wrap(raw_text, width=80))
    

    # 使用 Qwen 优化 writeup
    prompt = f"""
根据以下信息，生成一个完整渗透测试 write-up 报告：
日志摘要:
{wrapped_text}

漏洞分类:
{classes}

攻击路径:
{path}

漏洞解释:
{"; ".join(explanations)}

请输出 Markdown 格式。
"""
    qwen_response = call_qwen(prompt)

    if isinstance(qwen_response, dict):
        report_content = qwen_response.get("output_text", "")
    else:
        report_content = qwen_response

    with open(output_path, "w") as f:
        f.write(report_content)

    return output_path
