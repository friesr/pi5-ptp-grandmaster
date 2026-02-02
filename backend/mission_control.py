from flask import Blueprint, jsonify
import os, json

mission_api = Blueprint("mission_api", __name__)

@mission_api.route("/load/<day>")
def load_mission(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name, default=None):
        file = os.path.join(base, name)
        if os.path.exists(file):
            return json.load(open(file))
        return default

    return jsonify({
        "timing_confidence": load("timing_confidence.json", {}),
        "stability_prediction": load("stability_prediction.json", {}),
        "receiver_health": load("receiver_health.json", {}),
        "environment_change": load("environment_change.json", {}),
        "sla": load("sla_report.json", {}),
        "gnss_metrics": load("gnss_metrics.json", {}),
        "ptp_metrics": load("ptp_metrics.json", {}),
        "events": {
            "gnss": load("gnss_events.json", []),
            "ptp": load("ptp_events.json", []),
            "interference": load("interference.json", []),
            "sla": load("sla_violations.json", [])
        },
        "charts": {
            "confidence": load("confidence_timeseries.json", []),
            "timing_error": load("timing_error_timeseries.json", []),
            "interference": load("interference_timeseries.json", []),
            "availability": load("availability_timeseries.json", [])
        }
    })
