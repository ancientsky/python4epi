"""Video generation pipeline: YAML script → TTS → Manim → ffmpeg merge.

Orchestrates the full build process for a single tutorial video:

1. Parse YAML narration script.
2. Generate TTS audio for each segment (edge-tts).
3. Concatenate audio segments into one track (ffmpeg).
4. Write timing data so Manim can sync animations.
5. Render Manim scene (silent video).
6. Merge video + audio into the final .mp4 (ffmpeg).
"""

from __future__ import annotations

import json
import logging
import os
import pathlib
import subprocess
import tempfile

import yaml

from videos.src.tts import generate_all_segments

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_video(
    script_path: pathlib.Path,
    output_dir: pathlib.Path,
    *,
    quality: str = "h",
    skip_tts: bool = False,
) -> pathlib.Path:
    """Build a complete video from a YAML narration script.

    Parameters
    ----------
    script_path : pathlib.Path
        Path to the YAML narration script.
    output_dir : pathlib.Path
        Root output directory (``videos/output/``).
    quality : str
        Manim quality flag — ``"l"`` (480p), ``"m"`` (720p), ``"h"`` (1080p).
    skip_tts : bool
        If *True*, reuse cached audio files (skip TTS generation).

    Returns
    -------
    pathlib.Path
        Path to the final merged .mp4 file.
    """
    script = yaml.safe_load(script_path.read_text(encoding="utf-8"))
    meta = script["meta"]
    segments = script["segments"]

    concept = meta["concept"]
    chapter = meta["chapter"]
    voice = meta.get("voice", "zh-TW-HsiaoChenNeural")
    rate = meta.get("rate", "-10%")
    scene_module = meta["scene_module"]
    scene_class = meta["scene_class"]

    audio_dir = output_dir / "audio" / f"ch{chapter}_{concept}"
    raw_video_dir = output_dir / "raw_video"
    final_dir = output_dir / "final"

    # ------------------------------------------------------------------
    # Step 1: Generate TTS audio per segment
    # ------------------------------------------------------------------
    logger.info("Step 1/4  Generating TTS audio …")
    enriched = generate_all_segments(
        segments,
        audio_dir,
        voice=voice,
        rate=rate,
        force_cache=skip_tts,
    )

    # ------------------------------------------------------------------
    # Step 2: Concatenate audio segments
    # ------------------------------------------------------------------
    logger.info("Step 2/4  Concatenating audio …")
    combined_audio = audio_dir / "combined.mp3"
    _concat_audio(enriched, combined_audio)

    # ------------------------------------------------------------------
    # Step 3: Write timing data and render Manim
    # ------------------------------------------------------------------
    logger.info("Step 3/4  Rendering Manim scene …")
    timing_path = audio_dir / "timing.json"
    _write_timing(enriched, timing_path)

    raw_video = _render_manim(
        scene_module,
        scene_class,
        timing_path,
        raw_video_dir,
        quality=quality,
    )

    # ------------------------------------------------------------------
    # Step 4: Merge video + audio
    # ------------------------------------------------------------------
    logger.info("Step 4/4  Merging video + audio …")
    final_dir.mkdir(parents=True, exist_ok=True)
    final_path = final_dir / f"ch{chapter}_{concept}.mp4"
    _merge_audio_video(raw_video, combined_audio, final_path)

    logger.info("Done → %s", final_path)
    return final_path


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _concat_audio(segments: list[dict], output: pathlib.Path) -> None:
    """Concatenate segment audio files with silence padding via ffmpeg."""
    output.parent.mkdir(parents=True, exist_ok=True)

    # Build ffmpeg concat list
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8",
    ) as f:
        for seg in segments:
            f.write(f"file '{seg['audio_path']}'\n")
            pause = seg.get("pause_after", 0)
            if pause and pause > 0:
                # Generate a silence file for the pause
                silence_path = seg["audio_path"].parent / f"_silence_{seg['id']}.mp3"
                subprocess.run(
                    [
                        "ffmpeg", "-y",
                        "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", str(pause),
                        "-c:a", "libmp3lame",
                        str(silence_path),
                    ],
                    capture_output=True,
                    check=True,
                )
                f.write(f"file '{silence_path}'\n")
        concat_list = f.name

    # Always clean up the temp concat list, even if ffmpeg fails.
    try:
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_list,
                "-c", "copy",
                str(output),
            ],
            capture_output=True,
            check=True,
        )
    finally:
        try:
            os.unlink(concat_list)
        except OSError:
            pass


def _write_timing(segments: list[dict], path: pathlib.Path) -> None:
    """Write segment timing data as JSON for Manim scenes to read."""
    timing = []
    for seg in segments:
        entry: dict = {
            "id": seg["id"],
            "animation": seg["animation"],
            "audio_duration": seg["audio_duration"],
            "pause_after": seg.get("pause_after", 0),
            "total_duration": seg["audio_duration"] + seg.get("pause_after", 0),
        }
        # Forward extra keys (code, output, error_code, correct_code, etc.)
        for k, v in seg.items():
            if k not in {
                "id", "animation", "narration", "audio_duration",
                "pause_after", "audio_path", "total_duration",
            }:
                entry[k] = v
        timing.append(entry)
    path.write_text(json.dumps(timing, indent=2, ensure_ascii=False), encoding="utf-8")


def _render_manim(
    module: str,
    scene_class: str,
    timing_path: pathlib.Path,
    output_dir: pathlib.Path,
    *,
    quality: str = "h",
) -> pathlib.Path:
    """Invoke manim CLI to render a scene with timing data."""
    output_dir.mkdir(parents=True, exist_ok=True)
    project_root = str(pathlib.Path(__file__).resolve().parent.parent.parent)
    pythonpath = os.environ.get("PYTHONPATH", "")
    if project_root not in pythonpath.split(os.pathsep):
        pythonpath = project_root + (os.pathsep + pythonpath if pythonpath else "")
    env = {**os.environ, "EPI_VIDEO_TIMING": str(timing_path), "PYTHONPATH": pythonpath}

    module_path = module.replace(".", "/") + ".py"
    # Resolve against the project root (not the current working directory) so
    # the build works regardless of where it is invoked from.
    scene_file = pathlib.Path(project_root) / "videos" / module_path

    subprocess.run(
        [
            "manim", "render",
            f"-q{quality}",
            "--media_dir", str(output_dir),
            str(scene_file),
            scene_class,
        ],
        env=env,
        check=True,
    )

    # Manim writes to media_dir/videos/<filename>/<quality>/...
    # Find the rendered file
    for mp4 in output_dir.rglob(f"{scene_class}.mp4"):
        return mp4

    raise FileNotFoundError(
        f"Manim did not produce {scene_class}.mp4 in {output_dir}"
    )


def _merge_audio_video(
    video: pathlib.Path,
    audio: pathlib.Path,
    output: pathlib.Path,
) -> None:
    """Merge silent Manim video with TTS audio using ffmpeg."""
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(video),
            "-i", str(audio),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output),
        ],
        check=True,
    )
