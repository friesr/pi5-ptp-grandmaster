function loadLibrary() {
    fetch("/api/scenario_library/list")
        .then(r => r.json())
        .then(data => {
            let html = "<ul>";
            for (const category in data) {
                html += `<li><strong>${category}</strong><ul>`;
                data[category].forEach(f => {
                    html += `<li>${f}</li>`;
                });
                html += "</ul></li>";
            }
            html += "</ul>";
            document.getElementById("library").innerHTML = html;
        });
}

loadLibrary();
