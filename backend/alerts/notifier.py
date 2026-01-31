import time

_last_sent_ids = set()

def get_new_alerts(previous_ids, alerts):
    current_ids = {a["id"] for a in alerts}
    new_ids = current_ids - previous_ids
    new_alerts = [a for a in alerts if a["id"] in new_ids]
    return new_alerts, current_ids

def should_notify(alert):
    # Simple throttle hook if you want it later
    return True
