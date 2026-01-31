function loadForecast() {
    fetch("/api/constellation_forecast/predict")
        .then(r => r.json())
        .then(data => {
            renderTable(data);
            renderChart(data);
        });
}

function renderTable(data) {
    const el = document.getElementById("forecast-table");

    let html = `
        <table>
            <tr>
                <th>Constellation</th>
                <th>SNR</th>
                <th>Multipath</th>
                <th>Geometry</th>
                <th>Timing Corr</th>
                <th>Health</th>
            </tr>
    `;

    for (const c in data) {
        const d = data[c];
        html += `
            <tr>
                <td>${c}</td>
                <td>${d.forecast_snr.toFixed(1)}</td>
                <td>${d.forecast_multipath.toFixed(3)}</td>
                <td>${d.forecast_geometry.toFixed(1)}</td>
                <td>${d.forecast_timing_corr.toFixed(3)}</td>
                <td>${d.forecast_health_score.toFixed(1)}</td>
            </tr>
        `;
    }

    html += "</table>";
    el.innerHTML = html;
}

function renderChart(data) {
    const names = Object.keys(data);
    const scores = names.map(c => data[c].forecast_health_score);

    Plotly.newPlot("forecast-chart", [{
        x: names,
        y: scores,
        type: "bar"
    }], {
        margin: { t: 20 },
        yaxis: { title: "Forecast Health Score (0–100)" }
    });
}

loadForecast();
