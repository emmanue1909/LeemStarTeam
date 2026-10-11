$ErrorActionPreference = 'Stop'
$taskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
Set-Location -LiteralPath $PSScriptRoot
& $taskPython -m pip check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $taskPython run_local.py tests
exit $LASTEXITCODE
