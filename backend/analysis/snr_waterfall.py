import numpy as np

def build_snr_waterfall(rows):
    """
    rows: list of GNSS log entries with:
      - timestamp
      - prn
      - snr

    Returns:
      - prns: sorted list of PRNs
      - times: sorted list of timestamps
      - matrix: 2D array [PRN index][time index] = SNR or 0
    """

    prns = sorted(list({r["prn"] for r in rows}))
    times = sorted(list({r["timestamp"] for r in rows}))

    prn_index = {p: i for i, p in enumerate(prns)}
    time_index = {t: i for i, t in enumerate(times)}

    matrix = np.zeros((len(prns), len(times)))

    for r in rows:
        pi = prn_index[r["prn"]]
        ti = time_index[r["timestamp"]]
        matrix[pi][ti] = r["snr"]

    return prns, times, matrix.tolist()
