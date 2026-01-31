function loadDays() {
    fetch("/api/gnss_history/days")
        .then(r => r.json())
        .then(days => {
            const sel = document.getElementById("base-day");
            sel.innerHTML = "";
            days.forEach(d => {
                const opt = document.createElement("option");
                opt.value = d;
                opt.textContent = d;
                sel.appendChild(opt);
            });
        });
}

function buildScenario() {
    return {
        scenario_name: document.getElementById("scenario-name").value,
        base_day: document.getElementById("base-day").value,
        perturbations: {
            gnss_outage: {
                start: Number(document.getElementById("outage-start").value),
                duration: Number(document.getElementById("outage-duration").value)
            },
            interference: {
                severity: Number(document.getElementById("int-severity").value),
                start: Number(document.getElementById("int-start").value),
                duration: Number(document.getElementById("int-duration").value)
            },
            spoofing: {
                start: Number(document.getElementById("sp-start").value),
                duration: Number(document.getElementById("sp-duration").value)
            },
            multipath_boost: {
                factor: Number(document.getElementById("mp-factor").value)
            },
            constellation_failure: {
                constellation: document.getElementById("cf-const").value,
                start: Number(document.getElementById("cf-start").value),
                duration: Number(document.getElementById("cf-duration").value)
            },
            receiver_health_drop: {
                score: Number(document.getElementById("rh-score").value)
            }
        },
        servo_adjustments: {
            kp: Number(document.getElementById("kp").value),
            ki: Number(document.getElementById("ki").value)
        }
    };
}

function updatePreview() {
    const scenario = buildScenario();
    document.getElementById("preview").textContent =
        JSON.stringify(scenario, null, 2);
}

function saveScenario() {
    const scenario = buildScenario();

    fetch("/api/scenario/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(scenario)
    })
    .then(r => r.json())
    .then(data => {
        alert("Scenario saved: " + data.file);
    });
}

setInterval(updatePreview, 500);
loadDays();
