function loadScenarios() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById("scenario-select");
            sel.innerHTML = "";
            list.forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                sel.appendChild(opt);
            });
        });
}

function runSimulation() {
    const scenario = document.getElementById("scenario-select").value;

    fetch(`/api/digital_twin/run/${scenario}`)
        .then(r => r.json())
        .then(data => {
            const results = data.results;

            // Plot timing output
            const x = results.map(r => r.timestamp);
            const y = results.map(r => r.timing_output);

            Plotly.newPlot("timing-chart", [{
                x: x,
                y: y,
                type: "scatter"
            }], {
                margin: { t: 20 },
                yaxis: { title: "Simulated Timing Error (ns)" }
            });

            // Raw output
            document.getElementById("sim-output").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadScenarios();
