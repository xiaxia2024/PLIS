# path/pathgen.py
from models.qwen import call_qwen

def generate_attack_path(parsed: dict):
    prompt = f"""
你是渗透测试报告助手。根据下面的日志片段，生成一个按步骤编号的攻击路径（步骤语言简洁，每步包含证据/来源行）。
只输出 Markdown 列表（例如：1. step ... 证据: ...）。
日志片段:
{parsed['raw'][:2500]}
"""
    resp = call_qwen(prompt, max_tokens=1000)
    # 如果 qwen 返回空或错误，fallback to simple summary
    if resp.startswith("[QWEN call failed") or len(resp.strip()) < 10:
        # fallback: synthesize from detected keywords and ports
        parts = []
        if parsed.get("ports"):
            parts.append("1. 扫描端口，发现: " + ", ".join(parsed["ports"][:5]))
        if parsed.get("detected_keywords"):
            parts.append("2. 关键动作/命令: " + ", ".join(parsed["detected_keywords"][:8]))
        return "\n".join(parts)
    return resp
