from flask import Blueprint, jsonify, request
from backend.analysis.global.global_replay_engine import GlobalReplayEngine

# Injected by app.py
GLOBAL_NODE_REGISTRY = {}
GLOBAL_INTEL_ENGINE = None
GLOBAL_CORRELATION_ENGINE = None
GLOBAL_RISK_ENGINE = None
GLOBAL_REPLAY_ENGINE = None

global_replay_api = Blueprint("global_replay_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_REPLAY_ENGINE
    if GLOBAL_REPLAY_ENGINE is None:
        GLOBAL_REPLAY_ENGINE = GlobalReplayEngine(
            GLOBAL_NODE_REGISTRY,
            GLOBAL_INTEL_ENGINE,
            GLOBAL_CORRELATION_ENGINE,
            GLOBAL_RISK_ENGINE
        )
    return GLOBAL_REPLAY_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_replay_api.route("/timeline")
def timeline():
    """
    Returns a unified global timeline for replay.
    """
    engine = ensure_engine()
    minutes = int(request.args.get("minutes", 120))
    return jsonify(engine.build_global_timeline(minutes))

@global_replay_api.route("/window")
def window():
    """
    Returns all events between two timestamps.
    """
    engine = ensure_engine()
    start_ts = float(request.args.get("start"))
    end_ts = float(request.args.get("end"))
    return jsonify(engine.replay_window(start_ts, end_ts))

@global_replay_api.route("/state/<float:ts>")
def state(ts):
    """
    Reconstructs global state at a given timestamp.
    """
    engine = ensure_engine()
    return jsonify(engine.reconstruct_state(ts))

@global_replay_api.route("/snapshot")
def snapshot():
    """
    Returns:
      - timeline
      - recent clusters
      - risk
    """
    engine = ensure_engine()
    minutes = int(request.args.get("minutes", 120))
    return jsonify(engine.snapshot(minutes))
