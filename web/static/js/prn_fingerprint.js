function loadFingerprints() {
    fetch("/api/prn_fingerprint/load")
        .then(r => r.json())
        .then(data => {
            renderTable(data);
            renderChart(data);
        });
}

function renderTable(data) {
    const el = document.getElementById("prn-table");

    let html = `
        <table>
            <tr>
                <th>PRN</th>
                <th>SNR Avg</th>
                <th>SNR Var</th>
                <th>Multipath</th>
                <th>Geometry</th>
                <th>Timing Corr</th>
                <th>Health</th>
                <th>Anomalies</th>
                <th>Score</th>
            </tr>
    `;

    for (const prn in data) {
        const d = data[prn];
        html += `
            <tr>
                <td>${prn}</td>
                <td>${d.snr_avg.toFixed(1)}</td>
                <td>${d.snr_var.toFixed(2)}</td>
                <td>${d.multipath_avg.toFixed(3)}</td>
                <td>${d.geometry_avg.toFixed(1)}</td>
                <td>${d.timing_correlation.toFixed(3)}</td>
                <td>${d.health_avg.toFixed(1)}</td>
                <td>${d.anomaly_count}</td>
                <td>${d.fingerprint_score.toFixed(1)}</td>
            </tr>
        `;
    }

    html += "</table>";
    el.innerHTML = html;
}

function renderChart(data) {
    const prns = Object.keys(data);
    const scores = prns.map(p => data[p].fingerprint_score);

    Plotly.newPlot("prn-chart", [{
        x: prns,
        y: scores,
        type: "bar"
    }], {
        margin: { t: 20 },
        yaxis: { title: "Fingerprint Score (0–100)" }
    });
}

loadFingerprints();
