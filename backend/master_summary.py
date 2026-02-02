from flask import Blueprint, jsonify
import os, json

from backend.analysis.master_summary import build_master_summary

master_api = Blueprint("master_api", __name__)

@master_api.route("/load/<day>")
def load_master(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name, default=None):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else default

    components = {
        "timing_confidence": load("timing_confidence.json", {}),
        "stability_prediction": load("stability_prediction.json", {}),
        "receiver_health": load("receiver_health.json", {}),
        "environment_change": load("environment_change.json", {}),
        "sla": load("sla_report.json", {}),
        "gnss_metrics": load("gnss_metrics.json", {}),
        "ptp_metrics": load("ptp_metrics.json", {}),
        "predictive_maintenance": load("predictive_maintenance.json", {}),
        "events": {
            "gnss": load("gnss_events.json", []),
            "ptp": load("ptp_events.json", []),
            "interference": load("interference.json", []),
            "sla": load("sla_violations.json", [])
        }
    }

    summary = build_master_summary(day, components)
    return jsonify(summary)
