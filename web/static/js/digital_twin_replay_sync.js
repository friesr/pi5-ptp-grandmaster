function loadReplayAndTimeline() {
    const scenario = document.getElementById("scenario-select").value;

    // Load replay
    fetch(`/api/digital_twin_replay/run/${scenario}`)
        .then(r => r.json())
        .then(data => {
            replayData = data.results;
            index = 0;
            updateFrame();
        });

    // Load timeline
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
                customdata: [ev.start]
            }));

            Plotly.newPlot("timeline-chart", traces);

            document.getElementById("timeline-chart")
                .on("plotly_click", function(data) {
                    const ts = data.points[0].customdata;
                    ReplaySyncBus.emit(ts);
                });
        });
}
