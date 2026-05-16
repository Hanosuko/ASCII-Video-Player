# 🎬 ASCII Player Video Creator — V5 Oficial

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Pillow](https://img.shields.io/badge/Pillow-Latest-orange.svg)
![Status](https://img.shields.io/badge/Version-Official%20V5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue.svg)

Una suite profesional de creación de video basada en texto (CLI) que te permite reproducir y **exportar** cualquier video a arte ASCII de alta calidad. Esta es la versión oficial V5, que incluye un flujo interactivo completo y soporte multi-idioma.

---

## ✨ Características Principales

- **📽️ Motor de Exportación MP4**: Convierte cualquier video en un MP4 de estilo ASCII. Elige entre guardar solo el video o conservar cada frame individual en PNG.
- **🌍 Soporte Multi-Idioma**: Selector de idioma interactivo al inicio (Español, Inglés, Francés, Portugués, Alemán e Indonesio).
- **🖥️ Auto-Ajuste Proporcional**: Escalado en tiempo real para adaptarse a tu ventana de terminal (tanto ancho como alto) manteniendo la relación de aspecto.
- **🎨 Fondos Personalizados**: Elige el color de fondo para tus exportaciones (Negro, Blanco, Azul o cualquier color Hex personalizado).
- **🌈 Color ANSI de 24 bits**: Coloreado de caracteres de alta fidelidad para una experiencia visual premium.
- **⚡ Rendimiento Optimizado**: Decodificación en segundo plano y procesamiento vectorizado para una reproducción fluida.
- **🖋️ Set de Alta Densidad**: Conjunto de caracteres expandido para sombras profundas y detalles intrincados.

---

## 🛠️ Instalación

Asegúrate de tener instaladas las dependencias necesarias:

```bash
python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

---

## 🧩 Despliegue Local Desde Cero

Clona tu fork y entra al proyecto:

```bash
git clone https://github.com/Hanosuko/ASCII-Video-Player.git
cd ASCII-Video-Player
```

Instala las dependencias:

```bash
/usr/bin/python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

Inicia la interfaz web local:

```bash
/usr/bin/python3 ascii_web_gui.py
```

Abre:

```text
http://127.0.0.1:8765
```

Sube un archivo o elige uno desde `Video_temp`, ajusta color/ancho/audio y pulsa `Render`. Los resultados se guardan en `Video_temp`. Detén el servidor local con `Ctrl+C`.

Aplicación de escritorio Tkinter:

```bash
/usr/bin/python3 ascii_gui.py
```

Si Tkinter falla en macOS, usa la interfaz web.

---

## 🚀 Cómo Usar

Simplemente ejecuta el script y sigue el proceso interactivo guiado:

```bash
python ASCII_v5_official.py
```

### Flujo:
1. **Logo e Idioma**: Elige tu idioma preferido.
2. **Configuración**: Establece la ruta del video, modo de color, ancho y salto de cuadros.
3. **Previsualización**: Mira la versión ASCII en tu terminal.
4. **Exportación**: Tras la previsualización, elige si quieres exportar el resultado a un archivo de video MP4.
5. **Ciclo**: ¡Procesa otro video inmediatamente después de terminar!

---

## 💡 Créditos
- **Núcleo Original**: [stepanussaruran](https://github.com/stepanussaruran)
- **Mejoras V5 y Lógica de Exportación**: Nicolas Romero ([coralgamer](https://github.com/nicolas-romero))

## ⚖️ Licencia
Distribuido bajo la **Licencia MIT**. Consulta `LICENSE` para más información.
