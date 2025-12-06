import os
import textwrap

def generate_writeup(job_id, parsed, classes, path, explanations):
    output_dir = "data/outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{job_id}.md"

    # 自动换行，最多每行80字符
    raw_text = parsed["raw"][:5000]  # 取前5000字符，避免报告太大
    wrapped_text = "\n".join(textwrap.wrap(raw_text, width=80))

    content = f"""
# PLIS Auto Write-up  
**Job ID:** {job_id}

---

## 📝 1. Parsed Log Summary
{parsed["raw"][:500]}

## 🏷 2. Detected Keywords
{parsed["detected_keywords"]}

## 🧩 3. Vulnerability Classification
{classes}

## 🔗 4. Attack Path Summary
{path}

## 📘 5. Vulnerability Explanation
{"; ".join(explanations)}

---
Generated automatically by **PLIS**.
"""
    with open(output_path, "w") as f:
        f.write(content)

    return output_path
