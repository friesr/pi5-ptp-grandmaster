ALERT_RULES = [
    {
        "id": "ptp_offset_high",
        "severity": "critical",
        "message": "PTP offset exceeds 1 µs",
        "condition": lambda s: abs(s["ptp"]["offset_ns"]) > 1000
    },
    {
        "id": "ntp_offset_high",
        "severity": "warning",
        "message": "NTP offset exceeds 10 ms",
        "condition": lambda s: abs(s["ntp"]["offset_ms"]) > 10
    },
    {
        "id": "gnss_used_low",
        "severity": "warning",
        "message": "Few GNSS satellites used (< 3)",
        "condition": lambda s: s["gnss"]["used"] < 3
    },
    {
        "id": "storage_local_high",
        "severity": "warning",
        "message": "Local storage above 80%",
        "condition": lambda s: s["storage"]["local"]["percent"] > 80
    },
    {
        "id": "nas_unavailable",
        "severity": "warning",
        "message": "NAS not mounted or unreachable",
        "condition": lambda s: not s["storage"]["nas_health"]["mounted"]
    }
]
