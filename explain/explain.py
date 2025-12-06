from models.qwen import call_qwen

def explain_vulns(classes):
    prompt = f"""
我有以下漏洞分类，请生成每个漏洞的原理解读、危害和修复建议：
漏洞列表: {classes}
"""
    explanation_text = call_qwen(prompt)
    # 分割成列表，每行一个漏洞解释
    return explanation_text.splitlines()
