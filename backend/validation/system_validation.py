def validate_ptp(ptp):
    if not ptp["gm_present"]:
        return "red"

    offset = abs(ptp["offset_ns"])

    if offset > 500:
        return "red"
    if offset > 200:
        return "yellow"
    return "green"

def validate_system_health(system):
    if system["memory"] > 90:
        return "red"
    if system["memory"] > 75:
        return "yellow"

    load1 = system["cpu_load"][0]
    if load1 > 4.0:
        return "red"
    if load1 > 2.0:
        return "yellow"

    return "green"

def validate_storage(local_percent, nas_percent):
    if local_percent > 95 or nas_percent > 95:
        return "red"
    if local_percent > 80 or nas_percent > 80:
        return "yellow"
    return "green"
