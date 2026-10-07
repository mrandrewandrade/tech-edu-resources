"use strict";
const assert = require("assert");
const builder = require("../site/assets/leg-builder.js");

const test = (name, fn) => { fn(); process.stdout.write(`ok - ${name}\n`); };

test("1 slot width uses measured thickness plus total adjustment", () => {
  assert.strictEqual(builder.effectiveSlotWidth({ ...builder.defaults, materialThickness: 6, fitAdjustment: 0.15 }), 6.15);
});

test("2 straight preset makes a pair of legs", () => {
  assert.strictEqual(builder.parts({ ...builder.defaults, ...builder.presets.straight }).length, 2);
});

test("3 angled legs become wider as lean increases", () => {
  const upright = builder.parts({ ...builder.defaults, type: "angled", angle: 0, quantity: 1 })[0];
  const leaned = builder.parts({ ...builder.defaults, type: "angled", angle: 15, quantity: 1 })[0];
  assert.ok(leaned.width > upright.width);
});

test("4 a cross-foot pair exports two strips", () => {
  assert.strictEqual(builder.parts({ ...builder.defaults, type: "crossfoot", quantity: 1 }).length, 2);
});

test("5 invalid tab width is rejected", () => {
  const result = builder.validate({ ...builder.defaults, type: "straight", legWidth: 20, tabWidth: 20 });
  assert.match(result.errors.join(" "), /Tab width/);
});

test("6 a weak pivot ligament produces a warning", () => {
  const result = builder.validate({ ...builder.defaults, type: "easel", legWidth: 14, materialThickness: 3, pivotDiameter: 8 });
  assert.match(result.warnings.join(" "), /pivot hole/);
});

test("7 export is true-size and grouped", () => {
  const svg = builder.buildSvg({ ...builder.defaults, type: "straight", quantity: 2 });
  assert.match(svg, /width="[0-9.]+mm" height="[0-9.]+mm"/);
  for (const group of ["CUT_PARTS", "CUT_HOLES", "MATING_SLOTS", "FIT_COUPON", "GUIDES"]) assert.match(svg, new RegExp(`id="${group}"`));
  assert.doesNotMatch(svg, /<text|<image/);
});

