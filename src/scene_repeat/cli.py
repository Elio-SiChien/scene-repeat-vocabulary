from __future__ import annotations

import argparse
from pathlib import Path

from .generate_audio import generate_audio_for_notes
from .generate_days import generate_review


def main() -> None:
    parser = argparse.ArgumentParser(prog="scene-repeat")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate scene-based vocabulary review notes.")
    generate.add_argument("--vocab", type=Path, nargs="+", required=True, help="Vocabulary Markdown file(s).")
    generate.add_argument("--out", type=Path, required=True, help="Output review directory.")
    generate.add_argument("--rounds", type=int, default=3)
    generate.add_argument("--words-per-day", type=int, default=20)
    generate.add_argument("--seed", type=int, default=20261002)
    generate.add_argument("--tts", choices=["none", "kokoro"], default="none")
    generate.add_argument("--model", type=Path, help="Kokoro ONNX model path.")
    generate.add_argument("--voices", type=Path, help="Kokoro voices bin path.")
    generate.add_argument("--speed", type=float, default=0.95)

    args = parser.parse_args()
    if args.command == "generate":
        notes = generate_review(args.vocab, args.out, args.rounds, args.words_per_day, args.seed)
        if args.tts == "kokoro":
            if not args.model or not args.voices:
                raise SystemExit("--model and --voices are required when --tts kokoro")
            generate_audio_for_notes(notes, args.out / "audio", args.model, args.voices, args.speed)
        print(f"Generated {len(notes)} review notes in {args.out}")


if __name__ == "__main__":
    main()
