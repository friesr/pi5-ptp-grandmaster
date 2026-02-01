from flask import Blueprint, jsonify
from backend.analysis.global.global_correlation_engine import GlobalCorrelationEngine

# Injected by app.py
GLOBAL_NODE_REGISTRY = {}
GLOBAL_INTEL_ENGINE = None
GLOBAL_CORRELATION_ENGINE = None

global_correlation_api = Blueprint("global_correlation_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_CORRELATION_ENGINE
    if GLOBAL_CORRELATION_ENGINE is None:
        GLOBAL_CORRELATION_ENGINE = GlobalCorrelationEngine(
            GLOBAL_NODE_REGISTRY,
            GLOBAL_INTEL_ENGINE
        )
    return GLOBAL_CORRELATION_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_correlation_api.route("/events")
def correlation_events():
    """
    Returns the raw events used for correlation.
    """
    engine = ensure_engine()
    events = GLOBAL_INTEL_ENGINE.recent_events(300)
    return jsonify(events)

@global_correlation_api.route("/clusters")
def correlation_clusters():
    """
    Returns the full list of correlated clusters.
    """
    engine = ensure_engine()
    clusters = engine.correlate()
    return jsonify(clusters)

@global_correlation_api.route("/root_causes")
def correlation_root_causes():
    """
    Returns only the inferred root causes.
    """
    engine = ensure_engine()
    clusters = engine.correlate()
    causes = [c["root_cause"] for c in clusters]
    return jsonify({"root_causes": causes})

@global_correlation_api.route("/snapshot")
def correlation_snapshot():
    """
    Returns:
      - clusters
      - major events
      - count
    """
    engine = ensure_engine()
    return jsonify(engine.snapshot())

