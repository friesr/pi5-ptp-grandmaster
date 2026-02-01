# ------------------------------------------------------------
# Global Node Registry
# ------------------------------------------------------------
# This module manages all global observatory nodes (real or
# synthetic). It provides:
#
#   - Node creation and registration
#   - Node lookup and updates
#   - Health, drift, confidence, anomalies
#   - Snapshots for UI and API layers
#   - Summary statistics for the GlobalIntelBus
#
# The GlobalIntelBus depends on this registry as the root
# source of truth for all global intelligence engines.
# ------------------------------------------------------------

import time
import uuid
from dataclasses import dataclass, field


# ------------------------------------------------------------
# Node Model
# ------------------------------------------------------------
@dataclass
class GlobalNode:
    node_id: str
    name: str
    latitude: float
    longitude: float

    # Timing + health metrics
    drift_ns: float = 0.0
    confidence: float = 1.0
    health: str = "healthy"
    anomalies: list = field(default_factory=list)

    # Metadata
    created_at: float = field(default_factory=lambda: time.time())
    updated_at: float = field(default_factory=lambda: time.time())

    def snapshot(self):
        """Return a JSON‑safe snapshot of the node."""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "lat": self.latitude,
            "lon": self.longitude,
            "drift_ns": self.drift_ns,
            "confidence": self.confidence,
            "health": self.health,
            "anomalies": list(self.anomalies),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ------------------------------------------------------------
# Node Registry
# ------------------------------------------------------------
class GlobalNodeRegistry:
    """
    Central registry for all global observatory nodes.
    Provides CRUD operations, snapshots, and summary metrics.
    """

    def __init__(self):
        self.nodes = {}

        # ------------------------------------------------------------
        # Optional: initialize with a few synthetic nodes
        # ------------------------------------------------------------
        self._init_synthetic_nodes()

    # ------------------------------------------------------------
    # Synthetic Node Initialization
    # ------------------------------------------------------------
    def _init_synthetic_nodes(self):
        """Create a few default synthetic nodes for Phase 1."""
        self.add_node(
            name="Synthetic‑US‑West",
            latitude=37.7749,
            longitude=-122.4194,
            drift_ns=12.5,
            confidence=0.98,
        )

        self.add_node(
            name="Synthetic‑EU‑Central",
            latitude=50.1109,
            longitude=8.6821,
            drift_ns=4.2,
            confidence=0.99,
        )

        self.add_node(
            name="Synthetic‑Asia‑East",
            latitude=35.6895,
            longitude=139.6917,
            drift_ns=22.1,
            confidence=0.96,
        )

    # ------------------------------------------------------------
    # CRUD Operations
    # ------------------------------------------------------------
    def add_node(self, name, latitude, longitude, drift_ns=0.0, confidence=1.0):
        node_id = str(uuid.uuid4())
        node = GlobalNode(
            node_id=node_id,
            name=name,
            latitude=latitude,
            longitude=longitude,
            drift_ns=drift_ns,
            confidence=confidence,
        )
        self.nodes[node_id] = node
        return node

    def remove_node(self, node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]
            return True
        return False

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def update_node(self, node_id, **kwargs):
        node = self.nodes.get(node_id)
        if not node:
            return None

        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)

        node.updated_at = time.time()
        return node

    # ------------------------------------------------------------
    # Metrics + Summaries
    # ------------------------------------------------------------
    def count(self):
        return len(self.nodes)

    def summary(self):
        """Return high‑level metrics for the GlobalIntelBus."""
        return {
            "total_nodes": len(self.nodes),
            "healthy": sum(1 for n in self.nodes.values() if n.health == "healthy"),
            "degraded": sum(1 for n in self.nodes.values() if n.health == "degraded"),
            "faulted": sum(1 for n in self.nodes.values() if n.health == "faulted"),
        }

    # ------------------------------------------------------------
    # Snapshots
    # ------------------------------------------------------------
    def snapshot(self):
        """Return a list of node snapshots for UI/API layers."""
        return [node.snapshot() for node in self.nodes.values()]
