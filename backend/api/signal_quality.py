from flask import Blueprint, jsonify
import os, csv

from backend.analysis.signal_classifier import classify_signal
from backend.analysis.multipath import multipath_score

signal_quality_api = Blueprint("signal_quality_api", __name__)

@signal_quality_api.route("/load/<day>")
def load_signal_quality(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify([])

    rows = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            snr = float(row["snr"])
            el = float(row["elevation"])
            mp = multipath_score(el, snr)

            # Fade detection flags (simple version)
            fading = snr < 10
            recovering = snr > 25 and float(row["used"]) == 1

            state = classify_signal(
                snr=snr,
                multipath=mp,
                elevation=el,
                fading=fading,
                recovering=recovering
            )

            rows.append({
                "timestamp": float(row["timestamp"]),
                "prn": int(row["prn"]),
                "snr": snr,
                "multipath": mp,
                "state": state
            })

    return jsonify(rows)
