function loadOptFiles() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById("opt-select");
            sel.innerHTML = "";
            list.filter(f => f.endsWith("_opt.json")).forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                sel.appendChild(opt);
            });
        });
}

function runOptimization() {
    const opt = document.getElementById("opt-select").value;

    fetch(`/api/digital_twin_optimize/run/${opt}`)
        .then(r => r.json())
        .then(data => {
            renderTable(data);
        });
}

function renderTable(data) {
    const el = document.getElementById("opt-table");

    let html = `
        <table>
            <tr>
                <th>Parameters</th>
                <th>Max Error</th>
                <th>RMS Error</th>
                <th>Score</th>
            </tr>
    `;

    data.forEach(row => {
        const p = JSON.stringify(row.parameters);
        const s = row.summary;

        html += `
            <tr>
                <td>${p}</td>
                <td>${s.max_error.toFixed(2)}</td>
                <td>${s.rms_error.toFixed(2)}</td>
                <td>${row.score.toFixed(2)}</td>
            </tr>
        `;
    });

    html += "</table>";
    el.innerHTML = html;
}

loadOptFiles();
