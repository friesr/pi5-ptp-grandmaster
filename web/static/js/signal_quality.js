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

function loadSignalQuality() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/signal_quality/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const x = data.map(d => new Date(d.timestamp * 1000));
            const y = data.map(d => "PRN " + d.prn);
            const colors = data.map(d => {
                switch (d.state) {
                    case "clean": return "#2ecc71";
                    case "multipath": return "#e67e22";
                    case "fading": return "#f1c40f";
                    case "obstructed": return "#9b59b6";
                    case "lost": return "#e74c3c";
                    case "recovering": return "#3498db";
                }
            });

            Plotly.newPlot("quality-chart", [{
                x: x,
                y: y,
                mode: "markers",
                marker: { size: 8, color: colors }
            }], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Satellite (PRN)" }
            });
        });
}

loadDays();
