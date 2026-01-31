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

function loadOutages() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/gnss_outages/load/${day}`)
        .then(r => r.json())
        .then(data => {
            if (data.length === 0) {
                Plotly.newPlot("outage-chart", [], {
                    margin: { t: 20 },
                    xaxis: { title: "Time" },
                    yaxis: { title: "Duration (sec)" }
                });
                return;
            }

            const xStart = data.map(o => new Date(o.start * 1000));
            const xEnd = data.map(o => new Date(o.end * 1000));
            const durations = data.map(o => o.duration_sec);

            // Represent outages as horizontal bars
            const traces = data.map((o, idx) => ({
                x: [new Date(o.start * 1000), new Date(o.end * 1000)],
                y: [idx, idx],
                mode: "lines",
                line: { width: 8, color: "#e74c3c" },
                showlegend: false
            }));

            Plotly.newPlot("outage-chart", traces, {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: {
                    title: "Outage index",
                    showticklabels: false
                }
            });
        });
}

loadDays();
