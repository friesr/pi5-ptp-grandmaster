def compute_timing_confidence(
    geometry,
    snr,
    multipath,
    prn_health,
    interference_level,
    receiver_health_score,
    timing_error_ns,
    env_deviation
):
    """
    All inputs normalized to 0–100 except:
      - interference_level: 0–3
      - timing_error_ns: arbitrary scale
      - env_deviation: 0–1

    Returns:
      timing confidence score (0–100)
    """

    score = 100

    # Geometry penalty
    score -= max(0, 80 - geometry) * 0.3

    # SNR penalty
    score -= max(0, 30 - snr) * 0.5

    # Multipath penalty
    score -= multipath * 20

    # PRN health penalty
    score -= max(0, 80 - prn_health) * 0.2

    # Interference penalty
    if interference_level == 1:
        score -= 10
    elif interference_level == 2:
        score -= 30
    elif interference_level == 3:
        score -= 60

    # Receiver hardware penalty
    score -= max(0, 100 - receiver_health_score) * 0.3

    # Timing error penalty
    score -= min(timing_error_ns / 5, 40)

    # Environment deviation penalty
    score -= env_deviation * 20

    return max(0, min(100, score))
