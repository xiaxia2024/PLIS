import os
from fastapi import UploadFile
from pathlib import Path

INPUT_DIR = "data/inputs"

def save_log(machine_name: str, os_type: str, file: UploadFile):
    os.makedirs(INPUT_DIR, exist_ok=True)
    safe_machine = machine_name.replace(" ","_")
    safe_os = os_type.replace(" ","_")
    file_path = f"{INPUT_DIR}/{safe_machine}_{safe_os}.log"

    content = file.file.read() #读取内容

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path
    
def list_inputs():
    os.makedirs(INPUT_DIR, exist_ok=True)
    return sorted([p.name for p in Path(INPUT_DIR).iterdir() if p.is_file()])

def read_input(filename: str) -> str:
    path = Path(INPUT_DIR) / filename
    if not path.exists():
        raise FileNotFoundError(str(path))
    return path.read_text(encoding="utf-8", errors="ignore")

def parse_filename(filename: str):
    # filename expected: Machine_OS.txt or Machine_OS.log etc.
    base = Path(filename).stem
    parts = base.split("_")
    if len(parts) >= 2:
        machine = "_".join(parts[:-1])
        os_type = parts[-1]
    else:
        machine = base
        os_type = "unknown"
    return machine, os_type
