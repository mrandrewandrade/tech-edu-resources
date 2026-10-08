(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.LegBuilder = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function (root) {
  "use strict";

  const defaults = Object.freeze({
    unit: "in",
    type: "angled", height: 82.55, footprint: 57.15, legWidth: 25.4, angle: 10,
    materialThickness: 3.175, fitAdjustment: 0.1524, tabWidth: 15.875, tabDepth: 3.81,
    pivotDiameter: 4.7625, pivotOffset: 12.7, cornerRadius: 3.175, quantity: 2,
    partGap: 7.9375, includeSlots: true, includeCoupon: true,
    previewGuides: true, exportGuides: false
  });

  const presets = {
    straight: { type: "straight", height: 76.2, legWidth: 25.4, quantity: 2, tabWidth: 15.875, tabDepth: 3.81 },
    angled: { type: "angled", height: 82.55, legWidth: 25.4, angle: 10, quantity: 2, tabWidth: 15.875, tabDepth: 3.81 },
    triangle: { type: "triangle", height: 76.2, footprint: 63.5, quantity: 2, includeSlots: false },
    easel: { type: "easel", height: 133.35, legWidth: 22.225, pivotDiameter: 4.7625, pivotOffset: 12.7, quantity: 1, includeSlots: false },
    crossfoot: { type: "crossfoot", height: 25.4, footprint: 88.9, legWidth: 25.4, quantity: 1, includeSlots: false }
  };

  const numericKeys = ["height", "footprint", "legWidth", "angle", "materialThickness", "fitAdjustment", "tabWidth", "tabDepth", "pivotDiameter", "pivotOffset", "cornerRadius", "quantity", "partGap"];
  const dimensionalKeys = new Set(["height", "footprint", "legWidth", "materialThickness", "fitAdjustment", "tabWidth", "tabDepth", "pivotDiameter", "pivotOffset", "cornerRadius", "partGap"]);
  const boolKeys = ["includeSlots", "includeCoupon", "previewGuides", "exportGuides"];
  const round = value => Math.round(value * 1000) / 1000;
  const finite = (value, fallback) => Number.isFinite(Number(value)) ? Number(value) : fallback;
  const toMm = (value, unit) => Number(value) * (unit === "in" ? 25.4 : 1);
  const fromMm = (value, unit) => Number(value) / (unit === "in" ? 25.4 : 1);
  const displayNumber = (value, unit) => Number(fromMm(value, unit).toFixed(unit === "in" ? 4 : 3)).toString();
  const displayMeasurement = (value, unit) => `${displayNumber(value, unit)} ${unit}`;
  const esc = value => String(value).replace(/[&<>\"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[char]));

  function normalize(input) {
    const state = { ...defaults, ...(input || {}) };
    state.unit = state.unit === "in" ? "in" : "mm";
    numericKeys.forEach(key => state[key] = finite(state[key], defaults[key]));
    boolKeys.forEach(key => state[key] = state[key] === true || state[key] === "true" || state[key] === "1");
    state.quantity = Math.max(1, Math.min(4, Math.round(state.quantity)));
    return state;
  }

  function effectiveSlotWidth(raw) {
    const state = normalize(raw);
    return round(state.materialThickness + state.fitAdjustment);
  }

  function straightPart(state, id) {
    const w = state.legWidth, h = state.height, td = state.tabDepth;
    const left = (w - state.tabWidth) / 2, right = left + state.tabWidth;
    const d = `M 0 ${td} H ${left} V 0 H ${right} V ${td} H ${w} V ${td + h} H 0 Z`;
    return { id, width: w, height: td + h, outline: `<path id="${id}" d="${d}"/>`, holes: "" };
  }

  function angledPart(state, id) {
    const shift = state.height * Math.tan(state.angle * Math.PI / 180);
    const minX = Math.min(0, shift), maxX = Math.max(state.legWidth, shift + state.legWidth);
    const ox = -minX, td = state.tabDepth;
    const left = ox + (state.legWidth - state.tabWidth) / 2;
    const right = left + state.tabWidth;
    const topLeft = ox, topRight = ox + state.legWidth;
    const bottomLeft = ox + shift, bottomRight = bottomLeft + state.legWidth;
    const d = `M ${topLeft} ${td} H ${left} V 0 H ${right} V ${td} H ${topRight} L ${bottomRight} ${td + state.height} H ${bottomLeft} Z`;
    return { id, width: maxX - minX, height: td + state.height, outline: `<path id="${id}" d="${d}"/>`, holes: "" };
  }

  function trianglePart(state, id) {
    const d = `M 0 ${state.height} V 0 L ${state.footprint} ${state.height} Z`;
    return { id, width: state.footprint, height: state.height, outline: `<path id="${id}" d="${d}"/>`, holes: "" };
  }

  function easelPart(state, id) {
    const radius = Math.max(0, Math.min(state.cornerRadius, state.legWidth / 2));
    const holeY = Math.max(state.pivotOffset, state.pivotDiameter / 2 + state.materialThickness);
    return {
      id, width: state.legWidth, height: state.height,
      outline: `<rect id="${id}" x="0" y="0" width="${state.legWidth}" height="${state.height}" rx="${radius}" ry="${radius}"/>`,
      holes: `<circle id="${id}-pivot" cx="${state.legWidth / 2}" cy="${holeY}" r="${state.pivotDiameter / 2}"/>`
    };
  }

  function crossfootParts(state, pairIndex) {
    const slot = effectiveSlotWidth(state), x = (state.footprint - slot) / 2;
    const a = {
      id: `cross-foot-${pairIndex}-a`, width: state.footprint, height: state.legWidth,
      outline: `<rect id="cross-foot-${pairIndex}-a" x="0" y="0" width="${state.footprint}" height="${state.legWidth}"/>`,
      holes: `<rect id="cross-foot-${pairIndex}-a-slot" x="${x}" y="0" width="${slot}" height="${state.legWidth / 2}"/>`
    };
    const b = {
      id: `cross-foot-${pairIndex}-b`, width: state.footprint, height: state.legWidth,
      outline: `<rect id="cross-foot-${pairIndex}-b" x="0" y="0" width="${state.footprint}" height="${state.legWidth}"/>`,
      holes: `<rect id="cross-foot-${pairIndex}-b-slot" x="${x}" y="${state.legWidth / 2}" width="${slot}" height="${state.legWidth / 2}"/>`
    };
    return [a, b];
  }

  function parts(raw) {
    const state = normalize(raw), result = [];
    for (let i = 0; i < state.quantity; i += 1) {
      const number = String(i + 1).padStart(2, "0");
      if (state.type === "straight") result.push(straightPart(state, `straight-leg-${number}`));
      else if (state.type === "angled") result.push(angledPart(state, `angled-leg-${number}`));
      else if (state.type === "triangle") result.push(trianglePart(state, `triangle-support-${number}`));
      else if (state.type === "easel") result.push(easelPart(state, `easel-leg-${number}`));
      else if (state.type === "crossfoot") result.push(...crossfootParts(state, number));
    }
    return result;
  }

  function validate(raw) {
    const state = normalize(raw), errors = [], warnings = [];
    const slot = effectiveSlotWidth(state);
    if (state.height <= 0 || state.footprint <= 0 || state.legWidth <= 0) errors.push("Part dimensions must be greater than zero.");
    if (state.materialThickness <= 0) errors.push("Measured material thickness must be greater than zero.");
    if (slot <= 0) errors.push("Material thickness plus fit adjustment must leave a positive slot width.");
    if (state.partGap < 0) errors.push("Part gap cannot be negative.");
    if (["straight", "angled"].includes(state.type)) {
      if (state.tabWidth <= 0 || state.tabWidth >= state.legWidth) errors.push("Tab width must be greater than 0 and smaller than the leg width.");
      if (state.tabDepth <= 0) errors.push("Tab depth must be greater than zero.");
      if (state.tabDepth < state.materialThickness) warnings.push("The tab is shallower than the measured material thickness.");
    }
    if (state.type === "angled" && Math.abs(state.angle) >= 45) errors.push("Keep the leg angle between -45 and 45 degrees.");
    if (state.type === "easel") {
      if (state.pivotDiameter <= 0) errors.push("Pivot diameter must be greater than zero.");
      const sideLigament = (state.legWidth - state.pivotDiameter) / 2;
      if (sideLigament < 2 * state.materialThickness) warnings.push("Less than two material thicknesses remain beside the pivot hole.");
      if (state.pivotOffset + state.pivotDiameter / 2 >= state.height) errors.push("The pivot hole does not fit inside the leg.");
    }
    if (state.legWidth < 4 * state.materialThickness && state.type !== "triangle") warnings.push("The member is narrower than four material thicknesses; inspect slots, holes and grain carefully.");
    if (state.height / state.legWidth > 10 && ["straight", "angled", "easel"].includes(state.type)) warnings.push("The leg is slender; test out-of-plane bending and sideways wobble.");
    if (state.type === "triangle" && state.footprint < state.height / 2) warnings.push("The triangular support has a short footprint relative to its height.");
    return { valid: errors.length === 0, errors: [...new Set(errors)], warnings: [...new Set(warnings)], slotWidth: slot, parts: parts(state) };
  }

  function layout(raw) {
    const state = normalize(raw), result = validate(state), margin = 8;
    let x = margin, maxHeight = 0;
    const placed = result.parts.map(part => {
      const placedPart = { ...part, x, y: margin };
      x += part.width + state.partGap;
      maxHeight = Math.max(maxHeight, part.height);
      return placedPart;
    });
    const slotCount = state.includeSlots && ["straight", "angled"].includes(state.type) ? state.quantity : 0;
    const slotLength = state.tabWidth + state.fitAdjustment;
    const extrasHeight = (slotCount || state.includeCoupon) ? 45 : 0;
    const width = Math.max(80, x - state.partGap + margin);
    const height = margin + maxHeight + extrasHeight + margin;
    return { state, result, placed, width: round(width), height: round(height), slotCount, slotLength: round(slotLength), extrasY: margin + maxHeight + 12 };
  }

  function buildSvg(raw, options) {
    const data = layout(raw), state = data.state;
    const outlines = data.placed.map(part => `<g transform="translate(${part.x} ${part.y})">${part.outline}</g>`).join("");
    const holes = data.placed.map(part => part.holes ? `<g transform="translate(${part.x} ${part.y})">${part.holes}</g>` : "").join("");
    let slots = "";
    if (data.slotCount) {
      const total = data.slotCount * data.slotLength + (data.slotCount - 1) * state.partGap;
      let sx = (data.width - total) / 2;
      for (let i = 0; i < data.slotCount; i += 1) {
        slots += `<rect id="matching-slot-${String(i + 1).padStart(2, "0")}" x="${round(sx)}" y="${data.extrasY}" width="${data.slotLength}" height="${data.result.slotWidth}"/>`;
        sx += data.slotLength + state.partGap;
      }
    }
    let coupon = "";
    if (state.includeCoupon) {
      const cw = Math.max(35, data.slotLength + 16), ch = 25;
      const cx = data.width - cw - 8, cy = data.height - ch - 8;
      coupon = `<rect id="fit-coupon-outer" x="${cx}" y="${cy}" width="${cw}" height="${ch}" rx="2" ry="2"/><rect id="fit-coupon-slot" x="${cx + (cw - data.slotLength) / 2}" y="${cy + (ch - data.result.slotWidth) / 2}" width="${data.slotLength}" height="${data.result.slotWidth}"/>`;
    }
    const includeGuides = !!(options && options.includeGuides);
    const guides = includeGuides ? `<g id="GUIDES" fill="none" stroke="#68818c" stroke-width="0.25" stroke-dasharray="2 2"><rect x="0.5" y="0.5" width="${Math.max(0, data.width - 1)}" height="${Math.max(0, data.height - 1)}"/></g>` : `<g id="GUIDES"/>`;
    const exportWidth = `${displayNumber(data.width, state.unit)}${state.unit}`;
    const exportHeight = `${displayNumber(data.height, state.unit)}${state.unit}`;
    const metadata = esc(JSON.stringify({ generator: "Technology Commons Leg and Support Builder V1", geometryUnits: "mm", displayUnit: state.unit, settings: state, validation: { valid: data.result.valid, errors: data.result.errors, warnings: data.result.warnings } }));
    return `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${exportWidth}" height="${exportHeight}" viewBox="0 0 ${data.width} ${data.height}">\n<metadata>${metadata}</metadata>\n<g id="CUT_PARTS" fill="none" stroke="#ff0000" stroke-width="0.1">${outlines}</g>\n<g id="CUT_HOLES" fill="none" stroke="#ff0000" stroke-width="0.1">${holes}</g>\n<g id="MATING_SLOTS" fill="none" stroke="#245f9e" stroke-width="0.1">${slots}</g>\n<g id="FIT_COUPON" fill="none" stroke="#7a3f95" stroke-width="0.1">${coupon}</g>\n${guides}\n</svg>\n`;
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
    const host = doc && doc.getElementById("leg-builder");
    if (!host) return;
    let state = decodeState(root.location.search);
    const controls = [...host.querySelectorAll("[data-key]")];
    const unitButtons = [...host.querySelectorAll("[data-unit-button]")];
    controls.forEach(control => {
      if (!dimensionalKeys.has(control.dataset.key)) return;
      if (control.hasAttribute("min")) control.dataset.minMm = control.getAttribute("min");
      if (control.hasAttribute("step")) control.dataset.stepMm = control.getAttribute("step");
    });
    const read = () => {
      controls.forEach(control => {
        const key = control.dataset.key;
        if (control.type === "checkbox") state[key] = control.checked;
        else state[key] = dimensionalKeys.has(key) ? toMm(control.value, state.unit) : control.value;
      });
      state = normalize(state);
    };
    const write = () => {
      controls.forEach(control => {
        const key = control.dataset.key, value = state[key];
        if (control.type === "checkbox") control.checked = !!value;
        else control.value = dimensionalKeys.has(key) ? displayNumber(value, state.unit) : value;
        if (dimensionalKeys.has(key)) {
          if (control.dataset.minMm !== undefined) control.min = displayNumber(control.dataset.minMm, state.unit);
          if (control.dataset.stepMm !== undefined) control.step = displayNumber(control.dataset.stepMm, state.unit);
        }
      });
      host.querySelectorAll("[data-unit-symbol]").forEach(item => { item.textContent = state.unit; });
      unitButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.unitButton === state.unit)));
    };
    const render = (readControls = true) => {
      if (readControls) read();
      const result = validate(state), svg = buildSvg(state, { includeGuides: state.previewGuides });
      host.querySelector("[data-preview]").innerHTML = svg.replace("<svg ", '<svg role="img" aria-label="Generated laser-cut leg and support parts" ');
      host.querySelector("[data-slot-width]").textContent = displayMeasurement(result.slotWidth, state.unit);
      host.querySelector("[data-count]").textContent = String(result.parts.length);
      host.querySelector("[data-stiffness]").textContent = `${round(Math.pow(state.materialThickness / 3, 3))}×`;
      host.querySelector("[data-units]").textContent = state.unit === "in" ? "inches (in)" : "millimetres (mm)";
      const status = host.querySelector("[data-status]");
      status.className = `plate-status ${result.valid ? "is-valid" : "is-error"}`;
      status.innerHTML = result.valid
        ? `<strong>Geometry is ready for a test cut.</strong>${result.warnings.map(item => `<span>${esc(item)}</span>`).join("")}`
        : `<strong>Fix before export.</strong>${result.errors.map(item => `<span>${esc(item)}</span>`).join("")}`;
      host.querySelector("[data-download]").disabled = !result.valid;
      const query = encodeState(state);
      root.history.replaceState(null, "", `${root.location.pathname}${query ? "?" + query : ""}${root.location.hash}`);
    };
    const download = (text, filename, type) => {
      const link = doc.createElement("a");
      link.href = URL.createObjectURL(new Blob([text], { type }));
      link.download = filename;
      doc.body.appendChild(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    };
    controls.forEach(control => control.addEventListener("input", render));
    unitButtons.forEach(button => button.addEventListener("click", () => { state.unit = button.dataset.unitButton; write(); render(false); }));
    host.querySelector("[data-preset]").addEventListener("change", event => { state = normalize({ ...defaults, ...(presets[event.target.value] || {}), unit: state.unit }); write(); render(false); });
    host.querySelector("[data-reset]").addEventListener("click", () => { state = normalize({ ...defaults, unit: state.unit }); write(); render(false); });
    host.querySelector("[data-download]").addEventListener("click", () => download(buildSvg(state, { includeGuides: state.exportGuides }), "laser-cut-leg-parts.svg", "image/svg+xml"));
    host.querySelector("[data-json]").addEventListener("click", () => download(JSON.stringify(normalize(state), null, 2) + "\n", "laser-cut-leg-settings.json", "application/json"));
    host.querySelector("[data-copy]").addEventListener("click", async event => { await navigator.clipboard.writeText(root.location.href); event.target.textContent = "Link copied"; setTimeout(() => event.target.textContent = "Copy share link", 1500); });
    write(); render(false);
  }

  if (typeof document !== "undefined") document.addEventListener("DOMContentLoaded", () => init(document));
  return { defaults, presets, normalize, toMm, fromMm, displayMeasurement, effectiveSlotWidth, parts, validate, layout, buildSvg, encodeState, decodeState };
});
