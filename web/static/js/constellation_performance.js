function loadPerformance() {
    fetch("/api/constellation_performance/load")
        .then(r => r.json())
        .then(data => {
            renderTable(data);
            renderChart(data);
        });
}

function renderTable(data) {
    const el = document.getElementById("perf-table");

    let html = `
        <table>
            <tr>
                <th>Constellation</th>
                <th>SNR</th>
                <th>Multipath</th>
                <th>Geometry</th>
                <th>Availability</th>
                <th>Drift</th>
                <th>Timing Corr</th>
                <th>Health</th>
            </tr>
    `;

    for (const c in data) {
        const d = data[c];
        html += `
            <tr>
                <td>${c}</td>
                <td>${d.avg_snr.toFixed(1)}</td>
                <td>${d.avg_multipath.toFixed(3)}</td>
                <td>${d.avg_geometry.toFixed(1)}</td>
                <td>${d.avg_availability.toFixed(1)}%</td>
                <td>${d.avg_drift.toFixed(3)}</td>
                <td>${d.avg_timing_correlation.toFixed(3)}</td>
                <td>${d.health_score.toFixed(1)}</td>
            </tr>
        `;
    }

    html += "</table>";
    el.innerHTML = html;
}

function renderChart(data) {
    const names = Object.keys(data);
    const scores = names.map(c => data[c].health_score);

    Plotly.newPlot("health-chart", [{
        x: names,
        y: scores,
        type: "bar"
    }], {
        margin: { t: 20 },
        yaxis: { title: "Health Score (0–100)" }
    });
}

loadPerformance();
