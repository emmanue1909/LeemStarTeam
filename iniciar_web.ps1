$ErrorActionPreference = 'Stop'
$taskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    throw 'Crea .venv e instala requirements-lock.txt como indica README.md.'
}
Set-Location -LiteralPath $PSScriptRoot
& $taskPython -m streamlit run src/data_web.py --server.address 127.0.0.1 --server.headless false --browser.gatherUsageStats false
exit $LASTEXITCODE
