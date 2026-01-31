let ptpData = [];
let ntpData = [];
let gnssVisible = [];
let gnssUsed = [];
let timestamps = [];

function updateStatus() {
    fetch("/api/status/")
        .then(r => r.json())
        .then(data => {
            document.getElementById("status-block").innerText =
                JSON.stringify(data, null, 2);

            const ts = new Date().toLocaleTimeString();

            timestamps.push(ts);
            ptpData.push(data.ptp.offset_ns);
            ntpData.push(data.ntp.offset_ms);
            gnssVisible.push(data.gnss.visible);
            gnssUsed.push(data.gnss.used);

            if (timestamps.length > 50) {
                timestamps.shift();
                ptpData.shift();
                ntpData.shift();
                gnssVisible.shift();
                gnssUsed.shift();
            }

            Plotly.newPlot("ptp-chart", [{
                x: timestamps,
                y: ptpData,
                mode: "lines",
                line: { color: "#1db954" }
            }], { margin: { t: 20 } });

            Plotly.newPlot("ntp-chart", [{
                x: timestamps,
                y: ntpData,
                mode: "lines",
                line: { color: "#4be27a" }
            }], { margin: { t: 20 } });

            Plotly.newPlot("gnss-chart", [
                {
                    x: timestamps,
                    y: gnssVisible,
                    name: "Visible",
                    mode: "lines",
                    line: { color: "#1db954" }
                },
                {
                    x: timestamps,
                    y: gnssUsed,
                    name: "Used",
                    mode: "lines",
                    line: { color: "#4be27a" }
                }
            ], { margin: { t: 20 } });
        });
}

setInterval(updateStatus, 10000);
updateStatus();

function updateAdev() {
    fetch("/api/allan/adev")
        .then(r => r.json())
        .then(data => {
            Plotly.newPlot("adev-chart", [{
                x: data.tau,
                y: data.adev,
                mode: "lines+markers",
                line: { color: "#1db954" }
            }], {
                xaxis: { title: "Tau (s)" },
                yaxis: { title: "ADEV (ns)" },
                margin: { t: 20 }
            });
        });
}

setInterval(updateAdev, 30000);
updateAdev();
