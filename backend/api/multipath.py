from flask import Blueprint, jsonify
from backend.sampler.gnss_sampler import sample_gnss
from backend.analysis.multipath import compute_multipath_for_satellites

multipath_api = Blueprint("multipath_api", __name__)

@multipath_api.route("/scores")
def multipath_scores():
    gnss = sample_gnss()
    sats = gnss["satellites"]
    scores = compute_multipath_for_satellites(sats)
    return jsonify(scores)
