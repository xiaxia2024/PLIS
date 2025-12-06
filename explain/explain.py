def explain_vulns(classes):
    explanation_map = {
        "Privilege Escalation": "User gained root privileges via misconfig.",
        "Service Enumeration": "Mapped open ports and services.",
        "Exploitation": "Executed a remote code execution vector."
    }

    return [explanation_map.get(c, "General analysis step.") for c in classes]
