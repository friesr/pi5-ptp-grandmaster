from flask import Blueprint, jsonify
from backend.analysis.drift import compute_drift_model
import os
import csv

drift_api = Blueprint("drift_api", __name__)

def load_ptp_data():
    """Load timestamps + offsets from today's log."""
    path = "/opt/ptp-data/live"
    days = sorted(os.listdir(path))
    if not days:
        return [], []

    file = os.path.join(path, days[-1], "ptp.csv")
    if not os.path.exists(file):
        return [], []

    timestamps = []
    offsets = []

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamps.append(float(row["timestamp"]))
                offsets.append(float(row["offset_ns"]))
            except:
                pass

    return timestamps, offsets

@drift_api.route("/model")
def drift_model():
    timestamps, offsets = load_ptp_data()
    model = compute_drift_model(timestamps, offsets)

    if model is None:
        return jsonify({"error": "not_enough_data"})

    return jsonify(model)
