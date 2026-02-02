import numpy as np

def build_skyplot_density(rows, az_bins=36, el_bins=18):
    """
    rows: list of GNSS log entries with:
      - azimuth
      - elevation

    Returns:
      2D density matrix (elevation × azimuth)
    """

    density = np.zeros((el_bins, az_bins))

    for r in rows:
        az = r["azimuth"]
        el = r["elevation"]

        az_idx = int((az % 360) / (360 / az_bins))
        el_idx = int(el / (90 / el_bins))

        density[el_idx, az_idx] += 1

    return density.tolist()
