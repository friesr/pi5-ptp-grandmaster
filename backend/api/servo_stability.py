from flask import Blueprint, jsonify
import os, csv
from backend.analysis.servo_stability import compute_servo_stability

servo_stability_api = Blueprint("servo_stability_api", __name__)

@servo_stability_api.route("/current")
def servo_stability_current():
    path = "/opt/ptp-data/live"
    days = sorted(os.listdir(path))
    if not days:
        return jsonify({"error": "no_data"})

    file = os.path.join(path, days[-1], "servo.csv")
    if not os.path.exists(file):
        return jsonify({"error": "no_servo_data"})

    samples = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            samples.append({
                "freq_adj_ppb": float(row["freq_adj_ppb"]),
                "delay_ns": float(row["delay_ns"])
            })

    result = compute_servo_stability(samples)
    if result is None:
        return jsonify({"error": "not_enough_samples"})

    return jsonify(result)
