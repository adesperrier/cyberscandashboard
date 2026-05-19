# =====================================================
# CyberScan Dashboard - Windows Setup & Launch Script
# =====================================================
# Ce script installe les dépendances et lance l'app
# =====================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     CyberScan Dashboard - Windows Launcher       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Vérifier Python
Write-Host "🔍 Vérification de Python..." -ForegroundColor Yellow
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERREUR: Python n'est pas installé" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installez Python depuis: https://www.python.org/" -ForegroundColor Yellow
    Write-Host "Assurez-vous de cocher ""Add Python to PATH""" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Appuyez sur Entrée pour fermer"
    exit 1
}

Write-Host $pythonCheck
Write-Host "✓ Python trouvé" -ForegroundColor Green
Write-Host ""

# Installer les dépendances Python
Write-Host "📥 Installation des dépendances Python..." -ForegroundColor Yellow
pip install -q Flask==3.0.0
pip install -q python-nmap==0.0.1
pip install -q Werkzeug==3.0.0

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERREUR: Impossible d'installer les dépendances" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour fermer"
    exit 1
}
Write-Host "✓ Dépendances Python installées" -ForegroundColor Green
Write-Host ""

# Vérifier Nmap
Write-Host "🔍 Vérification de Nmap..." -ForegroundColor Yellow
$nmapCheck = nmap --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ ERREUR: Nmap n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "📖 Options:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1 - Installer Nmap manuellement:" -ForegroundColor Yellow
    Write-Host "  1. Téléchargez: https://nmap.org/download.html" -ForegroundColor Cyan
    Write-Host "  2. Exécutez l'installeur Windows" -ForegroundColor Cyan
    Write-Host "  3. Garder les réglages par défaut" -ForegroundColor Cyan
    Write-Host "  4. Redémarrez ce script" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Option 2 - Ajouter Nmap au PATH automatiquement:" -ForegroundColor Yellow
    Write-Host "  (Si Nmap est déjà installé)" -ForegroundColor Cyan
    Write-Host ""

    # Chercher Nmap dans les emplacements courants
    if (Test-Path "C:\Program Files (x86)\Nmap\nmap.exe") {
        Write-Host "✓ Nmap trouvé dans: C:\Program Files (x86)\Nmap" -ForegroundColor Green
        Write-Host "🔧 Ajout au PATH..." -ForegroundColor Yellow

        $env:Path += ";C:\Program Files (x86)\Nmap"
        [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)

        Write-Host "✓ Nmap ajouté au PATH" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔄 Redémarrez ce script pour continuer" -ForegroundColor Yellow
        Read-Host "Appuyez sur Entrée pour fermer"
        exit 1
    } elseif (Test-Path "C:\Program Files\Nmap\nmap.exe") {
        Write-Host "✓ Nmap trouvé dans: C:\Program Files\Nmap" -ForegroundColor Green
        Write-Host "🔧 Ajout au PATH..." -ForegroundColor Yellow

        $env:Path += ";C:\Program Files\Nmap"
        [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)

        Write-Host "✓ Nmap ajouté au PATH" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔄 Redémarrez ce script pour continuer" -ForegroundColor Yellow
        Read-Host "Appuyez sur Entrée pour fermer"
        exit 1
    } else {
        Write-Host ""
        Write-Host "ℹ️  Nmap n'a pas été trouvé dans les emplacements standards" -ForegroundColor Yellow
        Write-Host "   Installez-le depuis: https://nmap.org/download.html" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "Appuyez sur Entrée pour fermer"
        exit 1
    }
}

$nmapCheck | Select-Object -First 1
Write-Host "✓ Nmap détecté" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Démarrage de CyberScan Dashboard..." -ForegroundColor Green
Write-Host ""

# Lancer l'application
python launcher.py

Read-Host "Appuyez sur Entrée pour fermer"
