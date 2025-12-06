def classify_vulns(parsed):
    raw = parsed["raw"]

    classes = []
    if "sudo" in raw:
        classes.append("Privilege Escalation")
    if "nmap" in raw:
        classes.append("Service Enumeration")
    if "exploit" in raw:
        classes.append("Exploitation")

    if not classes:
        classes.append("General Attack / Recon")

    return classes
