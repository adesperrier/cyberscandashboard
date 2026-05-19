# 🚀 DÉMARRAGE RAPIDE

## Installation & Configuration

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

Cela installe Flask 3.0.0.

### 2️⃣ Lancer le serveur

```bash
python app.py
```

Le serveur démarre sur : **http://127.0.0.1:5000**

### 3️⃣ Ouvrir dans le navigateur

- **Local**: http://127.0.0.1:5000
- **Remote**: http://[votre-ip]:5000

---

## 📂 Structure Fichiers

```
CyberScanWeb/
├── app.py                 # Application Flask (10 lignes)
├── requirements.txt       # Dépendances
├── README.md             # Documentation
├── QUICKSTART.md         # Ce fichier
├── templates/
│   └── index.html        # Page landing (504 lignes)
└── static/
    ├── css/
    │   └── style.css     # Design cyberpunk (889 lignes)
    ├── js/
    │   └── script.js     # Interactions (155 lignes)
    └── img/              # Assets (placeholder)
```

---

## 🎨 Customization Rapide

### Changer le titre
- Fichier: `templates/index.html`
- Ligne: 6 (`<title>CyberScan Dashboard...</title>`)

### Changer les couleurs
- Fichier: `static/css/style.css`
- Variables CSS: lignes 1-10
  - `--primary-neon: #00d9ff` (cyan)
  - `--secondary-neon: #00ff88` (vert)
  - `--bg-dark: #0a0e27` (fond)

### Ajouter du contenu
- Fichier: `templates/index.html`
- Copier une section existante et adapter

---

## 🌍 Déploiement DigitalOcean

### Via Gunicorn + Nginx

```bash
# Installer gunicorn
pip install gunicorn

# Lancer avec gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Docker (optionnel)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| **HTML** | 504 lignes |
| **CSS** | 889 lignes |
| **JS** | 155 lignes |
| **Total** | 1.5K lignes |
| **Sections** | 9 |
| **Responsive** | Oui (mobile-first) |
| **Dépendances** | 1 (Flask) |

---

## 🔗 URLs Importantes

- GitHub: https://github.com/adesperrier/cyberscandashboard
- Flask: https://flask.palletsprojects.com
- Bootstrap: https://getbootstrap.com

---

**✅ Prêt pour production sur DigitalOcean + Namecheap**

Pour commencer: `python app.py` → http://127.0.0.1:5000
