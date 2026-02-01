import time
from datetime import datetime

class GlobalControlRoomEngine:
    """
    Fuses all global intelligence subsystems into a single
    operator-ready situational awareness snapshot.
    """

    def __init__(self, nodes, federation_engine, intel_engine, correlation_engine, risk_engine):
        self.nodes = nodes
        self.fed = federation_engine
        self.intel = intel_engine
        self.corr = correlation_engine
        self.risk = risk_engine

    # ------------------------------------------------------------
    # Node Summary
    # ------------------------------------------------------------
    def node_summary(self):
        summary = []
        for node_id, node in self.nodes.items():
            summary.append({
                "node_id": node_id,
                "health": node.health(),
                "drift": node.drift(),
                "confidence": node.confidence(),
                "anomalies": node.anomalies(),
                "interference": node.interference()
            })
        return summary

    # ------------------------------------------------------------
    # Federation Summary
    # ------------------------------------------------------------
    def federation_summary(self):
        return {
            "status": self.fed.federation_status(),
            "topology": self.fed.topology(),
            "sync": self.fed.sync_status()
        }

    # ------------------------------------------------------------
    # Intel Summary
    # ------------------------------------------------------------
    def intel_summary(self):
        snapshot = self.intel.snapshot()
        return {
            "recent_events": snapshot.get("recent_events", []),
            "high_impact": snapshot.get("high_impact", []),
            "constellation_activity": snapshot.get("constellation_activity", {})
        }

    # ------------------------------------------------------------
    # Correlation Summary
    # ------------------------------------------------------------
    def correlation_summary(self):
        snap = self.corr.snapshot()
        return {
            "clusters": snap.get("clusters", []),
            "major_events": snap.get("major_events", []),
            "count": snap.get("count", 0)
        }

    # ------------------------------------------------------------
    # Risk Summary
    # ------------------------------------------------------------
    def risk_summary(self):
        return self.risk.snapshot()

    # ------------------------------------------------------------
    # Global Alerts
    # ------------------------------------------------------------
    def global_alerts(self):
        alerts = []

        # Node-level alerts
        for node_id, node in self.nodes.items():
            conf = node.confidence().get("score", 1)
            if conf < 0.75:
                alerts.append({
                    "type": "node_confidence_low",
                    "node_id": node_id,
                    "severity": "warning" if conf > 0.6 else "critical",
                    "value": conf
                })

            if node.anomalies():
                alerts.append({
                    "type": "node_anomaly_detected",
                    "node_id": node_id,
                    "severity": "warning",
                    "count": len(node.anomalies())
                })

            if node.interference():
                alerts.append({
                    "type": "interference_detected",
                    "node_id": node_id,
                    "severity": "critical",
                    "details": node.interference()
                })

        # Global risk alerts
        global_risk = self.risk.global_risk()
        if global_risk > 0.7:
            alerts.append({
                "type": "global_risk_high",
                "severity": "critical",
                "value": global_risk
            })
        elif global_risk > 0.5:
            alerts.append({
                "type": "global_risk_elevated",
                "severity": "warning",
                "value": global_risk
            })

        return alerts

    # ------------------------------------------------------------
    # Full Snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        return {
            "timestamp": time.time(),
            "nodes": self.node_summary(),
            "federation": self.federation_summary(),
            "intel": self.intel_summary(),
            "correlation": self.correlation_summary(),
            "risk": self.risk_summary(),
            "alerts": self.global_alerts()
        }
