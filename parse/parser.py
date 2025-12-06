def parse_logs(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()

    # 解析端口和服务
    ports = []
    for line in content.splitlines():
        if "open" in line and "/" in line:
            ports.append(line.strip())

    # 解析关键字
    keywords = [k for k in ["nmap", "ssh", "sudo", "nc", "exploit", "root", "linpeas"] if k in content]

    return {
        "raw": content,
        "ports": ports,
        "detected_keywords": keywords
    }
