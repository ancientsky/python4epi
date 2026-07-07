"""Edge-TTS wrapper for generating narration audio clips.

Generates zh-TW Chinese narration using Microsoft Edge's free TTS service.
Each narration segment becomes a separate .mp3 file; durations are measured
via ffprobe so Manim animations can be timed to match.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import pathlib
import subprocess

import edge_tts

logger = logging.getLogger(__name__)

DEFAULT_VOICE = "zh-TW-HsiaoChenNeural"
DEFAULT_RATE = "-10%"


def _content_hash(text: str, voice: str, rate: str) -> str:
    """Stable hash of the inputs that determine a segment's audio.

    Used to invalidate the TTS cache when narration text (or voice/rate)
    changes — keying only on the segment id/filename would silently reuse
    stale audio after an edit.
    """
    payload = "|".join((text, voice, rate)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _hash_path(output_path: pathlib.Path) -> pathlib.Path:
    """Sidecar file that records the content hash of an audio segment."""
    return output_path.with_name(output_path.name + ".sha256")


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

async def _generate_one(
    text: str,
    output_path: pathlib.Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
) -> None:
    """Generate a single audio segment with edge-tts."""
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))


def get_audio_duration(path: pathlib.Path) -> float:
    """Return audio duration in seconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_segment_audio(
    text: str,
    output_path: pathlib.Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    *,
    force_cache: bool = False,
) -> float:
    """Generate audio for one narration segment and return its duration.

    Caching is content-aware: an existing audio file is reused only when its
    recorded content hash matches the current ``text``/``voice``/``rate``. If
    the narration changed, the stale audio is regenerated automatically.

    Parameters
    ----------
    text : str
        Chinese narration text.
    output_path : pathlib.Path
        Where to write the .mp3 file.
    voice : str
        edge-tts voice identifier.
    rate : str
        Speaking rate adjustment (e.g., ``"-10%"`` for slower).
    force_cache : bool
        If *True*, reuse any existing audio file regardless of its content
        hash (offline / animation-only iteration). A missing file is still
        generated.

    Returns
    -------
    float
        Duration of the generated audio in seconds.
    """
    want_hash = _content_hash(text, voice, rate)
    hash_path = _hash_path(output_path)

    if output_path.exists():
        if force_cache:
            logger.info("Cache hit (forced): %s", output_path.name)
            return get_audio_duration(output_path)
        cached_hash = hash_path.read_text().strip() if hash_path.exists() else None
        if cached_hash == want_hash:
            logger.info("Cache hit: %s", output_path.name)
            return get_audio_duration(output_path)
        logger.info("Narration changed, regenerating: %s", output_path.name)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_generate_one(text, output_path, voice=voice, rate=rate))
    hash_path.write_text(want_hash)
    duration = get_audio_duration(output_path)
    logger.info("Generated %s (%.1fs)", output_path.name, duration)
    return duration


def generate_all_segments(
    segments: list[dict],
    output_dir: pathlib.Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    *,
    force_cache: bool = False,
) -> list[dict]:
    """Generate TTS audio for all segments.

    Parameters
    ----------
    segments : list[dict]
        Segment dicts from a parsed YAML script.  Each must have ``id``
        and ``narration`` keys.
    output_dir : pathlib.Path
        Directory where per-segment .mp3 files are written.
    voice : str
        edge-tts voice identifier.
    rate : str
        Speaking rate adjustment.
    force_cache : bool
        Forwarded to :func:`generate_segment_audio` — reuse existing audio
        regardless of content hash.

    Returns
    -------
    list[dict]
        The same segment dicts enriched with ``audio_path`` and
        ``audio_duration`` keys.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    enriched: list[dict] = []
    for seg in segments:
        audio_path = output_dir / f"{seg['id']}.mp3"
        duration = generate_segment_audio(
            seg["narration"],
            audio_path,
            voice=voice,
            rate=rate,
            force_cache=force_cache,
        )
        enriched.append({**seg, "audio_path": audio_path, "audio_duration": duration})
    return enriched
