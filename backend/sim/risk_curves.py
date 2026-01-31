function loadMCConfigs() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById("mc-select");
            sel.innerHTML = "";
            list.filter(f => f.endsWith("_mc.json")).forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                sel.appendChild(opt);
            });
        });
}

function runMC() {
    const cfg = document.getElementById("mc-select").value;

    fetch(`/api/digital_twin_monte_carlo/run/${cfg}`)
        .then(r => r.json())
        .then(data => {
            const rms = data.map(r => r.summary.rms_error);

            Plotly.newPlot("mc-chart", [{
                x: rms,
                type: "histogram"
            }], {
                margin: { t: 20 },
                xaxis: { title: "RMS Timing Error (ns)" }
            });

            document.getElementById("mc-output").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadMCConfigs();
