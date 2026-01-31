// mobile_viz.js

function renderSparkline(canvasId, data, style) {
    const el = document.getElementById(canvasId);
    if (!el || !data || data.length === 0) return;

    const w = 120, h = 30;
    const min = Math.min(...data), max = Math.max(...data);
    const norm = v => h - ((v - min) / (max - min || 1)) * (h - 4) - 2;

    let path = "";
    data.forEach((v, i) => {
        const x = (i / Math.max(data.length - 1, 1)) * (w - 4) + 2;
        const y = norm(v);
        path += (i === 0 ? "M" : "L") + x + " " + y + " ";
    });

    let fill = "";
    if (style === "filled") {
        const lastX = (data.length - 1) / Math.max(data.length - 1, 1) * (w - 4) + 2;
        const firstX = 2;
        fill = `<path d="${path} L ${lastX} ${h} L ${firstX} ${h} Z" fill="rgba(0, 150, 255, 0.25)"/>`;
    }

    const strokeWidth = style === "bold" ? 2 : 1;

    el.innerHTML = `
      <svg width="${w}" height="${h}">
        ${fill}
        <path d="${path}" stroke="#00aaff" stroke-width="${strokeWidth}" fill="none"/>
      </svg>`;
}

function renderMiniHeatmap(canvasId, values) {
    const el = document.getElementById(canvasId);
    if (!el || !values || values.length === 0) return;

    const w = 120, h = 20;
    const max = Math.max(...values) || 1;
    const cellW = w / values.length;

    let rects = "";
    values.forEach((v, i) => {
        const intensity = v / max;
        const r = Math.round(255 * intensity);
        const g = Math.round(80 * (1 - intensity));
        const b = 0;
        rects += `<rect x="${i * cellW}" y="0" width="${cellW + 1}" height="${h}"
                        fill="rgb(${r},${g},${b})"/>`;
    });

    el.innerHTML = `<svg width="${w}" height="${h}">${rects}</svg>`;
}
