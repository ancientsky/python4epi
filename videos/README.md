# Tutorial Video Generation

Animated tutorial videos for each chapter's core Python concepts, using
**Manim** (animation) + **edge-tts** (Chinese narration) + **ffmpeg** (merge).

## Quick Start

```bash
# Install video dependencies (not needed for CI)
uv sync --group video
sudo apt install ffmpeg fonts-noto-cjk   # system deps (Linux)

# Build all videos (122 scripts x 2 languages, covering ch00–ch14)
uv run python videos/build.py --all --lang zh
uv run python videos/build.py --all --lang en

# Build one chapter, or one concept only
uv run python videos/build.py --chapter 08 --lang en
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

## Building in CI

The **Build Tutorial Videos** workflow renders **one video per job** rather than
looping through a chapter in a single job. Chapter 02 is what forced this: 13
videos and 190 narration segments, 65% more work than any other chapter, which
ran past the job timeout. Fanning out makes wall-clock time track the slowest
single video, and `fail-fast: false` means a broken render costs you that one
video instead of the whole chapter — re-run the failed job on its own.

The job matrix comes from `build.py --list`, which applies exactly the same
chapter/language/concept selection rules as a real build and prints the chosen
scripts as JSON:

```bash
uv run python videos/build.py --chapter ch02 --lang zh --list
# ["videos/scripts/ch02_01_dataframe.yaml", ...]
```

`--list` deliberately touches nothing but the standard library — the heavy
`manim` / `edge-tts` import is deferred until a build actually starts — so the
planning job skips installing the render stack. Paths are printed relative to
the repo root because CI feeds them to `hashFiles()`, which ignores absolute
paths.

Narration audio is cached between runs, keyed on the script file. Edit the
narration and that video's audio is re-synthesised; leave it alone and the
cached audio is reused. GitHub caps a workflow matrix at 256 jobs, so building
every chapter in both languages at once (244 videos) fits, but only just.

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

122 concepts span chapters 00–14, each with a Chinese script (`name.yaml`) and an
English one (`name_en.yaml`) driving the **same** Manim scene:

| Chapter | Videos | | Chapter | Videos |
|---------|-------:|-|---------|-------:|
| ch00 (導讀與工具) | 6 | | ch08 (空間流行病學) | 8 |
| ch01 (Python 基礎) | 6 | | ch09 (存活分析) | 8 |
| ch01b (開發者工具箱) | 8 | | ch10 (機器學習) | 8 |
| ch02 (資料處理與視覺化) | 13 | | ch11 (深度學習) | 8 |
| ch03 (描述統計與 2×2 表) | 7 | | ch12 (因果推論) | 7 |
| ch04 (群聚調查工作流) | 8 | | ch13 (可重現性) | 6 |
| ch05 (分層分析與干擾因子) | 8 | | ch14 (綜合案例) | 5 |
| ch06 (邏輯斯迴歸) | 8 | | | |
| ch07 (時間序列與預測) | 8 | | **Total** | **122** |

Chapters 15–17 (appendix, exercises, solutions) have no videos by design.

Scripts and scenes are paired by the `scene_module`/`scene_class` fields inside
each YAML's `meta:` block, not by filename — so a script's basename and its
scene file need not match exactly.

## Publishing to YouTube

`videos/youtube_ids.yaml` is the **single source of truth** for every video link
on the site. The build output filename *is* the registry key, so there is nothing
to look up:

| Built file | Registry key | Field |
|------------|--------------|-------|
| `ch08_04_morans_i.mp4` | `ch08_04_morans_i` | `zh:` |
| `ch08_04_morans_i_en.mp4` | `ch08_04_morans_i` | `en:` |

After uploading, paste either the full URL or the bare ID into the matching
entry. Both of these work:

```yaml
    zh: "https://youtu.be/dQw4w9WgXcQ"
    zh: "dQw4w9WgXcQ"
```

**Editing on github.com is enough — and nothing else has to happen.** The cards
are rendered from the registry *by the deploy itself*: `deploy-pages` runs
`sync_video_embeds.py` before building, so committing a link to
`videos/youtube_ids.yaml` on `main` triggers that deploy and the card is live a
few minutes later. Two smaller things run alongside it:

| Workflow | On a registry commit | Why |
|----------|----------------------|-----|
| `deploy-pages` | renders the cards, then builds and publishes | the actual update |
| `Check video links` | validates the registry in ~30 s | catches a mistyped link long before the build finishes |

There is deliberately **no bot commit** in this path. An earlier version of the
sync workflow pushed the regenerated embeds back to `main` and was rejected by
the branch ruleset (`GH013 … changes must be made through a pull request`).
Rendering at build time sidesteps that entirely: no write to `main` is needed,
so no bypass has to be granted to `github-actions[bot]`.

The flip side is that the embeds committed in the chapter markdown are a
**snapshot**, not the truth — they lag behind any link added from the web UI
until someone runs the sync in a checkout. The published site is never affected.
To refresh the snapshot (and `VIDEO_INDEX.md`) locally:

```bash
# regenerate the embeds in book/ and book_en/, plus VIDEO_INDEX.md
uv run python videos/sync_video_embeds.py
git commit -am "docs: add YouTube links for ch08" && git push
```

The sync is idempotent — safe to re-run any time. A video whose ID is still blank
renders **nothing**, so the site never shows a dead thumbnail; fill the ID in and
the card appears on the next build.

`videos/VIDEO_INDEX.md` is generated by the same command and gives the readable
chapter-by-chapter cross-reference of Chinese and English links with upload
progress. Never edit it by hand.

Two dry-run modes:

```bash
uv run python videos/sync_video_embeds.py --validate  # CI: registry is usable
uv run python videos/sync_video_embeds.py --check     # local: also fail if stale
```

`--validate` is what CI runs. It fails only on a registry the build could not
use — a marker key with no entry, or a link no YouTube ID can be read out of —
and merely *reports* staleness, because the deploy regenerates the embeds anyway.
`--check` is the stricter local version that also fails on a stale snapshot; CI
can't use it, since the snapshot on `main` is expected to lag and every unrelated
PR would fail. Both leave the working tree untouched, and a bad link aborts the
run before anything is written.

## Adding Videos for New Chapters

1. Create a YAML script in `scripts/` following the existing format
2. Create a Manim scene in `scenes/` inheriting from `EpiBaseScene`
3. Run `uv run python videos/build.py --script scripts/your_script.yaml`
