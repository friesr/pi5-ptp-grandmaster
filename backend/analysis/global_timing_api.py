# backend/api/global_timing_api.py

from flask import Blueprint, jsonify

global_timing_api = Blueprint("global_timing_api", __name__)

# This will be injected from app.py
GLOBAL_TIMING_ENGINE = None


@global_timing_api.route("/snapshot", methods=["GET"])
def timing_snapshot():
    """
    Return the current timing snapshot for the global observatory.

    Response shape:
      {
        "time_now": "...",
        "uncertainty_95_ns": ...,
        "reliability_95": ...,
        "clock_class": "...",
        "clock_accuracy": ...,
        "clock_variance": ...
      }
    """
    if GLOBAL_TIMING_ENGINE is None:
        return jsonify({"error": "Timing engine not initialized"}), 500

    snap = GLOBAL_TIMING_ENGINE.snapshot()
    return jsonify(snap)
