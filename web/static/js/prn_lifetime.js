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

function loadLifetime() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/prn_lifetime/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const prns = Object.keys(data);

            const visible = prns.map(p => data[p].visible_minutes);
            const used = prns.map(p => data[p].used_minutes);

            Plotly.newPlot("lifetime-chart", [
                {
                    x: prns,
                    y: visible,
                    name: "Visible (min)",
                    type: "bar"
                },
                {
                    x: prns,
                    y: used,
                    name: "Used (min)",
                    type: "bar"
                }
            ], {
                barmode: "group",
                margin: { t: 20 },
                yaxis: { title: "Minutes" }
            });
        });
}

loadDays();
