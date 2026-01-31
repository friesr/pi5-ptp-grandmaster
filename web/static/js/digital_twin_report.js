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

function generateReport() {
    const scenario = document.getElementById("scenario-select").value;

    fetch(`/api/digital_twin_report/generate/${scenario}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("report-output").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadScenarios();
