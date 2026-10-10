(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.LegBuilder = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function (root) {
  "use strict";

  const defaults = Object.freeze({
    unit: "in",
    type: "wideEasel", height: 82.55, bodyLength: 66.675, footprint: 57.15, legWidth: 44.45, angle: 10,
    materialThickness: 3.175, fitAdjustment: 0.1524, tabWidth: 15.875, tabDepth: 3.81,
    pivotDiameter: 4.7625, pivotOffset: 12.7, cornerRadius: 3.175, quantity: 1,
    backWidth: 76.2, shoulderDepth: 15.875,
    partGap: 7.9375, includeSlots: true, includeCoupon: false,
    previewGuides: true, exportGuides: false
  });

  const presets = {
    straight: { type: "straight", height: 76.2, legWidth: 25.4, quantity: 2, tabWidth: 15.875, tabDepth: 3.81, includeSlots: true, includeCoupon: true },
    angled: { type: "angled", height: 82.55, legWidth: 25.4, angle: 10, quantity: 2, tabWidth: 15.875, tabDepth: 3.81, includeSlots: true, includeCoupon: true },
    triangle: { type: "triangle", height: 76.2, footprint: 63.5, quantity: 2, includeSlots: false },
    easel: { type: "easel", height: 133.35, legWidth: 22.225, pivotDiameter: 4.7625, pivotOffset: 12.7, quantity: 1, includeSlots: false },
    wideEasel: { type: "wideEasel", height: 82.55, bodyLength: 66.675, backWidth: 76.2, shoulderDepth: 15.875, legWidth: 44.45, quantity: 1, includeSlots: true, includeCoupon: false },
    crossfoot: { type: "crossfoot", height: 25.4, footprint: 88.9, legWidth: 25.4, quantity: 1, includeSlots: false }
  };

  const numericKeys = ["height", "bodyLength", "footprint", "legWidth", "angle", "materialThickness", "fitAdjustment", "tabWidth", "tabDepth", "pivotDiameter", "pivotOffset", "cornerRadius", "backWidth", "shoulderDepth", "quantity", "partGap"];
  const dimensionalKeys = new Set(["height", "bodyLength", "footprint", "legWidth", "materialThickness", "fitAdjustment", "tabWidth", "tabDepth", "pivotDiameter", "pivotOffset", "cornerRadius", "backWidth", "shoulderDepth", "partGap"]);
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
    const supplied = input || {};
    const suppliedBodyLength = Object.prototype.hasOwnProperty.call(supplied, "bodyLength");
    const suppliedHeight = Object.prototype.hasOwnProperty.call(supplied, "height");
    const state = { ...defaults, ...(input || {}) };
    state.unit = state.unit === "in" ? "in" : "mm";
    numericKeys.forEach(key => state[key] = finite(state[key], defaults[key]));
    boolKeys.forEach(key => state[key] = state[key] === true || state[key] === "true" || state[key] === "1");
    state.quantity = Math.max(1, Math.min(4, Math.round(state.quantity)));
    if (state.type === "wideEasel") {
      if (suppliedBodyLength) state.height = canonical(state.bodyLength + state.shoulderDepth);
      else if (suppliedHeight) state.bodyLength = canonical(Math.max(0, state.height - state.shoulderDepth));
      else state.height = canonical(state.bodyLength + state.shoulderDepth);
    }
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
      if (state.bodyLength <= 0) errors.push("The body length must be greater than zero.");
      if (state.legWidth >= state.backWidth) errors.push("The centre body must be narrower than the top attachment area.");
      if (state.shoulderDepth >= state.height) errors.push("The top attachment depth must be smaller than the overall height.");
      if (state.includeSlots && state.legWidth + state.fitAdjustment <= 0) errors.push("The matching body slot must have a positive length.");
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
    let slotCount = 0;
    let slotLength = state.tabWidth + state.fitAdjustment;
    if (state.includeSlots && ["straight", "angled"].includes(state.type)) slotCount = state.quantity;
    if (state.includeSlots && state.type === "wideEasel") {
      slotCount = 1;
      slotLength = state.legWidth + state.fitAdjustment;
    }
    const extrasHeight = (slotCount || state.includeCoupon) ? 45 : 0;
    const slotsWidth = slotCount ? slotCount * slotLength + (slotCount - 1) * state.partGap + margin * 2 : 0;
    const width = Math.max(80, x - state.partGap + margin, slotsWidth);
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
        cut: "Cut two matching legs. Their tabs can locate them in a plaque or in a separate, depth-bearing base.",
        add: "These coplanar legs do not create front-to-back stability by themselves. The blue rectangles are mating-slot geometry to copy into a separately designed plaque or base."
      },
      angled: {
        name: "Two angled tabbed legs",
        cut: "Cut two matching legs. The angle shown is in the flat front view, so it spreads the feet sideways.",
        add: "Sideways spread resists side-to-side tipping, not front-to-back tipping. You still need a depth-bearing base or rear support and two matching slots."
      },
      triangle: {
        name: "Two triangular side cheeks",
        cut: "Cut two right-triangle side cheeks. In a complete stand, the plaque or shelf spans between them.",
        add: "The generator does not create the joints between the cheeks and plaque. Add verified tabs, slots or fasteners and a front stop before fabrication."
      },
      easel: {
        name: "Narrow hinged rear kickstand",
        cut: "Cut one narrow rear leg. The round hole is for a pivot or hinge connection to the back of a front frame.",
        add: "This part is not a complete easel. It needs a front frame or plaque, a pivot, and a stop that limits how far the leg opens."
      },
      wideEasel: {
        name: "Wide single easel back",
        cut: "Cut one T-shaped support. The SVG also includes a blue mating slot sized for the body of the support.",
        add: "The blue rectangle is geometry to copy into a separately designed plaque. A fixed slot joint and a hinged easel are different assemblies: choose one, then prototype the connection and the opening stop."
      },
      crossfoot: {
        name: "Interlocking X-base blank",
        cut: "Cut both half-slotted bars. Rotate one bar 90 degrees and slide the slots together.",
        add: "This output is only the X-shaped floor or tabletop base. It does not include the upright post or a plaque connection, so it is not a complete nameplate stand."
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
      caption = "Hinge shown; exported slot is a fixed-joint alternative";
    } else if (state.type === "easel") {
      backScene = `${plaque(42, 38, 206, 145)}<rect x="135" y="58" width="28" height="146" rx="12" fill="#e99a5b" fill-opacity=".82" stroke="#a34717" stroke-width="3"/><circle cx="149" cy="77" r="5" fill="#fff" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 359 216 L 316 54 L 337 48 L 381 211 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 347 70 L 456 211 L 443 222 L 334 80 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="344" cy="76" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/><line x1="365" y1="115" x2="421" y2="189" stroke="#7a3f95" stroke-width="3" stroke-dasharray="5 4"/>';
      label = "NARROW REAR LEG";
      connectionLabel = "PIVOT";
      caption = "Pivot plus a tether or stop controls the opening";
    } else if (state.type === "straight") {
      backScene = `${plaque(42, 38, 206, 145)}<path d="M 72 158 H 96 V 225 H 68 Z M 194 158 H 218 L 222 225 H 198 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 354 43 H 377 V 181 H 354 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 356 171 H 375 V 225 H 356 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="365" cy="176" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/><path d="M 391 185 H 466 V 222 H 391 Z" fill="none" stroke="#7a3f95" stroke-width="2" stroke-dasharray="5 4"/>';
      label = "TWO STRAIGHT LEGS";
      connectionLabel = "TAB / SLOT";
      caption = "Coplanar legs need a separate depth-bearing base";
      connectionX = 365; connectionY = 176; connectionTextX = 418; connectionTextY = 160;
    } else if (state.type === "angled") {
      backScene = `${plaque(42, 38, 206, 145)}<path d="M 77 158 H 101 L 88 225 H 64 Z M 189 158 H 213 L 226 225 H 202 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 354 43 H 377 V 181 H 354 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 356 171 H 375 V 225 H 356 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="365" cy="176" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/><path d="M 391 185 H 466 V 222 H 391 Z" fill="none" stroke="#7a3f95" stroke-width="2" stroke-dasharray="5 4"/>';
      label = "TWO ANGLED LEGS";
      connectionLabel = "TAB / SLOT";
      caption = "Lean is front-view spread; it does not create depth";
      connectionX = 365; connectionY = 176; connectionTextX = 418; connectionTextY = 160;
    } else if (state.type === "triangle") {
      backScene = `${plaque(42, 38, 206, 145)}<path d="M 68 225 L 96 139 L 132 225 Z M 170 225 L 204 139 L 226 225 Z" fill="#e99a5b" fill-opacity=".82" stroke="#a34717" stroke-width="3"/>`;
      sideScene = '<path d="M 343 67 L 386 190 L 365 197 L 322 74 Z" fill="#dcecf2" stroke="#245f74" stroke-width="3"/><path d="M 365 225 V 176 L 456 225 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><circle cx="371" cy="183" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "TWO TRIANGULAR SIDE CHEEKS";
      connectionLabel = "ATTACHMENT";
      caption = "Plaque spans between two cheeks; joints are not generated";
      connectionX = 371; connectionY = 183; connectionTextX = 426; connectionTextY = 164;
    } else {
      backScene = '<path d="M 55 205 H 235 V 220 H 55 Z M 138 160 H 153 V 238 H 138 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><path d="M 139 55 H 152 V 205 H 139 Z" fill="none" stroke="#7a3f95" stroke-width="3" stroke-dasharray="6 5"/>';
      sideScene = '<path d="M 305 210 H 480 V 225 H 305 Z" fill="#e99a5b" stroke="#a34717" stroke-width="3"/><path d="M 382 55 H 403 V 210 H 382 Z" fill="none" stroke="#7a3f95" stroke-width="3" stroke-dasharray="6 5"/><circle cx="393" cy="211" r="6" fill="#fff" stroke="#1b7560" stroke-width="4"/>';
      label = "X-BASE BLANK ONLY";
      connectionLabel = "POST NOT INCLUDED";
      caption = "The two bars make a base; design the upright separately";
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

  function dimensionInfo(raw) {
    const state = normalize(raw);
    const info = {
      wideEasel: {
        title: "Wide single easel back dimensions",
        derived: "The blue line is cut to make the hole that the leg can be inserted into.",
        note: ""
      },
      easel: {
        title: "Narrow hinged strut dimensions",
        derived: `Pivot centre is ${displayMeasurement(state.pivotOffset, state.unit)} from the top end; pivot diameter is ${displayMeasurement(state.pivotDiameter, state.unit)}.`,
        note: "This is one rear strut, not a complete easel. A front plaque, pivot hardware and opening stop are separate."
      },
      straight: {
        title: "Straight tabbed-leg dimensions",
        derived: `Cut-part height = leg length + tab depth = ${displayMeasurement(state.height, state.unit)} + ${displayMeasurement(state.tabDepth, state.unit)}.`,
        note: "The tab and slot locate the leg. A separate base must provide front-to-back depth."
      },
      angled: {
        title: "Angled tabbed-leg dimensions",
        derived: `Sideways offset = leg length × tan(lean) = ${displayMeasurement(Math.abs(state.height * Math.tan(state.angle * Math.PI / 180)), state.unit)}.`,
        note: "Lean is measured in the flat front view. It widens the stance sideways but does not create front-to-back depth."
      },
      triangle: {
        title: "Triangular side-cheek dimensions",
        derived: `The right triangle uses a vertical height of ${displayMeasurement(state.height, state.unit)} and a base footprint of ${displayMeasurement(state.footprint, state.unit)}.`,
        note: "Two cheeks can support a plaque spanning between them. Their tabs, slots or fasteners are not generated by this tool."
      },
      crossfoot: {
        title: "Interlocking X-base dimensions",
        derived: `Each bar is ${displayMeasurement(state.footprint, state.unit)} long and ${displayMeasurement(state.legWidth, state.unit)} wide; each centre slot is half the bar width deep.`,
        note: "This creates only the crossed base. The upright post and its connection to the plaque are not generated."
      }
    };
    return info[state.type] || info.wideEasel;
  }

  function buildDimensionPreview(raw) {
    const state = normalize(raw);
    const measure = value => esc(displayMeasurement(value, state.unit));
    const defs = '<defs><marker id="dim-arrow" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse"><path d="M 0 0 L 7 3.5 L 0 7 Z" fill="#1b7560"/></marker></defs>';
    const line = (x1, y1, x2, y2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#1b7560" stroke-width="2" marker-start="url(#dim-arrow)" marker-end="url(#dim-arrow)"/>`;
    const textAt = (x, y, value, anchor = "middle") => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="sans-serif" font-size="13" font-weight="700" fill="#155947">${value}</text>`;
    let drawing = "";
    if (state.type === "wideEasel") {
      drawing = `<path d="M 145 55 H 365 V 110 H 285 V 245 H 225 V 110 H 145 Z" fill="#f3b783" stroke="#a34717" stroke-width="3"/>
${line(145, 35, 365, 35)}${textAt(255, 25, `wide top ${measure(state.backWidth)}`)}
${line(390, 55, 390, 110)}${textAt(402, 86, `top depth ${measure(state.shoulderDepth)}`, "start")}
${line(225, 266, 285, 266)}${textAt(255, 287, `body width ${measure(state.legWidth)}`)}
${line(118, 55, 118, 245)}${textAt(106, 154, `overall ${measure(state.height)}`, "end")}
<rect x="425" y="178" width="145" height="22" fill="#dcecf2" stroke="#245f9e" stroke-width="3"/>
${textAt(497, 164, `slot ${measure(state.legWidth + state.fitAdjustment)} × ${measure(effectiveSlotWidth(state))}`)}
${textAt(497, 222, "copy into the mating plaque")}`;
    } else if (state.type === "easel") {
      drawing = `<rect x="235" y="45" width="90" height="205" rx="18" fill="#f3b783" stroke="#a34717" stroke-width="3"/><circle cx="280" cy="88" r="14" fill="#fff" stroke="#245f9e" stroke-width="3"/>
${line(210, 45, 210, 250)}${textAt(198, 150, `length ${measure(state.height)}`, "end")}
${line(235, 270, 325, 270)}${textAt(280, 291, `width ${measure(state.legWidth)}`)}
${line(350, 45, 350, 88)}${textAt(362, 70, `pivot offset ${measure(state.pivotOffset)}`, "start")}
${textAt(280, 84, `Ø ${measure(state.pivotDiameter)}`)}`;
    } else if (state.type === "triangle") {
      drawing = `<path d="M 175 245 V 55 L 430 245 Z" fill="#f3b783" stroke="#a34717" stroke-width="3"/>
${line(145, 55, 145, 245)}${textAt(133, 154, `height ${measure(state.height)}`, "end")}
${line(175, 270, 430, 270)}${textAt(302, 291, `base footprint ${measure(state.footprint)}`)}
${textAt(302, 145, "plaque spans between two cheeks")}`;
    } else if (state.type === "crossfoot") {
      drawing = `<rect x="115" y="132" width="370" height="46" fill="#f3b783" stroke="#a34717" stroke-width="3"/><rect x="267" y="45" width="46" height="220" fill="#e99a5b" fill-opacity=".85" stroke="#a34717" stroke-width="3"/><rect x="267" y="132" width="46" height="46" fill="#fff" stroke="#245f9e" stroke-width="3"/>
${line(115, 202, 485, 202)}${textAt(300, 224, `bar length ${measure(state.footprint)}`)}
${line(510, 132, 510, 178)}${textAt(522, 160, `bar width ${measure(state.legWidth)}`, "start")}
${textAt(290, 118, `centre slot ${measure(effectiveSlotWidth(state))} wide`)}
${textAt(290, 286, "upright post not included")}`;
    } else {
      const angled = state.type === "angled";
      const bottomShift = angled ? 75 : 0;
      drawing = `<path d="M 235 70 H 265 V 50 H 315 V 70 H 345 L ${345 + bottomShift} 245 H ${235 + bottomShift} Z" fill="#f3b783" stroke="#a34717" stroke-width="3"/>
${line(205, 70, 205, 245)}${textAt(193, 158, `leg length ${measure(state.height)}`, "end")}
${line(235 + bottomShift, 270, 345 + bottomShift, 270)}${textAt(290 + bottomShift, 291, `member width ${measure(state.legWidth)}`)}
${line(265, 35, 315, 35)}${textAt(290, 24, `tab width ${measure(state.tabWidth)}`)}
${line(370, 50, 370, 70)}${textAt(382, 64, `tab depth ${measure(state.tabDepth)}`, "start")}
${angled ? textAt(430, 110, `lean ${esc(state.angle)}°`) : ""}`;
    }
    const info = dimensionInfo(state);
    return `<svg viewBox="0 0 600 310" role="img" aria-label="${esc(info.title)}"><rect width="600" height="310" fill="#fff"/>${defs}${drawing}</svg>`;
  }

  function encodeState(raw) {
    const state = normalize(raw), params = new URLSearchParams();
    Object.keys(defaults).forEach(key => {
      if (state.type === "wideEasel" && key === "height") return;
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
    if (state.type === "wideEasel" && params.has("height") && !params.has("bodyLength")) delete state.bodyLength;
    return normalize(state);
  }

  function init(doc) {
    const host = doc && doc.getElementById("leg-builder");
    if (!host) return;
    let state = decodeState(root.location.search);
    const controls = [...host.querySelectorAll("[data-key]")];
    const unitButtons = [...host.querySelectorAll("[data-unit-button]")];
    doc.querySelectorAll("[data-reference-preview]").forEach(item => {
      const type = item.dataset.referencePreview;
      item.innerHTML = buildAssemblyPreview({ ...defaults, ...(presets[type] || {}), type });
    });
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
      if (widthLabel) widthLabel.textContent = state.type === "wideEasel" ? "Body width" : "Leg / member width";
      const quantityLabel = host.querySelector("[data-quantity-label]");
      if (quantityLabel) quantityLabel.textContent = ["straight", "angled", "triangle"].includes(state.type) ? "Number of matching supports" : "Quantity";
      doc.querySelectorAll("[data-support-reference]").forEach(item => {
        item.classList.toggle("is-selected", item.dataset.supportReference === state.type);
      });
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
      const dimensions = dimensionInfo(state);
      host.querySelector("[data-dimension-title]").textContent = dimensions.title;
      host.querySelector("[data-dimension-preview]").innerHTML = buildDimensionPreview(state);
      host.querySelector("[data-derived-size]").textContent = dimensions.derived;
      host.querySelector("[data-dimension-note]").textContent = dimensions.note;
      const wideSlot = host.querySelector("[data-wide-slot-size]");
      if (wideSlot) wideSlot.textContent = `${displayMeasurement(state.legWidth + state.fitAdjustment, state.unit)} × ${displayMeasurement(result.slotWidth, state.unit)}`;
      const totalHeight = host.querySelector("[data-wide-total-height]");
      if (totalHeight) totalHeight.textContent = displayMeasurement(state.height, state.unit);
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
    doc.querySelectorAll("[data-use-type]").forEach(button => button.addEventListener("click", () => {
      state = normalize({ ...defaults, ...(presets[button.dataset.useType] || {}), unit: state.unit });
      write(); render(false);
      host.scrollIntoView({ behavior: "smooth", block: "start" });
    }));
    unitButtons.forEach(button => button.addEventListener("click", () => { state.unit = button.dataset.unitButton; write(); render(false); }));
    host.querySelector("[data-reset]").addEventListener("click", () => { state = normalize({ ...defaults, unit: state.unit }); write(); render(false); });
    host.querySelector("[data-download]").addEventListener("click", () => download(buildSvg(state, { includeGuides: state.exportGuides }), "laser-cut-leg-parts.svg", "image/svg+xml"));
    host.querySelector("[data-json]").addEventListener("click", () => download(JSON.stringify(normalize(state), null, 2) + "\n", "laser-cut-leg-settings.json", "application/json"));
    host.querySelector("[data-copy]").addEventListener("click", async event => { await navigator.clipboard.writeText(root.location.href); event.target.textContent = "Link copied"; setTimeout(() => event.target.textContent = "Copy share link", 1500); });
    write(); render(false);
  }

  if (typeof document !== "undefined") document.addEventListener("DOMContentLoaded", () => init(document));
  return { defaults, presets, normalize, toMm, fromMm, displayMeasurement, effectiveSlotWidth, parts, validate, layout, buildSvg, assemblyInfo, buildAssemblyPreview, dimensionInfo, buildDimensionPreview, encodeState, decodeState };
});
