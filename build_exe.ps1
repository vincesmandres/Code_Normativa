param(
    [string]$Name = "NEC15_app",
    [string]$Python = "py -3.11"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$pythonCmd = $Python.Split(" ")
& $pythonCmd -m pip install -r requirements.txt
& $pythonCmd -m pip install -r requirements-build.txt

$entry = Join-Path $root "run_app.py"
$src = Join-Path $root "src"

& $pythonCmd -m PyInstaller --noconfirm --clean --windowed --onefile --name $Name --paths $src $entry

Write-Host "EXE created at dist\$Name.exe"
