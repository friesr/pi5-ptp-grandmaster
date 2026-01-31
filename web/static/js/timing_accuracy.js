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

function loadAccuracy() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/timing_accuracy/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const x = data.map(d => new Date(d.timestamp * 1000));
            const y = data.map(d => d.timing_error_ns);

            Plotly.newPlot("accuracy-chart", [{
                x: x,
                y: y,
                mode: "lines",
                name: "Predicted Timing Error (ns)"
            }], {
                margin: { t: 20 },
                yaxis: { title: "Timing Error (ns)" },
                xaxis: { title: "Time" }
            });
        });
}

loadDays();
