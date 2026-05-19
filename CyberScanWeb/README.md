# 🌐 CyberScan Dashboard - Site Vitrine

Site web moderne pour présenter **CyberScan Dashboard**, un outil de scan réseau et d'analyse cybersécurité.

## 🚀 Installation Rapide

### Option 1: Utilisateurs (Recommended)

**Windows:**
```bash
1. Téléchargez l'application
2. Double-cliquez sur run.bat
3. Le navigateur s'ouvre automatiquement
```

**Linux/Mac:**
```bash
./run.sh
```

### Option 2: Développeurs (Source Code)

```bash
git clone https://github.com/adesperrier/cyberscandashboard
cd cyberscandashboard/CyberScanSoft

# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

### Option 3: Manuel

```bash
pip install -r requirements.txt
python launcher.py
```

L'application s'ouvre automatiquement sur **http://127.0.0.1:5000**

## 🎯 Sections du Site

1. **Navbar** - Navigation fluide
2. **Hero** - Présentation du projet
3. **Fonctionnalités** - 6 features principales
4. **Architecture** - Flux utilisateur
5. **Technologies** - Stack complet
6. **Screenshots** - Aperçu interface
7. **Installation** - Guide démarrage
8. **Roadmap** - Futures fonctionnalités
9. **Footer** - Ressources & contact

## 🎨 Design

- Thème cyberpunk sombre
- Bleu néon (#00d9ff)
- Animations fluides
- Responsive mobile-first
- Performance optimisée

## 🔧 Prérequis

- Python 3.10+
- Flask 3.0.0
- Nmap (optionnel, pour scanning réseau)

**Windows:**
- Installer Python: https://www.python.org
- Installer Nmap: https://nmap.org/download.html

**Linux:**
```bash
sudo apt-get install python3 python3-pip nmap
```

## 📦 Structure du Projet

```
CyberScan/
├── CyberScanWeb/          # Site vitrine (ce dossier)
│   ├── app.py             # Flask simple
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── README.md
│
└── CyberScanSoft/         # Application desktop
    ├── run.bat            # Windows launcher
    ├── run.sh             # Linux launcher
    ├── launcher.py        # Python launcher
    ├── app.py             # Flask app
    ├── templates/
    ├── static/
    └── README.md
```

## ⚠️ Avertissement Légal

**Utilisation Autorisée UNIQUEMENT sur:**
- Systèmes dont vous êtes propriétaire
- Réseaux autorisés
- Tests de pénétration autorisés

L'utilisation non autorisée est **ILLÉGALE**.

## 📝 Lancer CyberScan

### 1️⃣ Installation

**Windows:**
```
Double-cliquez run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Manuel:**
```bash
pip install -r requirements.txt
python launcher.py
```

### 2️⃣ Scanner une Cible

1. Entrez une IP, CIDR ou domaine
2. Choisissez un mode de scan
3. Cliquez "Scanner"
4. Consultez les résultats

### 3️⃣ Analyser les Vulnérabilités

- Ports ouverts en vert
- Services identifiés
- Vulnérabilités détectées
- Solutions recommandées

## 🐛 Troubleshooting

### "Python n'est pas reconnu"
- **Windows:** Réinstallez Python avec "Add to PATH"
- **Linux:** Utilisez `python3` au lieu de `python`

### "Module Flask not found"
```bash
pip install -r requirements.txt
```

### "Port déjà utilisé"
L'application essaie automatiquement les ports 5000-9000.

### "Nmap introuvable"
```bash
# Windows: https://nmap.org/download.html
# Linux: sudo apt-get install nmap
```

## 🔗 Ressources

- **GitHub**: https://github.com/adesperrier/cyberscandashboard
- **Nmap**: https://nmap.org
- **Flask**: https://flask.palletsprojects.com
- **Bootstrap**: https://getbootstrap.com

## 💬 Support

- Issues: GitHub Issues
- Email: contact@cyberscan-dashboard.com
- LinkedIn: /in/adesperrier

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready
