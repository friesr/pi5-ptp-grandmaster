from flask import Blueprint, jsonify
import subprocess
import os
import time
from backend.sampler.system_sampler import sample_system

system_health_api = Blueprint("system_health_api", __name__)

def check_service(name):
    try:
        out = subprocess.check_output(
            ["systemctl", "is-active", name],
            text=True
        ).strip()
        return out == "active"
    except Exception:
        return False

def ping_host(host):
    try:
        out = subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", host],
            text=True
        )
        return True
    except Exception:
        return False

@system_health_api.route("/status")
def system_health_status():
    sys = sample_system()

    services = {
        "ptp4l": check_service("ptp4l"),
        "phc2sys": check_service("phc2sys"),
        "logger": check_service("logger.service"),
        "alerts": check_service("alerts.service"),
        "dashboard": check_service("dashboard.service")
    }

    network = {
        "gateway_reachable": ping_host("192.168.1.1"),
        "google_reachable": ping_host("8.8.8.8")
    }

    return jsonify({
        "system": sys,
        "services": services,
        "network": network
    })
