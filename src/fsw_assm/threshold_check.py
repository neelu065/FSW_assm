

def check_threshold(value, rule):

    """Descending order of their severity"""
    if "critical" in rule and value > rule["critical"]:
        return "CRITICAL", rule["critical_action"]

    elif "error" in rule and value > rule["error"]:
        return "ERROR", rule["error_action"]

    elif "warning" in rule and value > rule["warning"]:
        return "WARNING", rule["warning_action"]

    else:
        return "INFO", "No action required."
