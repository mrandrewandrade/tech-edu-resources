"use strict";
const assert = require("assert");
const builder = require("../site/assets/plate-builder.js");

const test = (name, fn) => { fn(); process.stdout.write(`ok - ${name}\n`); };

test("1 measured diameter adds total—not radial—clearance", () => {
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
  const svg = builder.buildSvg({ ...builder.presets.mount4, holeMode: "direct", holeDiameter: 5 });
  assert.match(svg, /width="100mm" height="70mm" viewBox="0 0 100 70"/);
  assert.match(svg, /id="CUT_OUTER"/); assert.match(svg, /id="CUT_HOLES"/); assert.match(svg, /id="GUIDES"/);
  assert.doesNotMatch(svg, /transform=|<text|<image/);
  assert.strictEqual((svg.match(/id="hole-/g) || []).length, 4);
});
