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

function loadExplanations() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/anomaly_explainer/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const list = document.getElementById("explanation-list");

            list.textContent = data
                .map(e => {
                    const ts = new Date(e.timestamp * 1000).toISOString();
                    return `Time: ${ts}\n- ${e.explanations.join("\n- ")}\n`;
                })
                .join("\n");
        });
}

loadDays();
