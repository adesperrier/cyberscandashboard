from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Softexe/CyberScan.exe')
def download_exe():
    exe_path = os.path.join(os.path.dirname(__file__), '..', 'Softexe', 'CyberScan.exe')
    if os.path.exists(exe_path):
        return send_file(exe_path, as_attachment=True, download_name='CyberScan.exe')
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
