function updateSatellites() {
    fetch("/api/status/")
        .then(r => r.json())
        .then(data => {
            const gnss = data.gnss;
            document.getElementById("satellite-block").innerText =
                JSON.stringify(gnss, null, 2);

            const sats = gnss.satellites;

            const az = sats.map(s => s.azimuth);
            const el = sats.map(s => 90 - s.elevation);  // invert for polar plot
            const snr = sats.map(s => s.snr);
            const used = sats.map(s => s.used ? "Used" : "Visible");

            const trace = {
                type: "scatterpolar",
                mode: "markers",
                r: el,
                theta: az,
                marker: {
                    size: 12,
                    color: snr,
                    colorscale: "Viridis",
                    colorbar: { title: "SNR" },
                    line: {
                        width: 2,
                        color: used.map(u => u === "Used" ? "#1db954" : "#888")
                    }
                },
                text: sats.map(s => `PRN ${s.prn}<br>SNR ${s.snr}`),
                hoverinfo: "text"
            };

            const layout = {
                polar: {
                    radialaxis: { visible: true, range: [0, 90] },
                    angularaxis: { direction: "clockwise" }
                },
                margin: { t: 20 }
            };

            Plotly.newPlot("skyplot", [trace], layout);
        });
}

setInterval(updateSatellites, 10000);
updateSatellites();
