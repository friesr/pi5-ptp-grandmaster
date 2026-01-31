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

function loadFadeEvents() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/fade_events/load/${day}`)
        .then(r => r.json())
        .then(events => {
            const fadeIn = events.filter(e => e.type === "fade_in");
            const fadeOut = events.filter(e => e.type === "fade_out");

            const traceIn = {
                x: fadeIn.map(e => new Date(e.timestamp * 1000)),
                y: fadeIn.map(e => "PRN " + e.prn),
                mode: "markers",
                marker: { color: "#2ecc71", size: 10 },
                name: "Fade In"
            };

            const traceOut = {
                x: fadeOut.map(e => new Date(e.timestamp * 1000)),
                y: fadeOut.map(e => "PRN " + e.prn),
                mode: "markers",
                marker: { color: "#e74c3c", size: 10 },
                name: "Fade Out"
            };

            Plotly.newPlot("fade-chart", [traceIn, traceOut], {
                margin: { t: 20 },
                xaxis: { title: "Time" },
                yaxis: { title: "Satellite (PRN)" }
            });
        });
}

loadDays();
