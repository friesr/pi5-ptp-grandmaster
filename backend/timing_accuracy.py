from flask import Blueprint, jsonify
import os, csv

from backend.analysis.timing_accuracy import estimate_timing_error
from backend.analysis.multipath import multipath_score
from backend.analysis.signal_classifier import classify_signal
from backend.analysis.geometry_score import compute_geometry_score
from backend.analysis.interference_detector import detect_interference

timing_accuracy_api = Blueprint("timing_accuracy_api", __name__)

@timing_accuracy_api.route("/load/<day>")
def load_timing_accuracy(day):
    base = f"/opt/ptp-data/live/{day}"
    gnss_file = os.path.join(base, "gnss.csv")
    ptp_file = os.path.join(base, "ptp4l.log")

    if not os.path.exists(gnss_file) or not os.path.exists(ptp_file):
        return jsonify([])

    # Load GNSS rows
    rows = []
    with open(gnss_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            snr = float(row["snr"])
            el = float(row["elevation"])
            mp = multipath_score(el, snr)

            geom = compute_geometry_score(
                float(row["gdop"]),
                float(row["pdop"]),
                float(row["hdop"]),
                float(row["vdop"]),
                float(row["tdop"])
            )["total_score"]

            fading = snr < 10
            recovering = snr > 25 and row["used"] == "1"

            state = classify_signal(
                snr=snr,
                multipath=mp,
                elevation=el,
                fading=fading,
                recovering=recovering
            )

            rows.append({
                "timestamp": float(row["timestamp"]),
                "snr": snr,
                "multipath": mp,
                "state": state,
                "geometry_score": geom
            })

    # Load PTP events for interference correlation
    with open(ptp_file) as f:
        ptp_events = f.readlines()

    # Detect interference
    interference_events = detect_interference(rows, [])

    # Build timeline
    out = []
    for r in rows:
        ts = r["timestamp"]

        # Determine interference level at this timestamp
        interference_level = 0
        for e in interference_events:
            if abs(e["timestamp"] - ts) < 1:
                if e["type"] == "rf_noise":
                    interference_level = max(interference_level, 1)
                elif e["type"] == "spoofing":
                    interference_level = max(interference_level, 2)
                elif e["type"] == "jamming":
                    interference_level = max(interference_level, 3)

        # Estimate timing error
        error = estimate_timing_error(
            geom=r["geometry_score"],
            snr=r["snr"],
            multipath=r["multipath"],
            prn_health=100,  # placeholder for now
            interference=interference_level
        )

        out.append({
            "timestamp": ts,
            "timing_error_ns": error
        })

    return jsonify(out)
