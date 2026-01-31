function loadScenarios() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const a = document.getElementById("scenario-a");
            const b = document.getElementById("scenario-b");

            list.forEach(s => {
                const optA = document.createElement("option");
                optA.value = s;
                optA.textContent = s;
                a.appendChild(optA);

                const optB = document.createElement("option");
                optB.value = s;
                optB.textContent = s;
                b.appendChild(optB);
            });
        });
}

function runDiff() {
    const scenarioA = document.getElementById("scenario-a").value;
    const scenarioB = document.getElementById("scenario-b").value;

    fetch("/api/digital_twin_diff/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            scenario_a: scenarioA,
            scenario_b: scenarioB
        })
    })
    .then(r => r.json())
    .then(data => {
        const diffs = data.diffs;

        Plotly.newPlot("delta-chart", [{
            x: diffs.map(d => d.timestamp),
            y: diffs.map(d => d.timing_error_delta),
            type: "scatter"
        }], {
            margin: { t: 20 },
            xaxis: { title: "Timestamp" },
            yaxis: { title: "Timing Error Delta (ns)" }
        });

        document.getElementById("summary-output").textContent =
            JSON.stringify(data.summary, null, 2);

        document.getElementById("diff-output").textContent =
            JSON.stringify(diffs, null, 2);
    });
}

loadScenarios();
