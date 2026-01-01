$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$pythonCmd = @("py", "-3.11")

if (-not (Test-Path ".venv")) {
    & $pythonCmd -m venv .venv
}

.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

Write-Host "Install complete. Run: .\.venv\Scripts\Activate.ps1; python -m espectro_nec.main"
