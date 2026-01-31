function loadPredictive() {
    fetch("/api/predictive/load")
        .then(r => r.json())
        .then(data => {
            document.getElementById("forecast").textContent =
                JSON.stringify(data, null, 2);
        });
}

loadPredictive();
