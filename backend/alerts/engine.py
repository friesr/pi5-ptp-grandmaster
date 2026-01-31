from backend.config.manager import load_config

def evaluate_alerts(status_snapshot):
    cfg = load_config()
    rules = cfg.get("alert_rules", {})

    active = []

    for rule_id, rule in rules.items():
        if not rule.get("enabled", True):
            continue

        try:
            if rule_id == "ptp_offset_high":
                if abs(status_snapshot["ptp"]["offset_ns"]) > rule["threshold_ns"]:
                    active.append({
                        "id": rule_id,
                        "severity": rule["severity"],
                        "message": rule["message"]
                    })

            elif rule_id == "ntp_offset_high":
                if abs(status_snapshot["ntp"]["offset_ms"]) > rule["threshold_ms"]:
                    active.append({
                        "id": rule_id,
                        "severity": rule["severity"],
                        "message": rule["message"]
                    })

            elif rule_id == "gnss_used_low":
                if status_snapshot["gnss"]["used"] < rule["threshold"]:
                    active.append({
                        "id": rule_id,
                        "severity": rule["severity"],
                        "message": rule["message"]
                    })

            elif rule_id == "storage_local_high":
                if status_snapshot["storage"]["local"]["percent"] > rule["threshold_percent"]:
                    active.append({
                        "id": rule_id,
                        "severity": rule["severity"],
                        "message": rule["message"]
                    })

            elif rule_id == "nas_unavailable":
                if not status_snapshot["storage"]["nas_health"]["mounted"]:
                    active.append({
                        "id": rule_id,
                        "severity": rule["severity"],
                        "message": rule["message"]
                    })

        except Exception:
            continue

    return active
