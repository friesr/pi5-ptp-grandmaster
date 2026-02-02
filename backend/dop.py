from flask import Blueprint, jsonify
from backend.sampler.gnss_sampler import sample_gnss
from backend.analysis.dop import compute_dop

dop_api = Blueprint("dop_api", __name__)

@dop_api.route("/current")
def dop_current():
    gnss = sample_gnss()
    sats = [s for s in gnss["satellites"] if s["used"]]

    dop = compute_dop(sats)
    if dop is None:
        return jsonify({"error": "not_enough_satellites"})

    return jsonify(dop)
