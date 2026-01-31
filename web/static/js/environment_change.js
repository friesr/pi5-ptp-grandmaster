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

function loadChange() {
    const day = document.getElementById("day-select").value;

    fetch(`/api/environment_change/load/${day}`)
        .then(r => r.json())
        .then(data => {
            const el = document.getElementById("status");

            let color = "#2ecc71";
            if (data.status === "mild_change") color = "#f1c40f";
            if (data.status === "significant_change") color = "#e67e22";
            if (data.status === "critical_change") color = "#e74c3c";

            el.style.color = color;
            el.textContent = data.status.replace("_", " ").toUpperCase();

            document.getElementById("factors").textContent =
                JSON.stringify(data.factors, null, 2);
        });
}

loadDays();
