def compute_prn_health(rows):
    """
    rows: list of GNSS entries for a single PRN:
      - timestamp
      - snr
      - multipath
      - used
      - state (clean/multipath/fading/obstructed/lost/recovering)
    """

    if not rows:
        return None

    snrs = [r["snr"] for r in rows]
    mps = [r["multipath"] for r in rows]
    used_count = sum(1 for r in rows if r["used"])
    total = len(rows)

    # Basic stats
    snr_min = min(snrs)
    snr_avg = sum(snrs) / total
    snr_max = max(snrs)

    mp_avg = sum(mps) / total
    mp_max = max(mps)

    # State counts
    state_counts = {}
    for r in rows:
        s = r["state"]
        state_counts[s] = state_counts.get(s, 0) + 1

    # Health score (0–100)
    score = 100
    score -= mp_avg * 40
    score -= (30 - snr_avg) if snr_avg < 30 else 0
    score -= (1 - used_count / total) * 30

    score = max(0, min(100, score))

    return {
        "snr_min": snr_min,
        "snr_avg": snr_avg,
        "snr_max": snr_max,
        "multipath_avg": mp_avg,
        "multipath_max": mp_max,
        "used_ratio": used_count / total,
        "state_counts": state_counts,
        "health_score": score
    }
