# backend/analysis/timing_engine.py

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import math
import time


@dataclass
class TimingSourceSample:
    timestamp: float          # when this sample was recorded (epoch seconds)
    offset_ns: float          # local clock offset vs this source (nanoseconds)
    jitter_ns: float          # short-term variation (nanoseconds)
    quality: float            # 0.0–1.0 confidence in this source


class TimingEngine:
    """
    Real timing engine scaffold.

    This is designed to eventually ingest real GNSS/PTP/NTP/system/servo samples.
    For now, it provides a structurally correct, observable timing snapshot that
    the frontend can consume immediately, while leaving clear hooks for wiring in
    real sampler data.
    """

    def __init__(self) -> None:
        # Latest samples from each source (to be wired to samplers/logging later)
        self.gnss: Optional[TimingSourceSample] = None
        self.ptp: Optional[TimingSourceSample] = None
        self.ntp: Optional[TimingSourceSample] = None
        self.system: Optional[TimingSourceSample] = None
        self.servo: Optional[TimingSourceSample] = None

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    def snapshot(self) -> Dict[str, Any]:
        """
        Return a timing snapshot suitable for the frontend Home page.

        Fields:
          - time_now: ISO8601 UTC timestamp
          - uncertainty_95_ns: 95% confidence bound on time error (nanoseconds)
          - reliability_95: 0.0–1.0 confidence in the timing solution
          - clock_class: string summary of quality (G, A, B, C, D, X, etc.)
          - clock_accuracy: rough accuracy bucket (nanoseconds)
          - clock_variance: normalized variance metric (0–1)
        """

        now = datetime.now(timezone.utc)

        # For now, we derive a synthetic but consistent solution based on
        # available sources. As you wire in real sampler data, this logic
        # will start reflecting actual observatory behavior.

        best = self._select_best_source()
        if best is None:
            # No sources yet: degrade gracefully but still give the UI something.
            return {
                "time_now": now.isoformat(),
                "uncertainty_95_ns": None,
                "reliability_95": 0.0,
                "clock_class": "X",          # Unknown
                "clock_accuracy": None,
                "clock_variance": None,
            }

        # Compute uncertainty from jitter + age of sample
        age_sec = max(0.0, time.time() - best.timestamp)
        base_uncertainty = abs(best.jitter_ns)
        age_penalty = age_sec * 1e3  # 1 µs per second of staleness
        uncertainty_95_ns = base_uncertainty + age_penalty

        # Reliability is a function of source quality and freshness
        reliability = max(0.0, min(1.0, best.quality * math.exp(-age_sec / 60.0)))

        clock_class = self._class_from_uncertainty(uncertainty_95_ns, reliability)
        clock_accuracy = uncertainty_95_ns
        clock_variance = self._variance_metric(best)

        return {
            "time_now": now.isoformat(),
            "uncertainty_95_ns": uncertainty_95_ns,
            "reliability_95": reliability,
            "clock_class": clock_class,
            "clock_accuracy": clock_accuracy,
            "clock_variance": clock_variance,
        }

    # -------------------------------------------------------------------------
    # Hooks for future sampler integration
    # -------------------------------------------------------------------------
    def update_gnss(self, timestamp: float, offset_ns: float, jitter_ns: float, quality: float) -> None:
        self.gnss = TimingSourceSample(timestamp, offset_ns, jitter_ns, quality)

    def update_ptp(self, timestamp: float, offset_ns: float, jitter_ns: float, quality: float) -> None:
        self.ptp = TimingSourceSample(timestamp, offset_ns, jitter_ns, quality)

    def update_ntp(self, timestamp: float, offset_ns: float, jitter_ns: float, quality: float) -> None:
        self.ntp = TimingSourceSample(timestamp, offset_ns, jitter_ns, quality)

    def update_system(self, timestamp: float, offset_ns: float, jitter_ns: float, quality: float) -> None:
        self.system = TimingSourceSample(timestamp, offset_ns, jitter_ns, quality)

    def update_servo(self, timestamp: float, offset_ns: float, jitter_ns: float, quality: float) -> None:
        self.servo = TimingSourceSample(timestamp, offset_ns, jitter_ns, quality)

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------
    def _select_best_source(self) -> Optional[TimingSourceSample]:
        """
        Simple priority-based source selection:
          GNSS > PTP > NTP > Servo > System
        """
        for src in [self.gnss, self.ptp, self.ntp, self.servo, self.system]:
            if src is not None:
                return src
        return None

    def _class_from_uncertainty(self, uncertainty_ns: float, reliability: float) -> str:
        """
        Map uncertainty + reliability into a simple clock class.
        You can refine these thresholds as your analytics mature.
        """
        if reliability < 0.5:
            return "X"  # Unreliable / degraded

        if uncertainty_ns <= 10:
            return "G"  # GNSS-grade
        if uncertainty_ns <= 100:
            return "A"
        if uncertainty_ns <= 1_000:
            return "B"
        if uncertainty_ns <= 10_000:
            return "C"
        return "D"

    def _variance_metric(self, src: TimingSourceSample) -> float:
        """
        Normalize jitter into a 0–1 variance metric.
        """
        # Assume 10 µs jitter is "bad" (1.0), 0 ns is "perfect" (0.0)
        scale = 10_000.0  # ns
        v = min(1.0, max(0.0, abs(src.jitter_ns) / scale))
        return v
