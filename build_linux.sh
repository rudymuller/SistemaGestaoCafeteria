#!/usr/bin/env bash
set -euo pipefail

python=".venv/bin/python"
if [[ ! -x "$python" ]]; then
    echo "Ambiente virtual não encontrado. Crie o .venv antes de executar este script." >&2
    exit 1
fi

"$python" -m pip install -r requirements.txt
"$python" -m pip install -r requirements-build.txt
"$python" -m PyInstaller --clean --noconfirm --onefile --windowed \
    --name SistemaGestaoCafeteria \
    --paths src \
    --collect-all fontawesomefree \
    src/Main.py

mkdir -p dist/data
echo "Executável criado em dist/SistemaGestaoCafeteria"
echo "Coloque o banco de dados em dist/data/SysDB.db antes de distribuir."