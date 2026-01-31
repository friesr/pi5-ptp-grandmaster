from flask import Blueprint, jsonify
import os, json

from backend.analysis.environment_fingerprint import build_environment_fingerprint

environment_api = Blueprint("environment_api", __name__)

@environment_api.route("/load")
def load_environment():
    base = "/opt/ptp-data/live"

    # Expect daily summary files
    summaries = []

    for day in sorted(os.listdir(base)):
        file = os.path.join(base, day, "daily_summary.json")
        if os.path.exists(file):
            summaries.append(json.load(open(file)))

    if not summaries:
        return jsonify({"error": "no summaries found"})

    fingerprint = build_environment_fingerprint(summaries)
    return jsonify(fingerprint)
