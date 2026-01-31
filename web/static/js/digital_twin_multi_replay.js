let replaySets = {};
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

function loadMultiReplay() {
    const sel = document.getElementById("scenario-select");
    const scenarios = Array.from(sel.selectedOptions).map(o => o.value);

    fetch("/api/digital_twin_multi_replay/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenarios })
    })
    .then(r => r.json())
    .then(data => {
        replaySets = data;
        index = 0;

        // Set timeline max to the shortest scenario length
        const lengths = Object.values(replaySets)
            .filter(v => Array.isArray(v))
            .map(v => v.length);

        document.getElementById("timeline").max = Math.min(...lengths) - 1;

        updateFrame();
    });
}

function updateFrame() {
    const traces = [];
    const sampleDump = {};

    for (const [name, results] of Object.entries(replaySets)) {
        if (!Array.isArray(results)) continue;

        const s = results[index];
        sampleDump[name] = s;

        traces.push({
            x: [s.timestamp],
            y: [s.timing_output],
            mode: "markers",
            name: name,
            marker: { size: 10 }
        });
    }

    Plotly.newPlot("multi-chart", traces, {
        margin: { t: 20 },
        xaxis: { title: "Timestamp" },
        yaxis: { title: "Timing Error (ns)" }
    });

    document.getElementById("sample-output").textContent =
        JSON.stringify(sampleDump, null, 2);

    document.getElementById("timeline").value = index;
}

function play() {
    if (playing) return;
    playing = true;

    timer = setInterval(() => {
        index++;
        const max = Number(document.getElementById("timeline").max);
        if (index >= max) {
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
    const max = Number(document.getElementById("timeline").max);
    index = Math.min(index + 1, max);
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
