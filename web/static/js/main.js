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


function updateDrift() {
    fetch("/api/drift/model")
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                return;
            }

            Plotly.newPlot("drift-chart", [{
                x: data.future_times_sec,
                y: data.future_predictions_ns,
                mode: "lines+markers",
                line: { color: "#4be27a" }
            }], {
                xaxis: { title: "Seconds into Future" },
                yaxis: { title: "Predicted Offset (ns)" },
                margin: { t: 20 }
            });
        });
}

function updateTempDrift() {
    fetch("/api/temp_drift/model")
        .then(r => r.json())
        .then(data => {
            if (data.error) return;

            Plotly.newPlot("temp-drift-chart", [{
                x: data.temps_c,
                y: data.predicted_offsets_ns,
                mode: "lines+markers",
                line: { color: "#e6b422" }
            }], {
                xaxis: { title: "Temperature (°C)" },
                yaxis: { title: "Predicted Offset (ns)" },
                margin: { t: 20 }
            });
        });
}

setInterval(updateTempDrift, 30000);
updateTempDrift();

setInterval(updateDrift, 30000);
updateDrift();

let servoTimes = [];
let servoFreq = [];

function updateServo() {
    fetch("/api/ptp_servo/status")
        .then(r => r.json())
        .then(data => {
            document.getElementById("servo-block").innerText =
                JSON.stringify(data, null, 2);

            const ts = new Date().toLocaleTimeString();

            servoTimes.push(ts);
            servoFreq.push(data.freq_adj_ppb);

            if (servoTimes.length > 50) {
                servoTimes.shift();
                servoFreq.shift();
            }

            Plotly.newPlot("servo-chart", [{
                x: servoTimes,
                y: servoFreq,
                mode: "lines",
                line: { color: "#e67e22" }
            }], {
                margin: { t: 20 },
                yaxis: { title: "Frequency Adjustment (ppb)" }
            });
        });
}

setInterval(updateServo, 10000);
updateServo();

function updateAlerts() {
    fetch("/api/alerts/current")
        .then(r => r.json())
        .then(alerts => {
            const ul = document.getElementById("alerts-list");
            ul.innerHTML = "";

            if (alerts.length === 0) {
                const li = document.createElement("li");
                li.textContent = "No active alerts";
                ul.appendChild(li);
                return;
            }

            alerts.forEach(a => {
                const li = document.createElement("li");
                li.textContent = `[${a.severity.toUpperCase()}] ${a.message}`;
                ul.appendChild(li);
            });
        });
}

setInterval(updateAlerts, 10000);
updateAlerts();

function updateServoStability() {
    fetch("/api/servo_stability/current")
        .then(r => r.json())
        .then(data => {
            document.getElementById("servo-stability-block").innerText =
                JSON.stringify(data, null, 2);
        });
}

setInterval(updateServoStability, 15000);
updateServoStability();

document.getElementById("nas-block").innerText =
    JSON.stringify(data.storage.nas_health, null, 2);
