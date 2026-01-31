from flask import Blueprint, jsonify
from backend.analysis.allan import compute_allan_deviation
import os
import csv

allan_api = Blueprint("allan_api", __name__)

def load_ptp_offsets():
    """Load recent PTP offsets from today's log."""
    path = "/opt/ptp-data/live"
    day = sorted(os.listdir(path))[-1]  # latest folder
    file = os.path.join(path, day, "ptp.csv")

    offsets = []
    if not os.path.exists(file):
        return offsets

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                offsets.append(float(row["offset_ns"]))
            except:
                pass

    return offsets

@allan_api.route("/adev")
def allan_deviation():
    offsets = load_ptp_offsets()

    tau_values = [1, 2, 5, 10, 20, 50, 100]

    adev = compute_allan_deviation(offsets, tau_values)

    return jsonify({
        "tau": tau_values,
        "adev": [adev[t] for t in tau_values]
    })
