# SceneRepeat Vocabulary

英语学习的本质是重复。

但很多人的重复是低效的：

1. 背的都是生僻词，平时生活中用不到。
2. 收藏了很多生活常用词，但收藏之后就再也不看，重复记忆没有发生。
3. 即使记住了单词，也不知道如何把它们组成句子，融入自己的生活；不会读，也不会用。

SceneRepeat Vocabulary solves these problems by turning your personal vocabulary list into a repeatable cycle of life-scene shadowing audio.

- Use the words you actually looked up, not somebody else's fixed word list.
- Split them into daily review notes, usually 20 words per day.
- Repeat the whole library for multiple rounds.
- Avoid plain word-list audio. Each day becomes a small life-scene paragraph.
- Generate local follow-along audio with Kokoro ONNX, no API key required.
- Within each round, every word appears once and only once; across rounds, words repeat deliberately.

## Why This Exists

Vocabulary apps often stop at collection. You save a word, feel productive, and never meet it again.

This project turns collection into a loop:

```text
personal words -> daily scene -> follow-along script -> local audio -> repeat -> retell
```

The goal is not just to remember a definition. The goal is to hear the word, say it, and place it inside a sentence you could imagine using.

## Features

- Markdown vocabulary input.
- Obsidian-friendly output.
- Scene-based daily review notes.
- Local Kokoro TTS audio generation.
- Configurable rounds and words per day.
- Round-level no-duplicate guarantee.
- No cloud API required.

## Install

```bash
pip install -e .
```

For local Kokoro TTS:

```bash
pip install -e ".[tts]"
```

Download Kokoro model files separately. They are not committed to this repository.

- `kokoro-v1.0.onnx`
- `voices-v1.0.bin`

See [docs/kokoro-setup.md](docs/kokoro-setup.md).

## Quick Start

Generate review notes without audio:

```bash
scene-repeat generate \
  --vocab ./examples/vocabulary_sample.md \
  --out ./review \
  --rounds 3 \
  --words-per-day 20
```

Generate review notes and Kokoro audio:

```bash
scene-repeat generate \
  --vocab ./examples/vocabulary_sample.md \
  --out ./review \
  --rounds 3 \
  --words-per-day 20 \
  --tts kokoro \
  --model ./models/kokoro-v1.0.onnx \
  --voices ./models/voices-v1.0.bin
```

## Vocabulary Format

```md
## archive /ˈɑːr.kaɪv/

- 释义：档案；归档
- 助记：archive 像把重要资料放进档案架。
- 助读：/ˈɑːr.kaɪv/；中文谐音：【啊克爱夫】；先按音标分段慢读。
- 来源：manual
```

## Output

Each day includes:

- today's word list
- a life-scene paragraph
- a follow-along script
- review checkboxes
- an optional local audio file

Example:

```text
review/
  README.md
  Day 001.md
  Day 002.md
  audio/
    day-001.wav
```

## Core Rule

Do not generate plain word-list audio.

Every review day should sound like a meaningful situation: office, commute, classroom, lab, home, shopping, travel, conversation, or another ordinary scene. The audio should help you repeat the words as language, not as isolated flashcards.

## License

MIT
