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

function loadScores() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/constellation_score/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const names = Object.keys(data);
            const scores = names.map(n => data[n].score);

            Plotly.newPlot("score-chart", [{
                x: names,
                y: scores,
                type: "bar",
                marker: {
                    color: scores.map(s => {
                        if (s > 80) return "#2ecc71";
                        if (s > 60) return "#f1c40f";
                        return "#e74c3c";
                    })
                }
            }], {
                margin: { t: 20 },
                yaxis: { title: "Score (0–100)" }
            });
        });
}

loadDays();
