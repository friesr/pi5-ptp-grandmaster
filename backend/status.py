from flask import Blueprint, jsonify
from backend.sampler.gnss_sampler import sample_gnss
from backend.sampler.ntp_sampler import sample_ntp
from backend.sampler.ptp_sampler import sample_ptp
from backend.sampler.system_sampler import sample_system

status_api = Blueprint("status_api", __name__)

@status_api.route("/")
def status():
    return jsonify({
        "gnss": sample_gnss(),
        "ntp": sample_ntp(),
        "ptp": sample_ptp(),
        "system": sample_system()
    })
