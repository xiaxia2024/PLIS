import os
from fastapi import UploadFile

def save_log(job_id: str, file: UploadFile):
    os.makedirs("data/inputs", exist_ok=True)
    file_path = f"data/inputs/{job_id}.log"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path
