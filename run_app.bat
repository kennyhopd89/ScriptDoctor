@echo off
title Script Doctor Pro Launcher
echo ===================================================
echo        SCRIPT DOCTOR PRO - AI ASSISTANT
echo ===================================================
echo.
echo [1/3] Dang xac dinh thu muc lam viec...
cd /d "%~dp0"

echo [2/3] Kiem tra moi truong Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Python chua duoc cai dat hoac khong co trong PATH.
    echo Vui long cai dat Python va thu lai.
    pause
    exit /b
)

echo [3/3] Dang khoi dong ung dung...
echo       Trinh duyet se tu dong mo sau vai giay.
echo.
echo ---------------------------------------------------
echo Nhan Ctrl+C tai cua so nay de dung ung dung.
echo ---------------------------------------------------
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [Setup] Tao moi truong ao (venv)...
    python -m venv .venv
)

call ".venv\Scripts\activate.bat"

echo [Setup] Cai dat phu thuoc...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

streamlit run app.py

if %errorlevel% neq 0 (
    echo.
    echo [LOI] Ung dung da dung dot ngot.
    pause
)
