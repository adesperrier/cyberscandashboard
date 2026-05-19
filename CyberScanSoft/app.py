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
        nm = nmap.PortScanner()
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

        return jsonify(scan_result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    history = []
    try:
        for filename in sorted(os.listdir(SCANS_DIR), reverse=True)[:10]:
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

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': 'online', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
