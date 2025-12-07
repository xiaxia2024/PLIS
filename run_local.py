# run_local.py
from ingest.ingest import list_inputs, read_input, parse_filename
from parse.parser import parse_logs
from classify.classify import classify_vulns
from path.pathgen import generate_attack_path
from explain.explain import explain_vulns
from writeup.writeup import generate_writeup
import os

def process_file(filename):
    print("Processing:", filename)
    machine, os_type = parse_filename(filename)
    parsed = parse_logs(os.path.join("data/inputs", filename))
    classes = classify_vulns(parsed)
    path = generate_attack_path(parsed)
    explanations = explain_vulns(classes)
    out = generate_writeup(machine, os_type, parsed, classes, path, explanations)
    print("-> wrote", out)

if __name__ == "__main__":
    files = list_inputs()
    for f in files:
        try:
            process_file(f)
        except Exception as e:
            print("ERROR processing", f, e)
