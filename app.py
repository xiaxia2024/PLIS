# app.py
import glob
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from ingest.ingest import save_log, list_inputs, read_input, parse_filename
from parse.parser import detect_os parse_logs
from classify.classify import classify_vulns
from path.pathgen import generate_attack_path
from explain.explain import explain_vulns
from writeup.writeup import generate_writeup
import os

app = FastAPI(title="PLIS - Penetration Learning Intelligence System")

@app.get("/inputs")
def get_inputs():
    files = list_inputs()
    return {"inputs": files}

@app.get("/analyze/{input_filename}")
def analyze(input_filename: str):
    # ensure exists
    try:
        raw = read_input(input_filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Input file not found in data/inputs")

    machine_name, _ = parse_filename(input_filename)

    # parse
    parsed = parse_logs(os.path.join("data/inputs", input_filename))

    # Detect OS (Linux/Windows)
    os_type = parsed.get("os_type", "Unknown")

    # classify
    classes = classify_vulns(parsed)

    # path
    path = generate_attack_path(parsed)

    # explain
    explanations = explain_vulns(classes)

    # writeup
    output_path = generate_writeup(
        machine_name=machine_name,
        os_type=os_type,
        parsed=parsed,
        classes=classes,
        path=attack_path,
        explanations=explanations
    )

    return {
        "machine": machine_name,
        "os_type": os_type,
        "writeup_file": writeup_path
    }

# Download a generated writeup
@app.get("/download/{writeup_filename}")
def download(writeup_filename: str):
    path = os.path.join("data/outputs", writeup_filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Writeup not found")
    return FileResponse(path, media_type="text/markdown", filename=writeup_filename)    
    
