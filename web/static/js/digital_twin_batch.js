function runBatch() {
    fetch("/api/digital_twin_batch/run")
        .then(r => r.json())
        .then(data => {
            renderTable(data);
        });
}

function renderTable(data) {
    const el = document.getElementById("batch-table");

    let html = `
        <table>
            <tr>
                <th>Scenario</th>
                <th>Max Error (ns)</th>
                <th>Min Error (ns)</th>
                <th>RMS Error (ns)</th>
            </tr>
    `;

    data.forEach(row => {
        const s = row.summary;
        html += `
            <tr>
                <td>${row.scenario}</td>
                <td>${s.max_error.toFixed(2)}</td>
                <td>${s.min_error.toFixed(2)}</td>
                <td>${s.rms_error.toFixed(2)}</td>
            </tr>
        `;
    });

    html += "</table>";
    el.innerHTML = html;
}
