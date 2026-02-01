# ------------------------------------------------------------
# Global Intelligence Bus
# ------------------------------------------------------------
# This module unifies all global engines into a single
# integration layer. The bus exposes:
#
#   - Node Registry
#   - Global Intel Engine
#   - Global Correlation Engine
#   - Global Risk Engine
#   - Global Federation Engine
#   - Global Replay Engine
#   - Global Storyboard Engine
#   - Global Archive Engine
#   - Global Control Room Engine
#
# Every global API endpoint receives its engine references
# from this bus during app initialization.
# ------------------------------------------------------------

from backend.analysis.global_nodes import GlobalNodeRegistry
from backend.analysis.global_intel_engine import GlobalIntelEngine
from backend.analysis.global_correlation_engine import GlobalCorrelationEngine
from backend.analysis.global_risk_engine import GlobalRiskEngine
from backend.analysis.global_federation_engine import GlobalFederationEngine
from backend.analysis.global_replay_engine import GlobalReplayEngine
from backend.analysis.global_storyboard_engine import GlobalStoryboardEngine
from backend.analysis.global_archive_engine import GlobalArchiveEngine
from backend.analysis.global_control_room_engine import GlobalControlRoomEngine


class GlobalIntelBus:
    """
    The Global Intelligence Bus is the central integration layer
    that wires together all global engines and exposes them as a
    unified interface for the global API layer.
    """

    def __init__(self):
        # ------------------------------------------------------------
        # Core registries
        # ------------------------------------------------------------
        self.nodes = GlobalNodeRegistry()

        # ------------------------------------------------------------
        # Core engines
        # ------------------------------------------------------------
        self.intel = GlobalIntelEngine(node_registry=self.nodes)
        self.correlation = GlobalCorrelationEngine(node_registry=self.nodes,
                                                   intel_engine=self.intel)
        self.risk = GlobalRiskEngine(node_registry=self.nodes,
                                     intel_engine=self.intel,
                                     correlation_engine=self.correlation)
        self.federation = GlobalFederationEngine(node_registry=self.nodes,
                                                 intel_engine=self.intel)
        self.replay = GlobalReplayEngine(node_registry=self.nodes,
                                         intel_engine=self.intel,
                                         correlation_engine=self.correlation,
                                         risk_engine=self.risk)
        self.storyboards = GlobalStoryboardEngine(replay_engine=self.replay,
                                                  intel_engine=self.intel,
                                                  correlation_engine=self.correlation,
                                                  risk_engine=self.risk)
        self.archive = GlobalArchiveEngine(node_registry=self.nodes,
                                           intel_engine=self.intel,
                                           correlation_engine=self.correlation,
                                           risk_engine=self.risk)
        self.control_room = GlobalControlRoomEngine(node_registry=self.nodes,
                                                    intel_engine=self.intel,
                                                    correlation_engine=self.correlation,
                                                    risk_engine=self.risk,
                                                    federation_engine=self.federation)

    # ------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------

    def summary(self):
        """
        Returns a high‑level summary of the global intelligence system.
        """
        return {
            "nodes": self.nodes.count(),
            "intel_events": self.intel.event_count(),
            "correlations": self.correlation.count(),
            "risk_events": self.risk.count(),
            "federation_links": self.federation.count(),
            "replay_sessions": self.replay.count(),
            "storyboards": self.storyboards.count(),
            "archive_items": self.archive.count(),
        }
