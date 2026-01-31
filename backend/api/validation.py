from flask import Blueprint, jsonify
from backend.sampler.gnss_sampler import sample_gnss
from backend.sampler.ntp_sampler import sample_ntp
from backend.sampler.ptp_sampler import sample_ptp
from backend.sampler.system_sampler import sample_system
from backend.storage.manager import get_directory_size_gb
from backend.config.manager import load_config

from backend.validation.gnss_validation import validate_gnss
from backend.validation.ntp_validation import validate_ntp
from backend.validation.system_validation import (
    validate_ptp,
    validate_system_health,
    validate_storage
)

validation_api = Blueprint("validation_api", __name__)

@validation_api.route("/status")
def validation_status():
    gnss = sample_gnss()
    ntp = sample_ntp()
    ptp = sample_ptp()
    system = sample_system()

    cfg = load_config()
    local = get_directory_size_gb("/opt/ptp-data/live")
    nas = get_directory_size_gb("/opt/ptp-data/archive")

    return jsonify({
        "gnss": validate_gnss(gnss),
        "ntp": validate_ntp(ntp),
        "ptp": validate_ptp(ptp),
        "system": validate_system_health(system),
        "storage": validate_storage(
            (local / cfg["local_max_gb"]) * 100,
            (nas / cfg["nas_max_gb"]) * 100
        )
    })
