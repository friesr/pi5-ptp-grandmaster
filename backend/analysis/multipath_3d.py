import math

def reconstruct_reflectors(samples):
    """
    samples: list of GNSS multipath samples with:
      - azimuth_deg
      - elevation_deg
      - multipath_delay_ns
      - multipath_strength

    Returns a list of inferred reflector points:
      - x, y, z (meters)
      - probability
    """

    reflectors = []

    for s in samples:
        az = math.radians(s["azimuth_deg"])
        el = math.radians(s["elevation_deg"])
        delay_ns = s["multipath_delay_ns"]

        # Convert delay to distance (speed of light)
        d = delay_ns * 0.2998  # meters

        # Estimate reflection point
        # Simple model: reflection lies along azimuth, distance scaled by elevation
        r = d / max(0.1, math.sin(el))

        x = r * math.cos(az)
        y = r * math.sin(az)
        z = r * math.sin(el) * 0.2  # small vertical component

        reflectors.append({
            "x": x,
            "y": y,
            "z": z,
            "probability": min(1.0, s["multipath_strength"] / 50.0)
        })

    return reflectors
