function loadHealth() {
    fetch("/api/receiver_health/load")
        .then(r => r.json())
        .then(data => {
            const summary = document.getElementById("health-summary");

            summary.innerHTML = `
                <h3>Status: ${data.issues.join(", ")}</h3>
                <p>Average PRN Health: ${data.avg_prn_health.toFixed(1)}</p>
                <p>Average SNR Drift: ${data.avg_drift.toFixed(3)} dB/day</p>
            `;

            document.getElementById("health-details").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadHealth();
