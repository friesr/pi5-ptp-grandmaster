from flask import Blueprint, jsonify
from backend.analysis.global.global_storyboard_engine import GlobalStoryboardEngine

# Injected by app.py
GLOBAL_NODE_REGISTRY = {}
GLOBAL_REPLAY_ENGINE = None
GLOBAL_CORRELATION_ENGINE = None
GLOBAL_RISK_ENGINE = None
GLOBAL_INTEL_ENGINE = None
GLOBAL_STORYBOARD_ENGINE = None

global_storyboard_api = Blueprint("global_storyboard_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_STORYBOARD_ENGINE
    if GLOBAL_STORYBOARD_ENGINE is None:
        GLOBAL_STORYBOARD_ENGINE = GlobalStoryboardEngine(
            GLOBAL_NODE_REGISTRY,
            GLOBAL_REPLAY_ENGINE,
            GLOBAL_CORRELATION_ENGINE,
            GLOBAL_RISK_ENGINE,
            GLOBAL_INTEL_ENGINE
        )
    return GLOBAL_STORYBOARD_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_storyboard_api.route("/major")
def major_storyboards():
    """
    Returns storyboards for all major correlated events.
    """
    engine = ensure_engine()
    return jsonify(engine.major_storyboards())

@global_storyboard_api.route("/incident")
def incident_summary():
    """
    Returns a summary of the most recent global incident.
    """
    engine = ensure_engine()
    return jsonify(engine.incident_summary())

@global_storyboard_api.route("/snapshot")
def snapshot():
    """
    Returns:
      - major storyboards
      - latest incident summary
      - cluster counts
    """
    engine = ensure_engine()
    return jsonify(engine.snapshot())

