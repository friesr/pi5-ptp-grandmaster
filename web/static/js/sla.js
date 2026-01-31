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

function loadSLA() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/sla/load/${day}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("sla-results").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadDays();
