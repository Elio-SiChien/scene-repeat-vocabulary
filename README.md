# SceneRepeat Vocabulary

> 英语不是收藏出来的，是重复出来的。  
> 最好的重复，不是盯着单词表硬背，而是在真实生活场景里反复听、读、复述、使用。

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Local TTS](https://img.shields.io/badge/TTS-Kokoro%20Local-orange)
![Obsidian Friendly](https://img.shields.io/badge/Obsidian-Friendly-7C3AED)

SceneRepeat Vocabulary 是一个面向中文英语学习者的开源工具。它把你查过但不会的单词，自动整理成每天 20 个词左右的生活场景短文，并用本地 Kokoro TTS 生成跟读音频。

English subtitle: turn your personal vocabulary list into scene-based repetition notes and local follow-along audio.

## 它解决什么问题

很多人不是不努力，而是重复方式太低效。

| 学习痛点 | 常见结果 | SceneRepeat 怎么解决 |
|---|---|---|
| 背的词太生僻 | 生活中用不上，很快忘 | 使用你自己查过、真正不会的词库 |
| 收藏后不再看 | 生词本变成仓库，没有重复 | 自动生成每日计划，完整循环多轮 |
| 会认不会用 | 不会造句，不会读，不敢说 | 生成生活场景短文和本地跟读音频 |
| 音频只是单词表 | 听起来枯燥，无法迁移 | 每天都是一段可复述的真实场景 |

## 学习闭环

```mermaid
flowchart LR
  A[你的生词本] --> B[按语义自由分组]
  B --> C[每日生活场景短文]
  C --> D[跟读稿]
  D --> E[Kokoro 本地音频]
  E --> F[听读复述]
  F --> G[3 轮循环重复]
  G --> B
```

核心不是“多收藏几个单词”，而是把单词变成每天都会重新遇见的声音和场景。

## 和传统背词有什么不同

| 传统方式 | SceneRepeat |
|---|---|
| 背别人给你的固定单词表 | 使用你自己查过的词 |
| 一个词一个中文释义 | 一个词进入一个生活场景 |
| 收藏后靠自觉复习 | 自动生成每日循环 |
| 音频只读单词 | 音频读场景、读句子、读跟读稿 |
| 记住了也不会说 | 每天听、读、复述，把词放回语言里 |

## 适合谁

- 中文英语学习者
- 有自己的生词本、查词记录、有道词典导出词库的人
- Obsidian 用户
- 想练英语跟读、听力和口语复述的人
- 不想把学习文本发给云端 API，希望本地生成音频的人

## 快速开始

安装项目：

```bash
pip install -e .
```

生成每日复习笔记，不生成音频：

```bash
scene-repeat generate \
  --vocab ./examples/vocabulary_sample.md \
  --out ./review \
  --rounds 3 \
  --words-per-day 20
```

如果你已经准备好 Kokoro 模型，也可以直接生成本地音频：

```bash
pip install -e ".[tts]"

scene-repeat generate \
  --vocab ./examples/vocabulary_sample.md \
  --out ./review \
  --rounds 3 \
  --words-per-day 20 \
  --tts kokoro \
  --model ./models/kokoro-v1.0.onnx \
  --voices ./models/voices-v1.0.bin
```

Kokoro 模型文件需要你自行下载，不会提交到 GitHub：

- `kokoro-v1.0.onnx`
- `voices-v1.0.bin`

配置说明见：[docs/kokoro-setup.md](docs/kokoro-setup.md)

## 输入格式

你可以用 Obsidian 风格的 Markdown 词条：

```md
## archive /ˈɑːr.kaɪv/

- 释义：档案；归档
- 助记：archive 像把重要资料放进档案架。
- 助读：/ˈɑːr.kaɪv/；中文谐音：【啊克爱夫】；先按音标分段慢读。
- 来源：manual
```

也可以只写最少信息：

```md
## commute /kəˈmjuːt/

- 释义：通勤；上下班路程
```

更多格式说明见：[docs/vocabulary-format.md](docs/vocabulary-format.md)

## 输出长什么样

生成结果是 Obsidian 友好的 Markdown：

```text
review/
  README.md
  Day 001.md
  Day 002.md
  audio/
    day-001.wav
```

每天一篇笔记，包含：

- 今日词表
- 生活场景短文
- 跟读稿
- 复习勾选
- 可选本地音频

示例文件：

- [examples/vocabulary_sample.md](examples/vocabulary_sample.md)
- [examples/Day 001.md](examples/Day%20001.md)
- [examples/audio_sample.wav](examples/audio_sample.wav)

## 一天的复习方式

建议每天 5-10 分钟：

1. 先听音频，不看词表。
2. 看 Day 笔记，跟读一遍。
3. 遮住中文释义，回忆每个词。
4. 用自己的话复述今天的场景。

重复不是机械刷次数，而是让同一个词在声音、句子、场景和表达里反复出现。

## 核心规则

> 不生成纯单词列表音频。

每一天都应该像一个可以想象的生活片段：办公室、通勤、课堂、实验室、家庭、超市、旅行、朋友聊天、项目汇报。音频要帮助你把词当作语言来重复，而不是当作孤立卡片来背。

## 文档

- [Obsidian 工作流](docs/obsidian-workflow.md)
- [Kokoro 本地 TTS 配置](docs/kokoro-setup.md)
- [词库格式](docs/vocabulary-format.md)

## 隐私与开源边界

这个仓库只包含通用代码、示例词库和示例音频。

不会提交：

- 你的私人 Obsidian vault
- 完整个人词库
- Kokoro 模型文件
- 批量生成的每日音频
- `.venv/` 虚拟环境

## License

MIT
