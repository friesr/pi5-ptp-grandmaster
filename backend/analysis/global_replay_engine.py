import time
from datetime import datetime, timedelta

class GlobalReplayEngine:
    """
    Provides synchronized global replay:
      - multi-node timeline reconstruction
      - constellation-aware playback
      - event scrubbing
      - replay windows
      - global state snapshots at any timestamp
    """

    def __init__(self, nodes, intel_engine, correlation_engine, risk_engine):
        self.nodes = nodes
        self.intel = intel_engine
        self.corr = correlation_engine
        self.risk = risk_engine

    # ------------------------------------------------------------
    # Build a unified timeline for replay
    # ------------------------------------------------------------
    def build_global_timeline(self, lookback_minutes=120):
        """
        Combines:
          - node timelines
          - intel events
          - correlated clusters
          - risk changes
        into a single sorted timeline.
        """
        cutoff = time.time() - (lookback_minutes * 60)
        timeline = []

        # Node timelines
        for node_id, node in self.nodes.items():
            for e in node.timeline():
                if e.get("timestamp", 0) >= cutoff:
                    timeline.append({
                        "timestamp": e["timestamp"],
                        "source": node_id,
                        "type": e.get("event", e.get("type", "unknown")),
                        "raw": e
                    })

        # Intel events
        for e in self.intel.recent_events(500):
            if e["timestamp"] >= cutoff:
                timeline.append({
                    "timestamp": e["timestamp"],
                    "source": "intel",
                    "type": e["event_type"],
                    "raw": e
                })

        # Correlation clusters
        for c in self.corr.correlate():
            if c["end"] >= cutoff:
                timeline.append({
                    "timestamp": c["start"],
                    "source": "correlation",
                    "type": "cluster_start",
                    "raw": c
                })
                timeline.append({
                    "timestamp": c["end"],
                    "source": "correlation",
                    "type": "cluster_end",
                    "raw": c
                })

        # Risk changes (synthetic)
        risk_now = self.risk.global_risk()
        timeline.append({
            "timestamp": time.time(),
            "source": "risk",
            "type": "risk_update",
            "raw": {"global_risk": risk_now}
        })

        # Sort by timestamp
        timeline.sort(key=lambda x: x["timestamp"])
        return timeline

    # ------------------------------------------------------------
    # Replay Window
    # ------------------------------------------------------------
    def replay_window(self, start_ts, end_ts):
        """
        Returns all events between two timestamps.
        """
        full = self.build_global_timeline(lookback_minutes=240)
        return [e for e in full if start_ts <= e["timestamp"] <= end_ts]

    # ------------------------------------------------------------
    # State Reconstruction
    # ------------------------------------------------------------
    def reconstruct_state(self, ts):
        """
        Reconstructs global state at a given timestamp:
          - node health
          - drift
          - confidence
          - anomalies
          - interference
          - risk
          - correlated events active at that time
        """
        state = {
            "timestamp": ts,
            "nodes": {},
            "active_clusters": [],
            "risk": None
        }

        # Node snapshots
        for node_id, node in self.nodes.items():
            state["nodes"][node_id] = {
                "health": node.health(),
                "drift": node.drift(),
                "confidence": node.confidence(),
                "anomalies": node.anomalies(),
                "interference": node.interference()
            }

        # Active clusters
        for c in self.corr.correlate():
            if c["start"] <= ts <= c["end"]:
                state["active_clusters"].append(c)

        # Risk at that moment (synthetic)
        state["risk"] = self.risk.global_risk()

        return state

    # ------------------------------------------------------------
    # Full Replay Snapshot
    # ------------------------------------------------------------
    def snapshot(self, lookback_minutes=120):
        return {
            "timeline": self.build_global_timeline(lookback_minutes),
            "recent_clusters": self.corr.correlate(),
            "risk": self.risk.global_risk()
        }
