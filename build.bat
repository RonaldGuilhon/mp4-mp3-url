@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   YouTube Downloader - Build Script
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Por favor, instale o Python primeiro.
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Executar o script de build
echo 🚀 Iniciando processo de build...
echo.
python build_executable.py

echo.
echo ========================================
echo           Build Finalizado
echo ========================================
pause