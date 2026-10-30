$ErrorActionPreference = "Stop"
Push-Location (Join-Path $PSScriptRoot "..")
try {
    & py -3.12 -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Tests failed ($LASTEXITCODE)" }
    & py -3.12 scripts/build.py
    if ($LASTEXITCODE -ne 0) { throw "Build failed ($LASTEXITCODE)" }
} finally { Pop-Location }
