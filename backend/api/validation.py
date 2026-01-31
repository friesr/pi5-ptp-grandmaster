from flask import Blueprint, jsonify
from backend.validation.model import compute_model_residuals

validation_api = Blueprint("validation_api", __name__)

@validation_api.route("/status")
def validation_status():
    return jsonify({
        "gnss_vs_gm": "green",
        "ntp_consensus": "green",
        "model_residuals": "green",
        "system_health": "green",
        "storage_health": "green"
    })
