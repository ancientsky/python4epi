# Debug Video Build

When the user reports a video build failure from GitHub Actions (`videos.yml`), follow this systematic debugging checklist.

## Step 1: Identify the failing step

Ask the user which step failed, or parse from the error log:
- **Install system dependencies** → missing C libs (pangocairo, cairo, etc.)
- **Install Python dependencies** (`uv sync --group video`) → dependency build failure
- **Build videos** (`videos/build.py`) → TTS, Manim, or ffmpeg error
- **Create GitHub Release** → gh CLI / permissions issue

## Step 2: Common error patterns and fixes

### `ModuleNotFoundError: No module named 'videos'`
**Cause:** Manim runs scene files in a subprocess without the project root on PYTHONPATH.
**Fix:** Ensure `videos/src/pipeline.py` `_render_manim()` adds project root to `PYTHONPATH` in the `env` dict.

### `TypeError: Code.__init__() got an unexpected keyword argument 'code'` (or `font_size`, `style`)
**Cause:** Manim v0.20.1 completely rewrote the `Code` class API.
**Fix:** Use the v0.20.1 API:
```python
Code(
    code_string="...",           # NOT code="..."
    language="python",
    formatter_style="monokai",   # NOT style="monokai"
    background="rectangle",
    background_config={"stroke_color": X, "stroke_width": 1},  # NOT background_stroke_color=
    paragraph_config={"font_size": 20},  # NOT font_size=20
)
```

### `AttributeError: Code object has no attribute 'background_mobject'`
**Cause:** Renamed in v0.20.1.
**Fix:** Use `code_mob.background` instead of `code_mob.background_mobject`.

### `NameError: name 'ORIGIN' is not defined` (or other Manim constants)
**Cause:** Missing import in scene file.
**Fix:** Add `ORIGIN` (or the missing constant) to the `from manim import (...)` block in the scene file. Audit all 6 scene files at once.

### `TypeError: ... missing 1 required positional argument: 'segments'`
**Cause:** `construct_from_segments()` was called without args but the method required them.
**Fix:** Ensure `construct_from_segments(segments=None)` with default None, loading from `EPI_VIDEO_TIMING` env var when None.

### `TypeError: ... got an unexpected keyword argument 'title'` (CodePanel/VariableBox)
**Cause:** Scene files pass kwargs that the mobject class doesn't accept.
**Fix:** Add the missing kwargs to the class `__init__` in `videos/src/code_mobjects.py`. Audit all scene files for constructor call mismatches.

### `Package 'pangocairo' was not found` (manimpango build failure)
**Cause:** Missing system libraries for Pango/Cairo.
**Fix:** Add to `videos.yml` system dependencies:
```bash
sudo apt-get install -y -qq ffmpeg fonts-noto-cjk libpango1.0-dev libcairo2-dev pkg-config
```

### Node.js 20 deprecation warnings
**Fix:** Add `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` to job-level `env:` in ALL workflows.

## Step 3: Systematic audit approach

When fixing scene/mobject mismatches, always audit ALL 6 scene files at once:
```
videos/scenes/ch01_01_variables.py
videos/scenes/ch01_02_arithmetic.py
videos/scenes/ch01_03_dictionaries.py
videos/scenes/ch01_04_lists.py
videos/scenes/ch01_05_conditionals.py
videos/scenes/ch01_06_functions.py
```

Check for:
1. Missing Manim imports (ORIGIN, UL, UR, etc.)
2. Constructor kwargs that don't match class signatures in `code_mobjects.py`
3. Method calls that don't match signatures in `base_scene.py`

## Step 4: After fixing

1. Commit with descriptive message explaining the root cause
2. Push to the working branch
3. User merges PR, then manually triggers `videos.yml` via workflow_dispatch
4. Check the next error — video pipeline issues often cascade (fixing one reveals the next)

## Key files

| File | Purpose |
|------|---------|
| `videos/src/code_mobjects.py` | Custom Manim mobjects (CodePanel, VariableBox, etc.) |
| `videos/src/base_scene.py` | Base scene class with shared helpers |
| `videos/src/pipeline.py` | TTS → Manim → ffmpeg orchestrator |
| `videos/src/tts.py` | edge-tts wrapper |
| `videos/build.py` | CLI entry point |
| `videos/scripts/ch01_*.yaml` | YAML narration scripts |
| `videos/scenes/ch01_*.py` | Manim scene classes |
| `.github/workflows/videos.yml` | GitHub Actions workflow |

## Reference: Manim v0.20.1 Code API

```python
Code(
    code_file=None,              # path to file
    code_string=None,            # inline code string
    language=None,               # syntax highlighting language
    formatter_style="vim",       # pygments style name
    tab_width=4,
    add_line_numbers=True,
    line_numbers_from=1,
    background="rectangle",      # or "window"
    background_config=None,      # dict: stroke_color, stroke_width, fill_color, etc.
    paragraph_config=None,       # dict: font_size, font, line_spacing, etc.
)
# Access background: code_mob.background (NOT background_mobject)
# Access code lines: code_mob.code_lines
# Access line numbers: code_mob.line_numbers
```
