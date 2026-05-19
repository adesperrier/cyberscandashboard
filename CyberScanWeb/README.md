# 🌐 CyberScan Dashboard - Site Vitrine

Site web moderne pour présenter **CyberScan Dashboard**, un outil de scan réseau et d'analyse cybersécurité.

## 🚀 Installation Rapide

### Option 1: Un clic (Windows) - RECOMMANDÉ

1. Téléchargez le projet
2. Allez dans le dossier `CyberScanSoft`
3. **Double-cliquez sur `start.bat`**
4. L'application démarre automatiquement

### Option 2: Ligne de commande (Linux/Mac)

```bash
cd CyberScanSoft
python3 setup.py
```

### Option 3: Manuel (tous les systèmes)

```bash
cd CyberScanSoft
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
7. **Installation** - Guide démarrage simplifié
8. **Roadmap** - Futures fonctionnalités
9. **Footer** - Ressources & contact

## 🎨 Design

- Thème cyberpunk sombre
- Bleu néon (#00d9ff)
- Animations fluides
- Responsive mobile-first
- Performance optimisée

## 🔧 Prérequis

- **Python 3.10+**
- **Nmap** (optionnel, pour scanning réseau)

**Windows:**
- Installer Python: https://www.python.org
- Installer Nmap (optionnel): https://nmap.org/download.html

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
    ├── start.bat          # Launcher Windows
    ├── setup.py           # Setup multi-plateforme
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

## 📝 Étapes de Démarrage

### 1️⃣ Installation (30 secondes)

**Windows:**
```
1. Double-cliquez CyberScanSoft/start.bat
2. Attendez l'installation (1-2 min)
3. Navigateur s'ouvre automatiquement
```

**Linux/Mac:**
```bash
cd CyberScanSoft
python3 setup.py
```

### 2️⃣ Scanner une Cible

1. Entrez une IP, CIDR ou domaine
2. Choisissez un mode de scan (Quick/Common/Full)
3. Cliquez "Scan"
4. Consultez les résultats

### 3️⃣ Analyser les Vulnérabilités

- Ports ouverts en vert
- Services identifiés
- Vulnérabilités détectées
- Solutions recommandées

## 🐛 Troubleshooting

### "Python n'est pas reconnu"
- **Windows:** Réinstallez Python avec "Add to PATH" coché
- **Linux:** Utilisez `python3` au lieu de `python`

### "Module Flask not found"
```bash
pip install -r requirements.txt
```

### "Port déjà utilisé"
L'application cherche automatiquement le prochain port disponible.

### "Nmap introuvable"
L'app marche sans Nmap mais le scan réseau ne fonctionne pas.
```bash
# Windows: https://nmap.org/download.html
# Linux: sudo apt-get install nmap
# macOS: brew install nmap
```

## 🔗 Ressources

- **GitHub**: https://github.com/adesperrier/cyberscandashboard
- **Nmap**: https://nmap.org
- **Flask**: https://flask.palletsprojects.com
- **Python**: https://python.org

## 💬 Support

- Issues: GitHub Issues
- Email: contact@cyberscan-dashboard.com
- LinkedIn: /in/adesperrier

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready
