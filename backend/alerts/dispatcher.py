import time
from backend.config.manager import load_config
from backend.api.status import get_status_snapshot
from backend.alerts.engine import evaluate_alerts
from backend.alerts.notifier import get_new_alerts, should_notify
from backend.alerts.webhook import send_webhook

def run_alert_dispatch_loop():
    previous_ids = set()

    while True:
        cfg = load_config()
        webhook_url = cfg.get("alert_webhook_url")

        status = get_status_snapshot()
        alerts = evaluate_alerts(status)

        new_alerts, previous_ids = get_new_alerts(previous_ids, alerts)

        if webhook_url and new_alerts:
            to_send = [a for a in new_alerts if should_notify(a)]
            if to_send:
                send_webhook(webhook_url, to_send)

        time.sleep(10)
