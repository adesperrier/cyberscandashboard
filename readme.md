# 🔐 CyberScan Dashboard

Un outil web de scan réseau et d'analyse sécurité permettant de scanner des IPs, domaines ou plages réseau pour détecter les ports ouverts, les services actifs et identifier les vulnérabilités connues.

## 📋 Fonctionnalités

- **Scan Nmap** : Scanning rapide, complet ou personnalisé
- **Détection de services** : Identification automatique des services et versions
- **Alertes de sécurité** : Détection de vulnérabilités connues avec solutions
- **Découverte ARP** : Liste les appareils présents sur le réseau local
- **Historique** : Conserve les 5 derniers scans
- **Interface web** : Dashboard moderne et responsive avec Bootstrap

## 🛠️ Stack Technique

- **Backend** : Python + Flask
- **Frontend** : HTML/CSS (Bootstrap 5) + JavaScript
- **Scanner** : Nmap
- **Dépendances** : python-nmap

---

## 📦 Installation

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/adesperrier/cyberscandashboard.git
cd CyberScan
```

### Étape 2 : Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### Étape 3 : Installer Nmap

#### Sur Windows

1. Télécharge Nmap depuis : https://nmap.org/download.html
2. Exécute le fichier d'installation `.exe`
3. Sélectionne le chemin d'installation (par défaut : `C:\Program Files\Nmap\` ou `C:\Program Files (x86)\Nmap\`)
4. Termine l'installation

#### Sur Linux

**Ubuntu/Debian :**
```bash
sudo apt-get update
sudo apt-get install nmap
```

**Fedora/RHEL :**
```bash
sudo dnf install nmap
```

**Arch :**
```bash
sudo pacman -S nmap
```

### Étape 4 : Configurer la variable d'environnement NMAP_PATH (Windows)

Après l'installation de Nmap, configure la variable d'environnement :

```powershell
.\setx NMAP_PATH "C:\Program Files (x86)\Nmap\nmap.exe"
```

**Note** : Redémarre PowerShell ou réouvre ton terminal après cette commande.

### Sur Linux

La variable d'environnement n'est généralement pas nécessaire si Nmap est installé via le gestionnaire de paquets (elle sera détectée automatiquement).

Si besoin, ajoute à ton `.bashrc` ou `.zshrc` :

```bash
export NMAP_PATH=/usr/bin/nmap
```

---

## 🚀 Lancer l'application

### Démarrer le serveur Flask

```bash
python app.py
```

Tu verras un message comme :

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Accéder à l'interface

Ouvre ton navigateur et accède à :

```
http://127.0.0.1:5000
```

ou

```
localhost:5000
```

---

## 💻 Utilisation

### 1. **Charger les voisins ARP**

Clique sur le bouton **↻ Actualiser ARP** pour découvrir les appareils du réseau local.

### 2. **Entrer une cible**

Rentre une cible parmi :
- **IP unique** : `192.168.1.10`
- **Plage réseau (CIDR)** : `10.0.0.0/24`
- **Domaine** : `example.com`

### 3. **Sélectionner un mode de scan**

- **Quick (rapide)** : Top 100 ports courants
- **Common (courants)** : 20+ ports critiques
- **Full (complet - très très lent)** : Tous les ports (1-65535)
- **Personnalisé** : Entre des ports spécifiques (ex: `80,443,8080`)

### 4. **Lancer le scan**

Clique sur **▶ Scanner maintenant** et attends les résultats.

### 5. **Analyser les résultats**

- **Résumé** : Nombre d'hôtes et ports ouverts
- **Tableau des ports** : État, service, version détectée
- **Alertes de sécurité** : Avertissements pour les services vulnérables avec solutions recommandées
- **Historique** : Consulte les 5 derniers scans

---

## 📝 Vulnérabilités détectées

L'outil détecte automatiquement les services courants vulnérables :

- **FTP** (Port 21) → Authentification faible, données en clair
- **Telnet** (Port 23) → Connexion non chiffrée
- **HTTP** (Port 80) → Sans chiffrement SSL/TLS
- **SSH** (Port 22) → Versions anciennes
- **SMB** (Port 445) → Partages réseau non sécurisés
- **MySQL/PostgreSQL** (Ports 3306/5432) → Base de données exposée
- **MongoDB** (Port 27017) → NoSQL sans authentification
- **Redis** (Port 6379) → Cache sans authentification

---

## 🔧 Configuration

### requirements.txt

```
Flask==3.0.0
python-nmap==0.0.1
```

### Structure du projet

```
CyberScan/
├── app.py                    # Application Flask principale
├── templates/
│   └── index.html            # Interface web (HTML/CSS/JS intégré)
├── static/
│   └── styles.css            # Feuille de styles CSS
├── requirements.txt          # Dépendances Python
└── README.md                 # Ce fichier
```

---

## 🐛 Troubleshooting

### **Erreur : "Nmap introuvable"**

1. Vérifie que Nmap est bien installé
2. Vérifie que la variable `NMAP_PATH` est correctement définie (Windows)
3. Redémarre PowerShell après avoir défini `NMAP_PATH`

### **Erreur : "Permission denied" (Linux)**

Certains scans Nmap nécessitent les droits `sudo` :

```bash
sudo python app.py
```

### **Port 5000 déjà utilisé**

Modifie le port dans `app.py` ligne finale :

```python
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  # Utilise 8080 au lieu de 5000
```

### **Aucun voisin ARP détecté**

- Sur Linux, tu peux avoir besoin de `sudo`
- Sur Windows, assure-toi que le réseau est connecté et visible

---

