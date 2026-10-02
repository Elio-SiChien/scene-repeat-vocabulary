from pathlib import Path


def test_no_private_windows_paths_in_source() -> None:
    root = Path(__file__).resolve().parents[1]
    forbidden = [
        "G:" + "\\0_PhD_Elio_" + "20260817",
        "G:" + "\\Daily " + "routine",
        "0_AI makes Elio " + "powerful",
    ]
    checked_suffixes = {".py", ".md", ".toml", ".gitignore"}
    for path in root.rglob("*"):
        if path.is_dir() or path.suffix not in checked_suffixes:
            continue
        if any(part in {".venv", "models", "review", "review_tts"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        assert not any(value in text for value in forbidden), path
