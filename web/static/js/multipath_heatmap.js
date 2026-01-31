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

function loadHeatmap() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/multipath_heatmap/load/${day}`)
        .then(r => r.json())
        .then(data => {
            Plotly.newPlot("heatmap", [{
                z: data,
                type: "heatmap",
                colorscale: [
                    [0, "#2ecc71"],   // clean
                    [0.5, "#f1c40f"], // moderate
                    [1, "#e74c3c"]    // severe
                ]
            }], {
                margin: { t: 20 },
                xaxis: { title: "Azimuth (bins)" },
                yaxis: { title: "Elevation (bins)" }
            });
        });
}

loadDays();
