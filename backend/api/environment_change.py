from flask import Blueprint, jsonify
import os, json

from backend.analysis.environment_change import compute_deviation

env_change_api = Blueprint("env_change_api", __name__)

@env_change_api.route("/load/<day>")
def load_env_change(day):
    base = f"/opt/ptp-data/live/{day}"

    # Load today's summary
    today_file = os.path.join(base, "daily_summary.json")
    if not os.path.exists(today_file):
        return jsonify({"error": "no daily summary"})

    today = json.load(open(today_file))

    # Load fingerprint
    fingerprint_file = "/opt/ptp-data/live/environment_fingerprint.json"
    if not os.path.exists(fingerprint_file):
        return jsonify({"error": "no fingerprint"})

    fingerprint = json.load(open(fingerprint_file))

    deviation, factors = compute_deviation(today, fingerprint)

    # Classification
    if deviation < 0.1:
        status = "stable"
    elif deviation < 0.25:
        status = "mild_change"
    elif deviation < 0.5:
        status = "significant_change"
    else:
        status = "critical_change"

    return jsonify({
        "deviation": deviation,
        "status": status,
        "factors": factors
    })
