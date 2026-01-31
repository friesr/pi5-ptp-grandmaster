import json
import requests  # make sure this is in requirements.txt

def send_webhook(url, alerts):
    payload = {
        "alerts": alerts
    }
    try:
        requests.post(url, json=payload, timeout=2)
    except Exception:
        # Fail silently for now
        pass
