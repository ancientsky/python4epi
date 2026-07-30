"""Regenerate the YouTube video cards embedded in the chapter markdown files.

``videos/youtube_ids.yaml`` is the single source of truth for every tutorial
video link. This script reads it and rewrites the embed blocks in both language
trees -- ``book/chapters`` gets the Chinese IDs, ``book_en/chapters`` gets the
English ones.

Each embed site in a chapter is delimited by a pair of HTML comments::

    <!-- video: ch07_01_ts_basics -->
    ```{raw} html
    ...generated card...
    ```
    <!-- /video -->

Only the text *between* the markers is regenerated, so the script is idempotent
and safe to re-run: fill in an ID, run it again, and that card appears. A video
whose ID is still blank renders nothing at all -- the markers stay behind as an
invisible placeholder, so no dead thumbnail is ever published.

The deploy workflow runs this script before building, so the published site
always matches the registry even when the checked-in markdown lags behind it.

Usage::

    uv run python videos/sync_video_embeds.py             # rewrite in place
    uv run python videos/sync_video_embeds.py --validate  # CI: registry sanity
    uv run python videos/sync_video_embeds.py --check     # local: fail if stale
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "videos/youtube_ids.yaml"
INDEX_MD = ROOT / "videos/VIDEO_INDEX.md"

#: Chapter key -> chapter markdown basename (shared by both language trees).
CHAPTER_MD: dict[str, str] = {
    "ch00": "00_guide",
    "ch01": "01_fundamentals",
    "ch01b": "01b_python_toolbox",
    "ch02": "02_data_wrangling",
    "ch03": "03_stats",
    "ch04": "04_outbreak_workflow",
    "ch05": "05_stratified",
    "ch06": "06_logistic_regression",
    "ch07": "07_time_series",
    "ch08": "08_spatial",
    "ch09": "09_survival",
    "ch10": "10_machine_learning",
    "ch11": "11_deep_learning",
    "ch12": "12_causal",
    "ch13": "13_reproducibility",
    "ch14": "14_case_studies",
}

#: Per-language rendering strings and the tree each language lives in.
LANGS: dict[str, dict[str, str]] = {
    "zh": {"tree": "book", "prefix": "教學影片：", "alt": "教學影片", "title": "title_zh"},
    "en": {"tree": "book_en", "prefix": "Tutorial video: ", "alt": "Tutorial video", "title": "title_en"},
}

MARKER_RX = re.compile(r"<!-- video: (?P<key>[A-Za-z0-9_]+) -->.*?<!-- /video -->", re.DOTALL)

_ID_RX = re.compile(r"^[A-Za-z0-9_-]{11}$")
_URL_RX = re.compile(
    r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/)([A-Za-z0-9_-]{11})"
)


def normalise_id(raw: str, *, where: str) -> str:
    """Accept a bare YouTube ID or any common YouTube URL and return the ID.

    Parameters
    ----------
    raw:
        The value as written in the registry. An empty string means "not
        uploaded yet" and is passed through unchanged.
    where:
        Human-readable location used in error messages.

    Returns
    -------
    str
        The 11-character video ID, or ``""`` when *raw* is blank.

    Raises
    ------
    ValueError
        If *raw* is neither blank, a bare ID, nor a recognisable YouTube URL.
    """
    raw = (raw or "").strip()
    if not raw:
        return ""
    if _ID_RX.match(raw):
        return raw
    match = _URL_RX.search(raw)
    if match:
        return match.group(1)
    raise ValueError(
        f"{where}: cannot read a YouTube ID from {raw!r}. "
        "Paste the full watch/youtu.be URL or the bare 11-character ID."
    )


def render_card(video_id: str, title: str, lang: str) -> str:
    """Build the raw-HTML embed block for one video, or ``""`` when unreleased."""
    if not video_id:
        return ""
    cfg = LANGS[lang]
    return (
        "```{raw} html\n"
        '<div class="video-card">\n'
        f'  <div class="video-title">{cfg["prefix"]}{title}</div>\n'
        f'  <div class="youtube-lite" data-id="{video_id}">\n'
        f'    <img src="https://img.youtube.com/vi/{video_id}/hqdefault.jpg" '
        f'loading="lazy" alt="{cfg["alt"]}">\n'
        "  </div>\n"
        "</div>\n"
        "```"
    )


def sync_chapter(path: pathlib.Path, videos: dict[str, dict[str, str]], lang: str) -> tuple[str, int, int]:
    """Regenerate every marked embed site in one chapter file.

    Returns
    -------
    tuple[str, int, int]
        The new file text, the number of markers found, and the number that
        rendered a real card.
    """
    text = path.read_text(encoding="utf-8")
    found = shown = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal found, shown
        key = match.group("key")
        found += 1
        if key not in videos:
            raise KeyError(f"{path}: marker '{key}' has no entry in {REGISTRY.name}")
        entry = videos[key]
        video_id = normalise_id(entry.get(lang, ""), where=f"{key}.{lang}")
        title = entry.get(LANGS[lang]["title"]) or key
        card = render_card(video_id, title, lang)
        shown += bool(card)
        body = f"\n{card}\n" if card else "\n"
        return f"<!-- video: {key} -->{body}<!-- /video -->"

    return MARKER_RX.sub(repl, text), found, shown


def build_index(videos: dict[str, dict[str, str]]) -> str:
    """Render the human-readable chapter/video/link cross-reference table."""
    by_chapter: dict[str, list[str]] = {}
    for key in videos:
        match = re.match(r"^(ch\d+b?)_", key)
        if match:
            by_chapter.setdefault(match.group(1), []).append(key)

    zh_done = sum(1 for v in videos.values() if v.get("zh"))
    en_done = sum(1 for v in videos.values() if v.get("en"))
    total = len(videos)

    lines = [
        "# 影片連結對照表 / Video Link Index",
        "",
        "<!-- 這個檔案由 videos/sync_video_embeds.py 自動產生，請勿手動編輯。 -->",
        "<!-- Auto-generated by videos/sync_video_embeds.py — do not edit by hand. -->",
        "",
        "要新增或修改連結，請編輯 **`videos/youtube_ids.yaml`**，然後執行：",
        "",
        "```bash",
        "uv run python videos/sync_video_embeds.py",
        "```",
        "",
        "## 進度總覽",
        "",
        "| 語言 | 已上傳 | 總數 | 進度 |",
        "|------|-------:|-----:|------|",
        f"| 中文 | {zh_done} | {total} | {zh_done * 100 // total}% |",
        f"| English | {en_done} | {total} | {en_done * 100 // total}% |",
        "",
        "圖例：✅ 已上線　⬜ 尚未上傳（網站上不會顯示該卡片）",
        "",
    ]

    for chapter, keys in by_chapter.items():
        num = chapter[2:]
        c_zh = sum(1 for k in keys if videos[k].get("zh"))
        c_en = sum(1 for k in keys if videos[k].get("en"))
        lines += [
            f"## 第 {num} 章 · `{CHAPTER_MD.get(chapter, '?')}.md`"
            f"　（中 {c_zh}/{len(keys)}　英 {c_en}/{len(keys)}）",
            "",
            "| # | 影片 key（= mp4 檔名） | 標題 | 中文 | English |",
            "|---|------------------------|------|------|---------|",
        ]
        for idx, key in enumerate(sorted(keys), start=1):
            entry = videos[key]
            zid, eid = entry.get("zh", ""), entry.get("en", "")
            zcell = f"✅ [{zid}](https://youtu.be/{zid})" if zid else "⬜"
            ecell = f"✅ [{eid}](https://youtu.be/{eid})" if eid else "⬜"
            lines.append(f"| {idx} | `{key}` | {entry.get('title_zh', '')} | {zcell} | {ecell} |")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Do not write; exit non-zero if any file is out of date.",
    )
    mode.add_argument(
        "--validate",
        action="store_true",
        help=(
            "Do not write; fail only on a broken registry (unknown marker key, "
            "unparseable YouTube ID). Staleness is reported but tolerated, "
            "because the deploy regenerates the embeds anyway."
        ),
    )
    args = parser.parse_args()
    dry_run = args.check or args.validate

    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    videos: dict[str, dict[str, str]] = registry["videos"]

    stale: list[str] = []
    totals: dict[str, tuple[int, int]] = {}
    pending: list[tuple[pathlib.Path, str]] = []

    # Render everything before writing anything. A mistyped link in the registry
    # then stops the run with one readable line -- rather than a traceback raised
    # halfway through, with some chapters already rewritten and others not.
    try:
        for lang, cfg in LANGS.items():
            found = shown = 0
            for chapter, basename in CHAPTER_MD.items():
                path = ROOT / cfg["tree"] / "chapters" / f"{basename}.md"
                if not path.exists():
                    continue
                new_text, f_n, s_n = sync_chapter(path, videos, lang)
                found += f_n
                shown += s_n
                if new_text != path.read_text(encoding="utf-8"):
                    stale.append(str(path.relative_to(ROOT)))
                    pending.append((path, new_text))
            totals[lang] = (shown, found)
    except (KeyError, ValueError) as exc:
        detail = exc.args[0] if exc.args else exc
        sys.exit(f"登錄表有誤 / registry error: {detail}")

    index_text = build_index(videos)
    if not INDEX_MD.exists() or INDEX_MD.read_text(encoding="utf-8") != index_text:
        stale.append(str(INDEX_MD.relative_to(ROOT)))
        pending.append((INDEX_MD, index_text))

    if not dry_run:
        for path, text in pending:
            path.write_text(text, encoding="utf-8")

    for lang, (shown, found) in totals.items():
        print(f"  {lang}: {shown}/{found} 個影片位有連結，已產生卡片")

    if args.validate:
        # Getting this far means every marker resolved and every ID parsed.
        # Staleness is informational only: deploy-pages re-renders the embeds
        # from the registry, so a committed snapshot lagging behind is expected
        # whenever a link is added straight from the GitHub web UI.
        print("\n登錄表格式正確，所有影片位都對得上。")
        if stale:
            print(f"（{len(stale)} 個產生檔與登錄表不同步，部署時會重新產生。）")
        return

    if args.check:
        if stale:
            print(f"\n以下檔案與 {REGISTRY.name} 不同步：", file=sys.stderr)
            for name in stale:
                print(f"  {name}", file=sys.stderr)
            print("\n請執行 uv run python videos/sync_video_embeds.py", file=sys.stderr)
            sys.exit(1)
        print("\n所有檔案都與登錄表同步。")
    else:
        print(f"\n更新了 {len(stale)} 個檔案。" if stale else "\n沒有需要更新的檔案。")


if __name__ == "__main__":
    main()
