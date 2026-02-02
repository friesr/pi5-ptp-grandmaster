from flask import Blueprint, jsonify
import os, json

from backend.analysis.multipath_3d import reconstruct_reflectors

multipath_3d_api = Blueprint("multipath_3d_api", __name__)

@multipath_3d_api.route("/reconstruct/<day>")
def reconstruct(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "multipath_samples.json")

    if not os.path.exists(file):
        return jsonify({"error": "no multipath samples"})

    samples = json.load(open(file))
    reflectors = reconstruct_reflectors(samples)

    return jsonify(reflectors)
