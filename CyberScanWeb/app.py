from flask import Flask, render_template, send_file, redirect
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Softexe/CyberScan.exe')
def download_exe():
    return redirect('https://github.com/adesperrier/cyberscandashboard/releases/download/dev/CyberScan.zip')

@app.route('/download/CyberScan.exe')
def download_exe_alt():
    return redirect('https://github.com/adesperrier/cyberscandashboard/releases/download/dev/CyberScan.zip')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
