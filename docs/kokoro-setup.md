# Kokoro Setup

Kokoro audio generation is optional. The notes can be generated without TTS.

Install optional dependencies:

```bash
pip install -e ".[tts]"
```

Download model files separately:

```text
models/kokoro-v1.0.onnx
models/voices-v1.0.bin
```

Then run:

```bash
scene-repeat generate \
  --vocab ./examples/vocabulary_sample.md \
  --out ./review \
  --tts kokoro \
  --model ./models/kokoro-v1.0.onnx \
  --voices ./models/voices-v1.0.bin
```

The generated audio reads the follow-along script, not the Chinese definitions.
