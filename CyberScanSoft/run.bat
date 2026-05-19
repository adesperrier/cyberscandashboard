@echo off
chcp 65001 >nul 2>&1
REM =====================================================
REM CyberScan Dashboard - Windows Setup & Launch Script
REM =====================================================
REM Ce script installe les dépendances et lance l'app
REM =====================================================

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║     CyberScan Dashboard - Windows Launcher       ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé
    echo.
    echo Installez Python depuis: https://www.python.org/
    echo Assurez-vous de cocher "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo ✓ Python trouvé
echo.

REM Installer les dépendances Python
echo 📥 Installation des dépendances Python...
pip install -q Flask==3.0.0
pip install -q python-nmap==0.0.1
pip install -q Werkzeug==3.0.0
if errorlevel 1 (
    echo ❌ ERREUR: Impossible d'installer les dépendances
    pause
    exit /b 1
)
echo ✓ Dépendances Python installées
echo.

REM Vérifier Nmap
echo 🔍 Vérification de Nmap...
nmap --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Nmap n'est pas installé ou pas dans le PATH
    echo.
    echo 📖 Options:
    echo.
    echo Option 1 - Installer Nmap manuellement:
    echo   1. Téléchargez: https://nmap.org/download.html
    echo   2. Exécutez l'installeur Windows
    echo   3. Garder les réglages par défaut
    echo   4. Redémarrez ce script
    echo.
    echo Option 2 - Ajouter Nmap au PATH automatiquement:
    echo   (Si Nmap est déjà installé)
    echo.

    REM Chercher Nmap dans les emplacements courants
    if exist "C:\Program Files (x86)\Nmap\nmap.exe" (
        echo ✓ Nmap trouvé dans: C:\Program Files\Nmap
        echo 🔧 Ajout au PATH...
        setx PATH "%PATH%;C:\Program Files\Nmap" >nul 2>&1
        if errorlevel 0 (
            echo ✓ Nmap ajouté au PATH
            echo.
            echo 🔄 Redémarrez ce script pour continuer
            pause
            exit /b 1
        )
    ) 
    ) else (
        echo.
        echo ℹ️  Nmap n'a pas été trouvé dans les emplacements standards
        echo    Installez-le depuis: https://nmap.org/download.html
        echo.
        pause
        exit /b 1
    )
)

nmap --version | findstr /R "Nmap" >nul
echo ✓ Nmap détecté
echo.

echo 🚀 Démarrage de CyberScan Dashboard...
echo.

REM Lancer l'application
python launcher.py

pause
