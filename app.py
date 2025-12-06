# app.py
from fastapi import FastAPI, UploadFile, File
import uuid
import os

from ingest.ingest import save_log
from parse.parser import parse_logs
from classify.classify import classify_vulns
from path.pathgen import generate_attack_path
from explain.explain import explain_vulns
from writeup.writeup import generate_writeup

app = FastAPI(title="PLIS - Penetration Learning Intelligence System")


# ---------- 上传日志 ----------
@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_path = save_log(job_id, file)
    return {"job_id": job_id, "file_path": file_path}


# ---------- 分析接口 ----------
@app.post("/analyze/{job_id}")
async def analyze(job_id: str):
    input_path = f"data/inputs/{job_id}.log"

    if not os.path.exists(input_path):
        return {"error": "Job ID not found or file missing."}

    # 1. 解析日志
    parsed = parse_logs(input_path)

    # 2. 漏洞分类
    classes = classify_vulns(parsed)

    # 3. 生成攻击路径摘要
    path = generate_attack_path(parsed)

    # 4. 解释漏洞原理
    explanations = explain_vulns(classes)

    # 5. 生成 write-up
    output_path = generate_writeup(job_id, parsed, classes, path, explanations)

    return {
        "job_id": job_id,
        "message": "Analysis complete.",
        "output": output_path
    }

