import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");
const sourcePath = resolve(
  repoRoot,
  "site/assets/branding/logo/aa-logo-fabrication.dxf",
);
const outputPath = resolve(
  repoRoot,
  "site/assets/branding/logo/aa-logo-stamp-32mm-mirrored.dxf",
);

const lines = (await readFile(sourcePath, "utf8")).split(/\r?\n/);
const entitiesLabel = lines.indexOf("ENTITIES");
const entitiesEnd = lines.indexOf("ENDSEC", entitiesLabel + 1);

if (entitiesLabel < 0 || entitiesEnd < 0) {
  throw new Error("DXF ENTITIES section was not found");
}

const bounds = {
  minX: 79.022,
  maxX: 432.978,
  minY: -452,
  maxY: -34.001,
};
const targetHeight = 32;
const scale = targetHeight / (bounds.maxY - bounds.minY);
const centerX = (bounds.minX + bounds.maxX) / 2;
const centerY = (bounds.minY + bounds.maxY) / 2;

for (let index = entitiesLabel + 1; index < entitiesEnd - 1; index += 1) {
  const code = lines[index].trim();
  const valueIndex = index + 1;
  if (code === "10") {
    const sourceX = Number.parseFloat(lines[valueIndex]);
    lines[valueIndex] = String(-(sourceX - centerX) * scale);
  } else if (code === "20") {
    const sourceY = Number.parseFloat(lines[valueIndex]);
    lines[valueIndex] = String((sourceY - centerY) * scale);
  } else if (code === "42") {
    const bulge = Number.parseFloat(lines[valueIndex]);
    lines[valueIndex] = String(-bulge);
  }
}

await writeFile(outputPath, `${lines.join("\r\n")}\r\n`, "utf8");
console.log(outputPath);
