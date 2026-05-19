import os
import sys
import threading
import webbrowser
import time
import socket

# Fix Unicode encoding on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def find_free_port(start=5000, end=9000):
    """Trouve un port libre."""
    for port in range(start, end):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            continue
    return 5000

def start_flask(port):
    """Démarre Flask."""
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = '0'

    from app import app
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False, threaded=True)

def main():
    port = find_free_port()

    print("\n" + "="*60)
    print("🔐 CyberScan Dashboard")
    print("="*60)
    print(f"Démarrage sur le port {port}...")

    # Démarrer Flask en thread daemon
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    # Attendre que Flask démarre
    time.sleep(2)

    # Ouvrir le navigateur
    url = f"http://127.0.0.1:{port}"
    print(f"✓ Ouverture du navigateur: {url}\n")
    webbrowser.open(url)

    print("="*60)
    print("Application en cours d'exécution")
    print(f"URL: {url}")
    print("Appuyez sur Ctrl+C pour arrêter")
    print("="*60 + "\n")

    try:
        flask_thread.join()
    except KeyboardInterrupt:
        print("\n\nArrêt de l'application...")
        return 0

if __name__ == '__main__':
    sys.exit(main())
