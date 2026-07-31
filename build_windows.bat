@echo off
setlocal

echo ============================================
echo  Gerando o programa SST (isso demora uns minutos)
echo  Voce so precisa fazer isso UMA VEZ.
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao foi encontrado.
    echo Instale em https://www.python.org/downloads/
    echo IMPORTANTE: marque a caixa "Add Python to PATH" durante a instalacao.
    echo Depois de instalar, feche esta janela e clique de novo neste arquivo.
    pause
    exit /b 1
)

echo [1/4] Criando ambiente temporario de build...
python -m venv .venv_build
call .venv_build\Scripts\activate.bat

echo.
echo [2/4] Instalando dependencias do programa...
pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO ao instalar as dependencias. Copie a mensagem acima e peca ajuda.
    pause
    exit /b 1
)

echo.
echo [3/4] Instalando o empacotador (PyInstaller)...
pip install pyinstaller
if errorlevel 1 (
    echo ERRO ao instalar o PyInstaller. Copie a mensagem acima e peca ajuda.
    pause
    exit /b 1
)

echo.
echo [4/4] Gerando o executavel...
pyinstaller --onefile --name SST-Saude-Seguranca-Trabalho ^
    --add-data "app/templates;app/templates" ^
    --add-data "app/static;app/static" ^
    --collect-all reportlab ^
    desktop_run.py

echo.
if exist "dist\SST-Saude-Seguranca-Trabalho.exe" (
    echo ============================================
    echo  PRONTO!
    echo.
    echo  O programa esta em:
    echo  dist\SST-Saude-Seguranca-Trabalho.exe
    echo.
    echo  Copie esse arquivo (so ele) para onde quiser
    echo  no seu computador ^(ex: Area de Trabalho^).
    echo  Da em diante, e so clicar duas vezes nele
    echo  para abrir o programa. Nao precisa mais
    echo  deste terminal.
    echo ============================================
) else (
    echo Algo deu errado e o executavel nao foi criado.
    echo Copie toda a mensagem que apareceu acima e peca ajuda.
)

call .venv_build\Scripts\deactivate.bat
echo.
pause
