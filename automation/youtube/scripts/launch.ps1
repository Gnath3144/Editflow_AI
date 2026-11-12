<#
.SYNOPSIS
    One-Click Desktop Launcher for Codealytica YouTube Publisher.
.DESCRIPTION
    Activates the dedicated virtual environment and launches the PySide6 desktop GUI.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Virtual environment not detected. Running initial setup..." -ForegroundColor Yellow
    & (Join-Path $ScriptDir "setup.ps1")
}

Write-Host "Launching Codealytica YouTube Publisher..." -ForegroundColor Cyan
& $VenvPython "app.py"
