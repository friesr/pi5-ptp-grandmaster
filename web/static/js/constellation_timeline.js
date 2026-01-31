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

    fetch(`/api/constellation_timeline/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const traces = [];
            const constellations = Object.keys(data);

            constellations.forEach((c, idx) => {
                const intervals = data[c];

                intervals.forEach(interval => {
                    traces.push({
                        x: [
                            new Date(interval.start * 1000),
                            new Date(interval.end * 1000)
                        ],
                        y: [c, c],
                        mode: "lines",
                        line: { width: 8 },
                        name: c,
                        showlegend: false
                    });
                });
            });

            Plotly.newPlot("timeline-chart", traces, {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Constellation" }
            });
        });
}

loadDays();
