# explain/explain.py
from models.qwen import call_qwen

def explain_vulns(vuln_list):
    if not vuln_list:
        return ["No vulnerabilities detected."]
    prompt = f"""
请为以下漏洞类型生成简短解释、危害说明与修复建议。返回为纯文本，每条用一行表示，格式：
漏洞类型: 解释；危害；修复建议

漏洞类型列表:
{vuln_list}
"""
    resp = call_qwen(prompt, max_tokens=800)
    # Split into lines, filter empties
    lines = [l.strip() for l in resp.splitlines() if l.strip()]
    if not lines:
        return [f"{v}: (no explanation returned)" for v in vuln_list]
    return lines
