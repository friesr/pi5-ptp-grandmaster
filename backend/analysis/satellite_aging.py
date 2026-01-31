import numpy as np

def compute_trend(values):
    if len(values) < 5:
        return 0.0
    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]
    return float(slope)

def compute_aging(prn_data):
    results = {}

    for prn, d in prn_data.items():
        snr_trend = compute_trend(d["snr"])
        mp_trend = compute_trend(d["multipath"])
        geom_trend = compute_trend(d["geometry"])
        clock_trend = compute_trend(d["clock"])
        anomaly_trend = compute_trend(d["anomalies"])

        # Unified aging score (lower is better)
        score = 100
        score -= snr_trend * -200      # SNR decreasing → bad
        score -= mp_trend * 300        # multipath increasing → bad
        score -= geom_trend * -50      # geometry contribution decreasing → bad
        score -= clock_trend * -100    # clock stability decreasing → bad
        score -= anomaly_trend * 20    # anomalies increasing → bad

        score = max(0, min(100, score))

        results[prn] = {
            "snr_trend": snr_trend,
            "multipath_trend": mp_trend,
            "geometry_trend": geom_trend,
            "clock_trend": clock_trend,
            "anomaly_trend": anomaly_trend,
            "aging_score": score
        }

    return results
