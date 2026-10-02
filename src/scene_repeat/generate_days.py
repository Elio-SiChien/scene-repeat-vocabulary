from __future__ import annotations

import re
from pathlib import Path

from .group_words import build_schedule
from .models import VocabEntry
from .parse_vocab import parse_vocab_paths


SCENE_CONFIGS = {
    "work": ("office project update", "In a small office, the team is preparing a calm project update."),
    "study": ("classroom and seminar", "In a classroom after a seminar, a student tries to explain the key ideas clearly."),
    "tech": ("software workflow", "At a desk with two screens, someone is cleaning up a software workflow."),
    "travel": ("commute and travel", "On the way across town, a traveler notices small details during the commute."),
    "social": ("friendly conversation", "During a friendly conversation, two people try to speak honestly and kindly."),
    "conflict": ("difficult conversation", "In a tense moment, a group tries to solve a conflict without making it worse."),
    "home": ("home and daily routine", "At home in the evening, ordinary objects make the day easier to remember."),
    "health": ("clinic and wellbeing", "In a quiet clinic, a person describes how they feel and asks for practical help."),
    "mixed": ("daily life", "During an ordinary day, several small moments connect into one useful memory."),
}


def generate_review(
    vocab_paths: list[Path],
    out_dir: Path,
    rounds: int,
    words_per_day: int,
    seed: int = 20261002,
) -> list[Path]:
    entries = parse_vocab_paths(vocab_paths)
    if not entries:
        raise ValueError("No vocabulary entries found")
    schedule = build_schedule(entries, rounds, words_per_day, seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "audio").mkdir(exist_ok=True)
    write_readme(out_dir, len(entries), rounds, words_per_day)
    days_per_round = (len(entries) + words_per_day - 1) // words_per_day

    paths: list[Path] = []
    for day_no, day_entries in enumerate(schedule, start=1):
        round_no = (day_no - 1) // days_per_round + 1
        day_in_round = (day_no - 1) % days_per_round + 1
        path = out_dir / f"Day {day_no:03d}.md"
        path.write_text(note_markdown(day_no, round_no, day_in_round, days_per_round, day_entries), encoding="utf-8")
        paths.append(path)
    return paths


def write_readme(out_dir: Path, total_entries: int, rounds: int, words_per_day: int) -> None:
    days_per_round = (total_entries + words_per_day - 1) // words_per_day
    content = f"""# Vocabulary Review

- Unique words per round: {total_entries}
- Words per day: up to {words_per_day}
- Rounds: {rounds}
- Total days: {days_per_round * rounds}

## Rules

- Each round covers every word once, without repetition inside the round.
- Words are grouped by scene and meaning, not by alphabetic order.
- Each daily note contains a meaningful life-scene paragraph, not a plain word list.
- Audio should read the English scene and follow-along prompt, not the definitions.
"""
    (out_dir / "README.md").write_text(content, encoding="utf-8")


def note_markdown(day_no: int, round_no: int, day_in_round: int, days_per_round: int, entries: list[VocabEntry]) -> str:
    scene_name, story, follow_lines = story_for_day(entries, round_no, day_in_round)
    lines = [
        f"# Vocabulary Review - Day {day_no:03d}",
        "",
        f"- Round: {round_no}",
        f"- Day in round: {day_in_round}/{days_per_round}",
        f"- Scene: {scene_name}",
        f"- Audio: ![[audio/day-{day_no:03d}.wav]]",
        "",
        "## 今日词表",
        "",
    ]
    for entry in entries:
        lines.extend(
            [
                f"- **{entry.word}**" + (f" /{entry.phonetic}/" if entry.phonetic else ""),
                f"  - 释义：{clean_meaning(entry.meaning)}",
                f"  - 助读：{entry.reading}" if entry.reading else "  - 助读：",
            ]
        )
    lines.extend(
        [
            "",
            "## 生活场景短文",
            "",
            story,
            "",
            "## 跟读稿",
            "",
            "\n".join(follow_lines),
            "",
            "## 复习勾选",
            "",
            "- [ ] Listen once without looking at the word list.",
            "- [ ] Read along once with the word list.",
            "- [ ] Cover the meanings and recall each word.",
            "- [ ] Retell today's scene in your own words.",
            "",
        ]
    )
    return "\n".join(lines)


def story_for_day(entries: list[VocabEntry], round_no: int, day_in_round: int) -> tuple[str, str, list[str]]:
    themes = [entry.theme for entry in entries]
    main_theme = max(set(themes), key=themes.count) if themes else "mixed"
    scene_name, opening = SCENE_CONFIGS.get(main_theme, SCENE_CONFIGS["mixed"])
    chunks = [entries[i : i + 4] for i in range(0, len(entries), 4)]
    sentences = [
        f"Today is round {round_no}, day {day_in_round}, and the scene is {scene_name}.",
        opening,
    ]
    templates = scene_sentence_templates(main_theme)
    for index, chunk in enumerate(chunks):
        template = templates[index % len(templates)]
        sentences.append(template.format(**chunk_entries(chunk)))
    sentences.append("Read the scene slowly, focus on meaning first, and then repeat the useful phrases.")
    story = " ".join(sentences)
    follow_lines = [
        f"Round {round_no}, day {day_in_round}. Listen to the scene first.",
        story,
        "Now repeat the key words in short chunks.",
    ]
    for chunk in chunks:
        follow_lines.append(". ".join(entry.word for entry in chunk) + ".")
    follow_lines.append("Now say one sentence about the scene in your own words.")
    return scene_name, story, follow_lines


def scene_sentence_templates(theme: str) -> list[str]:
    shared = [
        "The problem begins with {p1}, but {p2} quickly changes how everyone understands it, while {p3} stays in the background.",
        "In the middle of the scene, {p1} and {p2} become the two details people keep returning to, and {p3} makes the memory sharper.",
        "Someone mentions {p1}, then connects it with {p2}; after that, {p3} gives the scene a practical direction.",
        "By the time {p1} appears, {p2} is no longer just a word; with {p3}, it becomes part of the decision.",
    ]
    themed = {
        "work": ["In the meeting, {p1} shapes the agenda, while {p2} becomes the detail everyone has to explain."],
        "study": ["In class, {p1} appears in the lecture, and {p2} helps the student explain the idea aloud."],
        "tech": ["On the screen, {p1} causes confusion, but {p2} helps the workflow make sense again."],
        "travel": ["During the commute, {p1} appears in the announcement, and {p2} changes the plan for getting home."],
        "social": ["In the conversation, {p1} softens the mood, and {p2} gives the speaker a better way to respond."],
        "conflict": ["When the mood becomes tense, {p1} makes people pause, and {p2} becomes the safer way forward."],
        "home": ["At home, {p1} is part of the ordinary routine, and {p2} makes the memory easier to picture."],
        "health": ["In the clinic, {p1} describes the concern, and {p2} helps turn it into a practical next step."],
    }
    return themed.get(theme, []) + shared


def chunk_entries(entries: list[VocabEntry]) -> dict[str, str]:
    padded = entries + [entries[-1]] * (4 - len(entries))
    values: dict[str, str] = {}
    for index, entry in enumerate(padded[:4], start=1):
        values[f"p{index}"] = contextual_phrase(entry)
    return values


def contextual_phrase(entry: VocabEntry) -> str:
    word = entry.word
    if " " in word:
        return word
    lower = entry.meaning.lower().strip()
    first = re.split(r"[；;，,]", entry.meaning)[0]
    if lower.startswith("adj.") or first.endswith("的"):
        return f"{article_for(word)} {word} moment"
    if lower.startswith(("v.", "vi.", "vt.")):
        return f"to {word}"
    return f"{article_for(word)} {word}"


def article_for(word: str) -> str:
    return "an" if word[:1].lower() in {"a", "e", "i", "o", "u"} else "a"


def clean_meaning(meaning: str) -> str:
    meaning = re.sub(r"【名】.*", "", meaning)
    meaning = re.sub(r"\b(n|v|adj|adv|int|prep|conj|pron)\.\s*", "", meaning)
    return meaning.strip(" ；;") or "See vocabulary source"
