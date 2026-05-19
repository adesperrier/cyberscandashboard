#!/usr/bin/env python3
"""
CyberScan Dashboard - Setup & Launch Script
Installe les dépendances et lance l'application
"""

import sys
import subprocess
import os
import shutil

def print_header(text):
    print(f"\n{'='*60}")
    print(text)
    print('='*60)

def check_python():
    """Verify Python is installed"""
    version = sys.version.split()[0]
    print(f"[OK] Python {version} found")
    return True

def install_dependencies():
    """Install required packages"""
    print("[*] Installing dependencies...")

    packages = [
        "Flask==3.0.0",
        "python-nmap==0.7.1",
        "Werkzeug==3.0.0"
    ]

    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
            print(f"    [OK] {package}")
        except subprocess.CalledProcessError:
            print(f"    [ERROR] Failed to install {package}")
            return False

    return True

def check_nmap():
    """Check if nmap is installed"""
    nmap_path = shutil.which("nmap")

    if nmap_path:
        print(f"[OK] Nmap found at {nmap_path}")
        return True
    else:
        print("[!] Nmap not found")
        print("\n    Windows: Download from https://nmap.org/download.html")
        print("    Linux/Ubuntu: sudo apt-get install nmap")
        print("    macOS: brew install nmap")
        return False

def start_application():
    """Start the Flask application"""
    print("\n[*] Starting CyberScan Dashboard...")

    launcher_path = os.path.join(os.path.dirname(__file__), "launcher.py")

    if not os.path.exists(launcher_path):
        print("[ERROR] launcher.py not found!")
        return False

    try:
        subprocess.call([sys.executable, launcher_path])
        return True
    except KeyboardInterrupt:
        print("\n\n[*] Application stopped")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to start application: {e}")
        return False

def main():
    print_header("CyberScan Dashboard - Setup & Launch")

    # Check Python
    print("[*] Checking Python...")
    if not check_python():
        print("[ERROR] Python is required")
        return 1

    # Install dependencies
    print("\n[*] Installing Python packages...")
    if not install_dependencies():
        print("[ERROR] Failed to install dependencies")
        return 1

    # Check Nmap
    print("\n[*] Checking Nmap...")
    has_nmap = check_nmap()

    if not has_nmap:
        print("\n[WARNING] Nmap not found - network scanning will not work")
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return 1

    # Start application
    print_header("Starting Application")
    return 0 if start_application() else 1

if __name__ == "__main__":
    sys.exit(main())
