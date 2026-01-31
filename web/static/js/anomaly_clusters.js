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

function loadClusters() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/anomaly_clusters/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const rows = data.rows;

            const x = rows.map(r => new Date(r.timestamp * 1000));
            const y = rows.map(r => r.cluster);

            Plotly.newPlot("cluster-chart", [{
                x: x,
                y: y,
                mode: "markers",
                marker: { size: 8 }
            }], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Cluster ID" }
            });

            document.getElementById("cluster-centers").textContent =
                JSON.stringify(data.centers, null, 2);
        });
}

loadDays();
