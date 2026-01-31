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

function loadTimeline() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/unified_timeline/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const x = data.map(e => new Date(e.timestamp * 1000));
            const y = data.map(e => e.type);

            const colors = data.map(e => {
                if (e.type.startsWith("ptp")) return "#3498db";
                if (e.type.startsWith("gnss")) return "#2ecc71";
                if (e.type.startsWith("interference")) return "#e74c3c";
                if (e.type.startsWith("receiver")) return "#9b59b6";
                if (e.type.startsWith("environment")) return "#f1c40f";
                if (e.type.startsWith("sla")) return "#e67e22";
                return "#95a5a6";
            });

            Plotly.newPlot("timeline-chart", [{
                x: x,
                y: y,
                mode: "markers",
                marker: { size: 10, color: colors }
            }], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Event Type" }
            });

            document.getElementById("timeline-details").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadDays();
