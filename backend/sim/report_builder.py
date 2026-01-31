def build_report(scenario, results, summary):
    """
    scenario: dict
    results: list of simulation samples
    summary: dict with max/min/rms error
    """

    return {
        "scenario_name": scenario["scenario_name"],
        "base_day": scenario["base_day"],
        "perturbations": scenario.get("perturbations", {}),
        "servo_adjustments": scenario.get("servo_adjustments", {}),
        "summary": summary,
        "timing_output_stats": {
            "max_error_ns": summary["max_error"],
            "min_error_ns": summary["min_error"],
            "rms_error_ns": summary["rms_error"]
        },
        "result_count": len(results)
    }
