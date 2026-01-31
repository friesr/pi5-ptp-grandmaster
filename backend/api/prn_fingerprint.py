from flask import Blueprint, jsonify
import os, json

from backend.analysis.prn_fingerprint import build_prn_fingerprints

prn_fingerprint_api = Blueprint("prn_fingerprint_api", __name__)

@prn_fingerprint_api.route("/load")
def load_prn_fingerprints():
    base = "/opt/ptp-data/live"

    history = []
    for day in sorted(os.listdir(base)):
        file = os.path.join(base, day, "daily_summary.json")
        if os.path.exists(file):
            history.append(json.load(open(file)))

    if not history:
        return jsonify({"error": "no history"})

    fingerprints = build_prn_fingerprints(history)
    return jsonify(fingerprints)
