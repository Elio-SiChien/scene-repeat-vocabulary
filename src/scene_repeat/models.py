from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VocabEntry:
    word: str
    phonetic: str = ""
    meaning: str = ""
    mnemonic: str = ""
    reading: str = ""
    source: str = ""
    theme: str = "mixed"
