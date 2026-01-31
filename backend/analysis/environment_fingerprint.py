import numpy as np

def build_environment_fingerprint(history):
    """
    history: list of daily GNSS summaries, each containing:
      - avg_snr
      - avg_multipath
      - geometry_score
      - sky_density (2D matrix)
      - interference_count
      - prn_health_avg
      - drift (per constellation)

    Returns:
      fingerprint: a long-term statistical signature
    """

    # Aggregate simple metrics
    avg_snr = np.mean([h["avg_snr"] for h in history])
    avg_mp = np.mean([h["avg_multipath"] for h in history])
    avg_geom = np.mean([h["geometry_score"] for h in history])
    avg_prn_health = np.mean([h["prn_health_avg"] for h in history])
    avg_interference = np.mean([h["interference_count"] for h in history])

    # Aggregate skyplot density
    sky_matrices = [np.array(h["sky_density"]) for h in history]
    sky_density_avg = np.mean(sky_matrices, axis=0).tolist()

    # Aggregate drift
    drift_values = []
    for h in history:
        drift_values.extend(h["drift"].values())
    avg_drift = float(np.mean(drift_values))

    return {
        "avg_snr": float(avg_snr),
        "avg_multipath": float(avg_mp),
        "avg_geometry": float(avg_geom),
        "avg_prn_health": float(avg_prn_health),
        "avg_interference": float(avg_interference),
        "avg_sky_density": sky_density_avg,
        "avg_drift": avg_drift
    }
