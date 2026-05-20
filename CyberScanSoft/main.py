"""
Entry point for CyberScan EXE
This wrapper ensures Nmap is properly configured when running as standalone EXE
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_nmap():
    """Setup Nmap path for PyInstaller bundle"""
    try:
        # Try to find nmap in common Windows locations
        nmap_paths = [
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / 'Nmap' / 'nmap.exe',
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')) / 'Nmap' / 'nmap.exe',
            Path('C:\\Nmap\\nmap.exe'),
        ]
        
        for nmap_path in nmap_paths:
            if nmap_path.exists():
                os.environ['NMAP_PATH'] = str(nmap_path)
                return str(nmap_path)
        
        # If Nmap not found, it might be in PATH
        try:
            result = subprocess.run(['nmap', '--version'], capture_output=True)
            if result.returncode == 0:
                return 'nmap'  # Use from PATH
        except:
            pass
        
        return None
    except Exception as e:
        print(f"Error setting up Nmap: {e}")
        return None

if __name__ == '__main__':
    # Setup Nmap before importing the app
    nmap_path = setup_nmap()
    
    if not nmap_path:
        print("\n" + "=" * 60)
        print("⚠️  Nmap not found on your system")
        print("=" * 60)
        print("\nCyberScan Dashboard requires Nmap to perform network scans.")
        print("\nPlease install Nmap from: https://nmap.org/download")
        print("\nAfter installing, run CyberScan.exe again.")
        print("=" * 60 + "\n")
        sys.exit(1)
    
    # Import and run the app
    from app import app
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
