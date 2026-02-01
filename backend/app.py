from flask import Flask
from flask_cors import CORS

# Global Intelligence Bus
#from backend.analysis.global.global_intel_bus import GlobalIntelBus
from backend.analysis.global_intel_bus import GlobalIntelBus
# Global APIs
from backend.api.global.global_nodes_api import nodes_api
from backend.api.global.global_intel_api import global_intel_api
from backend.api.global.global_federation_api import federation_api
from backend.api.global.global_map_api import global_map_api
from backend.api.global.global_correlation_api import global_correlation_api
from backend.api.global.global_risk_api import global_risk_api
from backend.api.global.global_control_room_api import global_control_room_api
from backend.api.global.global_replay_api import global_replay_api
from backend.api.global.global_storyboard_api import global_storyboard_api
from backend.api.global.global_archive_api import global_archive_api


def create_app():
    app = Flask(__name__)
    CORS(app)

    # ------------------------------------------------------------
    # Initialize Global Intelligence Bus
    # ------------------------------------------------------------
    bus = GlobalIntelBus()

    # ------------------------------------------------------------
    # Inject engines into global APIs
    # ------------------------------------------------------------
    # Nodes
    nodes_api.GLOBAL_NODE_REGISTRY = bus.nodes

    # Intel
    global_intel_api.GLOBAL_NODE_REGISTRY = bus.nodes
    global_intel_api.GLOBAL_INTEL_ENGINE = bus.intel

    # Federation
    federation_api.GLOBAL_NODE_REGISTRY = bus.nodes
    federation_api.GLOBAL_FEDERATION_ENGINE = bus.federation

    # Map
    global_map_api.GLOBAL_NODE_REGISTRY = bus.nodes
    global_map_api.GLOBAL_FEDERATION_ENGINE = bus.federation
    global_map_api.GLOBAL_INTEL_ENGINE = bus.intel

    # Correlation
    global_correlation_api.GLOBAL_NODE_REGISTRY = bus.nodes
    global_correlation_api.GLOBAL_INTEL_ENGINE = bus.intel
    global_correlation_api.GLOBAL_CORRELATION_ENGINE = bus.correlation

    # Risk
    global_risk_api.GLOBAL_NODE_REGISTRY = bus.nodes
    global_risk_api.GLOBAL_INTEL_ENGINE = bus.intel
    global_risk_api.GLOBAL_CORRELATION_ENGINE = bus.correlation
    global_risk_api.GLOBAL_RISK_ENGINE = bus.risk

    # Control Room
    global_control_room_api.GLOBAL_NODE_REGISTRY = bus.nodes
    global_control_room_api.GLOBAL_FEDERATION_ENGINE = bus.federation
    global_control_room_api.GLOBAL_INTEL_ENGINE = bus.intel
    global_control_room_api.GLOBAL_CORRELATION_ENGINE = bus.correlation
    global_control_room_api.GLOBAL_RISK_ENGINE = bus.risk
    global_control_room_api.GLOBAL_CONTROL_ROOM_ENGINE = bus.control_room

    # Replay
    global_replay_api.GLOBAL_NODE_REGISTRY = bus.nodes
    global_replay_api.GLOBAL_INTEL_ENGINE = bus.intel
    global_replay_api.GLOBAL_CORRELATION_ENGINE = bus.correlation
    global_replay_api.GLOBAL_RISK_ENGINE = bus.risk
    global_replay_api.GLOBAL_REPLAY_ENGINE = bus.replay

    # Storyboards
    global_storyboard_api.GLOBAL_NODE_REGISTRY = bus.nodes
    global_storyboard_api.GLOBAL_REPLAY_ENGINE = bus.replay
    global_storyboard_api.GLOBAL_CORRELATION_ENGINE = bus.correlation
    global_storyboard_api.GLOBAL_RISK_ENGINE = bus.risk
    global_storyboard_api.GLOBAL_INTEL_ENGINE = bus.intel
    global_storyboard_api.GLOBAL_STORYBOARD_ENGINE = bus.storyboards

    # Archive
    global_archive_api.GLOBAL_ARCHIVE_ENGINE = bus.archive

    # ------------------------------------------------------------
    # Register Blueprints
    # ------------------------------------------------------------
    app.register_blueprint(nodes_api, url_prefix="/api/global/nodes")
    app.register_blueprint(global_intel_api, url_prefix="/api/global/intel")
    app.register_blueprint(federation_api, url_prefix="/api/global/federation")
    app.register_blueprint(global_map_api, url_prefix="/api/global/map")
    app.register_blueprint(global_correlation_api, url_prefix="/api/global/correlation")
    app.register_blueprint(global_risk_api, url_prefix="/api/global/risk")
    app.register_blueprint(global_control_room_api, url_prefix="/api/global/control_room")
    app.register_blueprint(global_replay_api, url_prefix="/api/global/replay")
    app.register_blueprint(global_storyboard_api, url_prefix="/api/global/storyboard")
    app.register_blueprint(global_archive_api, url_prefix="/api/global/archive")

    # ------------------------------------------------------------
    # Root Endpoint
    # ------------------------------------------------------------
    @app.route("/")
    def root():
        return {
            "status": "global-intelligence-online",
            "subsystems": bus.snapshot()
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
