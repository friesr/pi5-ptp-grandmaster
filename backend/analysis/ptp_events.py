import re

EVENT_PATTERNS = [
    (r"clock jump detected", "clock_jump", "error"),
    (r"offset\s+(-?\d+)", "offset", "info"),
    (r"freq\s+([+-]?\d+\.\d+)", "freq_adjust", "info"),
    (r"UNCALIBRATED to SLAVE", "lock", "success"),
    (r"SLAVE to UNCALIBRATED", "unlock", "warning"),
    (r"SYNCHRONIZATION_FAULT", "sync_fault", "error"),
    (r"master offset", "offset_report", "info")
]

def parse_ptp_events(lines):
    events = []

    for line in lines:
        # Extract timestamp if present
        ts_match = re.search(r"\[(\d+\.\d+)\]", line)
        ts = float(ts_match.group(1)) if ts_match else None

        for pattern, etype, severity in EVENT_PATTERNS:
            if re.search(pattern, line):
                events.append({
                    "timestamp": ts,
                    "type": etype,
                    "severity": severity,
                    "raw": line.strip()
                })
                break

    return events
