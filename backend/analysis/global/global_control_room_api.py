from flask import Blueprint, jsonify
from backend.analysis.global.global_control_room_engine import GlobalControlRoomEngine

# Injected by app.py
GLOBAL_NODE_REGISTRY = {}
GLOBAL_FEDERATION_ENGINE = None
GLOBAL_INTEL_ENGINE = None
GLOBAL_CORRELATION_ENGINE = None
GLOBAL_RISK_ENGINE = None
GLOBAL_CONTROL_ROOM_ENGINE = None

global_control_room_api = Blueprint("global_control_room_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_CONTROL_ROOM_ENGINE
    if GLOBAL_CONTROL_ROOM_ENGINE is None:
        GLOBAL_CONTROL_ROOM_ENGINE = GlobalControlRoomEngine(
            GLOBAL_NODE_REGISTRY,
            GLOBAL_FEDERATION_ENGINE,
            GLOBAL_INTEL_ENGINE,
            GLOBAL_CORRELATION_ENGINE,
            GLOBAL_RISK_ENGINE
        )
    return GLOBAL_CONTROL_ROOM_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_control_room_api.route("/snapshot")
def snapshot():
    engine = ensure_engine()
    return jsonify(engine.snapshot())

@global_control_room_api.route("/alerts")
def alerts():
    engine = ensure_engine()
    return jsonify(engine.global_alerts())

@global_control_room_api.route("/summary")
def summary():
    engine = ensure_engine()
    snap = engine.snapshot()
    return jsonify({
        "timestamp": snap["timestamp"],
        "global_risk": snap["risk"]["global_risk"],
        "major_clusters": snap["correlation"]["major_events"],
        "active_alerts": snap["alerts"],
        "node_count": len(snap["nodes"]),
        "federation_status": snap["federation"]["status"]
    })
