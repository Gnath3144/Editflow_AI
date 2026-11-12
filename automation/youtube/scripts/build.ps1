<#
.SYNOPSIS
    PyInstaller Standalone Executable Packaging Script.
.DESCRIPTION
    Compiles Codealytica YouTube Publisher into a standalone Windows binary.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

Write-Host "Building Codealytica YouTube Publisher Standalone Executable..." -ForegroundColor Cyan

& $VenvPython -m pip install pyinstaller

& $VenvPython -m PyInstaller `
    --name="Codealytica_YouTube_Publisher" `
    --windowed `
    --noconfirm `
    --clean `
    --add-data "config;config" `
    --hidden-import "googleapiclient" `
    --hidden-import "google_auth_oauthlib" `
    --hidden-import "PySide6" `
    "app.py"

Write-Host "`nBuild Complete! Executable located in: dist\Codealytica_YouTube_Publisher\" -ForegroundColor Green
