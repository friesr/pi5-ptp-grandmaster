def build_report(day, metrics, sla, timeline, predictions, env_change, confidence):
    """
    Build a structured report dictionary.
    """

    return {
        "day": day,
        "executive_summary": {
            "timing_confidence": confidence,
            "sla_overall": sla["overall_compliant"],
            "sla_details": sla,
            "gnss_availability": metrics["gnss_availability_pct"],
            "ptp_unlocks": metrics["unlock_count"],
            "interference_events": metrics["interference_count"],
            "receiver_health": metrics["receiver_health"]
        },

        "key_metrics": {
            "offset_stats": metrics["offset_stats"],
            "timing_error_stats": metrics["timing_error_stats"],
            "snr_avg": metrics["snr_avg"],
            "multipath_avg": metrics["multipath_avg"],
            "geometry_avg": metrics["geometry_avg"],
            "prn_health_avg": metrics["prn_health_avg"],
            "constellation_drift": metrics["drift"]
        },

        "events": {
            "timeline_highlights": timeline[:50],  # top 50 events
            "sla_violations": [e for e in timeline if e["type"] == "sla_violation"],
            "interference": [e for e in timeline if e["type"].startswith("interference")],
            "receiver": [e for e in timeline if e["type"].startswith("receiver")],
            "environment": [e for e in timeline if e["type"] == "environment_change"]
        },

        "predictions": predictions,

        "environment_change": env_change,

        "notes": {
            "generated_by": "GNSS Timing Observatory",
            "version": "1.0"
        }
    }
