from flask import Blueprint, jsonify
import os, csv

from backend.analysis.anomaly_features import build_feature_vector
from backend.analysis.anomaly_clustering import cluster_anomalies
from backend.analysis.multipath import multipath_score
from backend.analysis.signal_classifier import classify_signal
from backend.analysis.geometry_score import compute_geometry_score

anomaly_cluster_api = Blueprint("anomaly_cluster_api", __name__)

@anomaly_cluster_api.route("/load/<day>")
def load_clusters(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify([])

    rows = []
    feature_vectors = []

    with open(file) as f:
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

            # Placeholder PRN health
            prn_health = 100

            # Placeholder interference level
            interference_level = 0

            r = {
                "timestamp": float(row["timestamp"]),
                "snr": snr,
                "multipath": mp,
                "geometry_score": geom,
                "state": state,
                "interference_level": interference_level,
                "prn_health": prn_health
            }

            rows.append(r)
            feature_vectors.append(build_feature_vector(r))

    labels, centers = cluster_anomalies(feature_vectors)

    # Attach labels
    for r, label in zip(rows, labels):
        r["cluster"] = label

    return jsonify({
        "rows": rows,
        "centers": centers
    })
