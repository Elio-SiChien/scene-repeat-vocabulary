from __future__ import annotations

import re
from pathlib import Path

from .models import VocabEntry


THEME_KEYWORDS: dict[str, list[str]] = {
    "work": ["work", "office", "project", "meeting", "metric", "pilot", "application", "eligible", "function", "dashboard"],
    "study": ["study", "class", "course", "seminar", "lecture", "research", "formula", "heuristic", "feasibility"],
    "tech": ["computer", "screen", "software", "data", "fetch", "archive", "paste", "interactive", "threshold", "raster"],
    "travel": ["travel", "commute", "train", "bus", "pilot", "harbor", "migrate", "inhabit", "journey"],
    "social": ["praise", "compliment", "admiration", "familiar", "conversation", "friend", "harmony", "plea"],
    "conflict": ["conflict", "protest", "rebellion", "raid", "harassment", "bully", "villain", "forbid", "interfere"],
    "home": ["home", "family", "aroma", "cotton", "sponge", "bell", "mustache", "flat"],
    "health": ["health", "clinical", "depress", "disability", "intense", "hysterical", "fragrance"],
}


def parse_vocab_paths(paths: list[Path]) -> list[VocabEntry]:
    entries: list[VocabEntry] = []
    seen: set[str] = set()
    for path in paths:
        for entry in parse_vocab_file(path):
            key = entry.word.lower()
            if key in seen:
                continue
            seen.add(key)
            entries.append(entry)
    return entries


def parse_vocab_file(path: Path) -> list[VocabEntry]:
    content = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^##\s+", content)
    entries: list[VocabEntry] = []
    for part in parts[1:]:
        block = "## " + part.strip()
        heading = block.splitlines()[0].removeprefix("## ").strip()
        match = re.match(r"(?P<word>.+?)(?:\s+/(?P<phonetic>[^/]+)/)?$", heading)
        if not match:
            continue
        word = match.group("word").strip()
        if not word:
            continue
        phonetic = (match.group("phonetic") or "").strip()
        meaning = find_field(block, "释义") or find_field(block, "Meaning")
        mnemonic = find_field(block, "助记") or find_field(block, "Mnemonic")
        reading = find_field(block, "助读") or find_field(block, "Reading")
        source = find_field(block, "来源") or find_field(block, "Source")
        entries.append(
            VocabEntry(
                word=word,
                phonetic=phonetic,
                meaning=meaning,
                mnemonic=mnemonic,
                reading=reading,
                source=source,
                theme=classify_theme(word, meaning),
            )
        )
    return entries


def find_field(block: str, label: str) -> str:
    match = re.search(rf"(?m)^-\s*{re.escape(label)}[:：]\s*(.+)$", block)
    return match.group(1).strip() if match else ""


def classify_theme(word: str, meaning: str) -> str:
    haystack = f"{word.lower()} {meaning.lower()}"
    scores = {
        theme: sum(1 for keyword in keywords if keyword.lower() in haystack)
        for theme, keywords in THEME_KEYWORDS.items()
    }
    best_theme, best_score = max(scores.items(), key=lambda item: item[1])
    return best_theme if best_score > 0 else "mixed"
