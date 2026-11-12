# Editflow AI - Virtual Environment Activation Script
$venvPath = Join-Path $PSScriptRoot "..\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "[+] Editflow AI virtual environment active." -ForegroundColor Green
} else {
    Write-Host "[-] Virtual environment not found at $venvPath" -ForegroundColor Red
}
