function updateSystemHealth() {
    fetch("/api/system_health/status")
        .then(r => r.json())
        .then(data => {
            document.getElementById("system-block").innerText =
                JSON.stringify(data.system, null, 2);

            const services = data.services;
            const ul1 = document.getElementById("service-list");
            ul1.innerHTML = "";
            Object.keys(services).forEach(name => {
                const li = document.createElement("li");
                li.textContent = `${name}: ${services[name] ? "OK" : "DOWN"}`;
                li.style.color = services[name] ? "#2ecc71" : "#e74c3c";
                ul1.appendChild(li);
            });

            const network = data.network;
            const ul2 = document.getElementById("network-list");
            ul2.innerHTML = "";
            Object.keys(network).forEach(name => {
                const li = document.createElement("li");
                li.textContent = `${name}: ${network[name] ? "OK" : "FAIL"}`;
                li.style.color = network[name] ? "#2ecc71" : "#e74c3c";
                ul2.appendChild(li);
            });
        });
}

setInterval(updateSystemHealth, 10000);
updateSystemHealth();
