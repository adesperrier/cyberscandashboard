#!/bin/bash

# =====================================================
# CyberScan Dashboard - Linux Setup & Launch Script
# =====================================================
# Ce script installe les dépendances et lance l'app
# =====================================================

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║     CyberScan Dashboard - Linux Launcher        ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERREUR: Python3 n'est pas installé"
    echo ""
    echo "Installez Python3 avec:"
    echo "  Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y python3 python3-pip"
    echo "  Fedora:        sudo dnf install -y python3 python3-pip"
    echo "  Arch:          sudo pacman -S --noconfirm python python-pip"
    echo ""
    exit 1
fi

python3 --version
echo "✓ Python détecté"
echo ""

# Installer les dépendances Python
echo "📥 Installation des dépendances Python..."
pip3 install -q Flask==3.0.0
pip3 install -q python-nmap==0.0.1
pip3 install -q Werkzeug==3.0.0
if [ $? -ne 0 ]; then
    echo "❌ ERREUR: Impossible d'installer les dépendances"
    exit 1
fi
echo "✓ Dépendances Python installées"
echo ""

# Vérifier Nmap
echo "🔍 Vérification de Nmap..."
if ! command -v nmap &> /dev/null; then
    echo ""
    echo "❌ ERREUR: Nmap n'est pas installé"
    echo ""
    echo "📖 Installez Nmap avec:"
    echo ""

    if command -v apt-get &> /dev/null; then
        echo "   Ubuntu/Debian:"
        echo "   sudo apt-get update && sudo apt-get install -y nmap"
    fi

    if command -v dnf &> /dev/null; then
        echo "   Fedora:"
        echo "   sudo dnf install -y nmap"
    fi

    if command -v pacman &> /dev/null; then
        echo "   Arch:"
        echo "   sudo pacman -S nmap"
    fi

    if command -v brew &> /dev/null; then
        echo "   macOS:"
        echo "   brew install nmap"
    fi

    echo ""
    echo "Après installation, relancez ce script."
    exit 1
else
    nmap --version | head -1
    echo "✓ Nmap détecté"
fi

echo ""
echo "🚀 Démarrage de CyberScan Dashboard..."
echo ""

# Lancer l'application
python3 launcher.py

exit 0
