from flask import Blueprint, jsonify
from backend.analysis.global.global_risk_engine import GlobalRiskEngine

# Injected by app.py
GLOBAL_NODE_REGISTRY = {}
GLOBAL_INTEL_ENGINE = None
GLOBAL_CORRELATION_ENGINE = None
GLOBAL_RISK_ENGINE = None

global_risk_api = Blueprint("global_risk_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_RISK_ENGINE
    if GLOBAL_RISK_ENGINE is None:
        GLOBAL_RISK_ENGINE = GlobalRiskEngine(
            GLOBAL_NODE_REGISTRY,
            GLOBAL_INTEL_ENGINE,
            GLOBAL_CORRELATION_ENGINE
        )
    return GLOBAL_RISK_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_risk_api.route("/node")
def node_risk():
    engine = ensure_engine()
    result = {
        node_id: engine.node_risk(node)
        for node_id, node in GLOBAL_NODE_REGISTRY.items()
    }
    return jsonify(result)

@global_risk_api.route("/constellations")
def constellation_risk():
    engine = ensure_engine()
    return jsonify(engine.constellation_risk())

@global_risk_api.route("/global")
def global_risk():
    engine = ensure_engine()
    return jsonify({"global_risk": engine.global_risk()})

@global_risk_api.route("/forecast")
def forecast():
    engine = ensure_engine()
    return jsonify(engine.forecast())

@global_risk_api.route("/snapshot")
def snapshot():
    engine = ensure_engine()
    return jsonify(engine.snapshot())
