def detect_events(results):
    events = []
    active = {}

    def start_event(name, t):
        active[name] = t

    def end_event(name, t):
        if name in active:
            events.append({
                "event": name,
                "start": active[name],
                "end": t,
                "duration": t - active[name]
            })
            del active[name]

    for r in results:
        t = r["timestamp"]

        # Outage
        if r["snr"] == 0 or not r["tracking"]:
            if "outage" not in active:
                start_event("outage", t)
        else:
            end_event("outage", t)

        # Interference
        if r["snr"] < 20:
            if "interference" not in active:
                start_event("interference", t)
        else:
            end_event("interference", t)

        # Spoofing
        if r["pseudorange_residual"] > 30:
            if "spoofing" not in active:
                start_event("spoofing", t)
        else:
            end_event("spoofing", t)

        # Multipath
        if r["multipath"] > 1.5:
            if "multipath" not in active:
                start_event("multipath", t)
        else:
            end_event("multipath", t)

        # Servo instability
        if abs(r["timing_output"]) > 100:
            if "servo_instability" not in active:
                start_event("servo_instability", t)
        else:
            end_event("servo_instability", t)

    # Close any open events at end
    final_t = results[-1]["timestamp"]
    for name in list(active.keys()):
        end_event(name, final_t)

    return events
