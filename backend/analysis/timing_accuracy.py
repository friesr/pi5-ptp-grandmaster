def estimate_timing_error(geom, snr, multipath, prn_health, interference):
    """
    Inputs:
      geom: geometry score (0–100)
      snr: average SNR
      multipath: average multipath (0–1)
      prn_health: average PRN health (0–100)
      interference: 0 (none), 1 (noise), 2 (spoofing), 3 (jamming)

    Returns:
      estimated timing error in nanoseconds
    """

    # Base error (ideal conditions)
    error = 5  # ns

    # Geometry penalty
    if geom < 80:
        error += (80 - geom) * 0.5

    # SNR penalty
    if snr < 30:
        error += (30 - snr) * 0.8

    # Multipath penalty
    error += multipath * 20

    # PRN health penalty
    if prn_health < 80:
        error += (80 - prn_health) * 0.3

    # Interference penalty
    if interference == 1:
        error += 20
    elif interference == 2:
        error += 50
    elif interference == 3:
        error += 200

    return max(0, error)
