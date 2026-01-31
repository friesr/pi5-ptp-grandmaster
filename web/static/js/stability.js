function loadPrediction() {
    fetch("/api/stability/predict")
        .then(r => r.json())
        .then(data => {
            const el = document.getElementById("prediction");

            if (data.error) {
                el.textContent = data.error;
                el.style.color = "#e74c3c";
                return;
            }

            const ns = data.predicted_timing_error_ns.toFixed(1);
            const risk = data.risk_level;

            let color = "#2ecc71";
            if (risk === "moderate") color = "#f1c40f";
            if (risk === "high") color = "#e74c3c";

            el.style.color = color;
            el.textContent = `${ns} ns (${risk.toUpperCase()} RISK)`;
        });
}

loadPrediction();
