def build_feature_vector(r):
    """
    r: GNSS row with:
      - snr
      - multipath
      - geometry_score
      - state
      - interference_level
      - prn_health
    """

    state_map = {
        "clean": 0,
        "multipath": 1,
        "fading": 2,
        "obstructed": 3,
        "lost": 4,
        "recovering": 5
    }

    return [
        r["snr"],
        r["multipath"],
        r["geometry_score"],
        state_map.get(r["state"], 0),
        r["interference_level"],
        r["prn_health"]
    ]
