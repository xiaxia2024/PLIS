# parse/parser.py
import re
from pathlib import Path

SECTION_HDR_RE = re.compile(r"^=+\s*(.+?)\s*=+$")

def parse_logs(file_path: str):
    """
    Parse a combined log file (one file per machine).
    Returns a dict containing:
      - raw: full text
      - sections: {section_name: text}
      - ports: list of nmap-like 'port/service' lines
      - detected_keywords: list of keywords
    """
    p = Path(file_path)
    text = p.read_text(encoding="utf-8", errors="ignore")

    # split into sections by lines like "===== NMAP ====="
    sections = {}
    current = "general"
    buf = []
    for line in text.splitlines():
        m = SECTION_HDR_RE.match(line.strip())
        if m:
            # save previous
            if buf:
                sections[current] = "\n".join(buf).strip()
                buf = []
            current = m.group(1).strip().lower()
            continue
        buf.append(line)
    if buf:
        sections[current] = "\n".join(buf).strip()

    # extract ports: look for lines like "22/tcp open ssh" or "80/tcp open http"
    ports = []
    for sec_text in sections.values():
        for line in sec_text.splitlines():
            if "/tcp" in line or "/udp" in line:
                if "open" in line or "filtered" in line or "closed" in line:
                    ports.append(line.strip())

    # detect common keywords
    keylist = ["nmap", "ssh", "sudo", "su", "nc", "netcat", "exploit", "root", "linpeas", "gobuster", "dirb", "pspy", "suid", "cron", "docker", "kubelet", "rdp", "smb", "winrm"]
    detected = []
    lower = text.lower()
    for k in keylist:
        if k in lower:
            detected.append(k)

    # try to find evidence of credentials (very basic)
    creds = []
    for line in text.splitlines():
        if ":" in line and ("password" in line.lower() or "pass" in line.lower()):
            creds.append(line.strip())

    return {
        "raw": text,
        "sections": sections,
        "ports": ports,
        "detected_keywords": detected,
        "candidate_credentials": creds
    }
