# 🔐 CyberScan Dashboard

Application web de scan réseau et d'analyse cybersécurité développée en Python Flask.

## 🚀 Démarrage Rapide (1 clic)

### Windows
Double-cliquez sur **start.bat**

### Linux/Mac
```bash
python3 setup.py
```

L'application s'ouvre automatiquement sur **http://127.0.0.1:5000**

---

## 📂 Structure

```
CyberScanSoft/
├── start.bat                # Launcher Windows (1 clic)
├── setup.py                 # Setup & launcher multi-plateforme
├── launcher.py              # Flask launcher
├── app.py                   # Application Flask
├── requirements.txt         # Dépendances
├── templates/
│   └── index.html          # Interface web
├── static/
│   ├── styles.css          # Design cyberpunk
│   ├── dashboard.js        # Interactions
│   └── img/               # Assets
└── scans/                 # Historique JSON
```

## 🎯 Fonctionnalités

✅ **Scanner Réseau**
- Port scanning TCP
- Détection services
- Identification versions
- Détection vulnérabilités
- Mode rapide/complet/personnalisé

✅ **Interface Web Moderne**
- Dashboard cyberpunk sombre
- Formulaire scan interactif
- Tableau résultats dynamique
- Historique scans
- Modal vulnérabilités

## ⚙️ Configuration Requise

**Logiciel:**
- Python 3.10+
- Flask 3.0.0
- python-nmap 0.7.1

**Optionnel (pour scanning réseau):**
- Nmap (https://nmap.org)

**Système:**
- Windows 10+ / Linux / Mac
- 200 MB RAM minimum
- Connexion réseau

## 🔧 Utilisation

### Démarrage Automatique

**Windows:** Double-cliquez `start.bat` - c'est tout!

**Linux/Mac:** `python3 setup.py`

### Formulaire Scan

1. **Cible** : IP (`192.168.1.10`), CIDR (`10.0.0.0/24`) ou domaine
2. **Mode** : 
   - Quick : Top 100 ports
   - Common : Services courants
   - Full : Tous les ports (lent)
3. **Ports Custom** : Optionnel (ex: `80,443,8080`)

## 🛡️ Sécurité

⚠️ **IMPORTANT**: CyberScan doit UNIQUEMENT être utilisé sur:
- Systèmes dont vous êtes propriétaire
- Réseaux autorisés
- Tests autorisés

L'utilisation non autorisée est **ILLÉGALE**.

## 🎨 Design

**Thème Cyberpunk Sombre:**
- Fond: #0a0e27
- Bleu néon: #00d9ff
- Vert néon: #00ff88
- Animations fluides
- Responsive design

## 🐛 Troubleshooting

### "Python n'est pas reconnu"
- Windows: Réinstallez Python avec "Add to PATH" coché
- Linux: Utilisez `python3` au lieu de `python`

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port déjà utilisé"
setup.py cherche automatiquement le prochain port disponible (5000-9000)

### "Nmap introuvable"
```bash
# Windows: https://nmap.org/download.html
# Linux: sudo apt-get install nmap
# macOS: brew install nmap
```

L'application marche sans Nmap mais le scan réseau ne fonctionne pas.

### Chemin Nmap personnalisé
Si Nmap n'est pas dans le `PATH`, CyberScan peut aussi le prendre via une variable d'environnement :

```bash
set NMAP_PATH=C:\Program Files (x86)\Nmap\nmap.exe
```

Ou en pointant le dossier :

```bash
set NMAP_DIR=C:\Program Files (x86)\Nmap
```

Le lanceur et l'application essaient ensuite ce chemin avant les emplacements Windows standards.

## 🔗 Ressources

- GitHub: https://github.com/adesperrier/cyberscandashboard
- Nmap: https://nmap.org
- Flask: https://flask.palletsprojects.com

## 👤 Développeur

**Antoine Desperrier**
- GitHub: @adesperrier
- LinkedIn: /in/adesperrier

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready

