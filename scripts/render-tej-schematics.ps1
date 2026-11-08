$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceDir = Join-Path $repoRoot 'site/assets/electronics/schematics'
$buildDir = Join-Path $repoRoot '.tools/schematic-build'

$pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
$dvisvgm = Get-Command dvisvgm -ErrorAction SilentlyContinue
if (-not $pdflatex) { throw 'pdfLaTeX is required to generate CircuitikZ schematics.' }
if (-not $dvisvgm) { throw 'dvisvgm is required to export the generated schematics as SVG.' }

New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
$buildDirTeX = $buildDir.Replace('\', '/')

$schematicNames = @(
    'component-symbols-foundation',
    'first-led-circuit',
    'midterm-three-current-network',
    'midterm-three-current-loop1',
    'midterm-three-current-loop2',
    'transistor-led-switch',
    'op-amp-voltage-follower'
)

$schematicNames | ForEach-Object {
    $baseName = $_
    $sourcePath = Join-Path $sourceDir "$baseName.tex"
    $sourceTeX = $sourcePath.Replace('\', '/')
    & $pdflatex.Source '-interaction=nonstopmode' '-halt-on-error' "-output-directory=$buildDirTeX" $sourceTeX | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "CircuitikZ PDF generation failed for $sourcePath" }

    $generatedPdf = Join-Path $buildDir "$baseName.pdf"
    $pdfPath = Join-Path $sourceDir "$baseName.pdf"
    $svgPath = Join-Path $sourceDir "$baseName.svg"
    Copy-Item -LiteralPath $generatedPdf -Destination $pdfPath -Force
    & $dvisvgm.Source '--pdf' '--no-fonts' '--exact-bbox' '--bbox=min' "--output=$svgPath" $generatedPdf | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "CircuitikZ SVG generation failed for $($_.FullName)" }
    Write-Host "Generated $baseName.pdf and $baseName.svg"
}
