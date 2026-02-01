import time
import random
from datetime import datetime, timedelta

class GlobalIntelEngine:
    """
    Global intelligence bus:
      - event ingestion
      - event normalization
      - severity tagging
      - constellation tagging
      - timing impact classification
      - global event bus
    """

    def __init__(self, nodes):
        # nodes: dict[node_id] = NodeModel
        self.nodes = nodes
        self.event_bus = []  # global list of normalized events
        self.max_events = 5000

    # ------------------------------------------------------------
    # Event Normalization
    # ------------------------------------------------------------
    def normalize_event(self, node_id, raw):
        """
        Convert raw node events into a unified global format.
        """
        ts = raw.get("timestamp", time.time())

        event_type = raw.get("type", raw.get("event", "unknown"))
        severity = raw.get("severity", "info")

        # constellation tagging (synthetic heuristic)
        constellation = None
        if "gps" in event_type.lower():
            constellation = "GPS"
        elif "galileo" in event_type.lower():
            constellation = "Galileo"
        elif "glonass" in event_type.lower():
            constellation = "GLONASS"
        elif "beidou" in event_type.lower():
            constellation = "BeiDou"

        # timing impact heuristic
        timing_impact = "none"
        if event_type in ["drift_spike", "drift", "servo"]:
            timing_impact = "medium"
        if event_type in ["interference", "spoofing"]:
            timing_impact = "high"

        return {
            "node_id": node_id,
            "timestamp": ts,
            "event_type": event_type,
            "severity": severity,
            "constellation": constellation,
            "timing_impact": timing_impact,
            "raw": raw
        }

    # ------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------
    def ingest_from_node(self, node_id):
        """
        Pulls events from a node's timeline/anomalies/interference.
        """
        node = self.nodes[node_id]

        events = []

        # timeline events
        for e in node.timeline():
            events.append(self.normalize_event(node_id, e))

        # anomalies
        for a in node.anomalies():
            events.append(self.normalize_event(node_id, a))

        # interference
        for i in node.interference():
            events.append(self.normalize_event(node_id, i))

        # add to global bus
        for e in events:
            self.event_bus.append(e)

        # trim bus
        if len(self.event_bus) > self.max_events:
            self.event_bus = self.event_bus[-self.max_events:]

        return {"ingested": len(events)}

    def ingest_all(self):
        total = 0
        for node_id in self.nodes:
            total += self.ingest_from_node(node_id)["ingested"]
        return {"total_ingested": total}

    # ------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------
    def recent_events(self, limit=100):
        return sorted(self.event_bus, key=lambda e: e["timestamp"], reverse=True)[:limit]

    def events_by_node(self, node_id, limit=100):
        filtered = [e for e in self.event_bus if e["node_id"] == node_id]
        return sorted(filtered, key=lambda e: e["timestamp"], reverse=True)[:limit]

    def events_by_severity(self, severity, limit=100):
        filtered = [e for e in self.event_bus if e["severity"] == severity]
        return sorted(filtered, key=lambda e: e["timestamp"], reverse=True)[:limit]

    def events_by_constellation(self, constellation, limit=100):
        filtered = [e for e in self.event_bus if e["constellation"] == constellation]
        return sorted(filtered, key=lambda e: e["timestamp"], reverse=True)[:limit]

    def events_with_timing_impact(self, impact="high", limit=100):
        filtered = [e for e in self.event_bus if e["timing_impact"] == impact]
        return sorted(filtered, key=lambda e: e["timestamp"], reverse=True)[:limit]

    # ------------------------------------------------------------
    # Global Snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        """
        Returns a global intelligence snapshot:
          - recent events
          - high-impact timing events
          - constellation breakdown
        """
        recent = self.recent_events(50)
        high_impact = self.events_with_timing_impact("high", 20)

        constellations = {}
        for e in recent:
            c = e["constellation"]
            if c:
                constellations[c] = constellations.get(c, 0) + 1

        return {
            "recent_events": recent,
            "high_impact": high_impact,
            "constellation_activity": constellations
        }
