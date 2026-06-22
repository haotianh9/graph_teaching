from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from .common import copy_scene_outputs, load_config, render_subdir, run, scene_names


def render_scenes(video_dir: Path, quality: str | None = None, media_dir: Path | None = None) -> None:
    config = load_config(video_dir)
    quality = quality or getattr(config, "RENDER_QUALITY", "-qm")
    media_dir = media_dir or Path("/tmp") / f"{getattr(config, 'VIDEO_ID', video_dir.name)}_render"

    if media_dir.exists():
        shutil.rmtree(media_dir)
    media_dir.mkdir(parents=True, exist_ok=True)

    for scene in scene_names(config):
        run(
            [
                "manim",
                "--media_dir",
                media_dir,
                quality,
                "main.py",
                scene,
            ],
            cwd=video_dir,
        )

    copy_scene_outputs(media_dir, video_dir, config)
    print(f"rendered scenes to media/videos/main/{render_subdir(config)}", flush=True)


def main(video_dir: Path | None = None) -> None:
    parser = argparse.ArgumentParser(description="Render configured Manim scenes sequentially.")
    parser.add_argument("--quality", default=None)
    parser.add_argument("--media-dir", default=None)
    args = parser.parse_args()
    render_scenes(
        video_dir or Path.cwd(),
        quality=args.quality,
        media_dir=Path(args.media_dir) if args.media_dir else None,
    )

