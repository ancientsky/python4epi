# Tutorial Video Generation

Animated tutorial videos for each chapter's core Python concepts, using
**Manim** (animation) + **edge-tts** (Chinese narration) + **ffmpeg** (merge).

## Quick Start

```bash
# Install video dependencies (not needed for CI)
uv sync --group video
sudo apt install ffmpeg fonts-noto-cjk   # system deps (Linux)

# Build all videos (currently 72, covering ch00–ch07)
uv run python videos/build.py --all

# Build one concept only
uv run python videos/build.py --concept variables

# Low-quality preview (fast render)
uv run python videos/build.py --concept variables --quality l

# Reuse existing audio regardless of narration changes (offline / animation-only
# iteration). Without this flag, TTS is content-hash cached: a segment is only
# re-synthesized when its narration text (or voice/rate) actually changes.
uv run python videos/build.py --all --skip-tts

# Preview Manim scene without audio (development)
uv run manim render -ql videos/scenes/ch01_01_variables.py Ch01VariablesScene
```

`--all` isolates failures: one video that fails (TTS hiccup, a render error)
is logged and skipped, the rest keep building, and a success/failure summary
prints at the end (non-zero exit if any failed).

## Pipeline

```
YAML 腳本 (narration + animation instructions)
    → edge-tts generates speech (.mp3, zh-TW-HsiaoChenNeural)
    → ffprobe measures per-segment audio duration
    → Manim renders animations synced to timing (silent .mp4)
    → ffmpeg merges video + audio → final .mp4
```

## Directory Structure

```
videos/
├── build.py              # CLI entry point
├── README.md             # This file
├── src/
│   ├── tts.py            # edge-tts wrapper
│   ├── base_scene.py     # Manim base scene (colours, layout, helpers)
│   ├── pipeline.py       # TTS → Manim → ffmpeg orchestrator
│   └── code_mobjects.py  # Custom mobjects (CodePanel, VariableBox, etc.)
├── scripts/              # YAML narration scripts (one per video)
├── scenes/               # Manim scene classes (one per video)
└── output/               # Generated artifacts (gitignored)
```

## Visual Style

Anthropic Skilljar Academy-inspired light theme:

- Warm white background (`#FAF8F3`)
- White rounded-corner cards with subtle border (`#E8E5DF`)
- Dark code blocks (`#2B2B2B`) for contrast
- Anthropic accent colours: Orange `#D97757`, Blue `#6A9BCC`, Green `#788C5D`
- Serif titles, Noto Sans CJK TC body text, monospace code

## Three-Part Video Structure

Every video follows:

1. **Main lesson** — core concept with the Legionella outbreak scenario
2. **Extra epi example** — same concept in a different public health context
3. **Beginner blind spots** — 3 common mistakes with NG/OK comparison

## Coverage

72 videos currently exist, one YAML script paired 1:1 with a Manim scene, spanning
chapters 00–07 (chapters 08–17 do not have videos yet):

| Chapter | Videos |
|---------|--------|
| ch00 (導讀與工具) | 6 |
| ch01 (Python 基礎) | 6 |
| ch01b (開發者工具箱) | 8 |
| ch02 (資料處理與視覺化) | 13 |
| ch03 (描述統計與 2×2 表) | 7 |
| ch04 (群聚調查工作流) | 8 |
| ch05 (分層分析與干擾因子) | 8 |
| ch06 (邏輯斯迴歸) | 8 |
| ch07 (時間序列與預測) | 8 |

Scripts and scenes are paired by the `scene_module`/`scene_class` fields inside
each YAML's `meta:` block, not by filename — so a script's basename and its
scene file need not match exactly.

## Adding Videos for New Chapters

1. Create a YAML script in `scripts/` following the existing format
2. Create a Manim scene in `scenes/` inheriting from `EpiBaseScene`
3. Run `uv run python videos/build.py --script scripts/your_script.yaml`
