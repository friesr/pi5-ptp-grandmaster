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

function load3D() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/multipath_3d/reconstruct/${day}`)
        .then(r => r.json())
        .then(points => {
            Plotly.newPlot("plot3d", [{
                x: points.map(p => p.x),
                y: points.map(p => p.y),
                z: points.map(p => p.z),
                mode: "markers",
                marker: {
                    size: 4,
                    color: points.map(p => p.probability),
                    colorscale: "Viridis",
                    opacity: 0.8
                },
                type: "scatter3d"
            }], {
                margin: { t: 20 },
                scene: {
                    xaxis: { title: "X (m)" },
                    yaxis: { title: "Y (m)" },
                    zaxis: { title: "Z (m)" }
                }
            });
        });
}

loadDays();
