# classify/classify.py
from models.qwen import call_qwen
import json

FALLBACK_RULES = [
    ("Privilege Escalation", ["sudo", "suid", "cron", "capabilities", "linpeas"]),
    ("Service Enumeration", ["nmap", "port", "smb", "rdp"]),
    ("RCE / Exploitation", ["exploit", "command injection", "rce", "remote code"]),
    ("LFI/RFI", ["lfi", "local file inclusion", "file inclusion"]),
    ("Misconfiguration", ["misconfig", "world writable", "writable", "docker", "kubelet"])
]

def classify_vulns(parsed: dict):
    prompt = f"""
请把下面的渗透测试日志内容进行漏洞分类，并仅返回 JSON：
{{"vulnerabilities": ["..."]}}

日志内容:
{parsed['raw'][:3000]}
"""
    resp = call_qwen(prompt, max_tokens=800)
    # 尝试解析 JSON
    try:
        j = json.loads(resp)
        if "vulnerabilities" in j and isinstance(j["vulnerabilities"], list):
            return j["vulnerabilities"]
    except Exception:
        pass

    # fallback heuristic
    raw = parsed.get("raw", "").lower()
    found = set()
    for label, keys in FALLBACK_RULES:
        for k in keys:
            if k in raw:
                found.add(label)
                break
    if not found:
        return ["General / Recon"]
    return sorted(list(found))
