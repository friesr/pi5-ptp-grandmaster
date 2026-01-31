from backend.alerts.rules import ALERT_RULES

def evaluate_alerts(status_snapshot):
    """
    status_snapshot: combined dict with ptp, ntp, gnss, storage, etc.
    Returns list of active alerts.
    """
    active = []

    for rule in ALERT_RULES:
        try:
            if rule["condition"](status_snapshot):
                active.append({
                    "id": rule["id"],
                    "severity": rule["severity"],
                    "message": rule["message"]
                })
        except Exception:
            # If a field is missing, just skip that rule
            continue

    return active
