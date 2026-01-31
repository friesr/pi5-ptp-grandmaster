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

function loadPRNHealth() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/prn_health/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const prns = Object.keys(data).map(Number).sort((a, b) => a - b);
            const scores = prns.map(p => data[p].health_score);

            Plotly.newPlot("health-chart", [{
                x: prns.map(p => "PRN " + p),
                y: scores,
                type: "bar",
                marker: {
                    color: scores.map(s => {
                        if (s > 80) return "#2ecc71";
                        if (s > 60) return "#f1c40f";
                        if (s > 40) return "#e67e22";
                        return "#e74c3c";
                    })
                }
            }], {
                margin: { t: 20 },
                yaxis: { title: "Health Score (0–100)" }
            });

            const details = document.getElementById("health-details");
            details.textContent = JSON.stringify(data, null, 2);
        });
}

loadDays();
