from flask import Blueprint, jsonify
import os, json

from backend.analysis.receiver_health import infer_receiver_health

receiver_health_api = Blueprint("receiver_health_api", __name__)

@receiver_health_api.route("/load")
def load_receiver_health():
    base = "/opt/ptp-data/live"

    # Load constellation drift
    drift_file = os.path.join(base, "constellation_drift.json")
    prn_file = os.path.join(base, "prn_health.json")
    interference_file = os.path.join(base, "interference.json")

    if not (os.path.exists(drift_file) and os.path.exists(prn_file) and os.path.exists(interference_file)):
        return jsonify({"error": "missing data"})

    drift = json.load(open(drift_file))
    prn_health = json.load(open(prn_file))
    interference = json.load(open(interference_file))

    result = infer_receiver_health(drift, prn_health, interference)
    return jsonify(result)
