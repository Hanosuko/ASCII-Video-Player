"""
Browser-based GUI for ASCII Media Converter V5.

Run:
    /usr/bin/python3 ascii_web_gui.py

Then open:
    http://127.0.0.1:8765
"""

from __future__ import annotations

import contextlib
import cgi
import html
import http.server
import os
import queue
import re
import threading
import time
import urllib.parse
import uuid
import webbrowser
from pathlib import Path
from typing import Dict, List, Optional

from ASCII_v5_official import (
    ConverterConfig,
    detect_media_type,
    export_ascii_image,
    export_ascii_video,
)


HOST = "127.0.0.1"
PORT = 8765
ROOT = Path(__file__).resolve().parent
MEDIA_DIR = ROOT / "Video_temp"
MEDIA_DIR.mkdir(exist_ok=True)

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".mpeg", ".mpg"}
ALLOWED_SUFFIXES = IMAGE_SUFFIXES | VIDEO_SUFFIXES


class Job:
    def __init__(self) -> None:
        self.id = uuid.uuid4().hex[:10]
        self.status = "queued"
        self.progress = 0
        self.logs: List[str] = []
        self.output: Optional[Path] = None
        self.error: Optional[str] = None
        self.started_at = time.time()

    def log(self, line: str) -> None:
        if not line.strip():
            return
        self.logs.append(line.strip())
        self.logs = self.logs[-300:]
        match = re.search(r"Frame\s+(\d+)/(\d+)\s+->\s+written\s+(\d+)", line)
        if match:
            current = int(match.group(1))
            total = max(1, int(match.group(2)))
            self.progress = min(99, int(current / total * 100))


JOBS: Dict[str, Job] = {}


class QueueWriter:
    def __init__(self, job: Job) -> None:
        self.job = job
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
            self.job.log(line)
        return len(text)

    def flush(self) -> None:
        if self.buffer.strip():
            self.job.log(self.buffer)
            self.buffer = ""


def sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    safe = re.sub(r"[^A-Za-z0-9._ -]+", "_", name).strip()
    return safe or f"upload_{int(time.time())}"


def media_files() -> List[Path]:
    files = []
    for path in MEDIA_DIR.iterdir():
        if path.is_file() and path.suffix.lower() in ALLOWED_SUFFIXES:
            files.append(path)
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def render_job(job: Job, config: ConverterConfig) -> None:
    writer = QueueWriter(job)
    job.status = "running"
    try:
        with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
            media_type = detect_media_type(Path(config.input_path), config.media_type)
            if media_type == "image":
                output = export_ascii_image(config)
            else:
                output = export_ascii_video(config)
        writer.flush()
        job.output = Path(output)
        job.progress = 100
        job.status = "done"
    except Exception as exc:
        writer.flush()
        job.error = str(exc)
        job.status = "error"
        job.log(f"Error: {exc}")


def page(title: str, body: str, refresh: bool = False) -> bytes:
    refresh_tag = '<meta http-equiv="refresh" content="2">' if refresh else ""
    html_doc = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {refresh_tag}
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #101216;
      --panel: #181c22;
      --line: #2b313a;
      --text: #eef2f7;
      --muted: #9aa6b2;
      --accent: #51b6ff;
      --danger: #ff6868;
      --ok: #69d68d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{ max-width: 980px; margin: 0 auto; padding: 28px 18px 46px; }}
    h1 {{ font-size: 28px; margin: 0 0 18px; }}
    h2 {{ font-size: 17px; margin: 0 0 12px; color: var(--muted); }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      margin: 14px 0;
    }}
    label {{ display: block; margin: 12px 0 6px; color: var(--muted); }}
    input, select {{
      width: 100%;
      background: #0f1319;
      color: var(--text);
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      font-size: 14px;
    }}
    input[type="checkbox"] {{ width: auto; margin-right: 8px; }}
    input[type="file"] {{ padding: 8px; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .checkrow {{ display: flex; gap: 18px; flex-wrap: wrap; margin-top: 12px; }}
    .checkrow label {{ margin: 0; color: var(--text); }}
    button, .button {{
      display: inline-block;
      width: auto;
      background: var(--accent);
      color: #05101a;
      border: 0;
      border-radius: 6px;
      padding: 11px 16px;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      margin-top: 16px;
    }}
    .secondary {{ background: #303846; color: var(--text); }}
    .ok {{ color: var(--ok); }}
    .danger {{ color: var(--danger); }}
    .muted {{ color: var(--muted); }}
    pre {{
      white-space: pre-wrap;
      background: #0b0e13;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      min-height: 180px;
      max-height: 380px;
      overflow: auto;
    }}
    progress {{ width: 100%; height: 22px; }}
    @media (max-width: 760px) {{
      .grid, .grid-2 {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>{body}</main>
</body>
</html>"""
    return html_doc.encode("utf-8")


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return

    def send_html(self, title: str, body: str, refresh: bool = False, status: int = 200) -> None:
        content = page(title, body, refresh)
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def redirect(self, path: str) -> None:
        self.send_response(303)
        self.send_header("Location", path)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self.show_index()
        elif parsed.path == "/job":
            job_id = urllib.parse.parse_qs(parsed.query).get("id", [""])[0]
            self.show_job(job_id)
        elif parsed.path == "/file":
            rel = urllib.parse.parse_qs(parsed.query).get("path", [""])[0]
            self.send_file(rel)
        else:
            self.send_html("Not found", "<h1>Not found</h1>", status=404)

    def do_POST(self) -> None:
        if self.path != "/render":
            self.send_html("Not found", "<h1>Not found</h1>", status=404)
            return
        self.handle_render()

    def show_index(self) -> None:
        options = ['<option value="">Choose existing file...</option>']
        for path in media_files():
            name = path.name
            options.append(f'<option value="{html.escape(name)}">{html.escape(name)}</option>')

        body = f"""
<h1>ASCII Media Converter</h1>
<form class="panel" action="/render" method="post" enctype="multipart/form-data">
  <h2>Input</h2>
  <div class="grid-2">
    <div>
      <label>Upload image/video</label>
      <input type="file" name="upload">
    </div>
    <div>
      <label>Or choose from Video_temp</label>
      <select name="existing">{''.join(options)}</select>
    </div>
  </div>

  <h2 style="margin-top:18px">Output and render</h2>
  <div class="grid">
    <div>
      <label>Output</label>
      <input name="output_path" value="auto">
    </div>
    <div>
      <label>Type</label>
      <select name="media_type">
        <option value="auto">auto</option>
        <option value="image">image</option>
        <option value="video">video</option>
      </select>
    </div>
    <div>
      <label>Mode</label>
      <select name="color_mode">
        <option value="color">color</option>
        <option value="bw">black/white</option>
      </select>
    </div>
    <div>
      <label>Width</label>
      <input name="width" type="number" min="20" max="360" value="120">
    </div>
    <div>
      <label>Font size</label>
      <input name="font_size" type="number" min="6" max="30" value="10">
    </div>
    <div>
      <label>Skip frames</label>
      <input name="skip_frames" type="number" min="1" max="30" value="1">
    </div>
    <div>
      <label>Background</label>
      <input name="background" value="#000000">
    </div>
    <div>
      <label>Foreground</label>
      <input name="foreground" value="#FFFFFF">
    </div>
  </div>

  <div class="checkrow">
    <label><input type="checkbox" name="match_input_format" checked>Match input format</label>
    <label><input type="checkbox" name="preserve_audio" checked>Preserve audio</label>
    <label><input type="checkbox" name="keep_temp_frames">Keep PNG frames</label>
  </div>

  <button type="submit">Render</button>
</form>
<p class="muted">Files are stored in <code>{html.escape(str(MEDIA_DIR))}</code>.</p>
"""
        self.send_html("ASCII Media Converter", body)

    def show_job(self, job_id: str) -> None:
        job = JOBS.get(job_id)
        if not job:
            self.send_html("Job not found", '<h1>Job not found</h1><a class="button" href="/">Back</a>', status=404)
            return

        status_class = "ok" if job.status == "done" else "danger" if job.status == "error" else ""
        logs = html.escape("\n".join(job.logs) or "Waiting for render output...")
        output = ""
        if job.output:
            rel = urllib.parse.quote(str(job.output.relative_to(ROOT)) if job.output.is_relative_to(ROOT) else str(job.output))
            output = f'<p class="ok">Saved: {html.escape(str(job.output))}</p><a class="button" href="/file?path={rel}">Open/download result</a>'
        if job.error:
            output += f'<p class="danger">Error: {html.escape(job.error)}</p>'

        body = f"""
<h1>Render job</h1>
<div class="panel">
  <p>Status: <strong class="{status_class}">{html.escape(job.status)}</strong></p>
  <progress max="100" value="{job.progress}"></progress>
  <p class="muted">{job.progress}%</p>
  {output}
  <a class="button secondary" href="/">Back</a>
</div>
<div class="panel">
  <h2>Log</h2>
  <pre>{logs}</pre>
</div>
"""
        self.send_html("Render job", body, refresh=job.status in {"queued", "running"})

    def handle_render(self) -> None:
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST"})

        input_path: Optional[Path] = None
        upload = form["upload"] if "upload" in form else None
        if upload is not None and getattr(upload, "filename", ""):
            filename = sanitize_filename(upload.filename)
            input_path = MEDIA_DIR / filename
            with input_path.open("wb") as handle:
                while True:
                    chunk = upload.file.read(1024 * 1024)
                    if not chunk:
                        break
                    handle.write(chunk)

        existing = form.getfirst("existing", "").strip()
        if input_path is None and existing:
            candidate = MEDIA_DIR / sanitize_filename(existing)
            if candidate.exists():
                input_path = candidate

        if input_path is None:
            self.send_html("Missing input", '<h1>Choose or upload a file first</h1><a class="button" href="/">Back</a>', status=400)
            return

        def get_int(name: str, default: int) -> int:
            try:
                return int(form.getfirst(name, str(default)))
            except ValueError:
                return default

        config = ConverterConfig(
            input_path=str(input_path),
            output_path=form.getfirst("output_path", "auto").strip() or "auto",
            media_type=form.getfirst("media_type", "auto"),
            match_input_format="match_input_format" in form,
            width=get_int("width", 120),
            color=form.getfirst("color_mode", "color") == "color",
            background=form.getfirst("background", "#000000"),
            foreground=form.getfirst("foreground", "#FFFFFF"),
            font_size=get_int("font_size", 10),
            skip_frames=get_int("skip_frames", 1),
            preserve_audio="preserve_audio" in form,
            keep_temp_frames="keep_temp_frames" in form,
        )

        job = Job()
        JOBS[job.id] = job
        thread = threading.Thread(target=render_job, args=(job, config), daemon=True)
        thread.start()
        self.redirect(f"/job?id={job.id}")

    def send_file(self, rel: str) -> None:
        path = Path(urllib.parse.unquote(rel))
        if not path.is_absolute():
            path = ROOT / path
        try:
            path.resolve().relative_to(ROOT)
        except ValueError:
            self.send_html("Forbidden", "<h1>Forbidden</h1>", status=403)
            return
        if not path.exists() or not path.is_file():
            self.send_html("Not found", "<h1>File not found</h1>", status=404)
            return

        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f'attachment; filename="{path.name}"')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main() -> None:
    url = f"http://{HOST}:{PORT}"
    server = http.server.ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"ASCII web app: {url}")
    print("Press Ctrl+C to stop.")
    try:
        webbrowser.open(url)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
