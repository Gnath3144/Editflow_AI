# Editflow AI - Project Backup Script
param (
    [string]$Destination = "D:\Codealytica\Editflow AI\archive\backup"
)
Write-Host "[*] Creating backup of Editflow AI configuration and metadata to $Destination..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
Copy-Item "config" -Destination $Destination -Recurse -Force
Copy-Item "data\manifests" -Destination $Destination -Recurse -Force
Write-Host "[+] Backup completed successfully." -ForegroundColor Green
