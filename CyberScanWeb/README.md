# 🌐 CyberScan Dashboard - Site Vitrine

Site web moderne et professionnel pour présenter **CyberScan Dashboard**, un outil de scan réseau et d'analyse cybersécurité.

## 🎨 Design & Features

✨ **Design Cyberpunk Moderne**
- Thème sombre avec bleu néon primaire (#00d9ff) et vert néon secondaire (#00ff88)
- Animations subtiles et fluides
- Interface réactive et responsive
- Effets glow neon et ombres cybersécurité

📱 **Responsive & Accessible**
- Mobile-first approach
- Compatible tous les navigateurs modernes
- Accessibilité WCAG compliant

🚀 **Performance**
- CSS optimisé (~889 lignes)
- JavaScript vanilla minimal (~155 lignes)
- Pas de dépendances externes (sauf Bootstrap CDN)
- PageSpeed optimisé

## 📦 Structure du Projet

```
CyberScanWeb/
├── app.py                          # Flask minimaliste
├── requirements.txt                # Dépendances
├── templates/
│   └── index.html                  # Page landing complète
├── static/
│   ├── css/
│   │   └── style.css               # Design cyberpunk
│   ├── js/
│   │   └── script.js               # Interactions légères
│   └── img/                        # Assets (placeholder)
├── .gitignore
└── README.md                       # Ce fichier
```

## 🎯 Sections Incluses

1. **Navbar Fixe** - Navigation avec liens smooth scroll
2. **Hero Section** - Titre attrayant avec CTA
3. **Fonctionnalités** - 6 cards de features
4. **Architecture** - Diagramme flux utilisateur
5. **Technologies** - Stack technique complet
6. **Screenshots** - Galerie du logiciel
7. **Installation** - Guide étape par étape
8. **Roadmap** - Timeline des features futures
9. **Footer** - Links et mentions légales

## 🚀 Démarrage Rapide

### Installation

```bash
# Installer Flask
pip install -r requirements.txt
```

### Lancer le serveur

```bash
python app.py
```

### Accéder au site

Ouvrez votre navigateur :
```
http://127.0.0.1:5000
```

## 🎨 Customization

### Couleurs (CSS Variables)

Modifier `static/css/style.css` :

```css
:root {
    --primary-neon: #00d9ff;       /* Cyan néon */
    --secondary-neon: #00ff88;     /* Vert néon */
    --bg-dark: #0a0e27;            /* Fond principal */
    --text-light: #e0e0e0;         /* Texte clair */
}
```

### Contenu

Modifier `templates/index.html` pour :
- Changer les textes
- Ajouter/retirer des sections
- Personnaliser les links

## 📱 Responsive Breakpoints

- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px

## ⚡ Performance

- **CSS**: 889 lignes optimisées
- **JS**: 155 lignes vanilla (pas de framework)
- **Load Time**: < 1s (local)
- **PageSpeed**: Optimisé pour 90+ score

## 🔧 Dépendances

- **Flask 3.0.0** - Framework web
- **Bootstrap 5.3.0** - CSS framework (CDN)
- **Bootstrap Icons 1.11.0** - Icônes (CDN)

## 📝 License

Voir le projet principal CyberScan Dashboard.

## 🔗 Liens Utiles

- [GitHub CyberScan](https://github.com/adesperrier/cyberscandashboard)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Bootstrap 5 Docs](https://getbootstrap.com)
- [Nmap Official](https://nmap.org)

---

**Développé par Antoine Desperrier** 🔐

Prêt pour déploiement DigitalOcean/Namecheap.
