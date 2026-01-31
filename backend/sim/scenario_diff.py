def diff_scenarios(a, b):
    """
    a, b: lists of simulation samples
    Returns:
        - per-sample diffs
        - summary deltas
    """

    n = min(len(a), len(b))
    diffs = []

    for i in range(n):
        sa = a[i]
        sb = b[i]

        diffs.append({
            "timestamp": sa["timestamp"],
            "timing_error_delta": sb["timing_output"] - sa["timing_output"],
            "snr_delta": sb["snr"] - sa["snr"],
            "multipath_delta": sb["multipath"] - sa["multipath"],
            "tracking_delta": int(sb["tracking"]) - int(sa["tracking"]),
            "pseudorange_residual_delta": sb["pseudorange_residual"] - sa["pseudorange_residual"],
            "doppler_residual_delta": sb["doppler_residual"] - sa["doppler_residual"]
        })

    # Summary deltas
    summary = {
        "avg_timing_error_delta": sum(d["timing_error_delta"] for d in diffs) / n,
        "max_timing_error_delta": max(d["timing_error_delta"] for d in diffs),
        "min_timing_error_delta": min(d["timing_error_delta"] for d in diffs),
        "avg_snr_delta": sum(d["snr_delta"] for d in diffs) / n,
        "avg_multipath_delta": sum(d["multipath_delta"] for d in diffs) / n,
        "tracking_mismatch_count": sum(abs(d["tracking_delta"]) for d in diffs)
    }

    return {
        "diffs": diffs,
        "summary": summary
    }
