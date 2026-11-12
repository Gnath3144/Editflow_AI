# Editflow AI - Installation Validator
$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
Write-Host "[*] Validating Editflow AI Installation..." -ForegroundColor Cyan
& $python -m editflow validate
& $python -m editflow health
