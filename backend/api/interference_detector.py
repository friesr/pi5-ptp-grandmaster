from flask import Blueprint, jsonify
import os, csv

from backend.analysis.interference_detector import detect_interference
from backend.analysis.multipath import multipath_score
from backend.analysis.signal_classifier import classify_signal
from backend.analysis.geometry_score import compute_geometry_score
from backend.analysis.ptp_events import parse_ptp_events

interference_api = Blueprint("interference_api", __name__)

@interference_api.route("/load/<day>")
def load_interference(day):
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

    # Load PTP events
    with open(ptp_file) as f:
        ptp_events = parse_ptp_events(f.readlines())

    events = detect_interference(rows, ptp_events)
    return jsonify(events)
