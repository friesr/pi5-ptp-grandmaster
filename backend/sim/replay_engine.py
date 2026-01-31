def replay_day(samples):
    """
    samples: list of GNSS/PTP samples with timestamps
    Returns a generator yielding samples in chronological order.
    """
    for s in sorted(samples, key=lambda x: x["timestamp"]):
        yield s
