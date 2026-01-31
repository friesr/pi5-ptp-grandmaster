def normalize_event(timestamp, etype, severity, details):
    return {
        "timestamp": timestamp,
        "type": etype,
        "severity": severity,
        "details": details
    }


def build_unified_timeline(gnss_events, ptp_events, interference_events,
                           sla_events, receiver_events, env_events):
    timeline = []

    # GNSS events
    for e in gnss_events:
        timeline.append(normalize_event(
            e["timestamp"],
            "gnss_" + e["type"],
            e.get("severity", "info"),
            e
        ))

    # PTP events
    for e in ptp_events:
        timeline.append(normalize_event(
            e["timestamp"],
            "ptp_" + e["type"],
            e.get("severity", "info"),
            e
        ))

    # Interference
    for e in interference_events:
        timeline.append(normalize_event(
            e["timestamp"],
            "interference_" + e["type"],
            e["severity"],
            e
        ))

    # SLA violations
    for e in sla_events:
        timeline.append(normalize_event(
            e["timestamp"],
            "sla_violation",
            "warning",
            e
        ))

    # Receiver hardware
    for e in receiver_events:
        timeline.append(normalize_event(
            e["timestamp"],
            "receiver_" + e["issue"],
            "warning",
           
