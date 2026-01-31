function updateSatellites() {
    fetch("/api/status/")
        .then(r => r.json())
        .then(data => {
            document.getElementById("satellite-block").innerText =
                JSON.stringify(data.gnss, null, 2);
        });
}

setInterval(updateSatellites, 10000);
updateSatellites();
