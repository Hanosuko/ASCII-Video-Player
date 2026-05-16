# 🎬 ASCII Player Video Creator — V5 Oficial

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Pillow](https://img.shields.io/badge/Pillow-Latest-orange.svg)
![Status](https://img.shields.io/badge/Version-Official%20V5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue.svg)

Uma suíte profissional de criação de vídeo baseada em texto (CLI) que permite reproduzir e **exportar** qualquer vídeo em arte ASCII de alta qualidade. Esta versão é o lançamento oficial V5, apresentando um fluxo de trabalho interativo completo e suporte a vários idiomas.

---

## ✨ Principais Características

- **📽️ Motor de Exportação MP4**: Converta qualquer vídeo em um MP4 de estilo ASCII. Escolha entre salvar apenas o vídeo ou manter cada frame PNG individual.
- **🌍 Suporte Multi-idioma**: Seletor de idioma interativo ao iniciar (Inglês, Espanhol, Francês, Português, Alemão e Indonésio).
- **🖥️ Ajuste Automático Proporcional**: Dimensionamento em tempo real para caber na janela do seu terminal (largura e altura) mantendo a proporção.
- **🎨 Fundos Personalizados**: Escolha a cor de fundo para suas exportações (Preto, Branco, Azul ou qualquer cor Hex personalizada).
- **🌈 Cor ANSI de 24 bits**: Colorização de caracteres de alta fidelidade para uma experiência visual premium.
- **⚡ Desempenho Otimizado**: Decodificação em segundo plano e processamento vetorizado para reprodução suave.
- **🖋️ Conjunto de Alta Densidade**: Conjunto de caracteres expandido para sombreamento profundo e detalhes intrincados.

---

## 🛠️ Instalação

Certifique-se de ter as dependências necessárias instaladas:

```bash
python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

---

## 🧩 Configuração Local Do Zero

Clone seu fork e entre no projeto:

```bash
git clone https://github.com/Hanosuko/ASCII-Video-Player.git
cd ASCII-Video-Player
```

Instale as dependências:

```bash
/usr/bin/python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

Inicie a interface web local:

```bash
/usr/bin/python3 ascii_web_gui.py
```

Abra:

```text
http://127.0.0.1:8765
```

Envie um arquivo ou escolha um arquivo em `Video_temp`, ajuste cor/largura/áudio e clique em `Render`. Os resultados são salvos em `Video_temp`. Pare o servidor local com `Ctrl+C`.

Aplicativo desktop Tkinter:

```bash
/usr/bin/python3 ascii_gui.py
```

Se o Tkinter falhar no macOS, use a interface web.

---

## 🚀 Como Usar

Basta executar o script e seguir o processo interativo guiado:

```bash
python ASCII_v5_official.py
```

---

## 💡 Créditos
- **Núcleo Original**: [stepanussaruran](https://github.com/stepanussaruran)
- **Melhorias V5 e Lógica de Exportação**: Nicolas Romero ([coralgamer](https://github.com/nicolas-romero))

## ⚖️ Licencia
Distribuído sob a **Licença MIT**. Veja `LICENSE` para mais informações.
