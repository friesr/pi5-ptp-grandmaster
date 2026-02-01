from flask import Blueprint, jsonify
from backend.analysis.global.node_model import NodeModel

# Injected by app.py
GLOBAL_NODE_REGISTRY = {}
GLOBAL_FEDERATION_ENGINE = None
GLOBAL_INTEL_ENGINE = None

global_map_api = Blueprint("global_map_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def node_geo(node_id):
    """
    Synthetic regional cluster coordinates.
    Real node is the anchor.
    Synthetic nodes are placed in a small radius around it.
    """
    base_lat = 41.5   # Iowa-ish region (approx)
    base_lon = -93.5

    offsets = {
        "obs-real-01": (0.00, 0.00),
        "obs-sim-01": (0.12, -0.08),
        "obs-sim-02": (-0.10, 0.14),
        "obs-sim-03": (0.07, 0.11),
    }

    off = offsets.get(node_id, (0, 0))
    return {
        "lat": base_lat + off[0],
        "lon": base_lon + off[1]
    }

def node_status(node):
    """
    Convert node health + confidence into a map-friendly status.
    """
    health = node.health()
    conf = node.confidence()

    status = "green"
    if conf.get("score", 1) < 0.85:
        status = "yellow"
    if conf.get("score", 1) < 0.70:
        status = "red"

    return {
        "status": status,
        "cpu": health.get("cpu"),
        "mem": health.get("mem"),
        "temp": health.get("temp"),
        "confidence": conf.get("score")
    }

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_map_api.route("/nodes")
def map_nodes():
    """
    Returns:
      - node positions
      - node health status
      - confidence
    """
    nodes = []
    for node_id, node in GLOBAL_NODE_REGISTRY.items():
        nodes.append({
            "node_id": node_id,
            "geo": node_geo(node_id),
            "metadata": node.metadata(),
            "status": node_status(node)
        })
    return jsonify({"nodes": nodes})

@global_map_api.route("/topology")
def map_topology():
    """
    Federation links for map visualization.
    """
    if GLOBAL_FEDERATION_ENGINE is None:
        return jsonify({"links": []})

    topo = GLOBAL_FEDERATION_ENGINE.topology()
    return jsonify({
        "hub": topo["hub"],
        "nodes": topo["nodes"],
        "links": topo["links"]
    })

@global_map_api.route("/overlays")
def map_overlays():
    """
    Provides optional overlays:
      - interference zones
      - constellation activity
      - high-impact timing events
    """
    if GLOBAL_INTEL_ENGINE is None:
        return jsonify({"overlays": {}})

    intel = GLOBAL_INTEL_ENGINE.snapshot()

    # Synthetic interference zones
    interference_zones = []
    for node_id, node in GLOBAL_NODE_REGISTRY.items():
        for event in node.interference():
            interference_zones.append({
                "node_id": node_id,
                "geo": node_geo(node_id),
                "power": event.get("power", -95),
                "band": event.get("band", "L1"),
                "timestamp": event.get("timestamp")
            })

    return jsonify({
        "overlays": {
            "interference": interference_zones,
            "constellation_activity": intel.get("constellation_activity", {}),
            "high_impact_events": intel.get("high_impact", [])
        }
    })
