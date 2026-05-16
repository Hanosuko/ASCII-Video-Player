# 🎬 ASCII Player Video Creator — V5 Officiel

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Pillow](https://img.shields.io/badge/Pillow-Latest-orange.svg)
![Status](https://img.shields.io/badge/Version-Official%20V5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue.svg)

Une suite professionnelle de création vidéo basée sur le texte (CLI) qui vous permet de lire et d'**exporter** n'importe quelle vidéo en art ASCII de haute qualité. Cette version est la version officielle V5, dotée d'un flux de travail interactif complet et d'un support multilingue.

---

## ✨ Caractéristiques Clés

- **📽️ Moteur d'Exportation MP4** : Convertissez n'importe quelle vidéo en un MP4 de style ASCII. Choisissez entre enregistrer uniquement la vidéo ou conserver chaque image PNG individuelle.
- **🌍 Support Multilingue** : Sélecteur de langue interactif au démarrage (Anglais, Espagnol, Français, Portugais, Allemand et Indonésien).
- **🖥️ Ajustement Automatique Proportionnel** : Mise à l'échelle en temps réel pour s'adapter à votre fenêtre de terminal (largeur et hauteur) tout en conservant le rapport d'aspect.
- **🎨 Arrière-plans Personnalisés** : Choisissez la couleur d'arrière-plan pour vos exportations (Noir, Blanc, Bleu ou n'importe quelle couleur Hex personnalisée).
- **🌈 Modes de Couleur** : Rendu ASCII en couleur normale, couleur vivid plus saturée ou noir et blanc.
- **⚡ Performance Optimisée** : Décodage en arrière-plan et traitement vectorisé pour une lecture fluide.
- **🖋️ Jeu de Haute Densité** : Jeu de caractères étendu pour des ombrages profonds et des détails complexes.

---

## 🛠️ Installation

Assurez-vous d'avoir installé les dépendances requises :

```bash
python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

---

## 🧩 Installation Locale Depuis Zéro

Clonez votre fork et entrez dans le projet :

```bash
git clone https://github.com/Hanosuko/ASCII-Video-Player.git
cd ASCII-Video-Player
```

Installez les dépendances :

```bash
/usr/bin/python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

Démarrez l'interface web locale :

```bash
/usr/bin/python3 ascii_web_gui.py
```

Ouvrez :

```text
http://127.0.0.1:8765
```

Téléversez un fichier ou choisissez-en un dans `Video_temp`, réglez la couleur/la largeur/l'audio, puis cliquez sur `Render`. Les résultats sont enregistrés dans `Video_temp`. Arrêtez le serveur local avec `Ctrl+C`.

Pour des couleurs plus vives et saturées, choisissez `vivid` dans l'interface ou lancez :

```bash
python3 ASCII_v5_official.py --input Video_temp/clip.mp4 --vivid-color
```

Application de bureau Tkinter :

```bash
/usr/bin/python3 ascii_gui.py
```

Si Tkinter échoue sur macOS, utilisez l'interface web.

---

## 🚀 Comment Utiliser

Exécutez simplement le script et suivez le processus interactif guidé :

```bash
python ASCII_v5_official.py
```

---

## 💡 Crédits
- **Noyau Original** : [stepanussaruran](https://github.com/stepanussaruran)
- **Améliorations V5 et Logique d'Exportation** : Nicolas Romero ([coralgamer](https://github.com/nicolas-romero))

## ⚖️ Licence
Distribué sous la **Licence MIT**. Voir `LICENSE` pour plus d'informations.
