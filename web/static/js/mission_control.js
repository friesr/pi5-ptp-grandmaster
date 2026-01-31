function loadMission() {
    const today = new Date().toISOString().slice(0, 10);

    fetch(`/api/mission/load/${today}`)
        .then(r => r.json())
        .then(data => {
            renderHealth(data);
            renderCharts(data);
            renderEvents(data);
        });
}

function renderHealth(data) {
    const el = document.getElementById("health-summary");

    const conf = data.timing_confidence?.score ?? 0;
    const stab = data.stability_prediction?.predicted_timing_error_ns ?? 0;
    const recv = data.receiver_health?.issues ?? ["unknown"];
    const env = data.environment_change?.status ?? "unknown";
    const sla = data.sla?.overall_compliant ? "OK" : "VIOLATION";

    el.innerHTML = `
        <p><strong>Timing Confidence:</strong> ${conf}</p>
        <p><strong>Predicted Stability:</strong> ${stab.toFixed(1)} ns</p>
        <p><strong>Receiver Health:</strong> ${recv.join(", ")}</p>
        <p><strong>Environment:</strong> ${env}</p>
        <p><strong>SLA:</strong> ${sla}</p>
    `;
}

function renderCharts(data) {
    Plotly.newPlot("confidence-chart", [{
        x: data.charts.confidence.map(p => new Date(p.t * 1000)),
        y: data.charts.confidence.map(p => p.v),
        mode: "lines"
    }]);

    Plotly.newPlot("error-chart", [{
        x: data.charts.timing_error.map(p => new Date(p.t * 1000)),
        y: data.charts.timing_error.map(p => p.v),
        mode: "lines"
    }]);

    Plotly.newPlot("interference-chart", [{
        x: data.charts.interference.map(p => new Date(p.t * 1000)),
        y: data.charts.interference.map(p => p.v),
        mode: "lines"
    }]);

    Plotly.newPlot("availability-chart", [{
        x: data.charts.availability.map(p => new Date(p.t * 1000)),
        y: data.charts.availability.map(p => p.v),
        mode: "lines"
    }]);
}

function renderEvents(data) {
    const feed = document.getElementById("event-feed");

    const events = [
        ...data.events.gnss,
        ...data.events.ptp,
        ...data.events.interference,
        ...data.events.sla
    ].sort((a, b) => a.timestamp - b.timestamp);

    feed.textContent = events
        .slice(-50)
        .map(e => {
            const ts = new Date(e.timestamp * 1000).toISOString();
            return `${ts} — ${e.type}`;
        })
        .join("\n");
}

loadMission();
