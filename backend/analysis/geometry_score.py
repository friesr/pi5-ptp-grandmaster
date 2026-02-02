def compute_geometry_score(gdop, pdop, hdop, vdop, tdop):
    """
    Convert DOP values into a 0–100 geometry score.
    Lower DOP = better geometry.
    """

    # Normalize each DOP into a 0–100 score
    def dop_to_score(d):
        if d <= 1:
            return 100
        if d >= 10:
            return 0
        return max(0, 100 - (d - 1) * 12.5)

    scores = {
        "gdop_score": dop_to_score(gdop),
        "pdop_score": dop_to_score(pdop),
        "hdop_score": dop_to_score(hdop),
        "vdop_score": dop_to_score(vdop),
        "tdop_score": dop_to_score(tdop)
    }

    # Weighted total geometry score
    total = (
        scores["gdop_score"] * 0.30 +
        scores["pdop_score"] * 0.25 +
        scores["hdop_score"] * 0.20 +
        scores["vdop_score"] * 0.15 +
        scores["tdop_score"] * 0.10
    )

    scores["total_score"] = total
    return scores
