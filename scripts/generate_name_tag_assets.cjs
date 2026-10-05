/* Rebuild the aligned name-tag examples and layered PSD files.
 * Requires ImageMagick plus ag-psd and pngjs. Set NAME_TAG_NODE_MODULES to
 * the directory containing those packages when they are not installed locally.
 */

const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { createRequire } = require("module");

const repo = path.resolve(__dirname, "..");
const assets = path.join(repo, "site", "assets", "name-tag-photopea");
const downloads = path.join(assets, "downloads");
const sources = path.join(downloads, "source-files");
const font = path.join(repo, "site", "assets", "fonts", "SourceSans3-Bold.ttf").replace(/\\/g, "/");
const emblem = path.join(repo, "site", "assets", "branding", "emblem", "commons-emblem-monochrome-blue-transparent.png");
const aa = path.join(sources, "aa-logo-thickened.svg");
const temp = path.join(os.tmpdir(), "tc-name-tag-aligned");
const moduleRoot = process.env.NAME_TAG_NODE_MODULES || path.join(os.tmpdir(), "name-tag-psd-deps", "node_modules");
const localRequire = createRequire(path.join(moduleRoot, "entry.cjs"));
const { writePsdBuffer } = localRequire("ag-psd");
const { PNG } = localRequire("pngjs");

const W = 3300;
const H = 1200;
const INK = "#0b2e4f";
const AA_OPTICAL_DROP = 48;

fs.mkdirSync(temp, { recursive: true });

function magick(args) {
  execFileSync("magick", args, { stdio: "inherit" });
}

function pngData(file) {
  const png = PNG.sync.read(fs.readFileSync(file));
  return { width: png.width, height: png.height, data: new Uint8ClampedArray(png.data) };
}

function dimensions(file) {
  const png = PNG.sync.read(fs.readFileSync(file));
  return { width: png.width, height: png.height };
}

function blank(file, color = "none") {
  magick(["-size", `${W}x${H}`, `xc:${color}`, file]);
}

function preparedAsset(input, targetHeight, file) {
  magick([input, "-trim", "+repage", "-resize", `x${targetHeight}`, file]);
  return dimensions(file);
}

function preparedText(text, pointSize, maxWidth, file) {
  magick([
    "-background", "none",
    "-fill", INK,
    "-font", font,
    "-pointsize", String(pointSize),
    "label:" + text,
    "-trim", "+repage",
    file,
  ]);
  let size = dimensions(file);
  if (size.width > maxWidth) {
    const resized = file.replace(/\.png$/i, "-fit.png");
    magick([file, "-resize", `${maxWidth}x`, resized]);
    fs.copyFileSync(resized, file);
    size = dimensions(file);
  }
  return size;
}

function placeOnCanvas(source, x, y, file) {
  magick(["-size", `${W}x${H}`, "xc:none", source, "-geometry", `+${x}+${y}`, "-composite", file]);
}

function composite(layers, file) {
  const args = ["-size", `${W}x${H}`, "xc:white"];
  for (const layer of layers) args.push(layer, "-composite");
  args.push(file);
  magick(args);
}

function makeTextLayer(layerFile, text, pointSize, x, y, h) {
  return {
    name: `EDIT TEXT - ${text}`,
    imageData: pngData(layerFile),
    text: {
      text,
      transform: [1, 0, 0, 1, x, y + h],
      style: {
        font: { name: "SourceSans3Roman-Semibold" },
        fontSize: pointSize,
        fillColor: { r: 11, g: 46, b: 79 },
      },
    },
  };
}

function writePsd(output, compositeFile, layerSpecs) {
  const background = path.join(temp, "background.png");
  if (!fs.existsSync(background)) blank(background, "white");
  const psd = {
    width: W,
    height: H,
    imageData: pngData(compositeFile),
    imageResources: {
      resolutionInfo: {
        horizontalResolution: 300,
        horizontalResolutionUnit: "PPI",
        widthUnit: "Inches",
        verticalResolution: 300,
        verticalResolutionUnit: "PPI",
        heightUnit: "Inches",
      },
      gridAndGuidesInformation: {
        guides: [
          { location: 75, direction: "vertical" },
          { location: 3225, direction: "vertical" },
          { location: 75, direction: "horizontal" },
          { location: 1125, direction: "horizontal" },
          { location: 600, direction: "horizontal" },
        ],
      },
    },
    children: [
      ...layerSpecs,
      { name: "White background", imageData: pngData(background) },
    ],
  };
  fs.writeFileSync(output, writePsdBuffer(psd));
}

function buildVariation1() {
  const logoPrepared = path.join(temp, "v1-emblem-prepared.png");
  const textPrepared = path.join(temp, "v1-text-prepared.png");
  const logoSize = preparedAsset(emblem, 600, logoPrepared);
  const textSize = preparedText("A. ANDRADE", 500, 2350, textPrepared);
  const gap = 150;
  const total = logoSize.width + gap + textSize.width;
  const startX = Math.round((W - total) / 2);
  const logoY = Math.round((H - logoSize.height) / 2);
  const textY = Math.round((H - textSize.height) / 2);
  const logoLayer = path.join(temp, "v1-emblem-layer.png");
  const textLayer = path.join(temp, "v1-text-layer.png");
  placeOnCanvas(logoPrepared, startX, logoY, logoLayer);
  placeOnCanvas(textPrepared, startX + logoSize.width + gap, textY, textLayer);
  const output = path.join(assets, "08-variation-1-a-andrade.png");
  composite([logoLayer, textLayer], output);
  fs.copyFileSync(output, path.join(downloads, "variation-1-commons-a-andrade.png"));
  writePsd(path.join(downloads, "variation-1-commons-a-andrade.psd"), output, [
    makeTextLayer(textLayer, "A. ANDRADE", 500, startX + logoSize.width + gap, textY, textSize.height),
    { name: "Technology Commons emblem", imageData: pngData(logoLayer) },
  ]);
}

function buildVariation2() {
  const logoPrepared = path.join(temp, "v2-emblem-prepared.png");
  const textPrepared = path.join(temp, "v2-text-prepared.png");
  const logoSize = preparedAsset(emblem, 520, logoPrepared);
  const textSize = preparedText("ANDRADE", 650, 2470, textPrepared);
  const gap = 130;
  const total = logoSize.width + gap + textSize.width;
  const startX = Math.round((W - total) / 2);
  const logoY = Math.round((H - logoSize.height) / 2);
  const textY = Math.round((H - textSize.height) / 2);
  const logoLayer = path.join(temp, "v2-emblem-layer.png");
  const textLayer = path.join(temp, "v2-text-layer.png");
  placeOnCanvas(logoPrepared, startX, logoY, logoLayer);
  placeOnCanvas(textPrepared, startX + logoSize.width + gap, textY, textLayer);
  const output = path.join(assets, "09-variation-2-max-readability.png");
  composite([logoLayer, textLayer], output);
  fs.copyFileSync(output, path.join(downloads, "variation-2-maximum-readability.png"));
  writePsd(path.join(downloads, "variation-2-maximum-readability.psd"), output, [
    makeTextLayer(textLayer, "ANDRADE", 650, startX + logoSize.width + gap, textY, textSize.height),
    { name: "Technology Commons emblem", imageData: pngData(logoLayer) },
  ]);
}

function buildVariation3() {
  const emblemPrepared = path.join(temp, "v3-emblem-prepared.png");
  const aaPrepared = path.join(temp, "v3-aa-prepared.png");
  const textPrepared = path.join(temp, "v3-text-prepared.png");
  const emblemSize = preparedAsset(emblem, 480, emblemPrepared);
  const aaSize = preparedAsset(aa, 560, aaPrepared);
  const textSize = preparedText("NDRADE", 625, 1850, textPrepared);
  const gap1 = 120;
  const gap2 = 35;
  const total = emblemSize.width + gap1 + aaSize.width + gap2 + textSize.width;
  const startX = Math.round((W - total) / 2);
  const emblemY = Math.round((H - emblemSize.height) / 2);
  // The AA mark carries more visual weight above its geometric centre.
  // Lower it slightly so it looks balanced beside the wordmark.
  const aaY = Math.round((H - aaSize.height) / 2) + AA_OPTICAL_DROP;
  const textY = Math.round((H - textSize.height) / 2);
  const emblemLayer = path.join(temp, "v3-emblem-layer.png");
  const aaLayer = path.join(temp, "v3-aa-layer.png");
  const textLayer = path.join(temp, "v3-text-layer.png");
  placeOnCanvas(emblemPrepared, startX, emblemY, emblemLayer);
  placeOnCanvas(aaPrepared, startX + emblemSize.width + gap1, aaY, aaLayer);
  placeOnCanvas(textPrepared, startX + emblemSize.width + gap1 + aaSize.width + gap2, textY, textLayer);
  const output = path.join(assets, "10-variation-3-aa-ndrade.png");
  composite([emblemLayer, aaLayer, textLayer], output);
  const alignmentCheck = path.join(assets, "11-variation-3-alignment-check.png");
  magick([
    output,
    "-fill", "none",
    "-stroke", "#22a6cc",
    "-strokewidth", "6",
    "-draw", "rectangle 75,75 3225,1125 line 75,600 3225,600",
    "-fill", "#22a6cc",
    "-stroke", "none",
    "-font", font,
    "-pointsize", "46",
    "-draw", "text 120,150 'OPTICAL BALANCE: AA SITS SLIGHTLY LOWER'",
    alignmentCheck,
  ]);
  fs.copyFileSync(output, path.join(downloads, "variation-3-thick-aa-ndrade.png"));
  writePsd(path.join(downloads, "variation-3-thick-aa-ndrade.psd"), output, [
    makeTextLayer(textLayer, "NDRADE", 625, startX + emblemSize.width + gap1 + aaSize.width + gap2, textY, textSize.height),
    { name: "AA lettermark - thickened", imageData: pngData(aaLayer) },
    { name: "Technology Commons emblem", imageData: pngData(emblemLayer) },
  ]);
}

buildVariation1();
buildVariation2();
buildVariation3();
