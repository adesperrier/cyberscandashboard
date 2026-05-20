from flask import Flask, render_template, send_file
import os
import zipfile
import shutil
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download-cyberscan')
def download_cyberscan():
    """
    Télécharge le dossier CyberScanSoft sous forme de ZIP
    """
    try:
        # Chemins
        base_dir = Path(__file__).parent.parent  # CyberScan/
        cyberscan_soft_path = base_dir / 'CyberScanSoft'
        zip_path = Path(app.instance_path or '/tmp') / 'CyberScan.zip'
        
        # Créer le dossier instance s'il n'existe pas
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        
        # Créer le ZIP
        shutil.make_archive(str(zip_path.with_suffix('')), 'zip', cyberscan_soft_path.parent, 'CyberScanSoft')
        
        # Envoyer le fichier
        return send_file(
            zip_path,
            as_attachment=True,
            download_name='CyberScan_Dashboard.zip',
            mimetype='application/zip'
        )
    except Exception as e:
        print(f"Erreur téléchargement: {e}")
        return "Erreur lors du téléchargement", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
