# TEJ component schematics

The component `.tex` files in this directory are the canonical schematic sources for the beginner component lessons. They use CircuitikZ with the same typography, colour, symbol, and export conventions as the TEJ electronics asset library. The render script has an explicit manifest so it does not rebuild unrelated circuit assets in this shared directory.

Regenerate every PDF and SVG from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render-tej-schematics.ps1
```

Do not hand-edit the generated PDF or SVG files. Review the SVG at normal page size and in black and white after each change. Reuse the generated asset wherever the same circuit appears.
