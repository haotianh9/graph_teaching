from __future__ import annotations

import argparse
from pathlib import Path

from .common import ffprobe_streams, load_config
from .human_audio import build_human_audio_final
from .mux import mux_chinese_audio
from .public_assets import build_public_assets
from .render import render_scenes
from .tts import generate_chinese_audio


def build_all(
    video_dir: Path,
    *,
    skip_render: bool = False,
    skip_tts: bool = False,
    skip_tts_mux: bool = False,
    skip_public_assets: bool = False,
    skip_human_audio: bool = False,
    fail_if_missing_human_audio: bool = False,
) -> list[Path]:
    """Build the standard review package for one teaching video folder."""
    config = load_config(video_dir)
    outputs: list[Path] = []

    if not skip_render:
        render_scenes(video_dir)

    if not skip_tts:
        generate_chinese_audio(video_dir)

    if not skip_tts_mux:
        outputs.append(mux_chinese_audio(video_dir))

    if not skip_public_assets:
        outputs.extend(build_public_assets(video_dir))

    if not skip_human_audio:
        human_output = build_human_audio_final(
            video_dir,
            fail_if_missing=fail_if_missing_human_audio,
        )
        if human_output is not None:
            outputs.append(human_output)

    print("\nBuild outputs:", flush=True)
    for output in outputs:
        print(f"- {output.relative_to(video_dir)}", flush=True)
        if output.suffix.lower() == ".mp4":
            print(ffprobe_streams(output), flush=True)

    print(f"Finished {getattr(config, 'VIDEO_ID', video_dir.name)}.", flush=True)
    return outputs


def main(video_dir: Path | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build one video folder using the shared Network Science pipeline.")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--skip-tts", action="store_true")
    parser.add_argument("--skip-tts-mux", action="store_true")
    parser.add_argument("--skip-public-assets", action="store_true")
    parser.add_argument("--skip-human-audio", action="store_true")
    parser.add_argument("--fail-if-missing-human-audio", action="store_true")
    args = parser.parse_args()

    build_all(
        video_dir or Path.cwd(),
        skip_render=args.skip_render,
        skip_tts=args.skip_tts,
        skip_tts_mux=args.skip_tts_mux,
        skip_public_assets=args.skip_public_assets,
        skip_human_audio=args.skip_human_audio,
        fail_if_missing_human_audio=args.fail_if_missing_human_audio,
    )
