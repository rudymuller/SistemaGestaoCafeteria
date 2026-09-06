$ErrorActionPreference = "Stop"

$python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Ambiente virtual não encontrado. Crie o .venv antes de executar este script."
}

& $python -m pip install -r requirements.txt
& $python -m pip install -r requirements-build.txt
& $python -m PyInstaller --clean --noconfirm --onefile --windowed `
    --name SistemaGestaoCafeteria `
    --paths src `
    --collect-all fontawesomefree `
    src\Main.py

New-Item -ItemType Directory -Force -Path "dist\data" | Out-Null
Write-Host "Executável criado em dist\SistemaGestaoCafeteria.exe"
Write-Host "Coloque o banco de dados em dist\data\SysDB.db antes de distribuir."