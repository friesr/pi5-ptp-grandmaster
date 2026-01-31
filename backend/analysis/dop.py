import numpy as np

def compute_dop(sats):
    """
    sats: list of satellites with azimuth and elevation
    Returns GDOP, PDOP, HDOP, VDOP
    """

    if len(sats) < 4:
        return None  # not enough satellites

    H = []

    for s in sats:
        az = np.radians(s["azimuth"])
        el = np.radians(s["elevation"])

        # Convert to unit vector
        x = np.cos(el) * np.sin(az)
        y = np.cos(el) * np.cos(az)
        z = np.sin(el)

        # H matrix row
        H.append([x, y, z, 1])

    H = np.array(H)
    Q = np.linalg.inv(H.T @ H)

    GDOP = np.sqrt(np.trace(Q))
    PDOP = np.sqrt(Q[0,0] + Q[1,1] + Q[2,2])
    HDOP = np.sqrt(Q[0,0] + Q[1,1])
    VDOP = np.sqrt(Q[2,2])

    return {
        "gdop": GDOP,
        "pdop": PDOP,
        "hdop": HDOP,
        "vdop": VDOP
    }
