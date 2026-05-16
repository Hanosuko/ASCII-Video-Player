# 🎬 ASCII Player Video Creator — V5 Offizielle Version

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Pillow](https://img.shields.io/badge/Pillow-Latest-orange.svg)
![Status](https://img.shields.io/badge/Version-Official%20V5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue.svg)

Eine professionelle textbasierte (CLI) Videokreations-Suite, mit der Sie jedes Video in hochwertige ASCII-Art abspielen und **exportieren** können. Dies ist die offizielle V5-Version mit einem kompletten interaktiven Workflow und Unterstützung für mehrere Sprachen.

---

## ✨ Hauptmerkmale

- **📽️ MP4 Export-Engine**: Konvertieren Sie jedes Video in ein MP4 im ASCII-Stil. Wählen Sie, ob Sie nur das Video speichern oder jeden einzelnen PNG-Frame behalten möchten.
- **🌍 Mehrsprachige Unterstützung**: Interaktive Sprachauswahl beim Start (Englisch, Spanisch, Französisch, Portugiesisch, Deutsch und Indonesisch).
- **🖥️ Proportionale automatische Anpassung**: Echtzeit-Skalierung an Ihr Terminalfenster (Breite und Höhe) unter Beibehaltung des Seitenverhältnisses.
- **🎨 Benutzerdefinierte Hintergründe**: Wählen Sie die Hintergrundfarbe für Ihre Exporte (Schwarz, Weiß, Blau oder eine beliebige benutzerdefinierte Hex-Farbe).
- **🌈 Farbmodi**: Rendern Sie normales Farbbild, kräftiges vivid-Farbbild oder Schwarz-Weiß-ASCII.
- **⚡ Leistungsoptimiert**: Hintergrund-Dekodierung und vektorisierte Verarbeitung für eine flüssige Wiedergabe.
- **🖋️ Hochdichtes Set**: Erweiterter Zeichensatz für tiefe Schattierungen und komplexe Details.

---

## 🛠️ Installation

Stellen Sie sicher, dass die erforderlichen Abhängigkeiten installiert sind:

```bash
python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

---

## 🧩 Lokale Einrichtung Von Grund Auf

Klonen Sie Ihren Fork und wechseln Sie in das Projekt:

```bash
git clone https://github.com/Hanosuko/ASCII-Video-Player.git
cd ASCII-Video-Player
```

Installieren Sie die Abhängigkeiten:

```bash
/usr/bin/python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

Starten Sie die lokale Weboberfläche:

```bash
/usr/bin/python3 ascii_web_gui.py
```

Öffnen Sie:

```text
http://127.0.0.1:8765
```

Laden Sie eine Datei hoch oder wählen Sie eine Datei aus `Video_temp`, passen Sie Farbe/Breite/Audio an und klicken Sie auf `Render`. Ergebnisse werden in `Video_temp` gespeichert. Stoppen Sie den lokalen Server mit `Ctrl+C`.

Für hellere und sattere Farben wählen Sie `vivid` in der GUI oder führen Sie aus:

```bash
python3 ASCII_v5_official.py --input Video_temp/clip.mp4 --vivid-color
```

Tkinter-Desktop-App:

```bash
/usr/bin/python3 ascii_gui.py
```

Wenn Tkinter unter macOS abstürzt, verwenden Sie die Weboberfläche.

---

## 🚀 Bedienung

Führen Sie einfach das Skript aus und folgen Sie dem geführten interaktiven Prozess:

```bash
python ASCII_v5_official.py
```

---

## 💡 Credits
- **Original-Kern**: [stepanussaruran](https://github.com/stepanussaruran)
- **V5-Verbesserungen & Export-Logik**: Nicolas Romero ([coralgamer](https://github.com/nicolas-romero))

## ⚖️ Lizenz
Verteilt unter der **MIT-Lizenz**. Weitere Informationen finden Sie in `LICENSE`.
