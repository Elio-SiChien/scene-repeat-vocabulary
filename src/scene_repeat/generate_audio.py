from __future__ import annotations

import re
from pathlib import Path

from .tts_kokoro import synthesize_kokoro


def extract_follow_script(markdown: str) -> str:
    match = re.search(r"(?ms)^## 跟读稿\s*(.*?)(?=^## |\Z)", markdown)
    if match:
        return strip_markdown(match.group(1))
    return strip_markdown(markdown)


def strip_markdown(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[-*]\s+\[[ xX]\]\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()


def generate_audio_for_notes(notes: list[Path], audio_dir: Path, model: Path, voices: Path, speed: float = 0.95) -> list[Path]:
    outputs: list[Path] = []
    for note in notes:
        day_match = re.search(r"(\d+)", note.stem)
        if not day_match:
            continue
        day = int(day_match.group(1))
        text = extract_follow_script(note.read_text(encoding="utf-8"))
        output = audio_dir / f"day-{day:03d}.wav"
        synthesize_kokoro(text, output, model, voices, speed=speed)
        outputs.append(output)
    return outputs
