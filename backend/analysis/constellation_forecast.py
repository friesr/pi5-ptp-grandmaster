import numpy as np

def forecast_next(values):
    if len(values) < 5:
        return values[-1] if values else 0.0
    x = np.arange(len(values))
    slope, intercept = np.polyfit(x, values, 1)
    return float(intercept + slope * (len(values)))

def forecast_constellations(data):
    results = {}

    for c, d in data.items():
        snr_f = forecast_next(d["snr"])
        mp_f = forecast_next(d["multipath"])
        geom_f = forecast_next(d["geometry"])
        tc_f = forecast_next(d["timing_corr"])

        # Unified forecast score
        score = 100
        score -= max(0, 30 - snr_f) * 1.0
        score -= mp_f * 20
        score -= abs(tc_f) * 10
        score += (geom_f - 50) * 0.2
        score = max(0, min(100, score))

        results[c] = {
            "forecast_snr": snr_f,
            "forecast_multipath": mp_f,
            "forecast_geometry": geom_f,
            "forecast_timing_corr": tc_f,
            "forecast_health_score": score
        }

    return results
