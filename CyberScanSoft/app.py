import sys
import os
import subprocess
import json
import nmap
import socket
from datetime import datetime
from flask import Flask, render_template, request, jsonify

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

SCANS_DIR = os.path.join(os.path.dirname(__file__), 'scans')
os.makedirs(SCANS_DIR, exist_ok=True)
MAX_SCANS = 15


def resolve_nmap_search_path():
    """Return a list of Nmap executable locations to try in order."""
    search_paths = []

    explicit_path = os.environ.get('NMAP_PATH', '').strip()
    if explicit_path:
        search_paths.append(explicit_path)

    nmap_dir = os.environ.get('NMAP_DIR', '').strip()
    if nmap_dir:
        search_paths.append(os.path.join(nmap_dir, 'nmap.exe'))

    search_paths.extend([
        os.path.join(os.environ.get('PROGRAMFILES', r'C:\Program Files'), 'Nmap', 'nmap.exe'),
        os.path.join(os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)'), 'Nmap', 'nmap.exe'),
        r'C:\Nmap\nmap.exe',
    ])

    if os.name == 'nt':
        paths_value = os.environ.get('PATH', '')
        for folder in paths_value.split(os.pathsep):
            folder = folder.strip('"')
            if folder:
                search_paths.append(os.path.join(folder, 'nmap.exe'))

    unique_paths = []
    for candidate in search_paths:
        if candidate and candidate not in unique_paths:
            unique_paths.append(candidate)

    return unique_paths


def create_port_scanner():
    """Create a PortScanner with an explicit Nmap executable search path."""
    search_paths = resolve_nmap_search_path()

    for candidate in search_paths:
        if os.path.exists(candidate):
            return nmap.PortScanner(nmap_search_path=[candidate])

    return nmap.PortScanner(nmap_search_path=search_paths)

def cleanup_old_scans():
    """Keep only the MAX_SCANS most recent scans"""
    try:
        scans = sorted([f for f in os.listdir(SCANS_DIR) if f.endswith('.json')], reverse=True)
        if len(scans) > MAX_SCANS:
            for old_scan in scans[MAX_SCANS:]:
                os.remove(os.path.join(SCANS_DIR, old_scan))
    except Exception as e:
        print(f"Cleanup error: {e}")

VULNERABILITY_DB = {
    21: {'service': 'FTP', 'risk': 'HIGH', 'issues': ['Credentials in cleartext', 'Old protocol']},
    23: {'service': 'Telnet', 'risk': 'CRITICAL', 'issues': ['No encryption', 'Deprecated']},
    80: {'service': 'HTTP', 'risk': 'MEDIUM', 'issues': ['No encryption', 'Use HTTPS']},
    443: {'service': 'HTTPS', 'risk': 'LOW', 'issues': ['Verify certificate']},
    22: {'service': 'SSH', 'risk': 'LOW', 'issues': ['Verify key-based auth']},
    445: {'service': 'SMB', 'risk': 'HIGH', 'issues': ['Ransomware target', 'Patch required']},
    3306: {'service': 'MySQL', 'risk': 'HIGH', 'issues': ['Exposed DB', 'Weak credentials']},
    5432: {'service': 'PostgreSQL', 'risk': 'HIGH', 'issues': ['Exposed DB', 'No auth']},
    27017: {'service': 'MongoDB', 'risk': 'CRITICAL', 'issues': ['No authentication by default']},
    6379: {'service': 'Redis', 'risk': 'CRITICAL', 'issues': ['No auth by default', 'Data exposure']},
    3389: {'service': 'RDP', 'risk': 'HIGH', 'issues': ['Brute force target']},
    135: {'service': 'RPC', 'risk': 'HIGH', 'issues': ['Wormable service']},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target = data.get('target', '').strip()
    mode = data.get('mode', 'quick')
    custom_ports = data.get('custom_ports', '')

    if not target:
        return jsonify({'error': 'Target required'}), 400

    port_ranges = {
        'quick': '1-100',
        'common': '1,3,22,25,53,80,110,143,443,445,993,995,1433,3306,3389,5432,5900,8080,8443,27017,6379',
        'full': '1-65535'
    }

    if custom_ports:
        ports = custom_ports
    else:
        ports = port_ranges.get(mode, '1-100')

    try:
        nm = create_port_scanner()
        scan_args = f'-sV -p {ports}'
        nm.scan(target, arguments=scan_args)

        results = []
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        port_data = nm[host][proto][port]
                        port_num = int(port)
                        state = port_data['state']
                        service = port_data.get('name', 'unknown')
                        product = port_data.get('product', '')
                        version = port_data.get('version', '')

                        vuln_info = VULNERABILITY_DB.get(port_num, {})

                        results.append({
                            'host': host,
                            'port': port_num,
                            'state': state,
                            'service': service,
                            'product': product,
                            'version': version,
                            'risk': vuln_info.get('risk', 'LOW'),
                            'issues': vuln_info.get('issues', [])
                        })

        scan_result = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'ports': results,
            'summary': {
                'total_ports': len(results),
                'open_ports': len([r for r in results if r['state'] == 'open']),
                'filtered_ports': len([r for r in results if r['state'] == 'filtered']),
                'critical_issues': len([r for r in results if r['risk'] == 'CRITICAL']),
                'high_issues': len([r for r in results if r['risk'] == 'HIGH']),
            }
        }

        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{target.replace('/', '_')}.json"
        filepath = os.path.join(SCANS_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(scan_result, f, indent=2, ensure_ascii=False)

        cleanup_old_scans()

        return jsonify(scan_result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    history = []
    try:
        for filename in sorted(os.listdir(SCANS_DIR), reverse=True)[:MAX_SCANS]:
            if filename.endswith('.json'):
                filepath = os.path.join(SCANS_DIR, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    history.append({
                        'filename': filename,
                        'target': data.get('target'),
                        'timestamp': data.get('timestamp'),
                        'summary': data.get('summary')
                    })
    except:
        pass
    return jsonify(history)

@app.route('/api/scan/<filename>', methods=['GET'])
def get_scan_details(filename):
    try:
        filepath = os.path.join(SCANS_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Scan not found'}), 404
        with open(filepath, 'r') as f:
            data = json.load(f)
            return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan/<filename>', methods=['DELETE'])
def delete_scan(filename):
    try:
        filepath = os.path.join(SCANS_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Scan not found'}), 404
        os.remove(filepath)
        return jsonify({'success': True, 'message': 'Scan deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': 'online', 'version': '1.0.0'})

def open_browser():
    """Open the browser after a short delay to let Flask start"""
    import time
    import webbrowser
    time.sleep(2)
    try:
        webbrowser.open('http://127.0.0.1:5000')
    except Exception as e:
        print(f"Could not open browser: {e}")

if __name__ == '__main__':
    # Open browser in a separate thread
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n" + "=" * 60)
    print("CyberScan Dashboard - Starting...")
    print("=" * 60)
    print("\n🔍 Server running at: http://127.0.0.1:5000")
    print("🌐 Browser opening automatically...")
    print("\n✨ Press Ctrl+C to stop the server\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
