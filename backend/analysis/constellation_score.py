import numpy as np

def score_constellation(rows):
    """
    rows: list of GNSS log entries for a day
    Each row contains: prn, snr, elevation, used, constellation
    """

    constellations = {}

    for r in rows:
        c = r["constellation"]
        if c not in constellations:
            constellations[c] = {
                "snr": [],
                "elevation": [],
                "used": 0,
                "visible": 0
            }

        constellations[c]["snr"].append(r["snr"])
        constellations[c]["elevation"].append(r["elevation"])
        constellations[c]["visible"] += 1
        if r["used"]:
            constellations[c]["used"] += 1

    scores = {}

    for c, data in constellations.items():
        snr_avg = np.mean(data["snr"])
        elev_avg = np.mean(data["elevation"])
        used_ratio = data["used"] / data["visible"]

        # Normalize into 0–100 scores
        snr_score = min(100, max(0, (snr_avg - 20) * 2))
        elev_score = min(100, max(0, elev_avg))
        used_score = used_ratio * 100

        total = (snr_score * 0.4) + (elev_score * 0.3) + (used_score * 0.3)

        scores[c] = {
            "snr_avg": float(snr_avg),
            "elev_avg": float(elev_avg),
            "used_ratio": float(used_ratio),
            "score": float(total)
        }

    return scores
