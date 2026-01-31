function loadProfiles() {
    fetch("/static/ptp_profiles.json")
        .then(r => r.json())
        .then(profiles => {
            const sel = document.getElementById("profile-select");
            sel.innerHTML = "";

            Object.keys(profiles).forEach(name => {
                const opt = document.createElement("option");
                opt.value = name;
                opt.textContent = name;
                sel.appendChild(opt);
            });

            sel.onchange = () => {
                const p = profiles[sel.value];
                document.getElementById("profile-desc").innerText =
                    p.description;
            };

            sel.onchange();
        });
}

function applyProfile() {
    const name = document.getElementById("profile-select").value;

    fetch("/api/ptp_profile/apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ profile: name })
    })
    .then(r => r.json())
    .then(resp => {
        alert("Profile applied: " + resp.applied);
    });
}

loadProfiles();
