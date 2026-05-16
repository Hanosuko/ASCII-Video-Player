# 🎬 ASCII Player Video Creator — V5 Official

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Pillow](https://img.shields.io/badge/Pillow-Latest-orange.svg)
![Status](https://img.shields.io/badge/Version-Official%20V5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue.svg)

A professional text-based (CLI) video creation suite that allows you to play and **export** any video into high-quality ASCII art. This version is the official V5 release, featuring a complete interactive workflow and multi-language support.

---

## ✨ Key Features

- **📽️ MP4 Export Engine**: Convert any video into an ASCII-styled MP4. Choose between saving only the video or keeping every individual PNG frame.
- **🌍 Multi-Language Support**: Interactive language selector on startup (English, Spanish, French, Portuguese, German, and Indonesian).
- **🖥️ Proportional Auto-Fit**: Real-time scaling to fit your terminal window (both width and height) while maintaining aspect ratio.
- **🎨 Custom Backgrounds**: Choose the background color for your exports (Black, White, Blue, or any Custom Hex color).
- **🌈 24-bit ANSI Color**: High-fidelity character coloring for a premium visual experience.
- **⚡ Performance Optimized**: Background decoding and vectorized processing for smooth playback.
- **🖋️ High-Density Set**: Expanded character set for deep shading and intricate details.

---

## 🛠️ Installation

Ensure you have the required dependencies:

```bash
python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

---

## 🧩 Local Setup From Scratch

Clone your fork and enter the project:

```bash
git clone https://github.com/Hanosuko/ASCII-Video-Player.git
cd ASCII-Video-Player
```

Install dependencies:

```bash
/usr/bin/python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

Start the browser GUI:

```bash
/usr/bin/python3 ascii_web_gui.py
```

Open:

```text
http://127.0.0.1:8765
```

Upload or choose a file from `Video_temp`, adjust color/width/audio settings, then press `Render`. Results are saved in `Video_temp`. Stop the local server with `Ctrl+C`.

Tkinter desktop app:

```bash
/usr/bin/python3 ascii_gui.py
```

If Tkinter crashes on macOS, use the browser GUI.

---

## 🚀 How to Use

Simply run the script and follow the guided interactive process:

```bash
python ASCII_v5_official.py
```

### Flow:
1. **Logo & Language**: Choose your preferred language.
2. **Configuration**: Set video path, color mode, width, and frame skipping.
3. **Preview**: Watch the ASCII version in your terminal.
4. **Export**: After previewing, choose if you want to export the result to an MP4 video file.
5. **Cycle**: Process another video immediately after finishing!

---

## 💡 Credits
- **Original Core**: [stepanussaruran](https://github.com/stepanussaruran)
- **V5 Enhancements & Export Logic**: Nicolas Romero ([coralgamer](https://github.com/nicolas-romero))

## ⚖️ License
Distributed under the **MIT License**. See `LICENSE` for more information.

---
*Language Versions: [Español](README_ES.md) | [Français](README_FR.md) | [Português](README_PT.md) | [Deutsch](README_DE.md) | [Indonesian](README_ID.md)*
