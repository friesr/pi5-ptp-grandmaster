def classify_correlation(features):
    f = features

    # Environment issue: both receivers degrade similarly
    if f["snr_diff"] < 2 and f["multipath_diff"] < 0.05 and f["interference_diff"] < 1:
        return "environment_issue"

    # Receiver A issue: A is worse than B
    if f["snr_diff"] > 5 and f["timing_error_diff"] > 50:
        return "receiver_asymmetric_issue"

    # Spoofing: both receivers show timing divergence simultaneously
    if f["timing_error_diff"] > 200 and f["confidence_diff"] > 20:
        return "spoofing_suspected"

    # Healthy: small differences
    if f["snr_diff"] < 1 and f["timing_error_diff"] < 20:
        return "healthy"

    return "uncertain"
