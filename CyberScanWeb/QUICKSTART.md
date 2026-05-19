# 🚀 DÉMARRAGE RAPIDE

## Site Vitrine (CyberScanWeb)

### Lancer le site vitrine

```bash
python app.py
```

Le site s'ouvre sur : **http://127.0.0.1:5000**

---

## Application CyberScan Dashboard (CyberScanSoft)

### Windows - 1 clic

```
Allez dans CyberScanSoft/
Double-cliquez start.bat
```

### Linux/Mac

```bash
cd CyberScanSoft
python3 setup.py
```

L'application démarre automatiquement sur **http://127.0.0.1:5000**

---

## 📂 Structure du Projet

```
CyberScan/
├── CyberScanWeb/          # Site vitrine
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
│
└── CyberScanSoft/         # Application desktop
    ├── start.bat          # Launcher Windows
    ├── setup.py           # Setup multi-plateforme
    ├── launcher.py
    ├── app.py
    ├── requirements.txt
    ├── templates/
    └── static/
```

---

## 🎯 Qu'est-ce que quoi?

**CyberScanWeb** = Site de présentation du projet
- Page d'accueil avec infos, features, screenshots
- Lancer avec: `python app.py`

**CyberScanSoft** = Application réelle de scanning réseau
- Scanne réseaux avec Nmap
- Interface web moderne
- Historique des scans
- Lancer avec: `start.bat` (Windows) ou `python3 setup.py` (Linux/Mac)

---

## ⚙️ Prérequis

- **Python 3.10+**
- **Nmap** (optionnel, pour CyberScanSoft uniquement)

### Windows
- Installer Python: https://www.python.org
- Installer Nmap (optionnel): https://nmap.org/download.html

### Linux
```bash
sudo apt-get install python3 python3-pip nmap
```

---

## 🎨 Customization (Site Vitrine)

### Changer le titre
- Fichier: `templates/index.html`
- Ligne: 6

### Changer les couleurs
- Fichier: `static/css/style.css`
- Variables CSS: lignes 1-10

### Ajouter du contenu
- Fichier: `templates/index.html`
- Copier une section existante

---

## 🌍 Déploiement DigitalOcean

### Gunicorn + Nginx

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

---

## 🔗 URLs Importantes

- **GitHub**: https://github.com/adesperrier/cyberscandashboard
- **Flask**: https://flask.palletsprojects.com
- **Nmap**: https://nmap.org
- **Python**: https://python.org

---

**✅ Démarrage rapide:**
1. Site vitrine: `python app.py`
2. App dashboard: Double-cliquez `CyberScanSoft/start.bat` (Windows) ou `cd CyberScanSoft && python3 setup.py` (Linux/Mac)

