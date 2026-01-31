from flask import Blueprint, jsonify
import os, json

from backend.analysis.antenna_siting import compute_siting_score

antenna_siting_api = Blueprint("antenna_siting_api", __name__)

@antenna_siting_api.route("/evaluate/<day>")
def evaluate(day):
    base = f"/opt/ptp-data/live/{day}"

    # Load reflectors
    refl_file = os.path.join(base, "multipath_3d.json")
    if not os.path.exists(refl_file):
        return jsonify({"error": "no multipath 3D data"})
    reflectors = json.load(open(refl_file))

    # Load environment fingerprint
    env_file = "/opt/ptp-data/live/environment_fingerprint.json"
    env_fingerprint = json.load(open(env_file)) if os.path.exists(env_file) else {}

    # Load constellation performance
    const_file = "/opt/ptp-data/live/constellation_performance.json"
    constellation_perf = json.load(open(const_file)) if os.path.exists(const_file) else {}

    # Load candidate locations
    cand_file = "/opt/ptp-data/antenna_candidates.json"
    if not os.path.exists(cand_file):
        return jsonify({"error": "no candidate locations"})
    candidates = json.load(open(cand_file))

    results = []
    for c in candidates:
        score = compute_siting_score(c, reflectors, env_fingerprint, constellation_perf)
        results.append({
            "name": c["name"],
            "score": score,
            "x": c["x"],
            "y": c["y"],
            "z": c["z"]
        })

    # Sort best → worst
    results.sort(key=lambda x: -x["score"])

    return jsonify(results)
