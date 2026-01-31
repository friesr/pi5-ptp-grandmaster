from flask import Blueprint, jsonify
from backend.sim.batch_runner import run_batch

digital_twin_batch_api = Blueprint("digital_twin_batch_api", __name__)

@digital_twin_batch_api.route("/run")
def run():
    results = run_batch()
    return jsonify(results)
