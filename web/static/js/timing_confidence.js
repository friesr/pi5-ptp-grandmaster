function loadConfidence() {
    const today = new Date().toISOString().slice(0, 10);

    fetch(`/api/timing_confidence/load/${today}`)
        .then(r => r.json())
        .then(data => {
            const score = data.timing_confidence;
            const el = document.getElementById("confidence-score");

            let color = "#2ecc71";
            if (score < 70) color = "#f1c40f";
            if (score < 50) color = "#e67e22";
            if (score < 30) color = "#e74c3c";

            el.style.color = color;
            el.textContent = score.toFixed(1);
        });
}

loadConfidence();
