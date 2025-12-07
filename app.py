# app.py
import glob
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

from ingest.ingest import save_log, list_inputs, read_input, parse_filename
from parse.parser import parse_logs
from classify.classify import classify_vulns
from path.pathgen import generate_attack_path
from explain.explain import explain_vulns
from writeup.writeup import generate_writeup
import os

app = FastAPI(title="PLIS - Minimal Edition")

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

    machine_name, os_type = parse_filename(input_filename)

    # parse
    parsed = parse_logs(os.path.join("data/inputs", input_filename))

    # classify
    classes = classify_vulns(parsed)

    # path
    path = generate_attack_path(parsed)

    # explain
    explanations = explain_vulns(classes)

    # writeup
    output_path = generate_writeup(machine_name, os_type, parsed, classes, path, explanations)

    return {"status": "done", "output": output_path}
