function loadServices() {
    fetch("/api/services/list")
        .then(r => r.json())
        .then(services => {
            const table = document.getElementById("service-table");
            table.innerHTML = "";

            services.forEach(name => {
                const row = document.createElement("tr");

                const nameCell = document.createElement("td");
                nameCell.textContent = name;

                const statusCell = document.createElement("td");
                statusCell.id = "status-" + name;

                const btnStart = document.createElement("button");
                btnStart.textContent = "Start";
                btnStart.onclick = () => action(name, "start");

                const btnStop = document.createElement("button");
                btnStop.textContent = "Stop";
                btnStop.onclick = () => action(name, "stop");

                const btnRestart = document.createElement("button");
                btnRestart.textContent = "Restart";
                btnRestart.onclick = () => action(name, "restart");

                const btnCell = document.createElement("td");
                btnCell.appendChild(btnStart);
                btnCell.appendChild(btnStop);
                btnCell.appendChild(btnRestart);

                row.appendChild(nameCell);
                row.appendChild(statusCell);
                row.appendChild(btnCell);

                table.appendChild(row);

                updateStatus(name);
            });
        });
}

function updateStatus(name) {
    fetch(`/api/services/status/${name}`)
        .then(r => r.json())
        .then(data => {
            const cell = document.getElementById("status-" + name);
            cell.textContent = data.active ? "Active" : "Inactive";
            cell.style.color = data.active ? "#2ecc71" : "#e74c3c";
        });
}

function action(name, act) {
    fetch("/api/services/action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ service: name, action: act })
    })
    .then(r => r.json())
    .then(() => updateStatus(name));
}

loadServices();
setInterval(() => {
    fetch("/api/services/list")
        .then(r => r.json())
        .then(services => services.forEach(updateStatus));
}, 5000);
