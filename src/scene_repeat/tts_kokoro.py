from __future__ import annotations

from pathlib import Path

import soundfile as sf


def synthesize_kokoro(text: str, output: Path, model: Path, voices: Path, voice: str = "af_sarah", speed: float = 0.95) -> None:
    try:
        from kokoro_onnx import Kokoro
    except ImportError as exc:
        raise RuntimeError("Install the optional Kokoro dependencies first: pip install 'scene-repeat-vocabulary[tts]'") from exc
    if not model.exists():
        raise FileNotFoundError(f"Missing Kokoro model: {model}")
    if not voices.exists():
        raise FileNotFoundError(f"Missing Kokoro voices file: {voices}")
    kokoro = Kokoro(str(model), str(voices))
    samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
    output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output), samples, sample_rate)
