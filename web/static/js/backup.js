function downloadBackup() {
    window.location = "/api/backup/export";
}

function restoreBackup() {
    const fileInput = document.getElementById("backup-file");
    const status = document.getElementById("restore-status");

    if (fileInput.files.length === 0) {
        status.innerText = "No file selected";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/api/backup/restore", {
        method: "POST",
        body: formData
    })
    .then(r => r.json())
    .then(resp => {
        status.innerText = JSON.stringify(resp, null, 2);
    });
}
