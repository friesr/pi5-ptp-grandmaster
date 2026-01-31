function loadDays() {
    fetch("/api/gnss_history/days")
        .then(r => r.json())
        .then(days => {
            const sel = document.getElementById("day-select");
            sel.innerHTML = "";
            days.forEach(d => {
                const opt = document.createElement("option");
                opt.value = d;
                opt.textContent = d;
                sel.appendChild(opt);
            });
        });
}

function loadConfidence() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/timing_confidence2/compute/${day}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("score").textContent =
                data.confidence_score.toFixed(1);

            document.getElementById("features").textContent =
                JSON.stringify(data.features, null, 2);
        });
}

loadDays();
