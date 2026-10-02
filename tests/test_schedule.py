from pathlib import Path

from scene_repeat.generate_days import generate_review


def test_generate_review_sample(tmp_path: Path) -> None:
    vocab = Path(__file__).resolve().parents[1] / "examples" / "vocabulary_sample.md"
    out = tmp_path / "review"
    notes = generate_review([vocab], out, rounds=2, words_per_day=4, seed=1)
    assert len(notes) == 4
    assert (out / "README.md").exists()
    first = (out / "Day 001.md").read_text(encoding="utf-8")
    assert "## 生活场景短文" in first
    assert "## 跟读稿" in first
    assert "## 今日词表" in first
