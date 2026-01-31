function loadDrift() {
    fetch("/api/constellation_drift/load")
        .then(r => r.json())
        .then(data => {
            const days = data.days;
            const history = data.history;
            const drift = data.drift;

            const traces = [];

            // Build time series per constellation
            const constellations = Object.keys(history[0] || {});

            constellations.forEach(c => {
                const y = history.map(day => day[c]?.avg || null);

                traces.push({
                    x: days,
                    y: y,
                    mode: "lines",
                    name: c
                });
            });

            Plotly.newPlot("drift-chart", traces, {
                margin: { t: 20 },
                xaxis: { title: "Day" },
                yaxis: { title: "Average SNR (dB)" }
            });

            document.getElementById("drift-details").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadDrift();
