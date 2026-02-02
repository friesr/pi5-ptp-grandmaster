"""
Global Intelligence Bus
-----------------------

This module wires together all global intelligence engines:

  - Node Registry
  - Federation Engine
  - Global Intel Engine
  - Global Correlation Engine
  - Global Risk Engine
  - Global Control Room Engine
  - Global Replay Engine
  - Global Storyboard Engine
  - Global Archive Engine

It provides a single integration object that app.py can import
and use to initialize all global APIs cleanly.
"""
from backend.analysis.global_nodes import GlobalNode, GlobalNodeRegistry
#from backend.analysis.node_model import NodeModel
from backend.analysis.federation_engine import FederationEngine
from backend.analysis.global_intel_engine import GlobalIntelEngine
from backend.analysis.global_correlation_engine import GlobalCorrelationEngine
from backend.analysis.global_risk_engine import GlobalRiskEngine
from backend.analysis.global_control_room_engine import GlobalControlRoomEngine
from backend.analysis.global_replay_engine import GlobalReplayEngine
from backend.analysis.global_storyboard_engine import GlobalStoryboardEngine
from backend.analysis.global_archive_engine import GlobalArchiveEngine

class GlobalIntelBus:
    def __init__(self):
        # Registry of all global nodes
        self.nodes = {
            "obs-real-01": GlobalNode("obs-real-01", 35.2828, -90.1936, is_real=True),
            "obs-sim-01": GlobalNode("obs-sim-01", 35.2828, -90.1936),
            "obs-sim-02": GlobalNode("obs-sim-02", 35.2828, -90.1936),
            "obs-sim-03": GlobalNode("obs-sim-03", 35.2828, -90.1936),
        }
        # ------------------------------------------------------------
        # Engines
        # ------------------------------------------------------------
        self.federation = FederationEngine(self.nodes)
        self.intel = GlobalIntelEngine(self.nodes)
        self.correlation = GlobalCorrelationEngine(self.nodes, self.intel)
        self.risk = GlobalRiskEngine(self.nodes, self.intel, self.correlation)
        self.control_room = GlobalControlRoomEngine(
            self.nodes,
            self.federation,
            self.intel,
            self.correlation,
            self.risk
        )
        self.replay = GlobalReplayEngine(
            self.nodes,
            self.intel,
            self.correlation,
            self.risk
        )
        self.storyboards = GlobalStoryboardEngine(
            self.nodes,
            self.replay,
            self.correlation,
            self.risk,
            self.intel
        )
        self.archive = GlobalArchiveEngine()

    # ------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        return {
            "nodes": list(self.nodes.keys()),
            "federation": "ready",
            "intel": "ready",
            "correlation": "ready",
            "risk": "ready",
            "control_room": "ready",
            "replay": "ready",
            "storyboards": "ready",
            "archive": "ready"
        }
