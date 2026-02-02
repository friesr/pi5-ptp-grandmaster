def extract_features(row):
    """
    Convert a GNSS anomaly row into a feature vector.
    """
    return [
        row["snr"],
        row["multipath"],
        row["geometry_score"],
        row["prn_health"],
        row["interference_level"],
        row["state"]
    ]
