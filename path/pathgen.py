from models.qwen import call_qwen

def generate_attack_path(parsed):
    prompt = f"""
根据以下日志和检测到的关键字，生成渗透测试攻击路径摘要，按照步骤编号输出：
日志内容:
{parsed['raw'][:2000]}
关键字: {', '.join(parsed['detected_keywords'])}
"""
    return call_qwen(prompt)

