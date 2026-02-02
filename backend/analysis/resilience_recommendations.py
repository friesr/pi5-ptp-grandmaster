def generate_recommendations(ctx):
    recs = []

    # 1. Outage risk
    if ctx["outage_probability"] > 0.4:
        recs.append({
            "action": "Increase GNSS holdover margin",
            "impact": "high",
            "reason": "Outage probability is elevated; increasing holdover reduces timing jumps."
        })

    # 2. Timing instability
    if ctx["timing_predicted_error"] > 80:
        recs.append({
            "action": "Tighten PTP servo parameters",
            "impact": "medium",
            "reason": "Predicted timing error exceeds stable thresholds."
        })

    # 3. Interference
    if ctx["interference_level"] > 1.5:
        recs.append({
            "action": "Enable interference mitigation mode",
            "impact": "high",
            "reason": "RF interference is degrading GNSS tracking."
        })

    # 4. Environment shift
    if ctx["environment_shift"] > 0.3:
        recs.append({
            "action": "Re-run antenna siting optimizer",
            "impact": "medium",
            "reason": "RF environment has changed significantly."
        })

    # 5. Antenna siting
    if ctx["best_siting"] and ctx["best_siting"]["score"] < 70:
        recs.append({
            "action": f"Consider relocating antenna to {ctx['best_siting']['name']}",
            "impact": "high",
            "reason": "Antenna siting optimizer found a significantly better location."
        })

    # 6. Receiver health
    if ctx["receiver_health"].get("health_score", 100) < 70:
        recs.append({
            "action": "Perform receiver hardware diagnostics",
            "impact": "high",
            "reason": "Receiver health score indicates potential hardware degradation."
        })

    # Sort by impact
    impact_rank = {"high": 3, "medium": 2, "low": 1}
    recs.sort(key=lambda r: -impact_rank[r["impact"]])

    return recs
