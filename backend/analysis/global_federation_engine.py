# backend/analysis/global_federation_engine.py

from typing import Dict, List, Optional
from backend.analysis.global_nodes import GlobalNode, GlobalNodeRegistry


class GlobalFederationEngine:
    """
    The Federation Engine manages relationships between nodes, clusters,
    and global groups. It provides a unified interface for:
      - registering nodes
      - grouping nodes into federations
      - computing federation-level health
      - broadcasting state changes
      - providing summaries for the API layer
    """

    def __init__(self, registry: Optional[GlobalNodeRegistry] = None):
        self.registry = registry or GlobalNodeRegistry()
        self.federations: Dict[str, List[str]] = {}   # federation_name -> list of node_ids

    # ----------------------------------------------------------------------
    # Federation Management
    # ----------------------------------------------------------------------

    def create_federation(self, name: str) -> bool:
        """Create a new federation if it does not already exist."""
        if name in self.federations:
            return False
        self.federations[name] = []
        return True

    def delete_federation(self, name: str) -> bool:
        """Remove a federation and all node associations."""
        if name not in self.federations:
            return False
        del self.federations[name]
        return True

    def add_node_to_federation(self, federation: str, node_id: str) -> bool:
        """Add a node to a federation."""
        if federation not in self.federations:
            return False
        if not self.registry.has_node(node_id):
            return False
        if node_id not in self.federations[federation]:
            self.federations[federation].append(node_id)
        return True

    def remove_node_from_federation(self, federation: str, node_id: str) -> bool:
        """Remove a node from a federation."""
        if federation not in self.federations:
            return False
        if node_id in self.federations[federation]:
            self.federations[federation].remove(node_id)
        return True

    # ----------------------------------------------------------------------
    # Federation Analytics
    # ----------------------------------------------------------------------

    def federation_health(self, federation: str) -> Optional[float]:
        """
        Compute a simple federation health score based on node health.
        Returns None if federation does not exist.
        """
        if federation not in self.federations:
            return None

        node_ids = self.federations[federation]
        if not node_ids:
            return 1.0  # empty federation = neutral/healthy

        health_values = []
        for node_id in node_ids:
            node = self.registry.get_node(node_id)
            if node:
                health_values.append(node.health_score)

        if not health_values:
            return 0.0

        return sum(health_values) / len(health_values)

    def federation_summary(self, federation: str) -> Optional[dict]:
        """Return a structured summary for API responses."""
        if federation not in self.federations:
            return None

        node_ids = self.federations[federation]
        nodes = [self.registry.get_node(n) for n in node_ids if self.registry.get_node(n)]

        return {
            "federation": federation,
            "node_count": len(nodes),
            "nodes": [n.to_dict() for n in nodes],
            "health": self.federation_health(federation),
        }

    # ----------------------------------------------------------------------
    # Global Summary
    # ----------------------------------------------------------------------

    def all_federations(self) -> dict:
        """Return a summary of all federations."""
        return {
            name: self.federation_summary(name)
            for name in self.federations
        }
