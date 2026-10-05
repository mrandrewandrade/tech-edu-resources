(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.PlateBuilder = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function (root) {
  "use strict";

  const defaults = Object.freeze({
    base: "rounded", width: 190, height: 80, radius: 6, ringWall: 10,
    holeMode: "measured", holeDiameter: 5, objectDiameter: 34, clearance: 2,
    pattern: "row", rows: 1, columns: 4, spacingX: 42, spacingY: 42,
    radialCount: 6, radialRadius: 30, startAngle: -90, perimeterCount: 8,
    edgeMargin: 10, autoCentre: true, offsetX: 0, offsetY: 0,
    previewGuides: true, exportGuides: false
  });

  const presets = {
    blank: { base: "rounded", width: 120, height: 70, radius: 6, pattern: "single", holeMode: "direct", holeDiameter: 0 },
    mount4: { base: "rounded", width: 100, height: 70, radius: 5, pattern: "grid", rows: 2, columns: 2, spacingX: 70, spacingY: 40, holeMode: "direct", holeDiameter: 5, edgeMargin: 10 },
    bottles6: { base: "rounded", width: 270, height: 70, radius: 6, pattern: "row", columns: 6, spacingX: 42, holeMode: "measured", objectDiameter: 34, clearance: 2, edgeMargin: 8 },
    bottles2x3: { base: "rounded", width: 150, height: 105, radius: 6, pattern: "grid", rows: 2, columns: 3, spacingX: 42, spacingY: 42, holeMode: "measured", objectDiameter: 34, clearance: 2, edgeMargin: 8 },
    markers: { base: "rounded", width: 190, height: 65, radius: 6, pattern: "row", columns: 8, spacingX: 21, holeMode: "measured", objectDiameter: 14, clearance: 1.5, edgeMargin: 8 },
    drills: { base: "rounded", width: 180, height: 42, radius: 4, pattern: "row", columns: 10, spacingX: 16, holeMode: "direct", holeDiameter: 8, edgeMargin: 7 },
    cable: { base: "rounded", width: 120, height: 70, radius: 6, pattern: "grid", rows: 2, columns: 3, spacingX: 35, spacingY: 30, holeMode: "direct", holeDiameter: 10, edgeMargin: 8 }
  };

  const numericKeys = ["width","height","radius","ringWall","holeDiameter","objectDiameter","clearance","rows","columns","spacingX","spacingY","radialCount","radialRadius","startAngle","perimeterCount","edgeMargin","offsetX","offsetY"];
  const boolKeys = ["autoCentre","previewGuides","exportGuides"];
  const round = value => Math.round(value * 1000) / 1000;
  const finite = (value, fallback) => Number.isFinite(Number(value)) ? Number(value) : fallback;

  function normalize(input) {
    const state = { ...defaults, ...(input || {}) };
    numericKeys.forEach(key => state[key] = finite(state[key], defaults[key]));
    boolKeys.forEach(key => state[key] = state[key] === true || state[key] === "true" || state[key] === "1");
    state.rows = Math.max(1, Math.round(state.rows));
    state.columns = Math.max(1, Math.round(state.columns));
    state.radialCount = Math.max(1, Math.round(state.radialCount));
    state.perimeterCount = Math.max(1, Math.round(state.perimeterCount));
    if (state.base === "circle" || state.base === "ring") state.height = state.width;
    return state;
  }

  function effectiveHoleDiameter(state) {
    return state.holeMode === "measured" ? state.objectDiameter + state.clearance : state.holeDiameter;
  }

  function patternPoints(raw) {
    const s = normalize(raw), points = [];
    const cx = (s.autoCentre ? s.width / 2 : 0) + s.offsetX;
    const cy = (s.autoCentre ? s.height / 2 : 0) + s.offsetY;
    const grid = (rows, columns, stagger) => {
      const totalW = (columns - 1) * s.spacingX;
      const totalH = (rows - 1) * s.spacingY;
      for (let row = 0; row < rows; row += 1) {
        const shift = stagger && row % 2 ? s.spacingX / 2 : 0;
        for (let column = 0; column < columns; column += 1) {
          points.push({ x: cx - totalW / 2 + column * s.spacingX + shift, y: cy - totalH / 2 + row * s.spacingY });
        }
      }
    };
    if (s.pattern === "single") points.push({ x: cx, y: cy });
    else if (s.pattern === "row") grid(1, s.columns, false);
    else if (s.pattern === "column") grid(s.rows, 1, false);
    else if (s.pattern === "grid") grid(s.rows, s.columns, false);
    else if (s.pattern === "staggered") grid(s.rows, s.columns, true);
    else if (s.pattern === "radial") {
      for (let i = 0; i < s.radialCount; i += 1) {
        const angle = (s.startAngle + i * 360 / s.radialCount) * Math.PI / 180;
        points.push({ x: cx + Math.cos(angle) * s.radialRadius, y: cy + Math.sin(angle) * s.radialRadius });
      }
    } else if (s.pattern === "perimeter") {
      const left = s.edgeMargin, top = s.edgeMargin, right = s.width - s.edgeMargin, bottom = s.height - s.edgeMargin;
      const w = right - left, h = bottom - top, length = 2 * (w + h);
      for (let i = 0; i < s.perimeterCount; i += 1) {
        let d = i * length / s.perimeterCount;
        let x, y;
        if (d <= w) { x = left + d; y = top; }
        else if ((d -= w) <= h) { x = right; y = top + d; }
        else if ((d -= h) <= w) { x = right - d; y = bottom; }
        else { d -= w; x = left; y = bottom - d; }
        points.push({ x: x + s.offsetX, y: y + s.offsetY });
      }
    }
    return points.map(point => ({ x: round(point.x), y: round(point.y) }));
  }

  function validate(raw) {
    const s = normalize(raw), diameter = effectiveHoleDiameter(s), r = diameter / 2;
    const errors = [], warnings = [], points = diameter > 0 ? patternPoints(s) : [];
    if (s.width <= 0 || s.height <= 0) errors.push("Base dimensions must be greater than 0 mm.");
    if (s.base === "rounded" && (s.radius < 0 || s.radius > Math.min(s.width, s.height) / 2)) errors.push("Corner radius must be between 0 and half the shortest side.");
    if (s.base === "ring" && (s.ringWall <= 0 || s.ringWall >= s.width / 2)) errors.push("Ring wall must be greater than 0 and less than the outer radius.");
    if (diameter < 0) errors.push("Hole diameter cannot be negative.");
    if (s.holeMode === "measured" && s.clearance < 0) errors.push("Total clearance cannot be negative.");
    if (s.edgeMargin < 0) errors.push("Edge margin cannot be negative.");
    if ((s.spacingX < 0 || s.spacingY < 0) && ["row","column","grid","staggered"].includes(s.pattern)) errors.push("Pattern spacing cannot be negative.");
    if (s.pattern === "perimeter" && (s.width <= 2 * s.edgeMargin || s.height <= 2 * s.edgeMargin)) errors.push("The perimeter margin leaves no usable path.");

    const outside = point => {
      if (s.base === "circle" || s.base === "ring") {
        const distance = Math.hypot(point.x - s.width / 2, point.y - s.height / 2);
        if (distance + r + s.edgeMargin > s.width / 2) return true;
        if (s.base === "ring" && distance - r - s.edgeMargin < s.width / 2 - s.ringWall) return true;
        return false;
      }
      return point.x - r - s.edgeMargin < 0 || point.y - r - s.edgeMargin < 0 || point.x + r + s.edgeMargin > s.width || point.y + r + s.edgeMargin > s.height;
    };
    if (points.some(outside)) errors.push("One or more holes exceed the usable plate boundary or margin.");
    for (let i = 0; i < points.length; i += 1) {
      for (let j = i + 1; j < points.length; j += 1) {
        const gap = Math.hypot(points[i].x - points[j].x, points[i].y - points[j].y) - diameter;
        if (gap < 0) errors.push("Hole geometry overlaps; increase spacing or reduce the diameter.");
        else if (gap < 2) warnings.push("Less than 2 mm of material remains between some holes.");
      }
    }
    points.forEach(point => {
      const edge = Math.min(point.x - r, point.y - r, s.width - point.x - r, s.height - point.y - r);
      if (edge >= 0 && edge < 2) warnings.push("Less than 2 mm of material remains at an outer edge.");
    });
    return { valid: errors.length === 0, errors: [...new Set(errors)], warnings: [...new Set(warnings)], points, diameter: round(diameter) };
  }

  const esc = value => String(value).replace(/[&<>\"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[char]));
  function buildSvg(raw, options) {
    const s = normalize(raw), result = validate(s), includeGuides = !!(options && options.includeGuides);
    const outer = s.base === "circle" || s.base === "ring"
      ? `<circle id="outer-boundary" cx="${s.width / 2}" cy="${s.height / 2}" r="${s.width / 2}"/>`
      : `<rect id="outer-boundary" x="0" y="0" width="${s.width}" height="${s.height}"${s.base === "rounded" ? ` rx="${s.radius}" ry="${s.radius}"` : ""}/>`;
    const holes = [];
    if (s.base === "ring") holes.push(`<circle id="ring-inner" cx="${s.width / 2}" cy="${s.height / 2}" r="${s.width / 2 - s.ringWall}"/>`);
    result.points.forEach((point, index) => holes.push(`<circle id="hole-${String(index + 1).padStart(3, "0")}" cx="${point.x}" cy="${point.y}" r="${result.diameter / 2}"/>`));
    const guideMarkup = includeGuides ? `<g id="GUIDES" fill="none" stroke="#68818c" stroke-width="0.25" stroke-dasharray="2 2"><path id="guide-centres" d="M 0 ${s.height / 2} H ${s.width} M ${s.width / 2} 0 V ${s.height}"/><rect id="guide-margin" x="${s.edgeMargin}" y="${s.edgeMargin}" width="${Math.max(0, s.width - 2 * s.edgeMargin)}" height="${Math.max(0, s.height - 2 * s.edgeMargin)}"/></g>` : `<g id="GUIDES"/>`;
    const metadata = esc(JSON.stringify({ generator: "Technology Commons Fabrication Plate Builder V1", units: "mm", settings: s, validation: { valid: result.valid, errors: result.errors, warnings: result.warnings } }));
    return `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${s.width}mm" height="${s.height}mm" viewBox="0 0 ${s.width} ${s.height}">\n<metadata>${metadata}</metadata>\n<g id="CUT_OUTER" fill="none" stroke="#ff0000" stroke-width="0.1">${outer}</g>\n<g id="CUT_HOLES" fill="none" stroke="#ff0000" stroke-width="0.1">${holes.join("")}</g>\n${guideMarkup}\n</svg>\n`;
  }

  function encodeState(raw) {
    const state = normalize(raw), params = new URLSearchParams();
    Object.keys(defaults).forEach(key => { if (state[key] !== defaults[key]) params.set(key, String(state[key])); });
    return params.toString();
  }
  function decodeState(search) {
    const params = new URLSearchParams(String(search || "").replace(/^\?/, "")), state = {};
    params.forEach((value, key) => { if (key in defaults) state[key] = value; });
    return normalize(state);
  }

  function init(doc) {
    const host = doc && doc.getElementById("plate-builder");
    if (!host) return;
    let state = decodeState(root.location.search);
    const controls = [...host.querySelectorAll("[data-key]")];
    const read = () => {
      controls.forEach(control => {
        const key = control.dataset.key;
        state[key] = control.type === "checkbox" ? control.checked : control.value;
      });
      state = normalize(state);
    };
    const write = () => controls.forEach(control => {
      const value = state[control.dataset.key];
      if (control.type === "checkbox") control.checked = !!value;
      else control.value = value;
    });
    const render = () => {
      read();
      const result = validate(state), svg = buildSvg(state, { includeGuides: state.previewGuides });
      host.querySelector("[data-preview]").innerHTML = svg.replace("<svg ", '<svg role="img" aria-label="Generated fabrication plate preview" ');
      host.querySelector("[data-diameter]").textContent = `${result.diameter} mm`;
      host.querySelector("[data-count]").textContent = String(result.points.length);
      const status = host.querySelector("[data-status]");
      status.className = `plate-status ${result.valid ? "is-valid" : "is-error"}`;
      status.innerHTML = result.valid
        ? `<strong>Ready to export.</strong>${result.warnings.map(item => `<span>${esc(item)}</span>`).join("")}`
        : `<strong>Fix before export.</strong>${result.errors.map(item => `<span>${esc(item)}</span>`).join("")}`;
      host.querySelector("[data-download]").disabled = !result.valid;
      root.history.replaceState(null, "", `${root.location.pathname}${encodeState(state) ? "?" + encodeState(state) : ""}${root.location.hash}`);
    };
    const download = (text, filename, type) => {
      const link = doc.createElement("a");
      link.href = URL.createObjectURL(new Blob([text], { type })); link.download = filename;
      doc.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    };
    controls.forEach(control => control.addEventListener("input", render));
    host.querySelector("[data-preset]").addEventListener("change", event => { state = normalize({ ...defaults, ...(presets[event.target.value] || {}) }); write(); render(); });
    host.querySelector("[data-reset]").addEventListener("click", () => { state = normalize(defaults); write(); render(); });
    host.querySelector("[data-download]").addEventListener("click", () => download(buildSvg(state, { includeGuides: state.exportGuides }), "fabrication-plate.svg", "image/svg+xml"));
    host.querySelector("[data-json]").addEventListener("click", () => download(JSON.stringify(normalize(state), null, 2) + "\n", "fabrication-plate-settings.json", "application/json"));
    host.querySelector("[data-copy]").addEventListener("click", async event => { await navigator.clipboard.writeText(root.location.href); event.target.textContent = "Link copied"; setTimeout(() => event.target.textContent = "Copy share link", 1500); });
    write(); render();
  }

  if (typeof document !== "undefined") document.addEventListener("DOMContentLoaded", () => init(document));
  return { defaults, presets, normalize, effectiveHoleDiameter, patternPoints, validate, buildSvg, encodeState, decodeState };
});
