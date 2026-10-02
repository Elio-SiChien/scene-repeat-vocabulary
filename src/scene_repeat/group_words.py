from __future__ import annotations

import random
from collections import defaultdict

from .models import VocabEntry


def group_round(entries: list[VocabEntry], words_per_day: int, seed: int) -> list[list[VocabEntry]]:
    if words_per_day <= 0:
        raise ValueError("words_per_day must be positive")

    rng = random.Random(seed)
    buckets: dict[str, list[VocabEntry]] = defaultdict(list)
    for entry in entries:
        buckets[entry.theme].append(entry)
    for bucket in buckets.values():
        rng.shuffle(bucket)

    days = (len(entries) + words_per_day - 1) // words_per_day
    capacities = [words_per_day] * days
    overflow = sum(capacities) - len(entries)
    if overflow:
        capacities[-1] -= overflow

    theme_counts = sorted(buckets.items(), key=lambda item: len(item[1]), reverse=True)
    preferred_themes: list[str] = []
    while len(preferred_themes) < days:
        for theme, _bucket in theme_counts:
            preferred_themes.append(theme)
            if len(preferred_themes) == days:
                break
    rng.shuffle(preferred_themes)

    groups: list[list[VocabEntry]] = [[] for _ in range(days)]

    def room(index: int) -> int:
        return capacities[index] - len(groups[index])

    for theme, bucket in theme_counts:
        for entry in bucket:
            candidates = [
                index
                for index, preferred in enumerate(preferred_themes)
                if preferred == theme and room(index) > 0
            ]
            if not candidates:
                candidates = [index for index in range(days) if room(index) > 0]
            if not candidates:
                raise AssertionError("No room left while grouping words")
            target_index = min(candidates, key=lambda index: (len(groups[index]), rng.random()))
            groups[target_index].append(entry)

    for group in groups:
        rng.shuffle(group)
    validate_round(groups, len(entries), words_per_day)
    return groups


def build_schedule(entries: list[VocabEntry], rounds: int, words_per_day: int, seed: int = 20261002) -> list[list[VocabEntry]]:
    schedule: list[list[VocabEntry]] = []
    for round_index in range(rounds):
        schedule.extend(group_round(entries, words_per_day, seed + round_index * 7919))
    validate_schedule(schedule, len(entries), rounds, words_per_day)
    return schedule


def validate_round(groups: list[list[VocabEntry]], total_entries: int, words_per_day: int) -> None:
    words = [entry.word.lower() for group in groups for entry in group]
    if len(words) != total_entries:
        raise AssertionError(f"Expected {total_entries} word slots, got {len(words)}")
    if len(set(words)) != total_entries:
        raise AssertionError("Round contains duplicate words")
    if any(len(group) > words_per_day for group in groups):
        raise AssertionError("A day exceeds words_per_day")


def validate_schedule(schedule: list[list[VocabEntry]], total_entries: int, rounds: int, words_per_day: int) -> None:
    days_per_round = (total_entries + words_per_day - 1) // words_per_day
    expected_days = days_per_round * rounds
    if len(schedule) != expected_days:
        raise AssertionError(f"Expected {expected_days} days, got {len(schedule)}")
    for round_index in range(rounds):
        start = round_index * days_per_round
        validate_round(schedule[start : start + days_per_round], total_entries, words_per_day)
