function loadConfig() {
    fetch("/api/config/")
        .then(r => r.json())
        .then(cfg => {
            document.getElementById("refresh-rate").value = cfg.refresh_rate_ms;
            document.getElementById("ntp-period").value = cfg.ntp_poll_hours;
            document.getElementById("local-max").value = cfg.local_max_gb;
            document.getElementById("nas-max").value = cfg.nas_max_gb;

            const gpsList = document.getElementById("gps-list");
            gpsList.innerHTML = "";

            const options = ["stratux", "vk162", "vk172", "neom8t"];

            options.forEach(opt => {
                const checked = cfg.gps_receivers.includes(opt) ? "checked" : "";
                gpsList.innerHTML += `
                    <label>
                        <input type="checkbox" value="${opt}" ${checked}>
                        ${opt}
                    </label><br>
                `;
            });
        });
}

document.getElementById("save-refresh").onclick = () => {
    const value = parseInt(document.getElementById("refresh-rate").value);
    fetch("/api/config/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({refresh_rate_ms: value})
    });
};

document.getElementById("save-gps").onclick = () => {
    const selected = [...document.querySelectorAll("#gps-list input:checked")]
        .map(x => x.value);

    fetch("/api/config/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({gps_receivers: selected})
    });
};

document.getElementById("save-ntp").onclick = () => {
    const value = parseFloat(document.getElementById("ntp-period").value);
    fetch("/api/config/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ntp_poll_hours: value})
    });
};

document.getElementById("save-storage").onclick = () => {
    const local = parseFloat(document.getElementById("local-max").value);
    const nas = parseFloat(document.getElementById("nas-max").value);

    fetch("/api/config/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            local_max_gb: local,
            nas_max_gb: nas
        })
    });
};

loadConfig();
