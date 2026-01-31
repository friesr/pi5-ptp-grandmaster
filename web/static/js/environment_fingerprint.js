function loadEnvironment() {
    fetch("/api/environment/load")
        .then(r => r.json())
        .then(data => {
            const summary = document.getElementById("env-summary");

            summary.innerHTML = `
                <p><strong>Average SNR:</strong> ${data.avg_snr.toFixed(2)} dB</p>
                <p><strong>Average Multipath:</strong> ${data.avg_multipath.toFixed(3)}</p>
                <p><strong>Average Geometry Score:</strong> ${data.avg_geometry.toFixed(1)}</p>
                <p><strong>Average PRN Health:</strong> ${data.avg_prn_health.toFixed(1)}</p>
                <p><strong>Average Interference Events:</strong> ${data.avg_interference.toFixed(2)}</p>
                <p><strong>Average SNR Drift:</strong> ${data.avg_drift.toFixed(3)} dB/day</p>
            `;

            Plotly.newPlot("sky-density", [{
                z: data.avg_sky_density,
                type: "heatmap",
                colorscale: "YlGnBu"
            }], {
                margin: { t: 20 },
                xaxis: { title: "Azimuth (bins)" },
                yaxis: { title: "Elevation (bins)" }
            });
        });
}

loadEnvironment();
