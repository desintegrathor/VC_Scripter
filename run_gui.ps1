# Run VC Script Decompiler GUI from PowerShell
# This ensures the compiler can execute properly through subprocess

Write-Host "Starting VC Script Decompiler GUI..." -ForegroundColor Green
py -m vcdecomp gui
