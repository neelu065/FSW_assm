

def check_threshold(value, rule):

    if not isinstance(rule, dict):
        raise TypeError("Threshold rule must be a dictionary")
    
    """Descending order of their severity"""
    if "critical" in rule and value > rule["critical"]:
        return "CRITICAL", rule["critical_action"]

    if "error" in rule and value > rule["error"]:
        return "ERROR", rule["error_action"]

    if "warning" in rule and value > rule["warning"]:
        return "WARNING", rule["warning_action"]

    return "INFO", "No action required."
