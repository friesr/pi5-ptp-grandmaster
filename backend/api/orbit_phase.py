from flask import Blueprint, jsonify
import os, json

from backend.analysis.orbit_phase_stats import build_orbit_phase_stats

orbit_phase_api = Blueprint("orbit_phase_api", __name__)

@orbit_phase_api.route("/load/<day>")
def load_orbit_phase(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss_samples.json")

    if not os.path.exists(file):
        return jsonify({"error": "no GNSS samples"})

    samples = json.load(open(file))
    stats = build_orbit_phase_stats(samples)

    return jsonify(stats)
