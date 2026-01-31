from flask import Blueprint, jsonify
import os
import csv

from backend.analysis.multipath import multipath_score

skyplot_playback_api = Blueprint("skyplot_playback_api", __name__)


@skyplot_playback_api.route("/load/<day>")
def load_skyplot_day(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify([])

    frames = {}

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = float(row["timestamp"])
            prn = int(row["prn"])
            az = float(row["azimuth"])
            el = float(row["elevation"])
            snr = float(row["snr"])

            if ts not in frames:
                frames[ts] = []

            frames[ts].append({
                "prn": prn,
                "azimuth": az,
                "elevation": el,
                "snr": snr,
                "multipath": multipath_score(el, snr)
            })

    out = []
    for ts in sorted(frames.keys()):
        out.append({
            "timestamp": ts,
            "satellites": frames[ts]
        })

    return jsonify(out)
