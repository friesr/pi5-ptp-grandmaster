function updateValidation() {
    fetch("/api/validation/status")
        .then(r => r.json())
        .then(data => {
            document.getElementById("validation-block").innerText =
                JSON.stringify(data, null, 2);
        });
}

setInterval(updateValidation, 10000);
updateValidation();
