# Editflow AI - CLI Runner
param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ArgsList
)
$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
& $python -m editflow @ArgsList
