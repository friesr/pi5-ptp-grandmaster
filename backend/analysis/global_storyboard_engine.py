import time
from datetime import datetime

class GlobalStoryboardEngine:
    """
    Generates operator-ready storyboards from:
      - replay engine
      - correlation engine
      - risk engine
      - intel engine
      - node state
    """

    def __init__(self, nodes, replay_engine, correlation_engine, risk_engine, intel_engine):
        self.nodes = nodes
        self.replay = replay_engine
        self.corr = correlation_engine
        self.risk = risk_engine
        self.intel = intel_engine

    # ------------------------------------------------------------
    # Build a storyboard for a specific cluster
    # ------------------------------------------------------------
    def storyboard_for_cluster(self, cluster):
        start = cluster["start"]
        end = cluster["end"]

        # Replay window
        window = self.replay.replay_window(start, end)

        # Root cause
        root = cluster["root_cause"]

        # Severity
        severity = cluster["severity"]

        # Constellation groups
        constellations = cluster["constellation_groups"]

        # Node involvement
        nodes = sorted({e["node_id"] for e in cluster["events"]})

        return {
            "start": start,
            "end": end,
            "duration_sec": cluster["duration_sec"],
            "root_cause": root,
            "severity": severity,
            "nodes_involved": nodes,
            "constellations": list(constellations.keys()),
            "timeline": window
        }

    # ------------------------------------------------------------
    # Build storyboards for all major clusters
    # ------------------------------------------------------------
    def major_storyboards(self):
        clusters = self.corr.correlate()
        majors = [c for c in clusters if c["severity"] == "major"]
        return [self.storyboard_for_cluster(c) for c in majors]

    # ------------------------------------------------------------
    # Build a global incident summary
    # ------------------------------------------------------------
    def incident_summary(self):
        clusters = self.corr.correlate()
        if not clusters:
            return {"summary": "No incidents detected"}

        latest = clusters[-1]

        return {
            "summary": f"Incident from {latest['start']} to {latest['end']}",
            "root_cause": latest["root_cause"],
            "severity": latest["severity"],
            "nodes_involved": sorted({e["node_id"] for e in latest["events"]}),
            "constellations": list(latest["constellation_groups"].keys()),
            "duration_sec": latest["duration_sec"]
        }

    # ------------------------------------------------------------
    # Full storyboard snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        clusters = self.corr.correlate()
        majors = [c for c in clusters if c["severity"] == "major"]

        return {
            "timestamp": time.time(),
            "cluster_count": len(clusters),
            "major_count": len(majors),
            "major_storyboards": [self.storyboard_for_cluster(c) for c in majors],
            "latest_incident": self.incident_summary()
        }
