# 🔐 CyberScan Dashboard

Application web de scan réseau et d'analyse cybersécurité développée en Python Flask.

## 🚀 Démarrage Rapide (3 étapes)

### Windows
```bash
1. Double-cliquez sur run.bat
2. Attendez l'installation des dépendances
3. Le navigateur s'ouvre automatiquement
```

### Linux/Mac
```bash
1. chmod +x run.sh
2. ./run.sh
3. Le navigateur s'ouvre automatiquement
```

### Manuel (tous les systèmes)
```bash
# 1. Installer Python 3.10+
# Depuis: https://www.python.org/

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Installer Nmap (optionnel pour le scan réseau)
# Windows: https://nmap.org/download.html
# Linux: sudo apt-get install nmap

# 4. Lancer l'application
python launcher.py
```

L'application démarre sur **http://127.0.0.1:5000**

## 📂 Structure

```
CyberScanSoft/
├── run.bat                  # 🪟 Launcher Windows
├── run.sh                   # 🐧 Launcher Linux/Mac
├── launcher.py              # Script Python de lancement
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
- python-nmap 0.0.1

**Optionnel (pour scanning réseau):**
- Nmap (https://nmap.org)

**Système:**
- Windows 10+ / Linux / Mac
- 200 MB RAM minimum
- Connexion réseau

## 🔧 Utilisation

### Formulaire Scan

1. **Cible** : IP (`192.168.1.10`), CIDR (`10.0.0.0/24`) ou domaine
2. **Mode** : 
   - Quick : Top 100 ports
   - Common : Services courants
   - Full : Tous les ports (lent)
3. **Ports Custom** : Optionnel (ex: `80,443,8080`)

### Exemple Scan

```
Cible: 192.168.1.1
Mode: Quick
Résultat: 5 ports détectés, 2 alertes de sécurité
```

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
```bash
# Windows: Réinstallez Python avec "Add to PATH" coché
# Linux: python3 au lieu de python
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port déjà utilisé"
```bash
# Laissez launcher.py trouver un autre port (5000-9000)
# Ou fermez l'app qui utilise le port
```

### "Nmap introuvable"
```bash
# Installez Nmap depuis https://nmap.org/download.html
# Le scan réseau ne fonctionnera pas sans
```

## 📋 Requirements.txt

```
Flask==3.0.0
python-nmap==0.0.1
Werkzeug==3.0.0
```

## 🔗 Ressources

- GitHub: https://github.com/adesperrier/cyberscandashboard
- Nmap: https://nmap.org
- Flask: https://flask.palletsprojects.com
- Bootstrap: https://getbootstrap.com

## 📄 Licence

Voir LICENSE pour les détails.

## 👤 Développeur

**Antoine Desperrier**
- GitHub: @adesperrier
- LinkedIn: /in/adesperrier

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready
