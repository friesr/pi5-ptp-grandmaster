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

function loadGNSSHistory() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/gnss_history/load/${day}`)
        .then(r => r.json())
        .then(rows => {
            const byPRN = {};

            rows.forEach(r => {
                if (!byPRN[r.prn]) byPRN[r.prn] = { x: [], y: [] };
                byPRN[r.prn].x.push(new Date(r.timestamp * 1000));
                byPRN[r.prn].y.push(r.snr);
            });

            const traces = Object.keys(byPRN).map(prn => ({
                x: byPRN[prn].x,
                y: byPRN[prn].y,
                mode: "lines",
                name: "PRN " + prn
            }));

            Plotly.newPlot("snr-history-chart", traces, {
                margin: { t: 20 },
                yaxis: { title: "SNR (dB-Hz)" },
                xaxis: { title: "Time" }
            });
        });
}

loadDays();
