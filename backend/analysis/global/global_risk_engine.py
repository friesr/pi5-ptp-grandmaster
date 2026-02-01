import time
from datetime import datetime, timedelta
from statistics import mean

class GlobalRiskEngine:
    """
    Computes global timing risk:
      - node-level risk
      - constellation-level risk
      - global risk score
      - forecast windows
      - propagation modeling
    """

    def __init__(self, nodes, intel_engine, correlation_engine):
        self.nodes = nodes
        self.intel = intel_engine
        self.corr = correlation_engine

    # ------------------------------------------------------------
    # Node-Level Risk
    # ------------------------------------------------------------
    def node_risk(self, node):
        """
        Computes a risk score for a single node based on:
          - drift
          - confidence
          - anomalies
          - interference
        """
        drift = node.drift().get("drift_ppb", 0)
        conf = node.confidence().get("score", 1)
        anomalies = len(node.anomalies())
        interference = len(node.interference())

        # Normalize components
        drift_risk = min(abs(drift) / 5.0, 1.0)
        conf_risk = 1.0 - conf
        anomaly_risk = min(anomalies * 0.2, 1.0)
        interference_risk = min(interference * 0.3, 1.0)

        # Weighted sum
        score = (
            0.35 * drift_risk +
            0.35 * conf_risk +
            0.20 * anomaly_risk +
            0.10 * interference_risk
        )

        return {
            "node_id": node.node_id,
            "score": round(score, 3),
            "components": {
                "drift": drift_risk,
                "confidence": conf_risk,
                "anomalies": anomaly_risk,
                "interference": interference_risk
            }
        }

    # ------------------------------------------------------------
    # Constellation-Level Risk
    # ------------------------------------------------------------
    def constellation_risk(self):
        """
        Computes risk per constellation based on correlated events.
        """
        clusters = self.corr.correlate()
        constellations = {}

        for c in clusters:
            for const, events in c["constellation_groups"].items():
                if const not in constellations:
                    constellations[const] = []
                constellations[const].append(c["severity"])

        # Convert severity → numeric
        sev_map = {"info": 1, "minor": 2, "major": 3}

        result = {}
        for const, severities in constellations.items():
            numeric = [sev_map.get(s, 1) for s in severities]
            avg = mean(numeric)
            result[const] = round(avg / 3.0, 3)  # normalize to 0–1

        return result

    # ------------------------------------------------------------
    # Global Risk Score
    # ------------------------------------------------------------
    def global_risk(self):
        """
        Combines:
          - node-level risk
          - constellation-level risk
          - recent high-impact events
        """
        node_scores = [self.node_risk(n)["score"] for n in self.nodes.values()]
        const_scores = list(self.constellation_risk().values())
        high_impact = len(self.intel.events_with_timing_impact("high", 50))

        node_component = mean(node_scores) if node_scores else 0
        const_component = mean(const_scores) if const_scores else 0
        high_impact_component = min(high_impact * 0.05, 1.0)

        score = (
            0.5 * node_component +
            0.3 * const_component +
            0.2 * high_impact_component
        )

        return round(score, 3)

    # ------------------------------------------------------------
    # Forecast Window
    # ------------------------------------------------------------
    def forecast(self, hours=6):
        """
        Simple forecast:
          - extrapolate current risk
          - add correlation-based adjustments
        """
        base = self.global_risk()
        clusters = self.corr.correlate()

        # If major clusters exist, risk increases
        major = len([c for c in clusters if c["severity"] == "major"])
        adjustment = min(major * 0.1, 0.4)

        forecast = min(base + adjustment, 1.0)

        return {
            "current": base,
            "forecast": round(forecast, 3),
            "window_hours": hours,
            "major_clusters": major
        }

    # ------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        return {
            "node_risk": {n.node_id: self.node_risk(n) for n in self.nodes.values()},
            "constellation_risk": self.constellation_risk(),
            "global_risk": self.global_risk(),
            "forecast": self.forecast()
        }
