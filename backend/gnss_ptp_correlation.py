from flask import Blueprint, jsonify
import os, csv

from backend.analysis.gnss_ptp_correlation import correlate_gnss_ptp
from backend.analysis.multipath import multipath_score
from backend.analysis.signal_classifier import classify_signal
from backend.analysis.geometry_score import compute_geometry_score
from backend.analysis.ptp_events import parse_ptp_events

gnss_ptp_corr_api = Blueprint("gnss_ptp_corr_api", __name__)

@gnss_ptp_corr_api.route("/load/<day>")
def load_corr(day):
    base = f"/opt/ptp-data/live/{day}"

    gnss_file = os.path.join(base, "gnss.csv")
    ptp_file = os.path.join(base, "ptp4l.log")

    if not os.path.exists(gnss_file) or not os.path.exists(ptp_file):
        return jsonify([])

    # Load GNSS rows
    gnss_rows = []
    with open(gnss_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            snr = float(row["snr"])
            el = float(row["elevation"])
            mp = multipath_score(el, snr)

            # Geometry
            gdop = float(row["gdop"])
            pdop = float(row["pdop"])
            hdop = float(row["hdop"])
            vdop = float(row["vdop"])
            tdop = float(row["tdop"])
            geom = compute_geometry_score(gdop, pdop, hdop, vdop, tdop)["total_score"]

            # Simple fade flags
            fading = snr < 10
            recovering = snr > 25 and row["used"] == "1"

            state = classify_signal(
                snr=snr,
                multipath=mp,
                elevation=el,
                fading=fading,
                recovering=recovering
            )

            gnss_rows.append({
                "timestamp": float(row["timestamp"]),
                "snr": snr,
                "multipath": mp,
                "state": state,
                "geometry_score": geom
            })

    # Load PTP events
    with open(ptp_file) as f:
        ptp_events = parse_ptp_events(f.readlines())

    correlations = correlate_gnss_ptp(gnss_rows, ptp_events)
    return jsonify(correlations)
