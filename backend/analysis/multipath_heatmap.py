import numpy as np

def build_multipath_heatmap(rows, az_bins=36, el_bins=18):
    """
    rows: list of GNSS log entries with:
      - azimuth
      - elevation
      - multipath (0–1)

    az_bins: number of azimuth divisions (10° each if 36)
    el_bins: number of elevation divisions (5° each if 18)
    """

    heatmap = np.zeros((el_bins, az_bins))
    counts = np.zeros((el_bins, az_bins))

    for r in rows:
        az = r["azimuth"]
        el = r["elevation"]
        mp = r["multipath"]

        az_idx = int((az % 360) / (360 / az_bins))
        el_idx = int(el / (90 / el_bins))

        heatmap[el_idx, az_idx] += mp
        counts[el_idx, az_idx] += 1

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        avg = np.divide(heatmap, counts, out=np.zeros_like(heatmap), where=counts > 0)

    return avg.tolist()
