@echo off
setlocal enabledelayedexpansion

REM =======================================================
REM  NeuralPhish AI - One-Command Windows Startup Script
REM =======================================================

cd /d "%~dp0"
set "ROOT_DIR=%cd%"

echo ===========================================================
echo       NeuralPhish AI - Phishing Detection System
echo ===========================================================
echo Working Directory: %ROOT_DIR%
echo.

REM --- 1. Detect Python ---
set "PYTHON_CMD="
if exist "%ROOT_DIR%\venv\Scripts\python.exe" (
    set "PYTHON_CMD=%ROOT_DIR%\venv\Scripts\python.exe"
    echo [OK] Using virtual environment at: venv\Scripts\python.exe
) else if exist "%ROOT_DIR%\.venv\Scripts\python.exe" (
    set "PYTHON_CMD=%ROOT_DIR%\.venv\Scripts\python.exe"
    echo [OK] Using virtual environment at: .venv\Scripts\python.exe
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
        echo [OK] Using system Python
    ) else (
        echo [ERROR] Python was not found on your system!
        echo Please install Python 3.10+ from https://www.python.org/ or add it to PATH.
        pause
        exit /b 1
    )
)

REM --- 2. Check Python Dependencies ---
echo Checking Python dependencies...
"%PYTHON_CMD%" -c "import fastapi, uvicorn, pydantic, joblib, sklearn, pandas, nltk" >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Required Python dependencies are not fully installed.
    echo Installing dependencies from requirements.txt...
    "%PYTHON_CMD%" -m pip install -r "%ROOT_DIR%\requirements.txt"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Python dependencies. Please run:
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
)
echo [OK] Python dependencies verified.

REM --- 3. Detect Node & npm ---
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm was not found on your system!
    echo Please install Node.js (v18+) from https://nodejs.org/ to run the frontend.
    pause
    exit /b 1
)
echo [OK] npm detected.

REM --- 4. Check Frontend Dependencies ---
if not exist "%ROOT_DIR%\frontend\node_modules" (
    echo [INFO] frontend/node_modules not found. Installing frontend dependencies...
    cd /d "%ROOT_DIR%\frontend"
    call npm install
    cd /d "%ROOT_DIR%"
)
echo [OK] Frontend dependencies verified.

echo.
echo ===========================================================
echo  Select Startup Mode:
echo    [1] Full Development Mode (FastAPI Backend + Vite Frontend)
echo    [2] Single-Service Production Preview (FastAPI serves built frontend)
echo    [3] Build Frontend Only (npm run build)
echo ===========================================================
set /p "STARTUP_CHOICE=Enter choice [1, 2, or 3, default: 1]: "
if "%STARTUP_CHOICE%"=="" set "STARTUP_CHOICE=1"

if "%STARTUP_CHOICE%"=="2" goto mode_single_service
if "%STARTUP_CHOICE%"=="3" goto mode_build_only
goto mode_dev

:mode_dev
echo.
echo Starting NeuralPhish AI in Development Mode...
echo - Starting FastAPI backend on http://127.0.0.1:8000
echo - Starting Vite frontend on http://localhost:5173 (with API proxy)
echo.

start "NeuralPhish AI - Backend (FastAPI)" cmd /k "cd /d "%ROOT_DIR%" && "%PYTHON_CMD%" -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 2 /nobreak >nul

start "NeuralPhish AI - Frontend (Vite Dev Server)" cmd /k "cd /d "%ROOT_DIR%\frontend" && npm run dev"

echo.
echo ===========================================================
echo  NeuralPhish AI is running!
echo  - Frontend UI:        http://localhost:5173
echo  - Backend API:       http://localhost:8000
echo  - Swagger API Docs:  http://localhost:8000/docs
echo ===========================================================
echo Close the individual terminal windows to stop the servers.
pause
exit /b 0

:mode_single_service
echo.
if not exist "%ROOT_DIR%\frontend\dist\index.html" (
    echo [INFO] Production build not found in frontend/dist. Building frontend now...
    cd /d "%ROOT_DIR%\frontend"
    call npm run build
    cd /d "%ROOT_DIR%"
)
echo.
echo Starting NeuralPhish AI Single-Service Server...
echo - URL: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo.
"%PYTHON_CMD%" "%ROOT_DIR%\run.py"
pause
exit /b 0

:mode_build_only
echo.
echo Building frontend for production...
cd /d "%ROOT_DIR%\frontend"
call npm run build
cd /d "%ROOT_DIR%"
echo.
echo Frontend build complete in frontend/dist!
pause
exit /b 0
