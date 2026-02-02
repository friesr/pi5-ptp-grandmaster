from flask import Blueprint, jsonify
import os, csv

from backend.analysis.prn_health import compute_prn_health
from backend.analysis.multipath import multipath_score
from backend.analysis.signal_classifier import classify_signal

prn_health_api = Blueprint("prn_health_api", __name__)

@prn_health_api.route("/load/<day>")
def load_prn_health(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify({})

    # Group rows by PRN
    prn_rows = {}

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            prn = int(row["prn"])
            snr = float(row["snr"])
            el = float(row["elevation"])
            mp = multipath_score(el, snr)

            fading = snr < 10
            recovering = snr > 25 and row["used"] == "1"

            state = classify_signal(
                snr=snr,
                multipath=mp,
                elevation=el,
                fading=fading,
                recovering=recovering
            )

            entry = {
                "timestamp": float(row["timestamp"]),
                "snr": snr,
                "multipath": mp,
                "used": row["used"] == "1",
                "state": state
            }

            prn_rows.setdefault(prn, []).append(entry)

    # Compute health for each PRN
    out = {}
    for prn, rows in prn_rows.items():
        out[prn] = compute_prn_health(rows)

    return jsonify(out)
