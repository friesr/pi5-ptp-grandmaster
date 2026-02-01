import os
import json
import random
import time
from datetime import datetime, timedelta

DATA_ROOT = "/opt/ptp-data"

class NodeModel:
    """
    Represents a single observatory node (real or synthetic).
    Provides:
      - health
      - drift
      - confidence
      - anomalies
      - interference
      - unified timeline
      - metadata
    """

    def __init__(self, node_id, is_real=False, region="NA", synthetic_profile=None):
        self.node_id = node_id
        self.is_real = is_real
        self.region = region
        self.synthetic_profile = synthetic_profile or {}
        self.last_update = time.time()

    # ------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------
    def metadata(self):
        return {
            "node_id": self.node_id,
            "is_real": self.is_real,
            "region": self.region,
            "synthetic": not self.is_real,
            "last_update": self.last_update
        }

    # ------------------------------------------------------------
    # Real Node Data Loaders
    # ------------------------------------------------------------
    def _load_json(self, path):
        if os.path.exists(path):
            try:
                return json.load(open(path))
            except:
                return []
        return []

    def _real_path(self, name):
        return os.path.join(DATA_ROOT, name)

    def load_real_health(self):
        return self._load_json(self._real_path("system_health.json"))

    def load_real_drift(self):
        return self._load_json(self._real_path("drift.json"))

    def load_real_confidence(self):
        return self._load_json(self._real_path("timing_confidence.json"))

    def load_real_anomalies(self):
        return self._load_json(self._real_path("anomaly_clusters.json"))

    def load_real_interference(self):
        return self._load_json(self._real_path("interference.json"))

    def load_real_timeline(self):
        return self._load_json(self._real_path("unified_timeline.json"))

    # ------------------------------------------------------------
    # Synthetic Node Generators
    # ------------------------------------------------------------
    def _synthetic_value(self, base, jitter):
        return base + random.uniform(-jitter, jitter)

    def synthetic_health(self):
        return {
            "status": "ok",
            "cpu": self._synthetic_value(22, 5),
            "mem": self._synthetic_value(31, 4),
            "temp": self._synthetic_value(42, 3),
            "uptime_hours": random.randint(100, 500)
        }

    def synthetic_drift(self):
        base = self.synthetic_profile.get("drift_ppb", 1.2)
        jitter = self.synthetic_profile.get("drift_jitter", 0.3)
        return {
            "drift_ppb": self._synthetic_value(base, jitter),
            "trend": random.choice(["stable", "warming", "cooling"])
        }

    def synthetic_confidence(self):
        return {
            "score": self._synthetic_value(0.92, 0.05),
            "status": random.choice(["green", "yellow"])
        }

    def synthetic_anomalies(self):
        if random.random() < 0.1:
            return [{
                "timestamp": time.time(),
                "type": random.choice(["drift_spike", "interference", "geometry"]),
                "severity": random.choice(["minor", "major"])
            }]
        return []

    def synthetic_interference(self):
        if random.random() < 0.05:
            return [{
                "timestamp": time.time(),
                "band": random.choice(["L1", "L2", "L5"]),
                "power": self._synthetic_value(-92, 3)
            }]
        return []

    def synthetic_timeline(self):
        now = datetime.utcnow()
        return [{
            "timestamp": (now - timedelta(minutes=i)).isoformat(),
            "event": random.choice(["drift", "confidence", "tracking", "idle"])
        } for i in range(30)]

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------
    def health(self):
        return self.load_real_health() if self.is_real else self.synthetic_health()

    def drift(self):
        return self.load_real_drift() if self.is_real else self.synthetic_drift()

    def confidence(self):
        return self.load_real_confidence() if self.is_real else self.synthetic_confidence()

    def anomalies(self):
        return self.load_real_anomalies() if self.is_real else self.synthetic_anomalies()

    def interference(self):
        return self.load_real_interference() if self.is_real else self.synthetic_interference()

    def timeline(self):
        return self.load_real_timeline() if self.is_real else self.synthetic_timeline()
