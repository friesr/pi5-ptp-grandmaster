import numpy as np

def compute_constellation_performance(history):
    """
    history: list of daily summaries
    Each summary contains:
      - per_constellation: {
            "GPS": {...},
            "GAL": {...},
            "BDS": {...},
            "GLO": {...}
        }
    """

    constellations = ["GPS", "GAL", "BDS", "GLO"]
    results = {}

    for c in constellations:
        snr_vals = []
        mp_vals = []
        geom_vals = []
        avail_vals = []
        drift_vals = []
        timing_corr_vals = []

        for day in history:
            if c not in day["per_constellation"]:
                continue

            d = day["per_constellation"][c]

            snr_vals.append(d["avg_snr"])
            mp_vals.append(d["avg_multipath"])
            geom_vals.append(d["geometry_score"])
            avail_vals.append(d["availability_pct"])
            drift_vals.append(d["snr_drift"])
            timing_corr_vals.append(d["timing_correlation"])

        if not snr_vals:
            continue

        # Compute metrics
        results[c] = {
            "avg_snr": float(np.mean(snr_vals)),
            "avg_multipath": float(np.mean(mp_vals)),
            "avg_geometry": float(np.mean(geom_vals)),
            "avg_availability": float(np.mean(avail_vals)),
            "avg_drift": float(np.mean(drift_vals)),
            "avg_timing_correlation": float(np.mean(timing_corr_vals))
        }

        # Compute a unified health score (0–100)
        score = 100
        score -= max(0, 30 - results[c]["avg_snr"]) * 1.0
        score -= results[c]["avg_multipath"] * 20
        score -= max(0, 80 - results[c]["avg_availability"]) * 0.5
        score -= abs(results[c]["avg_drift"]) * 10
        score -= abs(results[c]["avg_timing_correlation"]) * 5

        results[c]["health_score"] = max(0, min(100, score))

    return results
