@echo off
echo Starting Promptify Cloud Backend (via uv)...
cd /d "%~dp0"
cd backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
