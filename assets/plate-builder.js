(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.PlateBuilder = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function (root) {
  "use strict";

  const defaults = Object.freeze({
    unit: "in",
    base: "rounded", width: 190.5, height: 82.55, radius: 6.35, ringWall: 10.16,
    patternOpenings: true, holeShape: "circle", holeMode: "measured", holeDiameter: 5.08, objectDiameter: 34.036, clearance: 2.032,
    holeRectWidth: 12.7, holeRectLength: 25.4,
    pattern: "row", rows: 1, columns: 4, spacingX: 41.91, spacingY: 41.91,
    radialCount: 6, radialRadius: 30.48, startAngle: -90, perimeterCount: 8,
    edgeMargin: 10.16, autoCentre: true, offsetX: 0, offsetY: 0,
    cornerHoles: false, cornerOffsetReference: "center",
    cornerAShape: "circle", cornerADiameter: 6.35, cornerARectWidth: 12.7, cornerARectLength: 25.4, cornerAOffset: 9.525,
    cornerBShape: "circle", cornerBDiameter: 6.35, cornerBRectWidth: 12.7, cornerBRectLength: 25.4, cornerBOffset: 9.525,
    cornerCShape: "circle", cornerCDiameter: 6.35, cornerCRectWidth: 12.7, cornerCRectLength: 25.4, cornerCOffset: 9.525,
    cornerDShape: "circle", cornerDDiameter: 6.35, cornerDRectWidth: 12.7, cornerDRectLength: 25.4, cornerDOffset: 9.525,
    previewGuides: true, exportGuides: false
  });

  const presets = {
    blank: { base: "rounded", width: 120.65, height: 69.85, radius: 6.35, patternOpenings: false, pattern: "single", holeMode: "direct", holeDiameter: 0 },
    mount4: { base: "rounded", width: 101.6, height: 69.85, radius: 5.08, pattern: "grid", rows: 2, columns: 2, spacingX: 69.85, spacingY: 38.1, holeMode: "direct", holeDiameter: 5.08, edgeMargin: 10.16 },
    bottles6: { base: "rounded", width: 273.05, height: 69.85, radius: 6.35, pattern: "row", columns: 6, spacingX: 41.91, holeMode: "measured", objectDiameter: 34.036, clearance: 2.032, edgeMargin: 7.62 },
    bottles2x3: { base: "rounded", width: 152.4, height: 107.95, radius: 6.35, pattern: "grid", rows: 2, columns: 3, spacingX: 41.91, spacingY: 41.91, holeMode: "measured", objectDiameter: 34.036, clearance: 2.032, edgeMargin: 7.62 },
    markers: { base: "rounded", width: 190.5, height: 63.5, radius: 6.35, pattern: "row", columns: 8, spacingX: 20.955, holeMode: "measured", objectDiameter: 13.97, clearance: 1.524, edgeMargin: 7.62 },
    drills: { base: "rounded", width: 177.8, height: 44.45, radius: 4.064, pattern: "row", columns: 10, spacingX: 15.875, holeMode: "direct", holeDiameter: 7.9375, edgeMargin: 6.985 },
    cable: { base: "rounded", width: 120.65, height: 69.85, radius: 6.35, pattern: "grid", rows: 2, columns: 3, spacingX: 34.925, spacingY: 29.972, holeMode: "direct", holeDiameter: 10.16, edgeMargin: 7.62 }
  };

  const cornerLabels = ["A", "B", "C", "D"];
  const cornerDimensionKeys = label => [`corner${label}Diameter`, `corner${label}RectWidth`, `corner${label}RectLength`, `corner${label}Offset`];
  const numericKeys = ["width","height","radius","ringWall","holeDiameter","objectDiameter","clearance","holeRectWidth","holeRectLength","rows","columns","spacingX","spacingY","radialCount","radialRadius","startAngle","perimeterCount","edgeMargin","offsetX","offsetY",...cornerLabels.flatMap(cornerDimensionKeys)];
  const dimensionalKeys = new Set(["width","height","radius","ringWall","holeDiameter","objectDiameter","clearance","holeRectWidth","holeRectLength","spacingX","spacingY","radialRadius","edgeMargin","offsetX","offsetY",...cornerLabels.flatMap(cornerDimensionKeys)]);
  const boolKeys = ["patternOpenings","autoCentre","cornerHoles","previewGuides","exportGuides"];
  const round = value => Math.round(value * 1000) / 1000;
  const finite = (value, fallback) => Number.isFinite(Number(value)) ? Number(value) : fallback;
  const toMm = (value, unit) => Number(value) * (unit === "in" ? 25.4 : 1);
  const fromMm = (value, unit) => Number(value) / (unit === "in" ? 25.4 : 1);
  const displayNumber = (value, unit) => Number(fromMm(value, unit).toFixed(unit === "in" ? 4 : 3)).toString();
  const displayMeasurement = (value, unit) => `${displayNumber(value, unit)} ${unit}`;

  function normalize(input) {
    const state = { ...defaults, ...(input || {}) };
    state.unit = state.unit === "in" ? "in" : "mm";
    numericKeys.forEach(key => state[key] = finite(state[key], defaults[key]));
    boolKeys.forEach(key => state[key] = state[key] === true || state[key] === "true" || state[key] === "1");
    state.rows = Math.max(1, Math.round(state.rows));
    state.columns = Math.max(1, Math.round(state.columns));
    state.radialCount = Math.max(1, Math.round(state.radialCount));
    state.perimeterCount = Math.max(1, Math.round(state.perimeterCount));
    state.holeShape = state.holeShape === "rectangle" ? "rectangle" : "circle";
    state.cornerOffsetReference = state.cornerOffsetReference === "edge" ? "edge" : "center";
    cornerLabels.forEach(label => { state[`corner${label}Shape`] = state[`corner${label}Shape`] === "rectangle" ? "rectangle" : "circle"; });
    if (state.base === "circle" || state.base === "ring") state.height = state.width;
    return state;
  }

  function effectiveHoleDiameter(state) {
    return state.holeMode === "measured" ? state.objectDiameter + state.clearance : state.holeDiameter;
  }

  function patternOpeningDimensions(state) {
    const s = normalize(state);
    const diameter = effectiveHoleDiameter(s);
    return s.holeShape === "rectangle"
      ? { shape: "rectangle", diameter, width: s.holeRectWidth, length: s.holeRectLength }
      : { shape: "circle", diameter, width: diameter, length: diameter };
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

  function cornerHoleSpecs(raw) {
    const s = normalize(raw);
    if (!s.cornerHoles) return [];
    return cornerLabels.map((label, index) => {
      const shape = s[`corner${label}Shape`];
      const diameter = s[`corner${label}Diameter`];
      const width = shape === "rectangle" ? s[`corner${label}RectWidth`] : diameter;
      const length = shape === "rectangle" ? s[`corner${label}RectLength`] : diameter;
      const offset = s[`corner${label}Offset`];
      const centerDistanceX = offset + (s.cornerOffsetReference === "edge" ? width / 2 : 0);
      const centerDistanceY = offset + (s.cornerOffsetReference === "edge" ? length / 2 : 0);
      const right = index === 1 || index === 2;
      const bottom = index >= 2;
      return {
        label,
        corner: ["top left", "top right", "bottom right", "bottom left"][index],
        shape,
        x: round(right ? s.width - centerDistanceX : centerDistanceX),
        y: round(bottom ? s.height - centerDistanceY : centerDistanceY),
        diameter: round(diameter),
        width: round(width),
        length: round(length),
        offset: round(offset),
        centerDistance: round(centerDistanceX),
        centerDistanceX: round(centerDistanceX),
        centerDistanceY: round(centerDistanceY)
      };
    });
  }

  function holeExtents(hole, extraMargin) {
    const margin = extraMargin || 0;
    if (hole.shape === "rectangle") return { halfWidth: hole.width / 2 + margin, halfLength: hole.length / 2 + margin };
    return { halfWidth: hole.diameter / 2 + margin, halfLength: hole.diameter / 2 + margin };
  }

  function pointFitsRoundedRectangle(s, x, y) {
    if (x < 0 || y < 0 || x > s.width || y > s.height) return false;
    if (s.radius <= 0) return true;
    const corners = [
      [x < s.radius && y < s.radius, s.radius, s.radius],
      [x > s.width - s.radius && y < s.radius, s.width - s.radius, s.radius],
      [x > s.width - s.radius && y > s.height - s.radius, s.width - s.radius, s.height - s.radius],
      [x < s.radius && y > s.height - s.radius, s.radius, s.height - s.radius]
    ];
    return corners.every(([inCorner, cx, cy]) => !inCorner || Math.hypot(x - cx, y - cy) <= s.radius);
  }

  function fitsInsideBase(s, hole, extraMargin) {
    const extents = holeExtents(hole, extraMargin);
    const clearance = extents.halfWidth;
    const x = hole.x, y = hole.y;
    if (s.base === "circle" || s.base === "ring") {
      const dx = Math.abs(x - s.width / 2), dy = Math.abs(y - s.height / 2);
      const outerDistance = hole.shape === "rectangle"
        ? Math.hypot(dx + extents.halfWidth, dy + extents.halfLength)
        : Math.hypot(dx, dy) + clearance;
      if (outerDistance > s.width / 2) return false;
      const innerDistance = hole.shape === "rectangle"
        ? Math.hypot(Math.max(dx - extents.halfWidth, 0), Math.max(dy - extents.halfLength, 0))
        : Math.hypot(dx, dy) - clearance;
      if (s.base === "ring" && innerDistance < s.width / 2 - s.ringWall) return false;
      return true;
    }
    if (x - extents.halfWidth < 0 || y - extents.halfLength < 0 || x + extents.halfWidth > s.width || y + extents.halfLength > s.height) return false;
    if (s.base !== "rounded" || s.radius <= 0) return true;
    if (hole.shape === "rectangle") {
      return [
        [x - extents.halfWidth, y - extents.halfLength], [x + extents.halfWidth, y - extents.halfLength],
        [x + extents.halfWidth, y + extents.halfLength], [x - extents.halfWidth, y + extents.halfLength]
      ].every(([px, py]) => pointFitsRoundedRectangle(s, px, py));
    }
    const cornerChecks = [
      [x < s.radius && y < s.radius, s.radius, s.radius],
      [x > s.width - s.radius && y < s.radius, s.width - s.radius, s.radius],
      [x > s.width - s.radius && y > s.height - s.radius, s.width - s.radius, s.height - s.radius],
      [x < s.radius && y > s.height - s.radius, s.radius, s.height - s.radius]
    ];
    return cornerChecks.every(([inCorner, cx, cy]) => !inCorner || Math.hypot(x - cx, y - cy) + clearance <= s.radius);
  }

  function holeSeparation(first, second) {
    const a = holeExtents(first, 0), b = holeExtents(second, 0);
    if (first.shape !== "rectangle" && second.shape !== "rectangle") {
      return Math.hypot(first.x - second.x, first.y - second.y) - a.halfWidth - b.halfWidth;
    }
    if (first.shape === "rectangle" && second.shape === "rectangle") {
      const gapX = Math.abs(first.x - second.x) - a.halfWidth - b.halfWidth;
      const gapY = Math.abs(first.y - second.y) - a.halfLength - b.halfLength;
      if (gapX <= 0 && gapY <= 0) return Math.max(gapX, gapY);
      if (gapX <= 0) return gapY;
      if (gapY <= 0) return gapX;
      return Math.hypot(gapX, gapY);
    }
    const rectangle = first.shape === "rectangle" ? first : second;
    const circle = first.shape === "rectangle" ? second : first;
    const rectangleExtents = first.shape === "rectangle" ? a : b;
    const gapX = Math.max(Math.abs(circle.x - rectangle.x) - rectangleExtents.halfWidth, 0);
    const gapY = Math.max(Math.abs(circle.y - rectangle.y) - rectangleExtents.halfLength, 0);
    return Math.hypot(gapX, gapY) - circle.diameter / 2;
  }

  function validate(raw) {
    const s = normalize(raw), diameter = effectiveHoleDiameter(s);
    const patternDimensions = patternOpeningDimensions(s);
    const patternHasSize = s.patternOpenings && (patternDimensions.shape === "rectangle"
      ? patternDimensions.width > 0 && patternDimensions.length > 0
      : patternDimensions.diameter > 0);
    const errors = [], warnings = [], points = patternHasSize ? patternPoints(s) : [];
    const cornerHoles = cornerHoleSpecs(s);
    if (s.width <= 0 || s.height <= 0) errors.push("Base dimensions must be greater than zero.");
    if (s.base === "rounded" && (s.radius < 0 || s.radius > Math.min(s.width, s.height) / 2)) errors.push("Corner radius must be between 0 and half the shortest side.");
    if (s.base === "ring" && (s.ringWall <= 0 || s.ringWall >= s.width / 2)) errors.push("Ring wall must be greater than 0 and less than the outer radius.");
    if (s.patternOpenings && s.holeShape === "circle" && diameter < 0) errors.push("Hole diameter cannot be negative.");
    if (s.patternOpenings && s.holeShape === "circle" && s.holeMode === "measured" && s.clearance < 0) errors.push("Total clearance cannot be negative.");
    if (s.patternOpenings && s.holeShape === "rectangle" && (s.holeRectWidth <= 0 || s.holeRectLength <= 0)) errors.push("Pattern rectangle width and length must be greater than zero.");
    if (s.patternOpenings && s.edgeMargin < 0) errors.push("Edge margin cannot be negative.");
    if (s.patternOpenings && (s.spacingX < 0 || s.spacingY < 0) && ["row","column","grid","staggered"].includes(s.pattern)) errors.push("Pattern spacing cannot be negative.");
    if (s.patternOpenings && s.pattern === "perimeter" && (s.width <= 2 * s.edgeMargin || s.height <= 2 * s.edgeMargin)) errors.push("The perimeter margin leaves no usable path.");

    if (s.cornerHoles && !["rectangle", "rounded"].includes(s.base)) errors.push("Corner openings A-D require a rectangular or rounded rectangular plate.");
    cornerHoles.forEach(hole => {
      if (hole.shape === "circle" && hole.diameter <= 0) errors.push(`Corner hole ${hole.label} diameter must be greater than zero.`);
      if (hole.shape === "rectangle" && (hole.width <= 0 || hole.length <= 0)) errors.push(`Corner rectangle ${hole.label} width and length must be greater than zero.`);
      if (hole.offset < 0) errors.push(`Corner hole ${hole.label} offset cannot be negative.`);
      const extents = holeExtents(hole, 0);
      if (s.cornerOffsetReference === "center" && (hole.centerDistanceX < extents.halfWidth || hole.centerDistanceY < extents.halfLength)) errors.push(`Corner hole ${hole.label} centre offset must be at least half its width and length.`);
      const hasPositiveSize = hole.shape === "rectangle" ? hole.width > 0 && hole.length > 0 : hole.diameter > 0;
      if (["rectangle", "rounded"].includes(s.base) && hasPositiveSize && !fitsInsideBase(s, hole, 0)) errors.push(`Corner hole ${hole.label} exceeds the plate boundary.`);
      const material = Math.min(hole.centerDistanceX - extents.halfWidth, hole.centerDistanceY - extents.halfLength);
      if (material >= 0 && material < 2) warnings.push(`Less than 0.079 in (2 mm) of material remains outside corner hole ${hole.label}.`);
    });

    const patternHoles = points.map((point, index) => ({ ...point, ...patternDimensions, id: `hole-${String(index + 1).padStart(3, "0")}` }));
    if (patternHoles.some(hole => !fitsInsideBase(s, hole, s.edgeMargin))) errors.push("One or more pattern holes exceed the usable plate boundary or margin.");
    const holes = [...patternHoles, ...cornerHoles.map(hole => ({ ...hole, id: `corner-hole-${hole.label}` }))];
    for (let i = 0; i < holes.length; i += 1) {
      for (let j = i + 1; j < holes.length; j += 1) {
        const gap = holeSeparation(holes[i], holes[j]);
        if (gap < 0) errors.push("Hole geometry overlaps; increase spacing or reduce its dimensions.");
        else if (gap < 2) warnings.push("Less than 0.079 in (2 mm) of material remains between some holes.");
      }
    }
    patternHoles.forEach(hole => {
      const extents = holeExtents(hole, 0);
      const edge = Math.min(hole.x - extents.halfWidth, hole.y - extents.halfLength, s.width - hole.x - extents.halfWidth, s.height - hole.y - extents.halfLength);
      if (edge >= 0 && edge < 2) warnings.push("Less than 0.079 in (2 mm) of material remains at an outer edge.");
    });
    return { valid: errors.length === 0, errors: [...new Set(errors)], warnings: [...new Set(warnings)], points, cornerHoles, holes, patternDimensions: { ...patternDimensions, diameter: round(diameter), width: round(patternDimensions.width), length: round(patternDimensions.length) }, diameter: round(diameter) };
  }

  const esc = value => String(value).replace(/[&<>\"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[char]));
  function buildSvg(raw, options) {
    const s = normalize(raw), result = validate(s), includeGuides = !!(options && options.includeGuides);
    const outer = s.base === "circle" || s.base === "ring"
      ? `<circle id="outer-boundary" cx="${s.width / 2}" cy="${s.height / 2}" r="${s.width / 2}"/>`
      : `<rect id="outer-boundary" x="0" y="0" width="${s.width}" height="${s.height}"${s.base === "rounded" ? ` rx="${s.radius}" ry="${s.radius}"` : ""}/>`;
    const holes = [];
    if (s.base === "ring") holes.push(`<circle id="ring-inner" cx="${s.width / 2}" cy="${s.height / 2}" r="${s.width / 2 - s.ringWall}"/>`);
    result.holes.forEach(hole => holes.push(hole.shape === "rectangle"
      ? `<rect id="${hole.id}" x="${round(hole.x - hole.width / 2)}" y="${round(hole.y - hole.length / 2)}" width="${hole.width}" height="${hole.length}"/>`
      : `<circle id="${hole.id}" cx="${hole.x}" cy="${hole.y}" r="${hole.diameter / 2}"/>`));
    const labelSize = round(Math.max(3, Math.min(6, Math.min(s.width, s.height) / 14)));
    const cornerLabelsMarkup = result.cornerHoles.map(hole => `<text x="${hole.x}" y="${hole.y}" text-anchor="middle" dominant-baseline="central" fill="#174e61" stroke="none" font-family="sans-serif" font-size="${labelSize}" font-weight="700">${hole.label}</text>`).join("");
    const guideMarkup = includeGuides ? `<g id="GUIDES" fill="none" stroke="#68818c" stroke-width="0.25" stroke-dasharray="2 2"><path id="guide-centres" d="M 0 ${s.height / 2} H ${s.width} M ${s.width / 2} 0 V ${s.height}"/><rect id="guide-margin" x="${s.edgeMargin}" y="${s.edgeMargin}" width="${Math.max(0, s.width - 2 * s.edgeMargin)}" height="${Math.max(0, s.height - 2 * s.edgeMargin)}"/>${cornerLabelsMarkup}</g>` : `<g id="GUIDES"/>`;
    const exportWidth = `${displayNumber(s.width, s.unit)}${s.unit}`;
    const exportHeight = `${displayNumber(s.height, s.unit)}${s.unit}`;
    const metadata = esc(JSON.stringify({ generator: "Technology Commons Fabrication Plate Builder V1", geometryUnits: "mm", displayUnit: s.unit, settings: s, validation: { valid: result.valid, errors: result.errors, warnings: result.warnings } }));
    return `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${exportWidth}" height="${exportHeight}" viewBox="0 0 ${s.width} ${s.height}">\n<metadata>${metadata}</metadata>\n<g id="CUT_OUTER" fill="none" stroke="#ff0000" stroke-width="0.1">${outer}</g>\n<g id="CUT_HOLES" fill="none" stroke="#ff0000" stroke-width="0.1">${holes.join("")}</g>\n${guideMarkup}\n</svg>\n`;
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
    const allCornerControls = [...host.querySelectorAll("[data-all-corner]")];
    const unitButtons = [...host.querySelectorAll("[data-unit-button]")];
    [...controls, ...allCornerControls].forEach(control => {
      const key = control.dataset.key || `cornerA${control.dataset.allCorner}`;
      if (!dimensionalKeys.has(key)) return;
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
    const writeAllCorners = () => {
      allCornerControls.forEach(control => {
        const suffix = control.dataset.allCorner;
        const values = cornerLabels.map(label => state[`corner${label}${suffix}`]);
        const dimensional = suffix !== "Shape";
        const same = values.every(value => dimensional ? Math.abs(value - values[0]) < 0.0001 : value === values[0]);
        control.value = same ? (dimensional ? displayNumber(values[0], state.unit) : values[0]) : "";
        control.placeholder = same ? "" : "Mixed";
        if (control.dataset.minMm !== undefined) control.min = displayNumber(control.dataset.minMm, state.unit);
        if (control.dataset.stepMm !== undefined) control.step = displayNumber(control.dataset.stepMm, state.unit);
      });
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
      writeAllCorners();
    };
    const render = (readControls = true) => {
      if (readControls) read();
      const roundBase = state.base === "circle" || state.base === "ring";
      const widthLabel = host.querySelector("[data-width-label]");
      if (widthLabel) widthLabel.textContent = roundBase ? "Outer diameter" : "Width";
      host.querySelectorAll("[data-show-base]").forEach(item => { item.hidden = !item.dataset.showBase.split(/\s+/).includes(state.base); });
      host.querySelectorAll("[data-show-pattern-openings]").forEach(item => { item.hidden = !state.patternOpenings; });
      host.querySelectorAll("[data-show-hole-shape]").forEach(item => { item.hidden = !state.patternOpenings || item.dataset.showHoleShape !== state.holeShape; });
      host.querySelectorAll("[data-show-hole-mode]").forEach(item => { item.hidden = !state.patternOpenings || state.holeShape !== "circle" || item.dataset.showHoleMode !== state.holeMode; });
      host.querySelectorAll("[data-show-pattern]").forEach(item => { item.hidden = !state.patternOpenings || !item.dataset.showPattern.split(/\s+/).includes(state.pattern); });
      host.querySelectorAll("[data-show-corner-holes]").forEach(item => { item.hidden = !state.cornerHoles; });
      host.querySelectorAll("[data-show-corner-shape]").forEach(item => {
        const [label, shape] = item.dataset.showCornerShape.split(":");
        item.hidden = !state.cornerHoles || state[`corner${label}Shape`] !== shape;
      });
      const sharedCornerShape = cornerLabels.every(label => state[`corner${label}Shape`] === state.cornerAShape) ? state.cornerAShape : "mixed";
      host.querySelectorAll("[data-show-all-corner-shape]").forEach(item => { item.hidden = !state.cornerHoles || item.dataset.showAllCornerShape !== sharedCornerShape; });
      const result = validate(state), svg = buildSvg(state, { includeGuides: state.previewGuides });
      host.querySelector("[data-preview]").innerHTML = svg.replace("<svg ", '<svg role="img" aria-label="Generated fabrication plate preview" ');
      host.querySelector("[data-pattern-size]").textContent = !state.patternOpenings
        ? "Off"
        : state.holeShape === "rectangle"
        ? `${displayMeasurement(result.patternDimensions.width, state.unit)} × ${displayMeasurement(result.patternDimensions.length, state.unit)} rectangle`
        : `${displayMeasurement(result.diameter, state.unit)} diameter circle`;
      host.querySelector("[data-count]").textContent = String(result.holes.length);
      host.querySelector("[data-corner-count]").textContent = state.cornerHoles ? "4 (A-D)" : "Off";
      host.querySelector("[data-units]").textContent = state.unit === "in" ? "inches (in)" : "millimetres (mm)";
      const status = host.querySelector("[data-status]");
      status.className = `plate-status ${result.valid ? "is-valid" : "is-error"}`;
      status.innerHTML = result.valid
        ? `<strong>Ready to export.</strong>${result.warnings.map(item => `<span>${esc(item)}</span>`).join("")}`
        : `<strong>Fix before export.</strong>${result.errors.map(item => `<span>${esc(item)}</span>`).join("")}`;
      host.querySelector("[data-download]").disabled = !result.valid;
      writeAllCorners();
      root.history.replaceState(null, "", `${root.location.pathname}${encodeState(state) ? "?" + encodeState(state) : ""}${root.location.hash}`);
    };
    const download = (text, filename, type) => {
      const link = doc.createElement("a");
      link.href = URL.createObjectURL(new Blob([text], { type })); link.download = filename;
      doc.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    };
    controls.forEach(control => control.addEventListener("input", render));
    allCornerControls.forEach(control => control.addEventListener("change", () => {
      if (control.value === "") return;
      const suffix = control.dataset.allCorner;
      const value = suffix === "Shape" ? control.value : toMm(control.value, state.unit);
      cornerLabels.forEach(label => { state[`corner${label}${suffix}`] = value; });
      state = normalize(state); write(); render(false);
    }));
    unitButtons.forEach(button => button.addEventListener("click", () => { state.unit = button.dataset.unitButton; write(); render(false); }));
    host.querySelector("[data-preset]").addEventListener("change", event => { state = normalize({ ...defaults, ...(presets[event.target.value] || {}), unit: state.unit }); write(); render(false); });
    host.querySelector("[data-reset]").addEventListener("click", () => { state = normalize({ ...defaults, unit: state.unit }); write(); render(false); });
    host.querySelector("[data-download]").addEventListener("click", () => download(buildSvg(state, { includeGuides: state.exportGuides }), "fabrication-plate.svg", "image/svg+xml"));
    host.querySelector("[data-json]").addEventListener("click", () => download(JSON.stringify(normalize(state), null, 2) + "\n", "fabrication-plate-settings.json", "application/json"));
    host.querySelector("[data-copy]").addEventListener("click", async event => { await navigator.clipboard.writeText(root.location.href); event.target.textContent = "Link copied"; setTimeout(() => event.target.textContent = "Copy share link", 1500); });
    write(); render(false);
  }

  if (typeof document !== "undefined") document.addEventListener("DOMContentLoaded", () => init(document));
  return { defaults, presets, normalize, toMm, fromMm, displayMeasurement, effectiveHoleDiameter, patternOpeningDimensions, patternPoints, cornerHoleSpecs, validate, buildSvg, encodeState, decodeState };
});
