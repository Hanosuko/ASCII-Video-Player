# 🎬 ASCII Player Video Creator — V5 Resmi

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Pillow](https://img.shields.io/badge/Pillow-Latest-orange.svg)
![Status](https://img.shields.io/badge/Version-Official%20V5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue.svg)

Suite kreasi video berbasis teks (CLI) profesional yang memungkinkan Anda memutar dan **mengekspor** video apa pun ke dalam seni ASCII berkualitas tinggi. Versi ini adalah rilis resmi V5, menampilkan alur kerja interaktif yang lengkap dan dukungan multi-bahasa.

---

## ✨ Fitur Utama

- **📽️ Mesin Ekspor MP4**: Konversi video apa pun menjadi MP4 bergaya ASCII. Pilih antara menyimpan video saja atau menyimpan setiap frame PNG individual.
- **🌍 Dukungan Multi-Bahasa**: Pemilih bahasa interaktif saat startup (Inggris, Spanyol, Prancis, Portugis, Jerman, dan Indonesia).
- **🖥️ Penyesuaian Otomatis Proporsional**: Penskalaan real-time agar sesuai dengan jendela terminal Anda (lebar dan tinggi) sambil tetap menjaga rasio aspek.
- **🎨 Latar Belakang Kustom**: Pilih warna latar belakang untuk ekspor Anda (Hitam, Putih, Biru, atau warna Hex Kustom apa pun).
- **🌈 Mode Warna**: Render ASCII dengan warna normal, warna vivid yang lebih jenuh, atau hitam-putih.
- **⚡ Performa Dioptimalkan**: Pengodean latar belakang dan pemrosesan vektor untuk pemutaran yang lancar.
- **🖋️ Set Kepadatan Tinggi**: Set karakter yang diperluas untuk bayangan dalam dan detail yang rumit.

---

## 🛠️ Instalasi

Pastikan Anda telah menginstal dependensi yang diperlukan:

```bash
python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

---

## 🧩 Setup Lokal Dari Awal

Clone fork Anda dan masuk ke folder proyek:

```bash
git clone https://github.com/Hanosuko/ASCII-Video-Player.git
cd ASCII-Video-Player
```

Instal dependensi:

```bash
/usr/bin/python3 -m pip install opencv-python numpy Pillow imageio-ffmpeg
```

Jalankan antarmuka web lokal:

```bash
/usr/bin/python3 ascii_web_gui.py
```

Buka:

```text
http://127.0.0.1:8765
```

Unggah file atau pilih file dari `Video_temp`, atur warna/lebar/audio, lalu tekan `Render`. Hasil disimpan di `Video_temp`. Hentikan server lokal dengan `Ctrl+C`.

Untuk warna yang lebih terang dan jenuh, pilih `vivid` di GUI atau jalankan:

```bash
python3 ASCII_v5_official.py --input Video_temp/clip.mp4 --vivid-color
```

Aplikasi desktop Tkinter:

```bash
/usr/bin/python3 ascii_gui.py
```

Jika Tkinter gagal di macOS, gunakan antarmuka web.

---

## 🚀 Cara Penggunaan

Cukup jalankan skrip dan ikuti proses interaktif yang dipandu:

```bash
python ASCII_v5_official.py
```

---

## 💡 Kredit
- **Core Asli**: [stepanussaruran](https://github.com/stepanussaruran)
- **Peningkatan V5 & Logika Ekspor**: Nicolas Romero ([coralgamer](https://github.com/nicolas-romero))

## ⚖️ Lisensi
Didistribusikan di bawah **Lisensi MIT**. Lihat `LICENSE` untuk informasi lebih lanjut.
