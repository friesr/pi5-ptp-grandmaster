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

function runEvents() {
    const scenario = document.getElementById("scenario-select").value;

    fetch(`/api/digital_twin_events/run/${scenario}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("event-output").textContent =
                JSON.stringify(data.events, null, 2);
        });
}

loadScenarios();
