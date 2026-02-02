def multipath_score(elevation_deg, snr_dbhz):
    """
    Simple multipath heuristic:
    - Low elevation normally has lower SNR
    - High elevation should have high SNR
    - If SNR is too low for the elevation, multipath is likely
    """

    # Expected SNR model (very rough)
    expected = 20 + (elevation_deg * 0.5)  # 20 dB-Hz at horizon, ~65 at zenith

    # Difference between expected and actual
    diff = expected - snr_dbhz

    # Score: 0 = clean, 1 = severe multipath
    score = max(0.0, min(1.0, diff / 20.0))

    return score


def compute_multipath_for_satellites(sats):
    results = []

    for s in sats:
        score = multipath_score(s["elevation"], s["snr"])
        results.append({
            "prn": s["prn"],
            "snr": s["snr"],
            "elevation": s["elevation"],
            "multipath_score": score
        })

    return results
