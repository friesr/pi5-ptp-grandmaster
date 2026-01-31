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

function loadGeometry() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/geometry_timeline/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const x = data.map(d => new Date(d.timestamp * 1000));
            const y = data.map(d => d.total_score);

            Plotly.newPlot("geometry-chart", [{
                x: x,
                y: y,
                mode: "lines",
                name: "Geometry Score"
            }], {
                margin: { t: 20 },
                yaxis: { title: "Score (0–100)" },
                xaxis: { title: "Time" }
            });
        });
}

loadDays();
