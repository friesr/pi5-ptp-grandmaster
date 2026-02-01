from flask import Blueprint, jsonify
from backend.analysis.global.node_model import NodeModel

# This will be injected by app.py at startup
GLOBAL_NODE_REGISTRY = {}

global_nodes_api = Blueprint("global_nodes_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def get_node(node_id):
    if node_id not in GLOBAL_NODE_REGISTRY:
        return None
    return GLOBAL_NODE_REGISTRY[node_id]

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_nodes_api.route("/list")
def list_nodes():
    return jsonify({
        "nodes": [
            node.metadata()
            for node in GLOBAL_NODE_REGISTRY.values()
        ]
    })

@global_nodes_api.route("/<node_id>/metadata")
def node_metadata(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.metadata())

@global_nodes_api.route("/<node_id>/health")
def node_health(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.health())

@global_nodes_api.route("/<node_id>/drift")
def node_drift(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.drift())

@global_nodes_api.route("/<node_id>/confidence")
def node_confidence(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.confidence())

@global_nodes_api.route("/<node_id>/anomalies")
def node_anomalies(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.anomalies())

@global_nodes_api.route("/<node_id>/interference")
def node_interference(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.interference())

@global_nodes_api.route("/<node_id>/timeline")
def node_timeline(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404
    return jsonify(node.timeline())

@global_nodes_api.route("/<node_id>/snapshot")
def node_snapshot(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "unknown node"}), 404

    return jsonify({
        "metadata": node.metadata(),
        "health": node.health(),
        "drift": node.drift(),
        "confidence": node.confidence(),
        "anomalies": node.anomalies(),
        "interference": node.interference(),
        "timeline": node.timeline()
    })

