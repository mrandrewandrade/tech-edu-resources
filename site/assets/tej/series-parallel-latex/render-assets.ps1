$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$tex = Join-Path $here 'series-parallel-assets.tex'
$pdf = Join-Path $here 'series-parallel-assets.pdf'

Push-Location $here
try {
    pdflatex -interaction=nonstopmode -halt-on-error $tex
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Remove-Item 'series-parallel-??.png' -ErrorAction SilentlyContinue
    magick -density 240 $pdf -background none -alpha on -trim +repage -bordercolor none -border 24x24 'series-parallel-%02d.png'
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Copy-Item 'series-parallel-00.png' 'guided-equations.png' -Force
    Copy-Item 'series-parallel-01.png' 'guided-solve-check.png' -Force
    Copy-Item 'series-parallel-02.png' 'question-2-equations.png' -Force
    Copy-Item 'series-parallel-03.png' 'question-2-solve-check.png' -Force
    Copy-Item 'series-parallel-04.png' 'question-2-final-answers.png' -Force
    Copy-Item 'series-parallel-05.png' 'question-4-equations.png' -Force
    Copy-Item 'series-parallel-06.png' 'question-4-solve-check.png' -Force
    Copy-Item 'series-parallel-07.png' 'series-parallel-rules.png' -Force
}
finally {
    Pop-Location
}

Write-Host 'Generated:'
Write-Host '  guided-equations.png'
Write-Host '  guided-solve-check.png'
Write-Host '  question-2-equations.png'
Write-Host '  question-2-solve-check.png'
Write-Host '  question-2-final-answers.png'
Write-Host '  question-4-equations.png'
Write-Host '  question-4-solve-check.png'
Write-Host '  series-parallel-rules.png'

