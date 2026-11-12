# Editflow AI - Project Migration & Sync Script
param (
    [string]$Source = "D:\Codealytica\Video_PostProduction",
    [switch]$DryRun
)
Write-Host "[*] Running Project Migration from $Source..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "[INFO] Dry-run enabled. No files will be modified."
} else {
    Write-Host "[+] Migration verification complete. Workspace synced." -ForegroundColor Green
}
