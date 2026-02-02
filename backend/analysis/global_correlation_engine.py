import time
from datetime import datetime, timedelta
from collections import defaultdict

class GlobalCorrelationEngine:
    """
    Performs cross-node event correlation:
      - temporal clustering
      - spatial clustering
      - constellation grouping
      - root-cause hypothesis
    """

    def __init__(self, nodes, intel_engine):
        self.nodes = nodes
        self.intel = intel_engine

    # ------------------------------------------------------------
    # Temporal Clustering
    # ------------------------------------------------------------
    def cluster_temporal(self, events, window_sec=30):
        """
        Groups events that occur within a time window.
        """
        if not events:
            return []

        events = sorted(events, key=lambda e: e["timestamp"])
        clusters = []
        current = [events[0]]

        for e in events[1:]:
            if e["timestamp"] - current[-1]["timestamp"] <= window_sec:
                current.append(e)
            else:
                clusters.append(current)
                current = [e]

        clusters.append(current)
        return clusters

    # ------------------------------------------------------------
    # Spatial Clustering (regional cluster heuristic)
    # ------------------------------------------------------------
    def cluster_spatial(self, clusters):
        """
        Groups clusters by node proximity.
        In a regional cluster, all nodes are considered "nearby".
        """
        # For now, spatial clustering = identity
        return clusters

    # ------------------------------------------------------------
    # Constellation Grouping
    # ------------------------------------------------------------
    def group_by_constellation(self, cluster):
        groups = defaultdict(list)
        for e in cluster:
            c = e.get("constellation", "Unknown")
            groups[c].append(e)
        return groups

    # ------------------------------------------------------------
    # Root Cause Hypothesis
    # ------------------------------------------------------------
    def infer_root_cause(self, cluster):
        """
        Simple heuristic:
          - If interference events present → interference
          - If drift spikes present → oscillator
          - If constellation events dominate → GNSS issue
        """
        types = [e["event_type"] for e in cluster]

        if any("interference" in t for t in types):
            return "Interference Event"

        if any("drift" in t for t in types):
            return "Oscillator Drift"

        constellations = [e.get("constellation") for e in cluster if e.get("constellation")]
        if constellations:
            return f"Constellation Issue ({max(set(constellations), key=constellations.count)})"

        return "Unknown"

    # ------------------------------------------------------------
    # Severity Aggregation
    # ------------------------------------------------------------
    def aggregate_severity(self, cluster):
        sev_map = {"info": 1, "minor": 2, "major": 3}
        scores = [sev_map.get(e["severity"], 1) for e in cluster]
        avg = sum(scores) / len(scores)
        if avg >= 2.5:
            return "major"
        if avg >= 1.5:
            return "minor"
        return "info"

    # ------------------------------------------------------------
    # Full Correlation Pipeline
    # ------------------------------------------------------------
    def correlate(self):
        # Step 1: get recent global events
        events = self.intel.recent_events(300)

        # Step 2: temporal clustering
        temporal_clusters = self.cluster_temporal(events)

        # Step 3: spatial clustering (regional cluster = identity)
        spatial_clusters = self.cluster_spatial(temporal_clusters)

        # Step 4: build correlation objects
        correlated = []
        for cluster in spatial_clusters:
            constellations = self.group_by_constellation(cluster)
            root = self.infer_root_cause(cluster)
            severity = self.aggregate_severity(cluster)

            correlated.append({
                "start": cluster[0]["timestamp"],
                "end": cluster[-1]["timestamp"],
                "duration_sec": cluster[-1]["timestamp"] - cluster[0]["timestamp"],
                "events": cluster,
                "constellation_groups": constellations,
                "root_cause": root,
                "severity": severity
            })

        return correlated

    # ------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        corr = self.correlate()
        return {
            "clusters": corr,
            "count": len(corr),
            "major_events": [c for c in corr if c["severity"] == "major"]
        }
