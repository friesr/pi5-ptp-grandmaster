def classify_signal(snr, multipath, elevation, fading, recovering):
    """
    Inputs:
      snr: float
      multipath: 0–1
      elevation: degrees
      fading: bool (from fade-out detection)
      recovering: bool (from fade-in detection)

    Returns:
      one of: clean, multipath, fading, obstructed, lost, recovering
    """

    # Lost / recovering states override everything
    if recovering:
        return "recovering"
    if fading:
        return "lost"

    # Obstructed: low elevation + low SNR
    if elevation < 15 and snr < 15:
        return "obstructed"

    # Multipath: high multipath score
    if multipath > 0.6:
        return "multipath"

    # Fading: SNR trending downward
    if snr < 20:
        return "fading"

    # Clean: good SNR + low multipath
    if snr > 30 and multipath < 0.3:
        return "clean"

    # Default fallback
    return "fading"
