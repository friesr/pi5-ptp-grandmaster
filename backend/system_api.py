from flask import Blueprint, jsonify

system_api = Blueprint("system_api", __name__)

@system_api.route("/api/system/health", methods=["GET"])
def system_health():
    return jsonify({
        "status": "ok",
        "backend": "running",
        "version": "1.0"
    })

@system_api.route("/debug/bus")
def debug_bus():
    from backend.analysis.global_intel_bus import GlobalIntelBus
    bus = GlobalIntelBus()
    return {
        "nodes": list(bus.nodes.keys()),
        "node_count": len(bus.nodes)
    }
