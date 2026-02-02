import numpy as np

def build_prn_fingerprints(history):
    """
    history: list of daily summaries
    Each summary contains per-PRN metrics:
      - prn_stats: {
            "G01": {...},
            "G02": {...},
            ...
        }
    """

    prn_data = {}

    # Aggregate per-PRN metrics across all days
    for day in history:
        stats = day.get("prn_stats", {})
        for prn, s in stats.items():
            if prn not in prn_data:
                prn_data[prn] = {
                    "snr": [],
                    "multipath": [],
                    "geometry": [],
                    "timing_corr": [],
                    "health": [],
                    "anomaly_count": 0
                }

            prn_data[prn]["snr"].append(s["avg_snr"])
            prn_data[prn]["multipath"].append(s["avg_multipath"])
            prn_data[prn]["geometry"].append(s["geometry_contrib"])
            prn_data[prn]["timing_corr"].append(s["timing_correlation"])
            prn_data[prn]["health"].append(s["health_score"])
            prn_data[prn]["anomaly_count"] += s.get("anomaly_count", 0)

    # Build fingerprints
    fingerprints = {}

    for prn, d in prn_data.items():
        snr_avg = float(np.mean(d["snr"]))
        snr_var = float(np.var(d["snr"]))
        mp_avg = float(np.mean(d["multipath"]))
        geom_avg = float(np.mean(d["geometry"]))
        timing_corr = float(np.mean(d["timing_corr"]))
        health_avg = float(np.mean(d["health"]))
        anomalies = d["anomaly_count"]

        # Unified fingerprint score
        score = 100
        score -= max(0, 30 - snr_avg) * 1.0
        score -= snr_var * 2
        score -= mp_avg * 20
        score -= abs(timing_corr) * 10
        score -= anomalies * 0.5
        score += (geom_avg - 50) * 0.1
        score += (health_avg - 80) * 0.2

        score = max(0, min(100, score))

        fingerprints[prn] = {
            "snr_avg": snr_avg,
            "snr_var": snr_var,
            "multipath_avg": mp_avg,
            "geometry_avg": geom_avg,
            "timing_correlation": timing_corr,
            "health_avg": health_avg,
            "anomaly_count": anomalies,
            "fingerprint_score": score
        }

    return fingerprints
