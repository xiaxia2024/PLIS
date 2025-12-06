import os

def generate_writeup(job_id, parsed, classes, path, explanations):
    output_dir = "data/outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{job_id}.md"

    content = f"""
# PLIS Auto Write-up  
**Job ID:** {job_id}

---

## 📝 1. Parsed Log Summary
