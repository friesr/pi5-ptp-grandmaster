from flask import Blueprint, jsonify
import json
import os

from backend.sim.monte_carlo_runner import run_monte_carlo
from backend.sim.risk_curves import compute_risk_curves

digital_twin_risk_api = Blueprint("digital_twin_risk_api", __name__)

@digital_twin_risk_api.route("/run/<cfg_file>")
def run(cfg_file):
    path = f"/opt/ptp-data/scenarios/{cfg_file}"
    mc_results = run_monte_carlo(path)
    curves = compute_risk_curves(mc_results)
    return jsonify(curves)
