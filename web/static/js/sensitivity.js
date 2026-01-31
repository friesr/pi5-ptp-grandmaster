function loadSweeps() {
    fetch("/api/gnss_history/scenarios")
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById("sweep-select");
            sel.innerHTML = "";
            list.filter(f => f.endsWith("_sweep.json")).forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                sel.appendChild(opt);
            });
        });
}

function runSweep() {
    const sweep = document.getElementById("sweep-select").value;

    fetch(`/api/sensitivity/run/${sweep}`)
        .then(r => r.json())
        .then(data => {
            renderTable(data);
        });
}

function renderTable(data) {
    const el = document.getElementById("sweep-table");

    let html = `
        <table>
            <tr>
                <th>Parameters</th>
                <th>Max Error</th>
                <th>Min Error</th>
                <th>RMS Error</th>
            </tr>
    `;

    data.forEach(row => {
        const p = JSON.stringify(row.parameters);
        const s = row.summary;

        html += `
            <tr>
                <td>${p}</td>
                <td>${s.max_error.toFixed(2)}</td>
                <td>${s.min_error.toFixed(2)}</td>
                <td>${s.rms_error.toFixed(2)}</td>
            </tr>
        `;
    });

    html += "</table>";
    el.innerHTML = html;
}

loadSweeps();
