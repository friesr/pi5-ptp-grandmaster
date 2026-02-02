def explain_anomaly(r):
    """
    r: a GNSS row with:
      - snr
      - multipath
      - geometry_score
      - state
      - interference_level
      - prn_health
      - cluster
    """

    explanations = []

    # SNR issues
    if r["snr"] < 10:
        explanations.append("Very low SNR, likely fading or obstruction.")
    elif r["snr"] < 20:
        explanations.append("Moderately low SNR, possible partial obstruction or noise.")

    # Multipath
    if r["multipath"] > 0.6:
        explanations.append("High multipath detected, likely reflection from nearby surfaces.")

    # Geometry
    if r["geometry_score"] < 40:
        explanations.append("Poor satellite geometry reducing timing accuracy.")

    # PRN health
    if r["prn_health"] < 60:
        explanations.append("Satellite health degraded, contributing to instability.")

    # Interference
    if r["interference_level"] == 1:
        explanations.append("RF noise detected in the band.")
    elif r["interference_level"] == 2:
        explanations.append("Possible spoofing indicators detected.")
    elif r["interference_level"] == 3:
        explanations.append("Strong jamming event detected.")

    # Cluster-based explanation
    cluster_map = {
        0: "Normal operation.",
        1: "Low-elevation obstruction pattern.",
        2: "Multipath-heavy environment.",
        3: "Interference-related anomaly.",
        4: "Receiver instability signature."
    }

    explanations.append(cluster_map.get(r["cluster"], "Unclassified anomaly."))

    return explanations
