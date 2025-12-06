from models.qwen import call_qwen

def classify_vulns(parsed):
    # 构造 prompt 让 Qwen 帮你分类
    prompt = f"""
我有一个渗透测试日志，请帮我自动分析并分类漏洞类型，输出 JSON 格式：
日志内容:
{parsed['raw'][:2000]}
返回格式：
{{"vulnerabilities": ["Privilege Escalation", "RCE", "LFI", "Misconfiguration", ...]}}
"""
    result = call_qwen(prompt)
    try:
        import json
        return json.loads(result)["vulnerabilities"]
    except:
        # fallback
        return ["General"]

