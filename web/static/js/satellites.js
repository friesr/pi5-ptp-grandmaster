function renderSkyplot(sats) {
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
}

function renderSNRChart(sats) {
    const prn = sats.map(s => "PRN " + s.prn);
    const snr = sats.map(s => s.snr);
    const used = sats.map(s => s.used);

    const colors = used.map(u => u ? "#1db954" : "#888");

    Plotly.newPlot("snr-chart", [{
        x: prn,
        y: snr,
        type: "bar",
        marker: { color: colors }
    }], {
        margin: { t: 20 },
        yaxis: { title: "SNR (dB-Hz)" }
    });
}

function renderConstellationChart(sats) {
    function constellationOf(prn) {
        if (prn >= 1 && prn <= 32) return "GPS";
        if (prn >= 65 && prn <= 96) return "GLONASS";
        if (prn >= 201 && prn <= 237) return "BeiDou";
        if (prn >= 301 && prn <= 336) return "Galileo";
        return "Other";
    }

    const counts = {};
    sats.forEach(s => {
        const c = constellationOf(s.prn);
        counts[c] = (counts[c] || 0) + 1;
    });

    Plotly.newPlot("constellation-chart", [{
        labels: Object.keys(counts),
        values: Object.values(counts),
        type: "pie"
    }], {
        margin: { t: 20 }
    });
}

function updateSatellites() {
    fetch("/api/status/")
        .then(r => r.json())
        .then(data => {
            const gnss = data.gnss;
            const sats = gnss.satellites;

            // Raw JSON block
            document.getElementById("satellite-block").innerText =
                JSON.stringify(gnss, null, 2);

            // Charts
            renderSkyplot(sats);
            renderSNRChart(sats);
            renderConstellationChart(sats);

            fetch("/api/multipath/scores")
                .then(r => r.json())
                .then(scores => renderMultipathChart(scores));

        });
}

setInterval(updateSatellites, 10000);
updateSatellites();


function renderMultipathChart(scores) {
    Plotly.newPlot("multipath-chart", [{
        x: scores.map(s => "PRN " + s.prn),
        y: scores.map(s => s.multipath_score),
        type: "bar",
        marker: {
            color: scores.map(s => {
                if (s.multipath_score > 0.7) return "#e74c3c";   // severe
                if (s.multipath_score > 0.4) return "#f1c40f";   // moderate
                return "#2ecc71";                                // clean
            })
        }
    }], {
        margin: { t: 20 },
        yaxis: { title: "Multipath Score (0 = clean, 1 = severe)" }
    });
}
