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

function loadEvents() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/ptp_events/load/${day}`)
        .then(r => r.json())
        .then(events => {
            const x = events.map(e => new Date(e.timestamp * 1000));
            const y = events.map(e => e.type);
            const colors = events.map(e => {
                if (e.severity === "error") return "#e74c3c";
                if (e.severity === "warning") return "#f1c40f";
                if (e.severity === "success") return "#2ecc71";
                return "#3498db";
            });

            Plotly.newPlot("event-chart", [{
                x: x,
                y: y,
                mode: "markers",
                marker: { size: 10, color: colors }
            }], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Event Type" }
            });

            const list = document.getElementById("event-list");
            list.textContent = events.map(e => e.raw).join("\n");
        });
}

loadDays();
