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

function loadInterference() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/interference/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const x = data.map(e => new Date(e.timestamp * 1000));
            const y = data.map(e => e.type);

            const colors = data.map(e => {
                if (e.type === "jamming") return "#e74c3c";
                if (e.type === "spoofing") return "#9b59b6";
                return "#f1c40f"; // rf_noise
            });

            Plotly.newPlot("interference-chart", [{
                x: x,
                y: y,
                mode: "markers",
                marker: { size: 12, color: colors }
            }], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Interference Type" }
            });

            document.getElementById("interference-details").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadDays();
