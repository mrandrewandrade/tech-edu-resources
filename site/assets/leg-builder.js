(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.LegBuilder = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function (root) {
  "use strict";

  const defaults = Object.freeze({
    unit: "in",
    type: "wideEasel", height: 82.55, footprint: 57.15, legWidth: 44.45, angle: 10,
    materialThickness: 3.175, fitAdjustment: 0.1524, tabWidth: 15.875, tabDepth: 3.81,
    pivotDiameter: 4.7625, pivotOffset: 12.7, cornerRadius: 3.175, quantity: 1,
    backWidth: 76.2, shoulderDepth: 15.875,
    partGap: 7.9375, includeSlots: false, includeCoupon: false,
    previewGuides: true, exportGuides: false
  });

  const presets = {
    straight: { type: "straight", height: 76.2, legWidth: 25.4, quantity: 2, tabWidth: 15.875, tabDepth: 3.81, includeSlots: true, includeCoupon: true },
    angled: { type: "angled", height: 82.55, legWidth: 25.4, angle: 10, quantity: 2, tabWidth: 15.875, tabDepth: 3.81, includeSlots: true, includeCoupon: true },
    triangle: { type: "triangle", height: 76.2, footprint: 63.5, quantity: 2, includeSlots: false },
    easel: { type: "easel", height: 133.35, legWidth: 22.225, pivotDiameter: 4.7625, pivotOffset: 12.7, quantity: 1, includeSlots: false },
    wideEasel: { type: "wideEasel", height: 82.55, backWidth: 76.2, shoulderDepth: 15.875, legWidth: 44.45, quantity: 1, includeSlots: false, includeCoupon: false },
    crossfoot: { type: "crossfoot", height: 25.4, footprint: 88.9, legWidth: 25.4, quantity: 1, includeSlots: false }
  };

  const numericKeys = ["height", "footprint", "legWidth", "angle", "materialThickness", "fitAdjustment", "tabWidth", "tabDepth", "pivotDiameter", "pivotOffset", "cornerRadius", "backWidth", "shoulderDepth", "quantity", "partGap"];
  const dimensionalKeys = new Set(["height", "footprint", "legWidth", "materialThickness", "fitAdjustment", "tabWidth", "tabDepth", "pivotDiameter", "pivotOffset", "cornerRadius", "backWidth", "shoulderDepth", "partGap"]);
  const boolKeys = ["includeSlots", "includeCoupon", "previewGuides", "exportGuides"];
  const round = value => Math.round(value * 1000) / 1000;
  const canonical = value => Math.round(Number(value) * 1000000) / 1000000;
  const finite = (value, fallback) => Number.isFinite(Number(value)) ? Number(value) : fallback;
  const toMm = (value, unit) => canonical(Number(value) * (unit === "in" ? 25.4 : 1));
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

  function wideEaselPart(state, id) {
    const width = state.backWidth;
    const bodyWidth = Math.min(state.legWidth, width);
    const shoulderDepth = Math.min(state.shoulderDepth, state.height);
    const left = (width - bodyWidth) / 2;
    const right = left + bodyWidth;
    const radius = Math.max(0, Math.min(state.cornerRadius, shoulderDepth / 2, width / 2));
    const d = [
      `M ${radius} 0`,
      `H ${width - radius}`,
      `Q ${width} 0 ${width} ${radius}`,
      `V ${shoulderDepth}`,
      `H ${right}`,
      `V ${state.height}`,
      `H ${left}`,
      `V ${shoulderDepth}`,
      "H 0",
      `V ${radius}`,
      `Q 0 0 ${radius} 0`,
      "Z"
    ].join(" ");
    return { id, width, height: state.height, outline: `<path id="${id}" d="${d}"/>`, holes: "" };
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
      else if (state.type === "wideEasel") result.push(wideEaselPart(state, `wide-easel-back-${number}`));
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
    if (state.type === "wideEasel") {
      if (state.backWidth <= 0 || state.shoulderDepth <= 0) errors.push("The wide easel back needs a positive top width and top depth.");
      if (state.legWidth >= state.backWidth) errors.push("The centre body must be narrower than the top attachment area.");
      if (state.shoulderDepth >= state.height) errors.push("The top attachment depth must be smaller than the overall height.");
      if (state.legWidth < 6 * state.materialThickness) warnings.push("The wide easel body's centre section is narrow relative to the material thickness.");
    }
    if (state.legWidth < 4 * state.materialThickness && !["triangle", "wideEasel"].includes(state.type)) warnings.push("The member is narrower than four material thicknesses; inspect slots, holes and grain carefully.");
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

  function assemblyInfo(raw) {
    const state = normalize(raw);
    const info = {
      straight: {
        name: "Two straight tabbed legs",
        cut: "Cut two matching legs. The tabs go into two matching slots in the plaque or a separate base.",
        add: "You still need the plaque or base with those slots. Use the blue slot rectangles only as geometry to copy into that mating part."
      },
      angled: {
        name: "Two angled tabbed legs",
        cut: "Cut two matching legs and place them apart so the plaque cannot twist.",
        add: "You still need two matching slots in the plaque or base. Prototype the viewing angle before cutting the finished material."
      },
      triangle: {
        name: "Two triangular side supports",
        cut: "Cut two triangles and attach one near each end of the plaque.",
        add: "You still need a deliberate attachment method and a front stop so the plaque cannot slide."
      },
      easel: {
        name: "Narrow hinged rear kickstand",
        cut: "Cut one narrow rear leg. The round hole is for a pivot or hinge connection to the back of a front frame.",
        add: "This part is not a complete easel. It needs a front frame or plaque, a pivot, and a stop that limits how far the leg opens."
      },
      wideEasel: {
        name: "Wide single easel back",
        cut: "Cut one large T-shaped rear support. The wide top is the attachment or hinge zone; the broad centre body reaches the table.",
        add: "This is the large single support shown in the reference easel. It still needs a front plaque, a hinge or other tested attachment at the top, and a stop or tether that fixes the open angle."
      },
      crossfoot: {
        name: "Interlocking cross-foot",
        cut: "Cut both half-slotted bars. Rotate one bar 90 degrees and slide the slots together.",
        add: "You still need a slot, tab, or other connection between the crossed base and the plaque."
      }
    };
    return info[state.type] || info.angled;
  }

  function buildAssemblyPreview(raw) {
    const state = normalize(raw);
    const plaque = (x, y, width, height) => `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="8" fill="#dcecf2" stroke="#245f74" stroke-width="3"/>`;
    let backScene = "";
    let sideScene = "";
    let label = "SUPPORT";
    let connectionLabel = "ATTACHMENT";
    let caption = "Test the complete assembly";
    let connectionX = 344, connectionY = 77, connectionTextX = 390, connectionTextY = 66;
    if (state.type === "wideEasel") {
      backScene = `${plaque(42, 38, 206, 145)}<path d="M 72 58 H 218 Q 226 58 226 66 V 91 H 174 V 204 H 116 V 91 H 64 V 66 Q 64 58 72 58 Z" fill="#e99a5b" fill-opacity=".82" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 359 216 L 316 54 L 337 48 L 381 211 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 349 73 L 458 211 L 441 222 L 335 82 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="344" cy="77" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "WIDE REAR SUPPORT";
      connectionLabel = "HINGE / ATTACH";
      caption = "The rear support opens behind the plaque";
    } else if (state.type === "easel") {
      backScene = `${plaque(42, 38, 206, 145)}<rect x="135" y="58" width="28" height="146" rx="12" fill="#e99a5b" fill-opacity=".82" stroke="#a34717" stroke-width="3"/><circle cx="149" cy="77" r="5" fill="#fff" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 359 216 L 316 54 L 337 48 L 381 211 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 347 70 L 456 211 L 443 222 L 334 80 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="344" cy="76" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "NARROW REAR LEG";
      connectionLabel = "PIVOT";
      caption = "The rear leg pivots behind the plaque";
    } else if (state.type === "straight") {
      backScene = `${plaque(42, 38, 206, 145)}<path d="M 72 158 H 96 V 225 H 68 Z M 194 158 H 218 L 222 225 H 198 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 342 44 L 365 43 L 389 184 L 366 187 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 366 171 H 384 L 386 225 H 366 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="375" cy="176" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "TWO STRAIGHT LEGS";
      connectionLabel = "TAB / SLOT";
      caption = "The legs continue below the plaque";
      connectionX = 375; connectionY = 176; connectionTextX = 421; connectionTextY = 160;
    } else if (state.type === "angled") {
      backScene = `${plaque(42, 38, 206, 145)}<path d="M 77 158 H 101 L 88 225 H 64 Z M 189 158 H 213 L 226 225 H 202 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 342 44 L 365 43 L 389 184 L 366 187 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 366 171 H 384 L 430 225 H 407 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="375" cy="176" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "TWO ANGLED LEGS";
      connectionLabel = "TAB / SLOT";
      caption = "The feet move outward to widen the footprint";
      connectionX = 375; connectionY = 176; connectionTextX = 421; connectionTextY = 160;
    } else if (state.type === "triangle") {
      backScene = `${plaque(42, 38, 206, 145)}<path d="M 68 225 L 96 139 L 132 225 Z M 170 225 L 204 139 L 226 225 Z" fill="#e99a5b" fill-opacity=".82" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 342 44 L 365 43 L 389 184 L 366 187 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 367 176 L 456 225 H 375 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="376" cy="180" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "TWO TRIANGULAR SIDES";
      connectionLabel = "ATTACHMENT";
      caption = "A triangle braces the plaque from the side";
      connectionX = 376; connectionY = 180; connectionTextX = 425; connectionTextY = 163;
    } else {
      backScene = `${plaque(95, 35, 100, 135)}<path d="M 55 205 H 235 V 220 H 55 Z M 138 160 H 153 V 238 H 138 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 382 55 H 403 V 210 H 382 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 305 210 H 480 V 225 H 305 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="393" cy="211" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "CROSS-FOOT BASE";
      connectionLabel = "BASE SLOT";
      caption = "The plaque needs its own connection to the base";
      connectionX = 393; connectionY = 211; connectionTextX = 445; connectionTextY = 196;
    }
    return `<svg viewBox="0 0 520 265" role="img" aria-label="Schematic showing the selected support behind a plaque">
<rect width="520" height="265" fill="#ffffff"/>
<text x="145" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="700" fill="#284650">BACK VIEW</text>
${backScene}
<text x="145" y="247" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#7a3515">${label}</text>
<text x="397" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="700" fill="#284650">SIDE VIEW</text>
<line x1="280" y1="225" x2="495" y2="225" stroke="#52636b" stroke-width="3"/>
${sideScene}
<line x1="${connectionX}" y1="${connectionY}" x2="${connectionTextX - 4}" y2="${connectionTextY + 3}" stroke="#1b7560" stroke-width="1.5"/>
<text x="${connectionTextX}" y="${connectionTextY}" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#1b7560">${connectionLabel}</text>
<text x="397" y="247" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#52636b">${caption}</text>
</svg>`;
  }

  function encodeState(raw) {
    const state = normalize(raw), params = new URLSearchParams();
    Object.keys(defaults).forEach(key => {
      const same = typeof defaults[key] === "number"
        ? Math.abs(state[key] - defaults[key]) < 0.000001
        : state[key] === defaults[key];
      if (!same) params.set(key, String(state[key]));
    });
    return params.toString();
  }

  function decodeState(search) {
    const params = new URLSearchParams(String(search || "").replace(/^\?/, ""));
    const state = { ...(presets[params.get("type")] || {}) };
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
      host.querySelectorAll("[data-show-for]").forEach(item => {
        item.hidden = !item.dataset.showFor.split(/\s+/).includes(state.type);
      });
      const widthLabel = host.querySelector("[data-leg-width-label]");
      if (widthLabel) widthLabel.textContent = state.type === "wideEasel" ? "Centre-body width" : "Leg / member width";
      const quantityLabel = host.querySelector("[data-quantity-label]");
      if (quantityLabel) quantityLabel.textContent = ["straight", "angled", "triangle"].includes(state.type) ? "Number of matching supports" : "Quantity";
    };
    const render = (readControls = true) => {
      if (readControls) read();
      const result = validate(state), svg = buildSvg(state, { includeGuides: state.previewGuides });
      host.querySelector("[data-preview]").innerHTML = svg.replace("<svg ", '<svg role="img" aria-label="Generated laser-cut leg and support parts" ');
      host.querySelector("[data-slot-width]").textContent = displayMeasurement(result.slotWidth, state.unit);
      host.querySelector("[data-count]").textContent = String(result.parts.length);
      host.querySelector("[data-stiffness]").textContent = `${round(Math.pow(state.materialThickness / 3, 3))}×`;
      host.querySelector("[data-units]").textContent = state.unit === "in" ? "inches (in)" : "millimetres (mm)";
      const info = assemblyInfo(state);
      host.querySelector("[data-assembly-name]").textContent = info.name;
      host.querySelector("[data-assembly-cut]").textContent = info.cut;
      host.querySelector("[data-assembly-add]").textContent = info.add;
      host.querySelector("[data-assembly-preview]").innerHTML = buildAssemblyPreview(state);
      const status = host.querySelector("[data-status]");
      status.className = `plate-status ${result.valid ? "is-valid" : "is-error"}`;
      status.innerHTML = result.valid
        ? `<strong>The flat cut outline is ready for a test cut.</strong>${result.warnings.map(item => `<span>${esc(item)}</span>`).join("")}`
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
    controls.forEach(control => {
      if (control.dataset.key !== "type") control.addEventListener("input", render);
    });
    const typeControl = host.querySelector('[data-key="type"]');
    typeControl.addEventListener("change", event => {
      state = normalize({ ...defaults, ...(presets[event.target.value] || {}), unit: state.unit });
      write(); render(false);
    });
    unitButtons.forEach(button => button.addEventListener("click", () => { state.unit = button.dataset.unitButton; write(); render(false); }));
    host.querySelector("[data-reset]").addEventListener("click", () => { state = normalize({ ...defaults, unit: state.unit }); write(); render(false); });
    host.querySelector("[data-download]").addEventListener("click", () => download(buildSvg(state, { includeGuides: state.exportGuides }), "laser-cut-leg-parts.svg", "image/svg+xml"));
    host.querySelector("[data-json]").addEventListener("click", () => download(JSON.stringify(normalize(state), null, 2) + "\n", "laser-cut-leg-settings.json", "application/json"));
    host.querySelector("[data-copy]").addEventListener("click", async event => { await navigator.clipboard.writeText(root.location.href); event.target.textContent = "Link copied"; setTimeout(() => event.target.textContent = "Copy share link", 1500); });
    write(); render(false);
  }

  if (typeof document !== "undefined") document.addEventListener("DOMContentLoaded", () => init(document));
  return { defaults, presets, normalize, toMm, fromMm, displayMeasurement, effectiveSlotWidth, parts, validate, layout, buildSvg, assemblyInfo, buildAssemblyPreview, encodeState, decodeState };
});
