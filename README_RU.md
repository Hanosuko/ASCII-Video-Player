# 🎬 ASCII Player Video Creator — V5 Official

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![NumPy](https://img.shields.io/badge/NumPy-1.20+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue.svg)
![Pillow](https://img.shields.io/badge/Pillow-Latest-orange.svg)
![Status](https://img.shields.io/badge/Version-Official%20V5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)


Официальный выпуск V5: конвертация видео и изображений в ASCII через JSON-конфиг, поддержка разных входных форматов и сохранение звука в видео.

Профессиональный CLI-конвертер, который превращает видео и фотографии в ASCII-стилизованные файлы. Настройки задаются в `ascii_config.json`, а аудиодорожка видео переносится из исходного файла через `ffmpeg`.

---

## ✨ Основные возможности

- **📽️ Экспорт ASCII-видео**: Преобразуйте видео в цветной или черно-белый ASCII-ролик.
- **🖼️ Экспорт ASCII-изображений**: Обрабатывайте `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tif`, `.tiff`.
- **🎞️ Разные входные форматы**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v` и другие форматы, которые читает OpenCV.
- **🔊 Сохранение звука**: Аудиодорожка автоматически переносится из исходного файла в итоговый ролик.
- **⚙️ JSON-конфиг**: Меняйте путь к видео, ширину ASCII, цвет, фон, шрифт, пропуск кадров и временные файлы без редактирования Python.
- **🎨 Цветной режим**: Символы могут окрашиваться в цвета исходного кадра.
- **🖋️ Расширенный набор символов**: Плотная палитра ASCII-символов для более детального затенения.

---

## 🛠️ Установка

Убедитесь, что у вас установлены необходимые зависимости:

```bash
python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

---

## 🧩 Локальное развертывание с нуля

Склонируйте fork и перейдите в папку проекта:

```bash
git clone https://github.com/Hanosuko/ASCII-Video-Player.git
cd ASCII-Video-Player
```

Установите зависимости:

```bash
/usr/bin/python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

Запустите браузерное локальное приложение:

```bash
/usr/bin/python3 ascii_web_gui.py
```

Откройте в браузере:

```text
http://127.0.0.1:8765
```

В web-интерфейсе загрузите фото/видео или выберите файл из `Video_temp`, настройте цвет, ширину, звук и нажмите `Render`. Результаты сохраняются в `Video_temp`. Чтобы остановить сервер, нажмите `Ctrl+C` в Terminal.

Если хочется попробовать desktop-окно:

```bash
/usr/bin/python3 ascii_gui.py
```

Если Tkinter падает на macOS с `Abort trap: 6`, используйте браузерное приложение выше.

---

## 🚀 Как использовать

V5 теперь работает через удобный JSON-конфиг. Откройте `ascii_config.json` и укажите нужные параметры:

```json
{
  "input_path": "Video_temp/data.mp4",
  "output_path": "auto",
  "media_type": "auto",
  "match_input_format": true,
  "width": 120,
  "color": true,
  "background": "#000000",
  "foreground": "#FFFFFF",
  "font_size": 10,
  "skip_frames": 1,
  "preserve_audio": true,
  "final_video_codec": "libx264"
}
```

Запуск конвертации:

```bash
python3 ASCII_v5_official.py --config ascii_config.json
```

Запуск окна-приложения:

```bash
/usr/bin/python3 ascii_gui.py
```

На macOS можно просто открыть файл `run_gui.command` двойным кликом.

В окне можно выбрать фото или видео, настроить цветной/чёрно-белый режим, ширину ASCII, размер шрифта, сохранение звука и формат экспорта.

Если Tkinter-окно падает с ошибкой вроде `Abort trap: 6`, запускайте браузерное приложение:

```bash
/usr/bin/python3 ascii_web_gui.py
```

Или двойным кликом откройте `run_web_gui.command`, затем перейдите в браузере на:

```text
http://127.0.0.1:8765
```

Создать новый конфиг с настройками по умолчанию:

```bash
python3 ASCII_v5_official.py --init-config my_config.json
```

Можно переопределять параметры прямо из терминала:

```bash
python3 ASCII_v5_official.py --config ascii_config.json --input Video_temp/data.mov --width 140 --color
```

Обработка фотографии:

```bash
python3 ASCII_v5_official.py --input Photo/input.jpg --width 160 --color
```

Если `media_type` стоит `auto`, скрипт сам поймет, что `.jpg`/`.png` — это картинка. Можно указать явно:

```bash
python3 ASCII_v5_official.py --input Photo/input.webp --output Photo/input_ascii.jpg --media-type image --width 140
```

### Формат экспорта

По умолчанию результат сохраняется в том же формате, что и входной файл:

- `Video_temp/clip.MOV` -> `Video_temp/clip_ASCII.MOV`
- `Video_temp/movie.mp4` -> `Video_temp/movie_ASCII.mp4`
- `Photo/image.jpg` -> `Photo/image_ASCII.jpg`
- `Photo/picture.png` -> `Photo/picture_ASCII.png`

За это отвечают настройки:

```json
"output_path": "auto",
"match_input_format": true
```

Если указать `--output Video_temp/result.mp4` для файла `.MOV`, скрипт все равно заменит расширение и сохранит `Video_temp/result.MOV`. Чтобы использовать расширение из `--output` как есть, добавьте флаг:

```bash
python3 ASCII_v5_official.py --input Video_temp/clip.MOV --output Video_temp/result.mp4 --keep-output-format
```

### Форматы видео

Входной файл не ограничен `.mp4`. Скрипт принимает любой формат, который может прочитать OpenCV на вашей системе: обычно `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v`, `.mpeg`, `.mpg`.

При `match_input_format: true` выходной видеофайл получает то же расширение, что и входной:

```json
"input_path": "Video_temp/result.mov",
"output_path": "auto",
"match_input_format": true
```

### Форматы изображений

Для фотографий и картинок поддерживаются форматы, которые открывает Pillow: обычно `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tif`, `.tiff`.

Для картинки лучше указывать выходной файл с расширением изображения:

```json
"input_path": "Photo/input.jpg",
"output_path": "auto",
"media_type": "auto"
```

Если вход — изображение, итоговый файл получит такое же расширение: `.jpg` останется `.jpg`, `.png` останется `.png`.

### Звук

Чтобы сохранить звук из исходного видео, оставьте:

```json
"preserve_audio": true
```

Видео сначала создается как ASCII-ролик без звука, затем `ffmpeg` подклеивает аудиодорожку из исходника. Для этого установлен пакет `imageio-ffmpeg`, который дает скрипту встроенный `ffmpeg`. Если в исходном видео нет звука, итоговый файл просто будет без аудио.

Финальный видеофайл перекодируется в `H.264/AVC + AAC` с `yuv420p` и `faststart`, чтобы его нормально принимали Telegram, браузеры и мобильные плееры. Если оставить старый `mp4v`, Telegram может показать только первый кадр, пока звук продолжает идти.

### Основные настройки

- `input_path`: путь к исходному видео.
- `output_path`: куда сохранить ASCII-видео или ASCII-изображение.
- `media_type`: `auto`, `video` или `image`. В обычном случае оставьте `auto`.
- `match_input_format`: `true`, чтобы выходной файл сохранял расширение исходника.
- `width`: ширина ASCII-картинки в символах. Больше значение = детальнее, но медленнее.
- `color`: `true` для цветного ASCII, `false` для черно-белого.
- `background`: цвет фона в формате `#RRGGBB`.
- `foreground`: цвет символов в черно-белом режиме.
- `font_size`: размер шрифта в итоговом видео.
- `skip_frames`: `1` конвертирует каждый кадр, `2` каждый второй кадр и так далее.
- `keep_temp_frames`: `true`, если нужно сохранить PNG-кадры в `temp_dir`.
- `preserve_audio`: сохранять аудиодорожку из исходного видео.
- `final_video_codec`: финальный кодек видео. По умолчанию `libx264`, это самый совместимый вариант для Telegram.
- `final_video_crf`: качество H.264. Меньше значение = выше качество и больше файл.
- `final_video_preset`: скорость/эффективность кодирования H.264.

---

## 💡 Авторы
- **Исходное ядро**: [stepanussaruran](https://github.com/stepanussaruran)
- **Улучшения V5 и логика экспорта**: Nicolas Romero ([coralgamer](https://github.com/nicolas-romero))

## ⚖️ Лицензия
Распространяется под лицензией **MIT**. Дополнительную информацию см. в файле `LICENSE`.

---
*Версии на языках: [Español](README_ES.md) | [Français](README_FR.md) | [Português](README_PT.md) | [Deutsch](README_DE.md) | [Indonesian](README_ID.md) | [Русский](README_RU.md)*
