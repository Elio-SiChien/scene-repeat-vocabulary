# Obsidian Workflow

SceneRepeat output is plain Markdown, so it works well inside an Obsidian vault.

Recommended layout:

```text
English/
  Vocabulary/
    A.md
    B.md
  Vocabulary Review/
    README.md
    Day 001.md
    audio/
      day-001.wav
```

Run:

```bash
scene-repeat generate --vocab English/Vocabulary/*.md --out "English/Vocabulary Review"
```

Open `Day 001.md`, listen to the linked audio, then check off the review tasks.
