function loadGAConfigs() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById("ga-select");
            sel.innerHTML = "";
            list.filter(f => f.endsWith("_ga.json")).forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                sel.appendChild(opt);
            });
        });
}

function runGA() {
    const cfg = document.getElementById("ga-select").value;

    fetch(`/api/digital_twin_evolve/run/${cfg}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("ga-output").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadGAConfigs();
