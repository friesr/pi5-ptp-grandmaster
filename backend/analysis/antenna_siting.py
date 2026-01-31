import math
import numpy as np

def distance(a, b):
    return math.sqrt(
        (a["x"] - b["x"])**2 +
        (a["y"] - b["y"])**2 +
        (a["z"] - b["z"])**2
    )

def compute_siting_score(candidate, reflectors, env_fingerprint, constellation_perf):
    """
    candidate: {x, y, z}
    reflectors: list of {x, y, z, probability}
    env_fingerprint: long-term environment metrics
    constellation_perf: constellation performance dictionary
    """

    # 1. Multipath penalty
    multipath_penalty = 0
    for r in reflectors:
        d = distance(candidate, r)
        multipath_penalty += r["probability"] * max(0, 20 - d)

    # 2. Environment stability
    env_penalty = env_fingerprint.get("avg_env_deviation", 0) * 50

    # 3. Constellation performance
    const_score = np.mean([v["health_score"] for v in constellation_perf.values()])

    # 4. Combine
    score = 100
    score -= multipath_penalty * 0.5
    score -= env_penalty
    score += (const_score - 50) * 0.2

    return max(0, min(100, score))
