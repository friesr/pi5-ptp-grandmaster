function loadAging() {
    fetch("/api/satellite_aging/analyze")
        .then(r => r.json())
        .then(data => {
            document.getElementById("aging-output").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadAging();
