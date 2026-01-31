def validate_ntp(ntp):
    if ntp["offset_ms"] is None:
        return "red"

    offset = abs(ntp["offset_ms"])

    if offset > 5:
        return "red"
    if offset > 1:
        return "yellow"
    return "green"
