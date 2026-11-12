# Editflow AI - Environment Setup Script
Write-Host "[*] Setting up Editflow AI Environment..." -ForegroundColor Cyan

$pythonExe = "C:\Users\gnath\AppData\Local\Programs\Python\Python312\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python.exe"
}

Write-Host "[*] Using Python: $pythonExe"
& $pythonExe -m venv ".venv"
Write-Host "[+] Virtual environment created at .venv" -ForegroundColor Green
