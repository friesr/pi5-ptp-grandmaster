function updateStatus() {
    fetch("/api/status/")
        .then(r => r.json())
        .then(data => {
            document.getElementById("status-block").innerText =
                JSON.stringify(data, null, 2);
        });
}

setInterval(updateStatus, 10000);
updateStatus();
