import numpy as np

def compute_clock_stability(prn_data):
    results = {}

    for prn, d in prn_data.items():
        pr_res = np.array(d["pr_res"])
        dop_res = np.array(d["dop_res"])
        timing_corr = np.array(d["timing_corr"])
        eclipse = np.array(d["eclipse"]).astype(int)
        elevation = np.array(d["elevation"])

        # Drift = slope of pseudorange residual
        if len(pr_res) > 1:
            drift = float(np.polyfit(range(len(pr_res)), pr_res, 1)[0])
        else:
            drift = 0.0

        # Noise = variance of Doppler residual
        noise = float(np.var(dop_res)) if len(dop_res) else 0.0

        # Thermal sensitivity = correlation with eclipse flag
        if np.std(eclipse) > 0:
            thermal_corr = float(np.corrcoef(pr_res, eclipse)[0, 1])
        else:
            thermal_corr = 0.0

        # Elevation sensitivity = correlation with elevation
        if np.std(elevation) > 0:
            elevation_corr = float(np.corrcoef(pr_res, elevation)[0, 1])
        else:
            elevation_corr = 0.0

        # Unified score
        score = 100
        score -= abs(drift) * 200
        score -= noise * 5
        score -= abs(thermal_corr) * 20
        score -= abs(elevation_corr) * 10
        score -= abs(np.mean(timing_corr)) * 10

        score = max(0, min(100, score))

        results[prn] = {
            "drift": drift,
            "noise": noise,
            "thermal_corr": thermal_corr,
            "elevation_corr": elevation_corr,
            "timing_corr_avg": float(np.mean(timing_corr)),
            "clock_stability_score": score
        }

    return results
