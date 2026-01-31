import pandas as pd
import io
import time

def generate_excel_export():
    # Simulated data for now — will be replaced with real logs later
    timestamps = []
    ptp_offsets = []
    ntp_offsets = []
    gnss_used = []
    gnss_visible = []

    # Generate 100 rows of simulated data
    for i in range(100):
        timestamps.append(time.time() - (100 - i) * 10)
        ptp_offsets.append((i % 20) - 10)
        ntp_offsets.append((i % 5) - 2)
        gnss_used.append(5 + (i % 3))
        gnss_visible.append(8 + (i % 4))

    df = pd.DataFrame({
        "timestamp": timestamps,
        "ptp_offset_ns": ptp_offsets,
        "ntp_offset_ms": ntp_offsets,
        "gnss_used": gnss_used,
        "gnss_visible": gnss_visible
    })

    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output
