from flask import Blueprint, jsonify
from backend.sampler.ptp_servo_sampler import sample_ptp_servo

ptp_servo_api = Blueprint("ptp_servo_api", __name__)

@ptp_servo_api.route("/status")
def servo_status():
    return jsonify(sample_ptp_servo())
