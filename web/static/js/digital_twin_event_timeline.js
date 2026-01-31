function loadScenarios() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById("scenario-select");
            sel.innerHTML = "";
            list.forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                sel.appendChild(opt);
            });
        });
}

function loadTimeline() {
    const scenario = document.getElementById("scenario-select").value;

    fetch(`/api/digital_twin_event_timeline/run/${scenario}`)
        .then(r => r.json())
        .then(data => {
            const events = data.events;

            const traces = events.map(ev => ({
                x: [ev.start, ev.end],
                y: [ev.event, ev.event],
                mode: "lines",
                line: { width: 12 },
                name: ev.event,
                customdata: [ev.start],   // store timestamp
                hovertemplate:
                    `Event: ${ev.event}<br>` +
                    `Start: ${ev.start}<br>` +
                    `End: ${ev.end}<br>` +
                    `Duration: ${ev.duration} s<extra></extra>`
            }));

            Plotly.newPlot("timeline-chart", traces, {
                margin: { t: 20 },
                xaxis: { title: "Timestamp (s)" },
                yaxis: { title: "Event Type" }
            });

            document.getElementById("timeline-chart")
                .on("plotly_click", function(data) {
                    const ts = data.points[0].customdata;
                    ReplaySyncBus.emit(ts);
                });
        });
}
loadScenarios();
