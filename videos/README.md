# Tutorial Video Generation

Animated tutorial videos for each chapter's core Python concepts, using
**Manim** (animation) + **edge-tts** (Chinese narration) + **ffmpeg** (merge).

## Quick Start

```bash
# Install video dependencies (not needed for CI)
uv sync --group video
sudo apt install ffmpeg fonts-noto-cjk   # system deps (Linux)

# Build all Chapter 01 videos
uv run python videos/build.py --all

# Build one concept only
uv run python videos/build.py --concept variables

# Low-quality preview (fast render)
uv run python videos/build.py --concept variables --quality l

# Preview Manim scene without audio (development)
uv run manim render -ql videos/scenes/ch01_01_variables.py Ch01VariablesScene
```

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

## Chapter 01 Videos

| # | Concept | File |
|---|---------|------|
| 1 | 數值變數 | `ch01_01_variables` |
| 2 | 計算指標 | `ch01_02_arithmetic` |
| 3 | 字典 | `ch01_03_dictionaries` |
| 4 | 列表 | `ch01_04_lists` |
| 5 | 條件判斷 | `ch01_05_conditionals` |
| 6 | 函式 | `ch01_06_functions` |

## Adding Videos for New Chapters

1. Create a YAML script in `scripts/` following the existing format
2. Create a Manim scene in `scenes/` inheriting from `EpiBaseScene`
3. Run `uv run python videos/build.py --script scripts/your_script.yaml`
