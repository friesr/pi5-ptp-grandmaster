from backend.sim.replay_engine import replay_day
from backend.sim.perturbation_engine import apply_perturbations
from backend.sim.timing_model import simulate_timing_response

def run_simulation(samples, scenario):
    state = {"integrator": 0, "timing_output": 0}
    results = []

    for s in replay_day(samples):
        s2 = apply_perturbations(dict(s), scenario)
        state = simulate_timing_response(s2, state, scenario)

        results.append({
            "timestamp": s2["timestamp"],
            "timing_output": state["timing_output"],
            "snr": s2["snr"],
            "multipath": s2["multipath"],
            "
