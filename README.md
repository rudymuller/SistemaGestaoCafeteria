# Sistema Gestão Cafeteria — Python project

This repository now includes a Python virtual environment (.venv) and basic project files.

## Quick start — Windows (PowerShell)

1. Open PowerShell in the project root (h:\Atividades Extensionistas\Sistema Gestão Cafeteria)

2. Activate the venv:

- If policy allows executing scripts, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

- If Activation.ps1 is blocked by execution policy, you can enable it for the current process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Add packages and update requirements:

```powershell
pip install <package>
pip freeze > requirements.txt
```

## Other shells

- Command Prompt (cmd): `.venv\Scripts\activate.bat`
- Git Bash / WSL / macOS: `source .venv/bin/activate`

## Notes

- To create the venv yourself: `py -3 -m venv .venv` or `python -m venv .venv`
- The `.gitignore` already excludes `.venv/` so the environment won't be committed.
