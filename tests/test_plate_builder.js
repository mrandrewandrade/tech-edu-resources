"use strict";
const assert = require("assert");
const builder = require("../site/assets/plate-builder.js");

const test = (name, fn) => { fn(); process.stdout.write(`ok - ${name}\n`); };

test("0 inches are the default display unit", () => {
  assert.strictEqual(builder.defaults.unit, "in");
  assert.strictEqual(builder.displayMeasurement(builder.defaults.width, "in"), "7.5 in");
});

test("1 measured diameter adds total, not radial, clearance", () => {
  assert.strictEqual(builder.effectiveHoleDiameter({ ...builder.defaults, objectDiameter: 34, clearance: 2 }), 36);
});
test("2 direct diameter is preserved", () => {
  assert.strictEqual(builder.effectiveHoleDiameter({ ...builder.defaults, holeMode: "direct", holeDiameter: 6.4 }), 6.4);
});
test("3 a single hole is centred", () => {
  assert.deepStrictEqual(builder.patternPoints({ ...builder.defaults, pattern: "single", width: 100, height: 60 }), [{ x: 50, y: 30 }]);
});
test("4 a four-hole row has stable centres", () => {
  assert.deepStrictEqual(builder.patternPoints({ ...builder.defaults, pattern: "row", columns: 4, width: 180, spacingX: 42 }).map(p => p.x), [27,69,111,153]);
});
test("5 a 2 by 3 grid produces six holes", () => {
  assert.strictEqual(builder.patternPoints({ ...builder.defaults, pattern: "grid", rows: 2, columns: 3 }).length, 6);
});
test("6 staggered rows offset alternate centres", () => {
  const points = builder.patternPoints({ ...builder.defaults, pattern: "staggered", rows: 2, columns: 2, spacingX: 20 });
  assert.strictEqual(points[2].x - points[0].x, 10);
});
test("7 radial pattern uses requested count", () => {
  assert.strictEqual(builder.patternPoints({ ...builder.defaults, pattern: "radial", radialCount: 7 }).length, 7);
});
test("8 perimeter pattern uses requested count", () => {
  assert.strictEqual(builder.patternPoints({ ...builder.defaults, pattern: "perimeter", perimeterCount: 9 }).length, 9);
});
test("9 invalid rounded radius is rejected", () => {
  assert.match(builder.validate({ ...builder.defaults, width: 40, height: 20, radius: 11 }).errors.join(" "), /Corner radius/);
});
test("10 invalid ring wall is rejected", () => {
  assert.match(builder.validate({ ...builder.defaults, base: "ring", width: 40, ringWall: 20 }).errors.join(" "), /Ring wall/);
});
test("11 overlapping holes are rejected", () => {
  assert.match(builder.validate({ ...builder.defaults, holeMode: "direct", holeDiameter: 12, columns: 2, spacingX: 10 }).errors.join(" "), /overlaps/);
});
test("12 out-of-bound holes are rejected", () => {
  assert.match(builder.validate({ ...builder.defaults, width: 50, height: 40, holeMode: "direct", holeDiameter: 20, edgeMargin: 10, pattern: "row", columns: 3, spacingX: 20 }).errors.join(" "), /boundary/);
});
test("13 export is true-size, grouped and transform-free", () => {
  const svg = builder.buildSvg({ ...builder.presets.mount4, unit: "mm", holeMode: "direct", holeDiameter: 5.08 });
  assert.match(svg, /width="101.6mm" height="69.85mm" viewBox="0 0 101.6 69.85"/);
  assert.match(svg, /id="CUT_OUTER"/); assert.match(svg, /id="CUT_HOLES"/); assert.match(svg, /id="GUIDES"/);
  assert.doesNotMatch(svg, /transform=|<text|<image/);
  assert.strictEqual((svg.match(/id="hole-/g) || []).length, 4);
});

test("14 inch entry converts to canonical millimetres", () => {
  assert.strictEqual(builder.toMm(11, "in"), 279.4);
  assert.strictEqual(builder.fromMm(101.6, "in"), 4);
});

test("15 inch export keeps the physical size", () => {
  const svg = builder.buildSvg({ ...builder.defaults, unit: "in", width: 279.4, height: 101.6, pattern: "single" });
  assert.match(svg, /width="11in" height="4in" viewBox="0 0 279.4 101.6"/);
  assert.match(svg, /&quot;geometryUnits&quot;:&quot;mm&quot;/);
  assert.match(svg, /&quot;displayUnit&quot;:&quot;in&quot;/);
});

test("16 corner holes A-D use clockwise centre offsets", () => {
  const holes = builder.cornerHoleSpecs({
    ...builder.defaults, cornerHoles: true, base: "rectangle", width: 100, height: 60,
    cornerADiameter: 6, cornerBDiameter: 6, cornerCDiameter: 6, cornerDDiameter: 6,
    cornerAOffset: 10, cornerBOffset: 10, cornerCOffset: 10, cornerDOffset: 10
  });
  assert.deepStrictEqual(holes.map(hole => [hole.label, hole.x, hole.y]), [
    ["A", 10, 10], ["B", 90, 10], ["C", 90, 50], ["D", 10, 50]
  ]);
});

test("17 edge offsets add each corner hole radius", () => {
  const holes = builder.cornerHoleSpecs({
    ...builder.defaults, cornerHoles: true, cornerOffsetReference: "edge", base: "rectangle", width: 100, height: 60,
    cornerADiameter: 6, cornerBDiameter: 8, cornerCDiameter: 10, cornerDDiameter: 12,
    cornerAOffset: 10, cornerBOffset: 10, cornerCOffset: 10, cornerDOffset: 10
  });
  assert.deepStrictEqual(holes.map(hole => hole.centerDistance), [13, 14, 15, 16]);
});

test("18 corner holes validate their own boundary and collisions", () => {
  const outside = builder.validate({
    ...builder.defaults, cornerHoles: true, base: "rectangle", cornerOffsetReference: "center",
    cornerADiameter: 10, cornerAOffset: 4
  });
  assert.match(outside.errors.join(" "), /Corner hole A centre offset/);
  const overlap = builder.validate({
    ...builder.defaults, width: 60, height: 60, pattern: "single", holeMode: "direct", holeDiameter: 10,
    cornerHoles: true, base: "rectangle", cornerADiameter: 10, cornerBDiameter: 10,
    cornerCDiameter: 10, cornerDDiameter: 10, cornerAOffset: 30, cornerBOffset: 30,
    cornerCOffset: 30, cornerDOffset: 30
  });
  assert.match(overlap.errors.join(" "), /overlaps/);
});

test("19 SVG exports corner cuts and optional non-cut A-D labels", () => {
  const state = { ...builder.defaults, cornerHoles: true, base: "rectangle", pattern: "single", holeMode: "direct", holeDiameter: 0 };
  const cutOnly = builder.buildSvg(state);
  const withGuides = builder.buildSvg(state, { includeGuides: true });
  assert.strictEqual((cutOnly.match(/id="corner-hole-/g) || []).length, 4);
  assert.doesNotMatch(cutOnly, /<text/);
  assert.match(withGuides, /<text[^>]*>A<\/text>/);
  assert.match(withGuides, /<text[^>]*>D<\/text>/);
});

test("20 corner settings survive a share-link round trip", () => {
  const state = { ...builder.defaults, cornerHoles: true, cornerOffsetReference: "edge", cornerCDiameter: 7.5, cornerCOffset: 12 };
  const decoded = builder.decodeState(builder.encodeState(state));
  assert.strictEqual(decoded.cornerHoles, true);
  assert.strictEqual(decoded.cornerOffsetReference, "edge");
  assert.strictEqual(decoded.cornerCDiameter, 7.5);
  assert.strictEqual(decoded.cornerCOffset, 12);
});

test("21 rectangular corner openings use width, length and edge offsets", () => {
  const holes = builder.cornerHoleSpecs({
    ...builder.defaults, cornerHoles: true, cornerOffsetReference: "edge", base: "rectangle", width: 100, height: 60,
    cornerAShape: "rectangle", cornerARectWidth: 20, cornerARectLength: 10, cornerAOffset: 5,
    cornerBShape: "rectangle", cornerBRectWidth: 8, cornerBRectLength: 12, cornerBOffset: 5
  });
  assert.deepStrictEqual(
    holes.slice(0, 2).map(hole => [hole.label, hole.shape, hole.x, hole.y, hole.width, hole.length]),
    [["A", "rectangle", 15, 10, 20, 10], ["B", "rectangle", 91, 11, 8, 12]]
  );
});

test("22 SVG exports rectangular corner openings as cut rectangles", () => {
  const state = {
    ...builder.defaults, cornerHoles: true, base: "rectangle", pattern: "single", holeMode: "direct", holeDiameter: 0,
    cornerAShape: "rectangle", cornerARectWidth: 20, cornerARectLength: 10, cornerAOffset: 15
  };
  const svg = builder.buildSvg(state);
  assert.match(svg, /<rect id="corner-hole-A" x="5" y="10" width="20" height="10"\/>/);
  assert.strictEqual((svg.match(/id="corner-hole-/g) || []).length, 4);
});

test("23 rectangular corner dimensions are validated", () => {
  const invalidSize = builder.validate({
    ...builder.defaults, cornerHoles: true, base: "rectangle", cornerAShape: "rectangle", cornerARectWidth: 0
  });
  assert.match(invalidSize.errors.join(" "), /Corner rectangle A width and length/);
  const invalidOffset = builder.validate({
    ...builder.defaults, cornerHoles: true, base: "rectangle", cornerAShape: "rectangle",
    cornerARectWidth: 20, cornerARectLength: 30, cornerAOffset: 10
  });
  assert.match(invalidOffset.errors.join(" "), /Corner hole A centre offset/);
});

test("24 rectangular corner settings survive a share-link round trip", () => {
  const state = {
    ...builder.defaults, cornerHoles: true, cornerCShape: "rectangle",
    cornerCRectWidth: 8, cornerCRectLength: 16, cornerCOffset: 12
  };
  const decoded = builder.decodeState(builder.encodeState(state));
  assert.strictEqual(decoded.cornerCShape, "rectangle");
  assert.strictEqual(decoded.cornerCRectWidth, 8);
  assert.strictEqual(decoded.cornerCRectLength, 16);
  assert.strictEqual(decoded.cornerCOffset, 12);
});

test("25 the main pattern can use shared rectangle dimensions", () => {
  const dimensions = builder.patternOpeningDimensions({
    ...builder.defaults, holeShape: "rectangle", holeRectWidth: 18, holeRectLength: 30
  });
  assert.deepStrictEqual(dimensions, {
    shape: "rectangle", diameter: builder.effectiveHoleDiameter(builder.defaults), width: 18, length: 30
  });
});

test("26 SVG exports centre pattern openings as rectangles", () => {
  const svg = builder.buildSvg({
    ...builder.defaults, base: "rectangle", width: 100, height: 80, edgeMargin: 0,
    pattern: "single", holeShape: "rectangle", holeRectWidth: 20, holeRectLength: 30
  });
  assert.match(svg, /<rect id="hole-001" x="40" y="25" width="20" height="30"\/>/);
  assert.doesNotMatch(svg, /<circle id="hole-001"/);
});

test("27 rectangular pattern openings validate overlap and round boundaries", () => {
  const overlap = builder.validate({
    ...builder.defaults, base: "rectangle", width: 100, height: 80, edgeMargin: 0,
    pattern: "row", columns: 2, spacingX: 15, holeShape: "rectangle", holeRectWidth: 20, holeRectLength: 10
  });
  assert.match(overlap.errors.join(" "), /overlaps/);
  const outsideCircle = builder.validate({
    ...builder.defaults, base: "circle", width: 100, edgeMargin: 0,
    pattern: "single", holeShape: "rectangle", holeRectWidth: 80, holeRectLength: 80
  });
  assert.match(outsideCircle.errors.join(" "), /boundary/);
});

test("28 rectangular pattern settings survive a share-link round trip", () => {
  const state = {
    ...builder.defaults, holeShape: "rectangle", holeRectWidth: 18, holeRectLength: 31
  };
  const decoded = builder.decodeState(builder.encodeState(state));
  assert.strictEqual(decoded.holeShape, "rectangle");
  assert.strictEqual(decoded.holeRectWidth, 18);
  assert.strictEqual(decoded.holeRectLength, 31);
});

test("29 pattern openings can be disabled for a plain plate", () => {
  const result = builder.validate({
    ...builder.defaults, patternOpenings: false, cornerHoles: false,
    holeShape: "rectangle", holeRectWidth: -1, holeRectLength: 0,
    edgeMargin: -1, spacingX: -1, spacingY: -1
  });
  assert.strictEqual(result.valid, true);
  assert.strictEqual(result.holes.length, 0);
  assert.strictEqual(result.points.length, 0);
});

test("30 a plain plate SVG contains no pattern cuts", () => {
  const svg = builder.buildSvg({ ...builder.defaults, patternOpenings: false, cornerHoles: false });
  assert.match(svg, /<g id="CUT_OUTER"/);
  assert.match(svg, /<g id="CUT_HOLES"[^>]*><\/g>/);
  assert.doesNotMatch(svg, /id="hole-|id="corner-hole-/);
});

test("31 corner openings remain available without centre openings", () => {
  const result = builder.validate({
    ...builder.defaults, patternOpenings: false, cornerHoles: true, base: "rectangle"
  });
  assert.strictEqual(result.holes.length, 4);
  assert.deepStrictEqual(result.cornerHoles.map(hole => hole.label), ["A", "B", "C", "D"]);
});

test("32 the no-pattern option survives a share-link round trip", () => {
  const decoded = builder.decodeState(builder.encodeState({ ...builder.defaults, patternOpenings: false }));
  assert.strictEqual(decoded.patternOpenings, false);
});
