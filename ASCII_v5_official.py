"""
ASCII Media Converter V5
========================

Config-driven image/video-to-ASCII exporter with optional video audio
preservation. Video inputs use OpenCV, image inputs use Pillow.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczmwqpdbkhao*#MW&8%B@$0QSXGZJKPHDAUYTRENVLCF"
CHARS_ARRAY = np.array(list(ASCII_CHARS))
SUPPORTED_VIDEO_HINT = ".mp4, .mov, .avi, .mkv, .webm, .m4v, .mpeg, .mpg"
SUPPORTED_IMAGE_HINT = ".png, .jpg, .jpeg, .webp, .bmp, .tif, .tiff"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VIDEO_OUTPUT_SUFFIXES = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}
AUTO_OUTPUT_VALUES = {"", "auto"}


@dataclass
class ConverterConfig:
    input_path: str = "Video_temp/data.mp4"
    output_path: str = "auto"
    media_type: str = "auto"
    match_input_format: bool = True
    width: int = 120
    color: bool = True
    background: str = "#000000"
    foreground: str = "#FFFFFF"
    font_size: int = 10
    skip_frames: int = 1
    preserve_audio: bool = True
    keep_temp_frames: bool = False
    temp_dir: str = "Video_temp/temp_ascii_frames"
    video_codec: str = "mp4v"
    final_video_codec: str = "libx264"
    final_video_crf: int = 22
    final_video_preset: str = "medium"
    audio_bitrate: str = "192k"
    progress_every: int = 10


@dataclass
class VideoInfo:
    fps: float
    frame_count: int
    width: int
    height: int

    @property
    def duration(self) -> float:
        return self.frame_count / max(self.fps, 1.0)


def parse_hex_color(value: str) -> Tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise ValueError(f"Color must be in #RRGGBB format: {value}")
    try:
        return tuple(int(raw[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise ValueError(f"Color must be in #RRGGBB format: {value}") from exc


def load_config(path: Optional[str]) -> ConverterConfig:
    config = ConverterConfig()
    if not path:
        return config

    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    allowed = {field.name for field in fields(ConverterConfig)}
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"Unknown config keys: {', '.join(unknown)}")

    return ConverterConfig(**{**config.__dict__, **data})


def save_default_config(path: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(ConverterConfig().__dict__, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def apply_cli_overrides(config: ConverterConfig, args: argparse.Namespace) -> ConverterConfig:
    overrides: Dict[str, Any] = {
        "input_path": args.input,
        "output_path": args.output,
        "media_type": args.media_type,
        "match_input_format": args.match_input_format,
        "width": args.width,
        "color": args.color,
        "preserve_audio": args.preserve_audio,
        "skip_frames": args.skip_frames,
    }
    for key, value in overrides.items():
        if value is not None:
            setattr(config, key, value)
    return config


def detect_media_type(path: Path, configured_type: str) -> str:
    media_type = configured_type.strip().lower()
    if media_type in {"image", "video"}:
        return media_type
    if media_type != "auto":
        raise ValueError("media_type must be one of: auto, image, video")
    return "image" if path.suffix.lower() in IMAGE_SUFFIXES else "video"


def open_video(path: Path) -> Tuple[cv2.VideoCapture, VideoInfo]:
    if not path.exists():
        raise FileNotFoundError(f"Input video not found: {path}")

    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(
            f"Could not open '{path}'. Try another file or convert it to a common codec first."
        )

    fps = capture.get(cv2.CAP_PROP_FPS)
    info = VideoInfo(
        fps=fps if fps and fps > 0 else 30.0,
        frame_count=int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        width=int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        height=int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    return capture, info


def open_image_as_frame(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Input image not found: {path}")
    try:
        image = Image.open(path).convert("RGB")
    except Exception as exc:
        raise RuntimeError(f"Could not open image '{path}'.") from exc
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def frame_to_ascii(frame: np.ndarray, width: int) -> Tuple[np.ndarray, np.ndarray]:
    height = max(1, int(frame.shape[0] * width / frame.shape[1] / 2))
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    brightness = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    indices = np.clip(
        (brightness / 255.0 * (len(ASCII_CHARS) - 1)).astype(np.int32),
        0,
        len(ASCII_CHARS) - 1,
    )
    return CHARS_ARRAY[indices], rgb


def load_font(font_size: int) -> ImageFont.ImageFont:
    candidates = [
        "Menlo.ttc",
        "Monaco.ttf",
        "Consolas.ttf",
        "consola.ttf",
        "cour.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, font_size)
        except OSError:
            continue
    return ImageFont.load_default()


def char_cell_size(font: ImageFont.ImageFont, font_size: int) -> Tuple[int, int]:
    probe = Image.new("RGB", (font_size * 4, font_size * 4))
    draw = ImageDraw.Draw(probe)
    bbox = draw.textbbox((0, 0), "M", font=font)
    width = max(1, bbox[2] - bbox[0])
    height = max(1, bbox[3] - bbox[1])
    return width, int(height * 1.35)


def ascii_to_image(
    char_map: np.ndarray,
    rgb_map: np.ndarray,
    config: ConverterConfig,
    font: ImageFont.ImageFont,
    cell_size: Tuple[int, int],
) -> Image.Image:
    rows, cols = char_map.shape
    cell_w, cell_h = cell_size
    background = parse_hex_color(config.background)
    foreground = parse_hex_color(config.foreground)

    image = Image.new("RGB", (cols * cell_w, rows * cell_h), background)
    draw = ImageDraw.Draw(image)

    for y in range(rows):
        y_pos = y * cell_h
        for x in range(cols):
            color = tuple(int(v) for v in rgb_map[y, x]) if config.color else foreground
            draw.text((x * cell_w, y_pos), str(char_map[y, x]), fill=color, font=font)

    return image


def temp_silent_output(output_path: Path) -> Path:
    return output_path.with_name(f"{output_path.stem}.silent{output_path.suffix or '.mp4'}")


def default_output_path(input_path: Path, media_type: str) -> Path:
    suffix = input_path.suffix or (".png" if media_type == "image" else ".mp4")
    return input_path.with_name(f"{input_path.stem}_ASCII{suffix}")


def resolve_output_path(input_path: Path, config: ConverterConfig, media_type: str) -> Path:
    configured = str(config.output_path).strip()
    if configured.lower() in AUTO_OUTPUT_VALUES:
        return default_output_path(input_path, media_type)

    output_path = Path(configured)
    if config.match_input_format:
        suffix = input_path.suffix or (".png" if media_type == "image" else ".mp4")
        return output_path.with_suffix(suffix)

    if media_type == "image" and (not output_path.suffix or output_path.suffix.lower() in VIDEO_OUTPUT_SUFFIXES):
        return output_path.with_suffix(".png")

    return output_path


def find_ffmpeg() -> Optional[str]:
    from_path = shutil.which("ffmpeg")
    if from_path:
        return from_path

    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def mux_audio(input_video: Path, silent_video: Path, output_video: Path, config: ConverterConfig) -> bool:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("Audio: ffmpeg not found, saving video without audio.")
        return False

    temp_muxed = output_video.with_name(f"{output_video.stem}.muxed{output_video.suffix or '.mp4'}")
    command = [
        ffmpeg,
        "-y",
        "-i",
        str(silent_video),
        "-i",
        str(input_video),
        "-map",
        "0:v:0",
        "-map",
        "1:a?",
        "-c:v",
        config.final_video_codec,
        "-preset",
        config.final_video_preset,
        "-crf",
        str(config.final_video_crf),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        config.audio_bitrate,
        "-shortest",
        "-movflags",
        "+faststart",
        str(temp_muxed),
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Audio: failed to mux audio, saving video without audio.")
        print(result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "Unknown ffmpeg error")
        return False

    temp_muxed.replace(output_video)
    return True


def normalize_common_config(config: ConverterConfig) -> None:
    config.width = max(20, int(config.width))
    config.font_size = max(6, int(config.font_size))
    config.skip_frames = max(1, int(config.skip_frames))
    parse_hex_color(config.background)
    parse_hex_color(config.foreground)


def export_ascii_image(config: ConverterConfig) -> Path:
    input_path = Path(config.input_path)
    output_path = resolve_output_path(input_path, config, "image")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    normalize_common_config(config)

    frame = open_image_as_frame(input_path)
    font = load_font(config.font_size)
    cell_size = char_cell_size(font, config.font_size)
    char_map, rgb_map = frame_to_ascii(frame, config.width)
    image = ascii_to_image(char_map, rgb_map, config, font, cell_size)

    print("ASCII Media Converter V5")
    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print(f"Type  : image")
    print(f"Mode  : {'color' if config.color else 'black/white'} ASCII")
    print(f"Images: commonly {SUPPORTED_IMAGE_HINT}")

    if output_path.suffix.lower() in {".jpg", ".jpeg"}:
        image.save(output_path, quality=95, optimize=True)
    else:
        image.save(output_path)

    print(f"Done: {output_path}")
    print(f"Size: {image.size[0]}x{image.size[1]}")
    return output_path


def export_ascii_video(config: ConverterConfig) -> Path:
    input_path = Path(config.input_path)
    output_path = resolve_output_path(input_path, config, "video")
    temp_dir = Path(config.temp_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    normalize_common_config(config)

    capture, info = open_video(input_path)
    export_fps = info.fps / config.skip_frames
    silent_path = temp_silent_output(output_path) if config.preserve_audio else output_path

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    font = load_font(config.font_size)
    cell_size = char_cell_size(font, config.font_size)
    writer: Optional[cv2.VideoWriter] = None
    written = 0
    read_index = 0

    print("ASCII Media Converter V5")
    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print(f"Type  : video")
    print(f"Mode  : {'color' if config.color else 'black/white'} ASCII")
    print(f"Audio : {'preserve' if config.preserve_audio else 'disabled'}")
    print(f"Videos: input depends on OpenCV codecs, commonly {SUPPORTED_VIDEO_HINT}")

    started = time.perf_counter()
    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                break

            read_index += 1
            if (read_index - 1) % config.skip_frames != 0:
                continue

            char_map, rgb_map = frame_to_ascii(frame, config.width)
            image = ascii_to_image(char_map, rgb_map, config, font, cell_size)
            frame_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            if writer is None:
                height, width = frame_bgr.shape[:2]
                fourcc = cv2.VideoWriter_fourcc(*config.video_codec[:4])
                writer = cv2.VideoWriter(str(silent_path), fourcc, export_fps, (width, height))
                if not writer.isOpened():
                    raise RuntimeError(f"Could not create output video: {silent_path}")

            writer.write(frame_bgr)
            written += 1

            if config.keep_temp_frames:
                frame_file = temp_dir / f"frame_{written:05d}.png"
                image.save(frame_file)

            if written % max(1, config.progress_every) == 0:
                total = info.frame_count or "?"
                print(f"Frame {read_index}/{total} -> written {written}", end="\r", flush=True)
    finally:
        capture.release()
        if writer:
            writer.release()

    if written == 0:
        raise RuntimeError("No frames were readable from the input video.")

    if not config.keep_temp_frames and temp_dir.exists():
        shutil.rmtree(temp_dir)

    audio_status = "not requested"
    if config.preserve_audio:
        audio_copied = mux_audio(input_path, silent_path, output_path, config)
        audio_status = "copied" if audio_copied else "not copied"
        if not audio_copied and silent_path.exists():
            silent_path.replace(output_path)
        if silent_path.exists():
            silent_path.unlink()

    elapsed = time.perf_counter() - started
    print()
    print(f"Done: {output_path}")
    print(f"Frames written: {written}")
    print(f"FPS: {export_fps:.2f}")
    print(f"Audio: {audio_status}")
    print(f"Elapsed: {elapsed:.1f}s")
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert images or videos to ASCII-style media using a JSON config.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--config", help="Path to JSON config.")
    parser.add_argument("--init-config", help="Create a default JSON config at this path and exit.")
    parser.add_argument("--input", help="Override input_path from config.")
    parser.add_argument("--output", help="Override output_path from config.")
    parser.add_argument("--media-type", choices=["auto", "image", "video"], help="How to treat the input file.")
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument(
        "--match-input-format",
        action="store_true",
        dest="match_input_format",
        help="Force output extension to match the input extension.",
    )
    format_group.add_argument(
        "--keep-output-format",
        action="store_false",
        dest="match_input_format",
        help="Use the extension from output_path exactly as written.",
    )
    parser.set_defaults(match_input_format=None)
    parser.add_argument("--width", type=int, help="Override ASCII width in characters.")
    parser.add_argument("--skip-frames", type=int, help="Render every Nth frame.")

    color_group = parser.add_mutually_exclusive_group()
    color_group.add_argument("--color", action="store_true", dest="color", help="Render colored ASCII.")
    color_group.add_argument("--no-color", action="store_false", dest="color", help="Render monochrome ASCII.")
    parser.set_defaults(color=None)

    audio_group = parser.add_mutually_exclusive_group()
    audio_group.add_argument("--preserve-audio", action="store_true", dest="preserve_audio")
    audio_group.add_argument("--no-audio", action="store_false", dest="preserve_audio")
    parser.set_defaults(preserve_audio=None)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.init_config:
        save_default_config(args.init_config)
        print(f"Config created: {args.init_config}")
        return 0

    try:
        config = apply_cli_overrides(load_config(args.config), args)
        media_type = detect_media_type(Path(config.input_path), config.media_type)
        if media_type == "image":
            export_ascii_image(config)
        else:
            export_ascii_video(config)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
