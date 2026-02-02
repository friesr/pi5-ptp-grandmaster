from flask import Blueprint, jsonify
import os, csv
from backend.analysis.servo_stability import compute_servo_stability

servo_history_api = Blueprint("servo_history_api", __name__)

@servo_history_api.route("/days")
def list_days():
    path = "/opt/ptp-data/live"
    if not os.path.exists(path):
        return jsonify([])
    return jsonify(sorted(os.listdir(path)))

@servo_history_api.route("/load/<day>")
def load_servo_day(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "servo.csv")

    if not os.path.exists(file):
        return jsonify([])

    rows = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "timestamp": float(row["timestamp"]),
                "freq_adj_ppb": float(row["freq_adj_ppb"]),
                "delay_ns": float(row["delay_ns"])
            })

    # Rolling window stability calculation
    out = []
    window = []

    for r in rows:
        window.append(r)
        if len(window) > 50:
            window.pop(0)

        stability = compute_servo_stability(window)
        if stability:
            out.append({
                "timestamp": r["timestamp"],
                "score": stability["score"]
            })

    return jsonify(out)
