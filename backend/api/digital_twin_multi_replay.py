let replayData = [];
let index = 0;
let playing = false;
let timer = null;

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

function loadReplay() {
    const scenario = document.getElementById("scenario-select").value;

    fetch(`/api/digital_twin_replay/run/${scenario}`)
        .then(r => r.json())
        .then(data => {
            replayData = data.results;
            index = 0;
            document.getElementById("timeline").max = replayData.length - 1;
            updateFrame();
        });
}

function updateFrame() {
    if (!replayData.length) return;

    const s = replayData[index];

    Plotly.newPlot("replay-chart", [{
        x: [s.timestamp],
        y: [s.timing_output],
        mode: "markers",
        marker: { size: 12 }
    }], {
        margin: { t: 20 },
        xaxis: { title: "Timestamp" },
        yaxis: { title: "Timing Error (ns)" }
    });

    document.getElementById("sample-output").textContent =
        JSON.stringify(s, null, 2);

    document.getElementById("timeline").value = index;
}

function play() {
    if (playing) return;
    playing = true;

    timer = setInterval(() => {
        index++;
        if (index >= replayData.length) {
            pause();
            return;
        }
        updateFrame();
    }, 100);
}

function pause() {
    playing = false;
    clearInterval(timer);
}

function stepForward() {
    index = Math.min(index + 1, replayData.length - 1);
    updateFrame();
}

function stepBack() {
    index = Math.max(index - 1, 0);
    updateFrame();
}

function scrub() {
    index = Number(document.getElementById("timeline").value);
    updateFrame();
}

loadScenarios();
