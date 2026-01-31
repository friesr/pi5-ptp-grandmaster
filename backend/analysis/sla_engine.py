def evaluate_sla(sla, metrics):
    """
    sla: SLA definition
    metrics: daily metrics including:
      - offset_samples (list of ns)
      - confidence_samples (list of 0–100)
      - unlock_count
      - gnss_availability_pct
      - max_interference_severity
    """

    results = {}

    # Offset SLA
    offset_ok = sum(1 for o in metrics["offset_samples"] if abs(o) <= sla["offset_ns_max"])
    offset_pct = offset_ok / len(metrics["offset_samples"]) * 100
    results["offset_compliant"] = offset_pct >= sla["offset_compliance_pct"]
    results["offset_pct"] = offset_pct

    # Confidence SLA
    conf_ok = sum(1 for c in metrics["confidence_samples"] if c >= sla["confidence_min"])
    conf_pct = conf_ok / len(metrics["confidence_samples"]) * 100
    results["confidence_compliant"] = conf_pct >= sla["confidence_compliance_pct"]
    results["confidence_pct"] = conf_pct

    # Unlock SLA
    results["unlock_compliant"] = metrics["unlock_count"] <= sla["max_unlocks_per_day"]

    # GNSS availability
    results["availability_compliant"] = (
        metrics["gnss_availability_pct"] >= sla["gnss_availability_min_pct"]
    )

    # Interference severity
    results["interference_compliant"] = (
        metrics["max_interference_severity"] <= sla["max_interference_severity"]
    )

    # Overall SLA
    results["overall_compliant"] = all(results[k] for k in results if k.endswith("_compliant"))

    return results
