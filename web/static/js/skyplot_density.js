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

function loadDensity() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/skyplot_density/load/${day}`)
        .then(r => r.json())
        .then(data => {
            Plotly.newPlot("density-chart", [{
                z: data,
                type: "heatmap",
                colorscale: "YlGnBu"
            }], {
                margin: { t: 20 },
                xaxis: { title: "Azimuth (bins)" },
                yaxis: { title: "Elevation (bins)" }
            });
        });
}

loadDays();
