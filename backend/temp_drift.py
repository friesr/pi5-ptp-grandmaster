from flask import Blueprint, jsonify
from backend.analysis.temp_drift import compute_temp_drift_model
import os
import csv

temp_drift_api = Blueprint("temp_drift_api", __name__)

def load_temp_and_offset():
    path = "/opt/ptp-data/live"
    days = sorted(os.listdir(path))
    if not days:
        return [], []

    file_ptp = os.path.join(path, days[-1], "ptp.csv")
    file_sys = os.path.join(path, days[-1], "system.csv")

    temps = []
    offsets = []

    if not os.path.exists(file_ptp) or not os.path.exists(file_sys):
        return temps, offsets

    # Load PTP offsets
    ptp_map = {}
    with open(file_ptp) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ptp_map[row["timestamp"]] = float(row["offset_ns"])

    # Load system temps and align timestamps
    with open(file_sys) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row["timestamp"]
            if ts in ptp_map:
                temps.append(float(row["cpu_temp_c"]))
                offsets.append(ptp_map[ts])

    return temps, offsets

@temp_drift_api.route("/model")
def temp_drift_model():
    temps, offsets = load_temp_and_offset()
    model = compute_temp_drift_model(temps, offsets)

    if model is None:
        return jsonify({"error": "not_enough_data"})

    return jsonify(model)
