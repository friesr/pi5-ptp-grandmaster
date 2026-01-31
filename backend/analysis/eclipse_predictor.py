import math

def predict_eclipse(sample):
    """
    sample fields expected:
      - sun_az
      - sun_el
      - sat_az
      - sat_el
      - earth_shadow_flag (optional boolean)
    Returns:
      True if satellite is considered in eclipse, else False.
    """

    # If the receiver/ephemeris already provides an explicit flag, trust it
    if sample.get("earth_shadow_flag") is True:
        return True

    # Simple geometric heuristic:
    # - satellite low in sky
    # - sun below horizon (from receiver perspective)
    sat_el = sample.get("sat_el", sample.get("elevation_deg", 0))
    sun_el = sample.get("sun_el", 0)

    if sat_el < 10 and sun_el < -5:
        return True

    return False
