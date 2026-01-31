let frames = [];
let frameIndex = 0;
let timer = null;
let speed = 500; // ms per frame

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

function loadPlayback() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/skyplot_playback/load/${day}`)
        .then(r => r.json())
        .then(data => {
            frames = data;
            frameIndex = 0;
            drawFrame();
        });
}

function drawFrame() {
    if (frames.length === 0) return;

    const f = frames[frameIndex];
    const sats = f.satellites;

    const r = sats.map(s => 90 - s.elevation);
    const theta = sats.map(s => s.azimuth);
    const labels = sats.map(s => "PRN " + s.prn);

    Plotly.newPlot("skyplot", [{
        type: "scatterpolar",
        mode: "markers+text",
        r: r,
        theta: theta,
        text: labels,
        textposition: "top center",
        marker: { size: 10 }
    }], {
        polar: {
            radialaxis: { visible: true, range: [0, 90] },
            angularaxis: { direction: "clockwise" }
        },
        margin: { t: 20 }
    });
}

function play() {
    if (timer) return;
    timer = setInterval(() => {
        frameIndex = (frameIndex + 1) % frames.length;
        drawFrame();
    }, speed);
}

function pause() {
    clearInterval(timer);
    timer = null;
}

function faster() {
    speed = Math.max(50, speed - 100);
    if (timer) {
        pause();
        play();
    }
}

function slower() {
    speed += 100;
    if (timer) {
        pause();
        play();
    }
}

loadDays();
