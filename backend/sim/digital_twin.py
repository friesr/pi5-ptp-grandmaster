from backend.sim.replay_engine import replay_day
from backend.sim.perturbation_engine import apply_perturbations
from backend.sim.timing_model import simulate_timing_response

def run_simulation(samples, scenario):
    """
    samples: list of GNSS/PTP samples for a given day
    scenario: scenario definition dict
    Returns:
        list of simulation results, each containing:
            - timestamp
            - timing_output (simulated)
            - snr (after perturbations)
            - multipath (after perturbations)
            - tracking (after perturbations)
            - pseudorange_residual (after perturbations)
            - doppler_residual (after perturbations)
    """

    # Internal servo state
    state = {
        "integrator": 0.0,
        "timing_output": 0.0
    }

    results = []

    # Replay samples in chronological order
    for s in replay_day(samples):

        # Apply perturbations to a copy of the sample
        perturbed = apply_perturbations(dict(s), scenario)

        # Feed perturbed sample into timing model
        state = simulate_timing_response(perturbed, state, scenario)

        # Record simulation output
        results.append({
            "timestamp": perturbed["timestamp"],
            "timing_output": state["timing_output"],
            "snr": perturbed.get("snr"),
            "multipath": perturbed.get("multipath"),
            "tracking": perturbed.get("tracking", True),
            "pseudorange_residual": perturbed.get("pseudorange_residual"),
            "doppler_residual": perturbed.get("doppler_residual")
        })

    return results
