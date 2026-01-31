def validate_gnss(gnss):
    if gnss["used"] < 3:
        return "red"
    if gnss["used"] < 5:
        return "yellow"
    return "green"
