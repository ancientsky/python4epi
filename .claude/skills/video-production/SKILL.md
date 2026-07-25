---
name: video-production
description: House visual style and build pipeline for this repo's tutorial videos and hand-crafted SVG diagrams — the Anthropic-Skilljar colour palette, SVG diagram conventions, the Manim + edge-TTS + FFMPEG pipeline, YAML narration script format, custom Manim mobjects, and the Manim v0.20.1 breaking-change/crash workarounds. Use when creating or editing anything under videos/ (scenes, scripts, build.py), when authoring or modifying SVG diagrams in book/chapters/images/, or when touching the youtube-lite CSS in book/_static/.
---

# Tutorial video & diagram production

The project generates animated tutorial videos under `videos/` (one per core concept,
every chapter sharing one visual style and pipeline). Run `ls videos/` for the current
layout. This palette is shared across **all** visual assets: Manim videos, the SVG
diagrams in `book/chapters/images/`, and the `youtube-lite` CSS in `book/_static/`.

### Video Pipeline
```
YAML 腳本 (narration + animation 指令)
    → edge-tts 產生語音 (.mp3, zh-TW-HsiaoChenNeural 女聲)
    → ffprobe 量測各段音檔時長
    → Manim 依時長渲染動畫 (silent .mp4)
    → ffmpeg 合併 video + audio → 最終 .mp4
```


### Visual Style (Anthropic Skilljar Academy-inspired)

All videos MUST follow this visual style consistently across all chapters:

**Color palette (light theme, warm white background):**
```python
BG_WARM = "#FAF8F3"          # Page background (warm white)
BG_CARD = "#FFFFFF"          # Card background (white)
BG_CARD_ALT = "#F5F3EE"     # Alternate card background (light warm gray)
ACCENT_ORANGE = "#D97757"    # Primary accent (Anthropic Orange)
ACCENT_BLUE = "#6A9BCC"      # Secondary accent (Anthropic Blue)
ACCENT_GREEN = "#788C5D"     # Success/correct (Anthropic Green)
TEXT_PRIMARY = "#1A1A1A"     # Primary text (dark)
TEXT_SECONDARY = "#6B6B6B"   # Secondary text (gray)
ERROR_RED = "#D94452"        # Error highlight
CODE_BG = "#2B2B2B"          # Code block background (dark for contrast)
CODE_TEXT = "#F8F8F2"        # Code text (light)
BORDER_LIGHT = "#E8E5DF"    # Card border (light gray)
```

> **Note:** This color palette is shared across **all visual assets**: Manim videos, SVG diagrams (in `book/chapters/images/`), and the `youtube-lite` CSS (`book/_static/`). When creating or modifying any visual element, always use these colors for consistency.


### SVG Diagram Style Guide

All hand-crafted SVG diagrams in `book/chapters/images/` follow these conventions:

- **Background**: `fill="#FAF8F3"` warm white with `rx="12"` rounded corners
- **Cards**: `fill="#FFFFFF"` white with `stroke="#E8E5DF"` border and drop shadow filter
- **Color usage**: `#D97757` for emphasis/disease/exposed, `#6A9BCC` for secondary/healthy/unexposed, `#788C5D` for success/CI/merge, `#D94452` for errors/warnings
- **Text**: `#1A1A1A` primary, `#6B6B6B` secondary, system-ui font stack
- **Structure**: `<svg xmlns="..." viewBox="0 0 W H" font-family="system-ui, -apple-system, sans-serif">`
- **Shadow filter**: `<filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="3" flood-opacity="0.1"/></filter>`
- **Labels**: Chinese prose for descriptions, English for technical terms (e.g., "暴露 Exposed")
- **Figure directive**: `{figure} images/filename.svg` with `:name:`, `:alt:`, `:width: 100%`
- **Self-contained**: no external fonts or assets; rely on system fonts

**Design principles:**
- Light warm-white background (#FAF8F3), clean and minimal
- Motion graphics style — no talking head, all animated
- White rounded-corner cards with subtle border (#E8E5DF)
- Code blocks use dark background (#2B2B2B) for contrast against the light page
- Serif font for titles (elegant feel), Noto Sans CJK TC for Chinese body text, monospace for code
- Step-by-step reveal: code appears line by line (typewriter animation) synced with narration
- Key terms highlighted with ACCENT_ORANGE (#D97757)
- Smooth FadeIn/FadeOut transitions between segments
- Step indicator (n/N) in top-right corner

**Layout template:**
```
┌──────────────────────────────────────┐
│  [Title]                   [Step n/N] │
│                                      │
│  ┌─────────────┐  ┌──────────────┐  │
│  │  Code Panel  │  │  Visuals     │  │
│  │  (dark bg)   │  │  (boxes,     │  │
│  │             │  │   diagrams)  │  │
│  └─────────────┘  └──────────────┘  │
│                                      │
│  ┌──────────────────────────────┐   │
│  │  Output Panel                │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
```


### Three-Part Video Structure

Every video follows this structure:
1. **Main lesson** — core concept taught with the Legionella outbreak scenario
2. **Extra epi example** — same concept applied to a different outbreak/public health scenario (e.g., COVID-19, dengue, enterovirus, TB, vaccination coverage)
3. **Beginner blind spots** — 3 common mistakes per video, shown with "wrong vs correct" side-by-side animation (red error panel vs green correct panel)


### Teaching Style
- Narration in Traditional Chinese (zh-TW-HsiaoChenNeural female voice)
- Humorous, relaxed, friend-like teaching tone — use metaphors, everyday examples, occasional jokes
- Speaking rate slightly slower than default (`-10%`) for beginners
- Code and variable names remain in English; only prose narration is in Chinese


### Video Build Commands
```bash
uv sync --group video                    # Install video dependencies (not in CI)
uv run python videos/build.py --all      # Build all videos
uv run python videos/build.py --concept variables  # Build one video
uv run manim render -ql videos/scenes/ch01_01_variables.py Ch01VariablesScene  # Preview
```


### Video Dependencies
Managed in a separate `video` dependency group in `pyproject.toml`:
- `manim>=0.18.0` (animation engine)
- `edge-tts>=6.1.0` (Microsoft Edge TTS, free zh-TW voices)
- `pyyaml>=6.0` (YAML script parsing)
- System deps: `ffmpeg`, `fonts-noto-cjk`

Video generation is **NOT** part of CI — it requires network access (TTS) and heavy system dependencies.


### YAML Script Format
Each video is driven by a YAML file pairing narration text with animation methods:
```yaml
meta:
  chapter: "01"
  concept: "variables"
  title: "數值變數——先把數字存起來"
  voice: "zh-TW-HsiaoChenNeural"
  scene_module: "scenes.ch01_01_variables"
  scene_class: "Ch01VariablesScene"

segments:
  - id: "intro"
    narration: "嗨！歡迎來到 Python 流行病學教室！..."
    animation: "show_title"
    pause_after: 0.5
  - id: "first_variable"
    narration: "看看這行程式碼..."
    animation: "show_variable_assignment"
    code: "total_residents = 280"
```


### Custom Manim Mobjects
- `VariableBox` — labeled box + value display (the "box" metaphor)
- `CodePanel` — syntax-highlighted code block with line highlighting
- `OutputPanel` — terminal-style output display
- `ArrowAssignment` — animated arrow showing value → box assignment
- `ErrorVsCorrect` — side-by-side NG/OK comparison panel using `Text(font=FONT_MONO)` on dark background (**NOT** `Code()` — see known issue below)
- `BlindSpotBanner` / `ExtraExampleBanner` — section title banners


## Manim v0.20.1 API Compatibility (Known Breaking Changes)

The video system uses Manim Community **v0.20.1**, which introduced major breaking changes from older tutorials/docs. When writing or modifying `Code()` calls, use the v0.20.1 API:

### Code class (`manim.mobject.text.code_mobject.Code`)

**Constructor signature (v0.20.1):**
```python
Code(
    code_file: StrPath | None = None,
    code_string: str | None = None,
    language: str | None = None,
    formatter_style: str = "vim",        # was: style
    tab_width: int = 4,
    add_line_numbers: bool = True,
    line_numbers_from: int = 1,
    background: Literal["rectangle", "window"] = "rectangle",
    background_config: dict | None = None,   # was: background_stroke_color, etc.
    paragraph_config: dict | None = None,    # was: font_size
)
```

**Migration table:**

| Old API (pre-0.20) | v0.20.1 API |
|---------------------|-------------|
| `Code(code="...")` | `Code(code_string="...")` |
| `font_size=20` | `paragraph_config={"font_size": 20}` |
| `style="monokai"` | `formatter_style="monokai"` |
| `background_stroke_color=X` | `background_config={"stroke_color": X}` |
| `background_stroke_width=1` | `background_config={"stroke_width": 1}` |
| `code_mob.background_mobject` | `code_mob.background` |

### Code() class `_gen_chars()` crash (IndexError: list index out of range)

Manim v0.20.1's `Code()` class has a bug in `Text._gen_chars()` where the rendered glyph count from Pango/Cairo doesn't match the expected character count. This crashes with `IndexError: list index out of range` for:
- Strings with `???`, `...`, or other special character sequences
- Multi-line code strings with CJK characters
- Non-Python code strings (shell commands like `git add .`, `pip install`, `command not found: uv`)
- Even `language="text"` doesn't fix it — the bug is in the text rendering layer, not Pygments

**Critical rule:** `ErrorVsCorrect` uses `Text(font=FONT_MONO)` instead of `Code()`. Do **NOT** reintroduce `Code()` in `ErrorVsCorrect.__init__()`. If you need syntax-highlighted code in comparison panels, use `CodePanel` (which handles the `Code()` lifecycle differently).

**For blindspot `error_code`/`correct_code` strings:** keep them single-line, ASCII-only, valid-looking (no `???`, no CJK characters, no multi-line `\n`). The Chinese explanation is delivered through TTS narration, not the code text.

### System dependencies for CI

Manim's `manimpango` requires C libraries to build from source. The `videos.yml` workflow installs:
```
ffmpeg fonts-noto-cjk libpango1.0-dev libcairo2-dev pkg-config
```

### PYTHONPATH for Manim subprocess

Manim runs scene files in a subprocess. The pipeline (`videos/src/pipeline.py`) automatically adds the project root to `PYTHONPATH` so `from videos.src.base_scene import EpiBaseScene` resolves correctly.

### GitHub Actions Node.js 24 migration

All workflows use `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` because `actions/checkout@v4`, `astral-sh/setup-uv@v5`, etc. internally run on Node.js 20 which is deprecated. The env var forces them to use Node.js 24.
