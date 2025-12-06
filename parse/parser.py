def parse_logs(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()

    # TODO：后续加入真正解析逻辑（nmap, linpeas, bash history）
    return {
        "raw": content,
        "detected_keywords": [
            k for k in ["nmap", "ssh", "sudo", "nc", "exploit", "root"]
            if k in content
        ]
    }
