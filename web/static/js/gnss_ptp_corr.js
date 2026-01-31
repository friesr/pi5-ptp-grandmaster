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

function loadCorr() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/gnss_ptp_corr/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const x = data.map(d => new Date(d.ptp_event.timestamp * 1000));
            const y = data.map(d => d.ptp_event.type);

            const colors = data.map(d => {
                if (d.multipath > 0.6) return "#e67e22";
                if (d.snr_min < 10) return "#e74c3c";
                if (d.geometry_score < 40) return "#9b59b6";
                return "#2ecc71";
            });

            Plotly.newPlot("corr-chart", [{
                x: x,
                y: y,
                mode: "markers",
                marker: { size: 12, color: colors }
            }], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "PTP Event Type" }
            });

            const list = document.getElementById("corr-list");
            list.textContent = JSON.stringify(data, null, 2);
        });
}

loadDays();
