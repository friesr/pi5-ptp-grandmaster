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

function loadWaterfall() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/snr_waterfall/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const prns = data.prns;
            const times = data.times.map(t => new Date(t * 1000));
            const matrix = data.matrix;

            Plotly.newPlot("waterfall", [{
                z: matrix,
                x: times,
                y: prns.map(p => "PRN " + p),
                type: "heatmap",
                colorscale: "Viridis"
            }], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Satellite (PRN)" }
            });
        });
}

loadDays();
