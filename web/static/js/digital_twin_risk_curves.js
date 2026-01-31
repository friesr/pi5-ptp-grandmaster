function loadMCConfigs() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById("rc-select");
            sel.innerHTML = "";
            list.filter(f => f.endsWith("_mc.json")).forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                sel.appendChild(opt);
            });
        });
}

function runRisk() {
    const cfg = document.getElementById("rc-select").value;

    fetch(`/api/digital_twin_risk/run/${cfg}`)
        .then(r => r.json())
        .then(data => {
            // PDF
            Plotly.newPlot("pdf-chart", [{
                x: data.pdf.x,
                y: data.pdf.y,
                type: "bar"
            }], {
                margin: { t: 20 },
                xaxis: { title: "RMS Error (ns)" },
                yaxis: { title: "Density" }
            });

            // CDF
            Plotly.newPlot("cdf-chart", [{
                x: data.cdf.x,
                y: data.cdf.y,
                type: "scatter"
            }], {
                margin: { t: 20 },
                xaxis: { title: "RMS Error (ns)" },
                yaxis: { title: "Cumulative Probability" }
            });

            document.getElementById("percentiles").textContent =
                JSON.stringify(data.percentiles, null, 2);

            document.getElementById("exceedance").textContent =
                JSON.stringify(data.exceedance, null, 2);
        });
}

loadMCConfigs();
