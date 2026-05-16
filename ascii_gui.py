"""
Desktop GUI for ASCII Media Converter V5.

Run:
    python3 ascii_gui.py
"""

from __future__ import annotations

import contextlib
import queue
import re
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from ASCII_v5_official import (
    ConverterConfig,
    detect_media_type,
    export_ascii_image,
    export_ascii_video,
)


VIDEO_TYPES = (
    ("Video files", "*.mp4 *.mov *.avi *.mkv *.webm *.m4v *.mpeg *.mpg"),
    ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff"),
    ("All files", "*.*"),
)

IMAGE_OUTPUT_TYPES = (
    ("PNG", "*.png"),
    ("JPEG", "*.jpg *.jpeg"),
    ("WEBP", "*.webp"),
    ("BMP", "*.bmp"),
    ("TIFF", "*.tif *.tiff"),
    ("All files", "*.*"),
)

VIDEO_OUTPUT_TYPES = (
    ("MP4", "*.mp4"),
    ("MOV", "*.mov"),
    ("AVI", "*.avi"),
    ("MKV", "*.mkv"),
    ("WEBM", "*.webm"),
    ("All files", "*.*"),
)


class QueueWriter:
    def __init__(self, output_queue: queue.Queue[str]) -> None:
        self.output_queue = output_queue
        self.buffer = ""

    def write(self, text: str) -> int:
        if not text:
            return 0

        self.buffer += text
        while "\n" in self.buffer or "\r" in self.buffer:
            newline_pos = self.buffer.find("\n") if "\n" in self.buffer else 10**9
            carriage_pos = self.buffer.find("\r") if "\r" in self.buffer else 10**9
            split_at = min(newline_pos, carriage_pos)
            line = self.buffer[:split_at]
            self.buffer = self.buffer[split_at + 1 :]
            if line.strip():
                self.output_queue.put(line)
        return len(text)

    def flush(self) -> None:
        if self.buffer.strip():
            self.output_queue.put(self.buffer)
            self.buffer = ""


class ASCIIConverterApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ASCII Media Converter")
        self.geometry("980x720")
        self.minsize(860, 640)

        self.events: queue.Queue[tuple[str, str]] = queue.Queue()
        self.worker: threading.Thread | None = None

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value="auto")
        self.media_type = tk.StringVar(value="auto")
        self.color_mode = tk.StringVar(value="color")
        self.vivid_saturation = tk.DoubleVar(value=1.75)
        self.vivid_brightness = tk.DoubleVar(value=1.15)
        self.width_value = tk.IntVar(value=120)
        self.font_size = tk.IntVar(value=10)
        self.skip_frames = tk.IntVar(value=1)
        self.match_input_format = tk.BooleanVar(value=True)
        self.preserve_audio = tk.BooleanVar(value=True)
        self.keep_frames = tk.BooleanVar(value=False)
        self.background = tk.StringVar(value="#000000")
        self.foreground = tk.StringVar(value="#FFFFFF")
        self.status = tk.StringVar(value="Ready")

        self._build_ui()
        self.after(100, self._poll_events)

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        title = ttk.Label(self, text="ASCII Media Converter", font=("TkDefaultFont", 22, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=18, pady=(18, 8))

        file_frame = ttk.LabelFrame(self, text="Files")
        file_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=8)
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text="Input").grid(row=0, column=0, sticky="w", padx=12, pady=8)
        ttk.Entry(file_frame, textvariable=self.input_path).grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        ttk.Button(file_frame, text="Browse", command=self._browse_input).grid(row=0, column=2, padx=8, pady=8)

        ttk.Label(file_frame, text="Output").grid(row=1, column=0, sticky="w", padx=12, pady=8)
        ttk.Entry(file_frame, textvariable=self.output_path).grid(row=1, column=1, sticky="ew", padx=8, pady=8)
        ttk.Button(file_frame, text="Save as", command=self._browse_output).grid(row=1, column=2, padx=8, pady=8)
        ttk.Button(file_frame, text="Auto", command=lambda: self.output_path.set("auto")).grid(
            row=1, column=3, padx=(0, 12), pady=8
        )

        settings = ttk.LabelFrame(self, text="Render settings")
        settings.grid(row=2, column=0, sticky="ew", padx=18, pady=8)
        for col in range(8):
            settings.columnconfigure(col, weight=1)

        ttk.Label(settings, text="Type").grid(row=0, column=0, sticky="w", padx=12, pady=8)
        ttk.Combobox(
            settings,
            textvariable=self.media_type,
            values=("auto", "image", "video"),
            state="readonly",
            width=10,
        ).grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(settings, text="Mode").grid(row=0, column=2, sticky="w", padx=12, pady=8)
        ttk.Combobox(
            settings,
            textvariable=self.color_mode,
            values=("color", "vivid", "black/white"),
            state="readonly",
            width=12,
        ).grid(row=0, column=3, sticky="ew", padx=8, pady=8)

        ttk.Label(settings, text="Width").grid(row=0, column=4, sticky="w", padx=12, pady=8)
        ttk.Spinbox(settings, from_=20, to=360, textvariable=self.width_value, width=8).grid(
            row=0, column=5, sticky="ew", padx=8, pady=8
        )

        ttk.Label(settings, text="Font").grid(row=0, column=6, sticky="w", padx=12, pady=8)
        ttk.Spinbox(settings, from_=6, to=30, textvariable=self.font_size, width=8).grid(
            row=0, column=7, sticky="ew", padx=8, pady=8
        )

        ttk.Label(settings, text="Skip frames").grid(row=1, column=0, sticky="w", padx=12, pady=8)
        ttk.Spinbox(settings, from_=1, to=30, textvariable=self.skip_frames, width=8).grid(
            row=1, column=1, sticky="ew", padx=8, pady=8
        )

        ttk.Label(settings, text="Background").grid(row=1, column=2, sticky="w", padx=12, pady=8)
        ttk.Entry(settings, textvariable=self.background, width=10).grid(row=1, column=3, sticky="ew", padx=8, pady=8)

        ttk.Label(settings, text="Foreground").grid(row=1, column=4, sticky="w", padx=12, pady=8)
        ttk.Entry(settings, textvariable=self.foreground, width=10).grid(row=1, column=5, sticky="ew", padx=8, pady=8)

        ttk.Label(settings, text="Vivid sat.").grid(row=1, column=6, sticky="w", padx=12, pady=8)
        ttk.Spinbox(settings, from_=1.0, to=3.0, increment=0.05, textvariable=self.vivid_saturation, width=8).grid(
            row=1, column=7, sticky="ew", padx=8, pady=8
        )

        ttk.Label(settings, text="Vivid bright.").grid(row=2, column=6, sticky="w", padx=12, pady=8)
        ttk.Spinbox(settings, from_=1.0, to=2.0, increment=0.05, textvariable=self.vivid_brightness, width=8).grid(
            row=2, column=7, sticky="ew", padx=8, pady=8
        )

        ttk.Checkbutton(settings, text="Match input format", variable=self.match_input_format).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=12, pady=8
        )
        ttk.Checkbutton(settings, text="Preserve audio", variable=self.preserve_audio).grid(
            row=2, column=2, columnspan=2, sticky="w", padx=12, pady=8
        )
        ttk.Checkbutton(settings, text="Keep PNG frames", variable=self.keep_frames).grid(
            row=2, column=4, columnspan=2, sticky="w", padx=12, pady=8
        )

        log_frame = ttk.LabelFrame(self, text="Render log")
        log_frame.grid(row=3, column=0, sticky="nsew", padx=18, pady=8)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log = tk.Text(log_frame, height=12, wrap="word")
        self.log.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)

        bottom = ttk.Frame(self)
        bottom.grid(row=4, column=0, sticky="ew", padx=18, pady=(8, 18))
        bottom.columnconfigure(1, weight=1)

        self.render_button = ttk.Button(bottom, text="Render", command=self._start_render)
        self.render_button.grid(row=0, column=0, padx=(0, 12))

        self.progress = ttk.Progressbar(bottom, mode="determinate", maximum=100)
        self.progress.grid(row=0, column=1, sticky="ew", padx=8)

        ttk.Label(bottom, textvariable=self.status).grid(row=0, column=2, sticky="e", padx=(12, 0))

    def _browse_input(self) -> None:
        filename = filedialog.askopenfilename(title="Choose media file", filetypes=VIDEO_TYPES)
        if filename:
            self.input_path.set(filename)
            if self.output_path.get().strip().lower() in {"", "auto"}:
                self.output_path.set("auto")

    def _browse_output(self) -> None:
        input_path = Path(self.input_path.get())
        media_type = self.media_type.get()
        if media_type == "auto" and input_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}:
            filetypes = IMAGE_OUTPUT_TYPES
        elif media_type == "image":
            filetypes = IMAGE_OUTPUT_TYPES
        else:
            filetypes = VIDEO_OUTPUT_TYPES

        filename = filedialog.asksaveasfilename(title="Choose output file", filetypes=filetypes)
        if filename:
            self.output_path.set(filename)

    def _build_config(self) -> ConverterConfig:
        return ConverterConfig(
            input_path=self.input_path.get().strip(),
            output_path=self.output_path.get().strip() or "auto",
            media_type=self.media_type.get(),
            match_input_format=self.match_input_format.get(),
            width=self.width_value.get(),
            color=self.color_mode.get() != "black/white",
            color_style={"color": "normal", "vivid": "vivid", "black/white": "mono"}[self.color_mode.get()],
            vivid_saturation=self.vivid_saturation.get(),
            vivid_brightness=self.vivid_brightness.get(),
            background=self.background.get().strip(),
            foreground=self.foreground.get().strip(),
            font_size=self.font_size.get(),
            skip_frames=self.skip_frames.get(),
            preserve_audio=self.preserve_audio.get(),
            keep_temp_frames=self.keep_frames.get(),
            progress_every=10,
        )

    def _start_render(self) -> None:
        if self.worker and self.worker.is_alive():
            return

        if not self.input_path.get().strip():
            messagebox.showerror("Missing input", "Choose an image or video first.")
            return

        self.log.delete("1.0", "end")
        self.progress["value"] = 0
        self.status.set("Rendering...")
        self.render_button.configure(state="disabled")

        config = self._build_config()
        self.worker = threading.Thread(target=self._render_worker, args=(config,), daemon=True)
        self.worker.start()

    def _render_worker(self, config: ConverterConfig) -> None:
        writer = QueueWriter(self.events)
        try:
            with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                media_type = detect_media_type(Path(config.input_path), config.media_type)
                if media_type == "image":
                    output = export_ascii_image(config)
                else:
                    output = export_ascii_video(config)
            writer.flush()
            self.events.put(("done", str(output)))
        except Exception as exc:
            writer.flush()
            self.events.put(("error", str(exc)))

    def _poll_events(self) -> None:
        try:
            while True:
                event = self.events.get_nowait()
                if isinstance(event, tuple):
                    event_type, value = event
                    if event_type == "done":
                        self.progress["value"] = 100
                        self.status.set("Done")
                        self.render_button.configure(state="normal")
                        messagebox.showinfo("Render complete", f"Saved:\n{value}")
                    elif event_type == "error":
                        self.status.set("Error")
                        self.render_button.configure(state="normal")
                        messagebox.showerror("Render failed", value)
                    else:
                        self._append_log(value)
                else:
                    self._append_log(str(event))
        except queue.Empty:
            pass

        self.after(100, self._poll_events)

    def _append_log(self, line: str) -> None:
        self.log.insert("end", line + "\n")
        self.log.see("end")

        match = re.search(r"Frame\s+(\d+)/(\d+)\s+->\s+written\s+(\d+)", line)
        if match:
            current = int(match.group(1))
            total = max(1, int(match.group(2)))
            self.progress["value"] = min(100, current / total * 100)
            self.status.set(f"{current}/{total} frames")


def main() -> None:
    app = ASCIIConverterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
