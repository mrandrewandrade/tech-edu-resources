$ErrorActionPreference = 'Stop'
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..\..')
$toolPath = Join-Path $repoRoot '.tools\equation-python'
$env:PYTHONPATH = $toolPath
python (Join-Path $PSScriptRoot 'render_assets.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
