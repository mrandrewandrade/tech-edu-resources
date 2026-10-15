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
