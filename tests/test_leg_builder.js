"use strict";
const assert = require("assert");
const builder = require("../site/assets/leg-builder.js");

const test = (name, fn) => { fn(); process.stdout.write(`ok - ${name}\n`); };

test("0 inches are the default display unit", () => {
  assert.strictEqual(builder.defaults.unit, "in");
  assert.strictEqual(builder.defaults.type, "wideEasel");
  assert.strictEqual(builder.displayMeasurement(builder.defaults.height, "in"), "3.25 in");
});

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
  const svg = builder.buildSvg({ ...builder.defaults, unit: "mm", type: "straight", quantity: 2 });
  assert.match(svg, /width="[0-9.]+mm" height="[0-9.]+mm"/);
  for (const group of ["CUT_PARTS", "CUT_HOLES", "MATING_SLOTS", "FIT_COUPON", "GUIDES"]) assert.match(svg, new RegExp(`id="${group}"`));
  assert.doesNotMatch(svg, /<text|<image/);
});

test("8 inch entry converts to canonical millimetres", () => {
  assert.strictEqual(builder.toMm(0.125, "in"), 3.175);
  assert.strictEqual(builder.fromMm(279.4, "in"), 11);
});

test("9 inch export keeps the physical size", () => {
  const svg = builder.buildSvg({ ...builder.defaults, unit: "in", type: "easel", height: 101.6, quantity: 1 });
  assert.match(svg, /width="[0-9.]+in" height="[0-9.]+in"/);
  assert.match(svg, /&quot;geometryUnits&quot;:&quot;mm&quot;/);
  assert.match(svg, /&quot;displayUnit&quot;:&quot;in&quot;/);
});

test("10 wide single easel back is one large T-shaped part", () => {
  const result = builder.validate({ ...builder.defaults, ...builder.presets.wideEasel });
  assert.strictEqual(result.valid, true);
  assert.strictEqual(result.parts.length, 1);
  assert.match(result.parts[0].outline, /wide-easel-back-01/);
  assert.match(result.parts[0].outline, /<path/);
  assert.strictEqual(result.parts[0].holes, "");
});

test("11 wide easel guidance distinguishes cut part from complete assembly", () => {
  const info = builder.assemblyInfo({ ...builder.defaults, type: "wideEasel" });
  assert.match(info.name, /Wide single easel back/);
  assert.match(info.add, /fixed slot joint/);
  assert.match(info.add, /hinged easel/);
  const diagram = builder.buildAssemblyPreview({ ...builder.defaults, type: "wideEasel" });
  assert.match(diagram, /BACK VIEW/);
  assert.match(diagram, /SIDE VIEW/);
  assert.match(diagram, /WIDE REAR SUPPORT/);
});

test("12 straight-leg side view shows a tab connection, not an easel hinge", () => {
  const diagram = builder.buildAssemblyPreview({ ...builder.defaults, type: "straight" });
  assert.match(diagram, /TAB \/ SLOT/);
  assert.match(diagram, /separate depth-bearing base/);
  assert.doesNotMatch(diagram, /HINGE|rear support opens/);
});

test("13 share links omit harmless inch conversion noise", () => {
  assert.strictEqual(builder.toMm(1.75, "in"), 44.45);
  const query = builder.encodeState({ ...builder.defaults, type: "straight", legWidth: 44.449999999999996 });
  assert.match(query, /type=straight/);
  assert.doesNotMatch(query, /legWidth|999999/);
});

test("14 a support-type link starts from that support's complete preset", () => {
  const state = builder.decodeState("?type=straight");
  assert.strictEqual(state.type, "straight");
  assert.strictEqual(state.quantity, 2);
  assert.strictEqual(state.legWidth, 25.4);
  assert.strictEqual(state.includeSlots, true);
  assert.strictEqual(state.includeCoupon, true);
});

test("15 wide easel overall height is derived from body length and top depth", () => {
  const state = builder.normalize({ ...builder.defaults, type: "wideEasel", bodyLength: 70, shoulderDepth: 20 });
  assert.strictEqual(state.height, 90);
  assert.strictEqual(builder.dimensionInfo(state).derived, "The blue line is cut to make the hole that the leg can be inserted into.");
  assert.strictEqual(builder.dimensionInfo(state).note, "");
  assert.doesNotMatch(builder.buildDimensionPreview(state), /body length/);
  assert.match(builder.buildDimensionPreview(state), /wide top/);
  assert.match(builder.buildDimensionPreview(state), /body width/);
});

test("16 wide easel export sizes its mating slot from body width and material thickness", () => {
  const state = { ...builder.defaults, ...builder.presets.wideEasel, backWidth: 76.2, materialThickness: 3.175, fitAdjustment: 0.1524, includeSlots: true };
  const data = builder.layout(state);
  assert.strictEqual(data.slotCount, 1);
  assert.strictEqual(data.slotLength, 44.602);
  assert.strictEqual(data.result.slotWidth, 3.327);
  const svg = builder.buildSvg(state);
  assert.match(svg, /id="matching-slot-01"/);
  assert.match(svg, /width="44\.602" height="3\.327"/);
});

test("17 incomplete support concepts say what is not generated", () => {
  assert.match(builder.assemblyInfo({ ...builder.defaults, type: "triangle" }).add, /does not create the joints/i);
  assert.match(builder.assemblyInfo({ ...builder.defaults, type: "crossfoot" }).add, /does not include the upright post/i);
  assert.match(builder.assemblyInfo({ ...builder.defaults, type: "straight" }).add, /do not create front-to-back stability/i);
});

