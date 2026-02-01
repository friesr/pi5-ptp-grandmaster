from flask import Blueprint, jsonify, request
from backend.analysis.global.global_intel_engine import GlobalIntelEngine

# Injected by app.py at startup
GLOBAL_NODE_REGISTRY = {}
GLOBAL_INTEL_ENGINE = None

global_intel_api = Blueprint("global_intel_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_INTEL_ENGINE
    if GLOBAL_INTEL_ENGINE is None:
        GLOBAL_INTEL_ENGINE = GlobalIntelEngine(GLOBAL_NODE_REGISTRY)
    return GLOBAL_INTEL_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_intel_api.route("/ingest")
def ingest_all():
    engine = ensure_engine()
    result = engine.ingest_all()
    return jsonify(result)

@global_intel_api.route("/recent")
def recent_events():
    engine = ensure_engine()
    limit = int(request.args.get("limit", 100))
    return jsonify(engine.recent_events(limit))

@global_intel_api.route("/high_impact")
def high_impact():
    engine = ensure_engine()
    limit = int(request.args.get("limit", 50))
    return jsonify(engine.events_with_timing_impact("high", limit))

@global_intel_api.route("/by_node/<node_id>")
def by_node(node_id):
    engine = ensure_engine()
    limit = int(request.args.get("limit", 100))
    return jsonify(engine.events_by_node(node_id, limit))

@global_intel_api.route("/by_severity/<level>")
def by_severity(level):
    engine = ensure_engine()
    limit = int(request.args.get("limit", 100))
    return jsonify(engine.events_by_severity(level, limit))

@global_intel_api.route("/by_constellation/<name>")
def by_constellation(name):
    engine = ensure_engine()
    limit = int(request.args.get("limit", 100))
    return jsonify(engine.events_by_constellation(name, limit))

@global_intel_api.route("/snapshot")
def snapshot():
    engine = ensure_engine()
    return jsonify(engine.snapshot())
