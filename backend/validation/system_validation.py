def validate_ptp(ptp):
    if not ptp["gm_present"]:
        return "red"

    offset = abs(ptp["offset_ns"])

    if offset > 500:
        return "red"
    if offset > 200:
        return "yellow"
    return "green"
