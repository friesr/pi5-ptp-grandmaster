let rules = {};

function loadRules() {
    fetch("/api/alert_rules/get")
        .then(r => r.json())
        .then(data => {
            rules = data;
            renderRules();
        });
}

function renderRules() {
    const container = document.getElementById("rules-container");
    container.innerHTML = "";

    Object.keys(rules).forEach(id => {
        const r = rules[id];

        const div = document.createElement("div");
        div.className = "rule-block";

        div.innerHTML = `
            <h3>${id}</h3>
            <label>Enabled: <input type="checkbox" id="${id}-enabled" ${r.enabled ? "checked" : ""}></label><br>
            <label>Severity: <input type="text" id="${id}-severity" value="${r.severity}"></label><br>
            <label>Message: <input type="text" id="${id}-message" value="${r.message}"></label><br>
        `;

        Object.keys(r).forEach(k => {
            if (k.includes("threshold")) {
                div.innerHTML += `
                    <label>${k}: <input type="number" id="${id}-${k}" value="${r[k]}"></label><br>
                `;
            }
        });

        container.appendChild(div);
    });
}

function saveRules() {
    const updated = {};

    Object.keys(rules).forEach(id => {
        const r = rules[id];
        const newRule = {
            enabled: document.getElementById(`${id}-enabled`).checked,
            severity: document.getElementById(`${id}-severity`).value,
            message: document.getElementById(`${id}-message`).value
        };

        Object.keys(r).forEach(k => {
            if (k.includes("threshold")) {
                newRule[k] = Number(document.getElementById(`${id}-${k}`).value);
            }
        });

        updated[id] = newRule;
    });

    fetch("/api/alert_rules/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated)
    })
    .then(r => r.json())
    .then(() => alert("Rules saved"));
}

loadRules();
