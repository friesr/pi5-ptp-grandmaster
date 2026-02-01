from flask import Blueprint, jsonify
from backend.analysis.global.federation_engine import FederationEngine

# Injected by app.py at startup
GLOBAL_NODE_REGISTRY = {}
GLOBAL_FEDERATION_ENGINE = None

federation_api = Blueprint("federation_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_FEDERATION_ENGINE
    if GLOBAL_FEDERATION_ENGINE is None:
        GLOBAL_FEDERATION_ENGINE = FederationEngine(GLOBAL_NODE_REGISTRY)
    return GLOBAL_FEDERATION_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@federation_api.route("/status")
def federation_status():
    engine = ensure_engine()
    return jsonify(engine.federation_status())

@federation_api.route("/topology")
def federation_topology():
    engine = ensure_engine()
    return jsonify(engine.topology())

@federation_api.route("/heartbeat/<node_id>")
def heartbeat(node_id):
    engine = ensure_engine()
    if node_id not in GLOBAL_NODE_REGISTRY:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(engine.heartbeat(node_id))

@federation_api.route("/sync/<node_id>")
def sync(node_id):
    engine = ensure_engine()
    if node_id not in GLOBAL_NODE_REGISTRY:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(engine.sync_node(node_id))

@federation_api.route("/snapshot")
def federation_snapshot():
    engine = ensure_engine()
    return jsonify(engine.snapshot())

