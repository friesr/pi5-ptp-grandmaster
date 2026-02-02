from flask import Blueprint, jsonify
import os, json

from backend.analysis.timing_confidence import compute_timing_confidence

timing_conf_api = Blueprint("timing_conf_api", __name__)

@timing_conf_api.route("/load/<day>")
def load_conf(day):
    base = f"/opt/ptp-data/live/{day}"

    # Load required components
    geom = json.load(open(os.path.join(base, "geometry.json")))
    snr = json.load(open(os.path.join(base, "snr.json")))
    mp = json.load(open(os.path.join(base, "multipath.json")))
    prn = json.load(open(os.path.join(base, "prn_health.json")))
    inter = json.load(open(os.path.join(base, "interference.json")))
    recv = json.load(open(os.path.join(base, "receiver_health.json")))
    acc = json.load(open(os.path.join(base, "timing_accuracy.json")))
    env = json.load(open(os.path.join(base, "environment_deviation.json")))

    score = compute_timing_confidence(
        geometry=geom["avg"],
        snr=snr["avg"],
        multipath=mp["avg"],
        prn_health=prn["avg"],
        interference_level=inter["level"],
        receiver_health_score=recv["score"],
        timing_error_ns=acc["avg_error_ns"],
        env_deviation=env["deviation"]
    )

    return jsonify({"timing_confidence": score})
