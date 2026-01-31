function loadDays() {
    fetch("/api/history/days")
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

function loadHistory() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/history/load/${day}`)
        .then(r => r.json())
        .then(data => {
            // PTP chart
            Plotly.newPlot("ptp-history", [{
                x: data.ptp.map(r => new Date(r.timestamp * 1000)),
                y: data.ptp.map(r => parseFloat(r.offset_ns)),
                mode: "lines",
                line: { color: "#1db954" }
            }]);

            // NTP chart
            Plotly.newPlot("ntp-history", [{
                x: data.ntp.map(r => new Date(r.timestamp * 1000)),
                y: data.ntp.map(r => parseFloat(r.offset_ms)),
                mode: "lines",
                line: { color: "#4be27a" }
            }]);

            // GNSS chart
            Plotly.newPlot("gnss-history", [
                {
                    x: data.gnss.map(r => new Date(r.timestamp * 1000)),
                    y: data.gnss.map(r => parseInt(r.visible)),
                    name: "Visible",
                    mode: "lines",
                    line: { color: "#1db954" }
                },
                {
                    x: data.gnss.map(r => new Date(r.timestamp * 1000)),
                    y: data.gnss.map(r => parseInt(r.used)),
                    name: "Used",
                    mode: "lines",
                    line: { color: "#4be27a" }
                }
            ]);
        });
}

loadDays();
