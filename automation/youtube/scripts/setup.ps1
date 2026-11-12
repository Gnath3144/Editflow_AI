<#
.SYNOPSIS
    Automated Environment Setup for Codealytica YouTube Publisher.
.DESCRIPTION
    Creates a dedicated Python virtual environment and installs all required dependencies.
#>

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Codealytica YouTube Publisher - Environment Setup     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Identify Python 3.11+ Executable
$PythonExe = "python.exe"
if (Test-Path "C:\Users\gnath\AppData\Local\Programs\Python\Python312\python.exe") {
    $PythonExe = "C:\Users\gnath\AppData\Local\Programs\Python\Python312\python.exe"
}

Write-Host "`n[1/3] Using Python: $PythonExe" -ForegroundColor Yellow
& $PythonExe --version

# 2. Create Virtual Environment
$VenvDir = Join-Path $ProjectRoot ".venv"
if (-not (Test-Path $VenvDir)) {
    Write-Host "`n[2/3] Creating virtual environment at $VenvDir..." -ForegroundColor Yellow
    & $PythonExe -m venv $VenvDir
} else {
    Write-Host "`n[2/3] Virtual environment already exists at $VenvDir." -ForegroundColor Green
}

# 3. Install Requirements
$PipExe = Join-Path $VenvDir "Scripts\pip.exe"
$ReqFile = Join-Path $ProjectRoot "requirements.txt"

Write-Host "`n[3/3] Upgrading pip and installing required packages..." -ForegroundColor Yellow
& $PipExe install --upgrade pip
& $PipExe install -r $ReqFile

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " Setup Complete! Launch with: .\scripts\launch.ps1       " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
