from flask import Blueprint, jsonify

# This will be injected by app.py at startup
GLOBAL_NODE_REGISTRY = None

global_nodes_api = Blueprint("global_nodes_api", __name__)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def get_node(node_id):
    registry = global_nodes_api.GLOBAL_NODE_REGISTRY
    if not registry:
        return None
    return registry.get(node_id)


# ------------------------------------------------------------
# Debug / Module Introspection
# ------------------------------------------------------------
@global_nodes_api.route("/debug")
def debug_registry():
    registry = global_nodes_api.GLOBAL_NODE_REGISTRY
    return jsonify({
        "registry_id": id(registry),
        "keys": list(registry.keys()) if registry else []
    })


@global_nodes_api.route("/module")
def module_info():
    import sys
    import backend.api.global_nodes_api as m
    return jsonify({
        "module_file": m.__file__,
        "module_id": id(m),
        "registry_id": id(m.GLOBAL_NODE_REGISTRY),
        "registry_keys": list(m.GLOBAL_NODE_REGISTRY.keys()) if m.GLOBAL_NODE_REGISTRY else [],
        "sys_path": sys.path,
    })


# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------
@global_nodes_api.route("/list")
def list_nodes():
    registry = global_nodes_api.GLOBAL_NODE_REGISTRY
    if not registry:
        return jsonify({"nodes": []})

    return jsonify({
        "nodes": [
            node.snapshot()
            for node in registry.values()
        ]
    })


@global_nodes_api.route("/<node_id>/metadata")
def node_metadata(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.snapshot())


@global_nodes_api.route("/<node_id>/health")
def node_health(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    return jsonify({
        "node_id": node.node_id,
        "health": node.health,
        "confidence": node.confidence,
        "drift_ns": node.drift_ns,
        "anomalies": list(node.anomalies),
    })


@global_nodes_api.route("/<node_id>/drift")
def node_drift(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    return jsonify({
        "node_id": node.node_id,
        "drift_ns": node.drift_ns,
    })


@global_nodes_api.route("/<node_id>/confidence")
def node_confidence(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    return jsonify({
        "node_id": node.node_id,
        "confidence": node.confidence,
    })


@global_nodes_api.route("/<node_id>/anomalies")
def node_anomalies(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    return jsonify({
        "node_id": node.node_id,
        "anomalies": list(node.anomalies),
    })


@global_nodes_api.route("/<node_id>/interference")
def node_interference(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    # Placeholder until interference engine is implemented
    return jsonify({
        "node_id": node.node_id,
        "interference": {
            "rf_noise": 0.0,
            "multipath_score": 0.0,
            "spoofing_risk": 0.0,
        }
    })


@global_nodes_api.route("/<node_id>/timeline")
def node_timeline(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    # Placeholder until timeline engine is implemented
    return jsonify({
        "node_id": node.node_id,
        "timeline": []
    })


@global_nodes_api.route("/<node_id>/snapshot")
def node_snapshot(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    return jsonify({
        "metadata": node.snapshot(),
        "health": {
            "health": node.health,
            "confidence": node.confidence,
            "drift_ns": node.drift_ns,
            "anomalies": list(node.anomalies),
        },
        "interference": {
            "rf_noise": 0.0,
            "multipath_score": 0.0,
            "spoofing_risk": 0.0,
        },
        "timeline": []
    })
