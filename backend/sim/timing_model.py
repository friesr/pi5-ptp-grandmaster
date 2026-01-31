def simulate_timing_response(sample, state, scenario):
    """
    sample: GNSS/PTP sample after perturbations
    state: internal servo state
    scenario: includes servo adjustments
    """

    kp = scenario.get("servo_adjustments", {}).get("kp", 1.0)
    ki = scenario.get("servo_adjustments", {}).get("ki", 0.01)

    error = sample.get("timing_error_ns", 0)

    # PI controller
    state["integrator"] += error * ki
    correction = kp * error + state["integrator"]

    # Simulated output timing error
    state["timing_output"] += correction * 0.1

    return state
