@echo off
chcp 65001 >nul
color 0A
mode con: cols=80 lines=30

echo.
echo ████████████████████████████████████████████████████████████████████████████████
echo █                                                                              █
echo █                    YouTube Downloader - Build Avançado                     █
echo █                        Criando Executável Portável                         █
echo █                                                                              █
echo ████████████████████████████████████████████████████████████████████████████████
echo.

REM Verificar se estamos no diretório correto
if not exist "main.py" (
    echo ❌ Erro: main.py não encontrado!
    echo    Certifique-se de executar este script na pasta do projeto.
    echo.
    pause
    exit /b 1
)

REM Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 Para instalar o Python:
    echo    1. Acesse: https://www.python.org/downloads/
    echo    2. Baixe a versão mais recente
    echo    3. Durante a instalação, marque "Add Python to PATH"
    echo    4. Reinicie o computador após a instalação
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% encontrado
echo.

REM Verificar se pip está funcionando
echo 🔍 Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip não encontrado!
    echo 🔧 Tentando instalar pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ Falha ao instalar pip!
        pause
        exit /b 1
    )
)
echo ✅ pip funcionando
echo.

REM Perguntar qual método usar
echo 🤔 Escolha o método de build:
echo.
echo    [1] Build Simples (Rápido)
echo    [2] Build Avançado (Otimizado)
echo    [3] Build Manual (Personalizado)
echo.
set /p "choice=Digite sua escolha (1-3): "

if "%choice%"=="1" goto simple_build
if "%choice%"=="2" goto advanced_build
if "%choice%"=="3" goto manual_build

echo ❌ Opção inválida!
pause
exit /b 1

:simple_build
echo.
echo 🚀 Iniciando Build Simples...
echo ════════════════════════════════════════
python build_executable.py
goto end

:advanced_build
echo.
echo 🚀 Iniciando Build Avançado...
echo ════════════════════════════════════════
python build_advanced.py
goto end

:manual_build
echo.
echo 🚀 Iniciando Build Manual...
echo ════════════════════════════════════════
echo.
echo 📦 Instalando dependências...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências!
    pause
    exit /b 1
)

echo.
echo 🔨 Executando PyInstaller...
if exist "YouTubeDownloader.spec" (
    echo    Usando arquivo .spec personalizado...
    python -m PyInstaller --clean YouTubeDownloader.spec
) else (
    echo    Usando configuração padrão...
    python -m PyInstaller --onefile --windowed --name=YouTubeDownloader --add-data="bin;bin" --hidden-import=tkinter --hidden-import=yt_dlp --clean main.py
)

if %errorlevel% neq 0 (
    echo ❌ Erro no PyInstaller!
    pause
    exit /b 1
)

echo.
echo 📁 Verificando resultado...
if exist "dist\YouTubeDownloader.exe" (
    echo ✅ Executável criado com sucesso!
    echo 📍 Localização: dist\YouTubeDownloader.exe
    
    REM Calcular tamanho do arquivo
    for %%A in ("dist\YouTubeDownloader.exe") do (
        set size=%%~zA
        set /a sizeMB=!size!/1048576
        echo 📊 Tamanho: !sizeMB! MB
    )
) else (
    echo ❌ Executável não foi criado!
    pause
    exit /b 1
)

:end
echo.
echo ████████████████████████████████████████████████████████████████████████████████
echo █                                                                              █
echo █                           BUILD FINALIZADO!                                █
echo █                                                                              █
echo ████████████████████████████████████████████████████████████████████████████████
echo.

REM Verificar se existe pasta release
if exist "release" (
    echo 🎉 Pacote de distribuição criado em: release\
    echo.
    echo 📋 Conteúdo do pacote:
    dir /b release
    echo.
    echo 💡 Dica: Você pode distribuir toda a pasta 'release'
) else if exist "dist\YouTubeDownloader.exe" (
    echo 🎉 Executável criado em: dist\YouTubeDownloader.exe
    echo.
    echo 💡 Dica: Você pode distribuir apenas este arquivo
)

echo.
echo 🚀 Para testar o executável:
if exist "release\YouTubeDownloader.exe" (
    echo    release\YouTubeDownloader.exe
) else (
    echo    dist\YouTubeDownloader.exe
)

echo.
echo ⚠️  Observações importantes:
echo    • Primeiro uso pode ser mais lento
echo    • Alguns antivírus podem alertar (falso positivo)
echo    • Mantenha o executável atualizado
echo.

set /p "test=Deseja testar o executável agora? (s/n): "
if /i "%test%"=="s" (
    if exist "release\YouTubeDownloader.exe" (
        start "" "release\YouTubeDownloader.exe"
    ) else if exist "dist\YouTubeDownloader.exe" (
        start "" "dist\YouTubeDownloader.exe"
    )
)

echo.
echo ✨ Obrigado por usar o YouTube Downloader!
pause