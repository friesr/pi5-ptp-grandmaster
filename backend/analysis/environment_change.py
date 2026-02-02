import numpy as np

def compute_deviation(current, fingerprint):
    """
    current: today's summary
    fingerprint: long-term fingerprint

    Returns:
      deviation score (0–1)
      contributing factors
    """

    factors = {}

    # Compare SNR
    snr_dev = abs(current["avg_snr"] - fingerprint["avg_snr"]) / 20
    factors["snr"] = snr_dev

    # Compare multipath
    mp_dev = abs(current["avg_multipath"] - fingerprint["avg_multipath"]) / 0.5
    factors["multipath"] = mp_dev

    # Compare geometry
    geom_dev = abs(current["geometry_score"] - fingerprint["avg_geometry"]) / 50
    factors["geometry"] = geom_dev

    # Compare PRN health
    prn_dev = abs(current["prn_health_avg"] - fingerprint["avg_prn_health"]) / 40
    factors["prn_health"] = prn_dev

    # Compare interference
    inter_dev = abs(current["interference_count"] - fingerprint["avg_interference"]) / 5
    factors["interference"] = inter_dev

    # Compare sky density (matrix difference)
    sky_current = np.array(current["sky_density"])
    sky_finger = np.array(fingerprint["avg_sky_density"])
    sky_dev = np.mean(np.abs(sky_current - sky_finger)) / 10
    factors["sky_density"] = float(sky_dev)

    # Combine
    deviation = float(np.mean(list(factors.values())))
    deviation = min(1.0, deviation)

    return deviation, factors
