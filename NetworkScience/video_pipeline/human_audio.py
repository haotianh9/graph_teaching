from __future__ import annotations

import argparse
from pathlib import Path

from .common import load_config, probe_duration, render_subdir, run, scene_timings, write_concat_file


def build_human_audio_final(video_dir: Path, fail_if_missing: bool = False) -> Path | None:
    config = load_config(video_dir)
    configured_audio = getattr(config, "HUMAN_AUDIO_PATH", None)
    if not configured_audio:
        print("No HUMAN_AUDIO_PATH configured; skipped.")
        return None

    audio_path = video_dir / configured_audio
    final_out = video_dir / getattr(config, "HUMAN_FINAL_OUT", f"media/videos/{config.VIDEO_ID}_human_audio_final_720p30.mp4")
    audio_filter = getattr(
        config,
        "HUMAN_AUDIO_FILTER",
        "loudnorm=I=-16:TP=-1.5:LRA=11",
    )

    if not audio_path.exists():
        message = f"No human audio found at {audio_path.relative_to(video_dir)}; skipped."
        if fail_if_missing:
            raise FileNotFoundError(message)
        print(message)
        return None

    video_scene_dir = video_dir / "media" / "videos" / "main" / render_subdir(config)
    work_dir = video_dir / "media" / "videos" / "main" / f"{render_subdir(config)}_human_audio_segments"
    work_dir.mkdir(parents=True, exist_ok=True)
    final_out.parent.mkdir(parents=True, exist_ok=True)

    segment_paths: list[Path] = []
    for scene, start, end in scene_timings(config):
        target_duration = end - start
        video_path = video_scene_dir / f"{scene}.mp4"
        output_path = work_dir / f"{scene}.mp4"
        if not video_path.exists():
            raise FileNotFoundError(video_path)
        video_duration = probe_duration(video_path)
        video_pad = max(0.0, target_duration - video_duration)
        filter_spec = (
            f"fps=30,format=yuv420p,"
            f"tpad=stop_mode=clone:stop_duration={video_pad:.3f},"
            f"trim=duration={target_duration:.3f},setpts=PTS-STARTPTS"
        )
        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                video_path,
                "-an",
                "-vf",
                filter_spec,
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                output_path,
            ]
        )
        segment_paths.append(output_path)
        print(f"{scene}: scene={video_duration:.1f}s target={target_duration:.1f}s", flush=True)

    concat_file = work_dir / "concat_human_video.txt"
    write_concat_file(segment_paths, concat_file)
    silent_video = work_dir / f"{config.VIDEO_ID}_human_silent_720p30.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", concat_file, "-c", "copy", silent_video])
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            silent_video,
            "-i",
            audio_path,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-af",
            audio_filter,
            "-shortest",
            final_out,
        ]
    )
    print(f"combined: {final_out.relative_to(video_dir)} ({probe_duration(final_out):.1f}s)", flush=True)
    return final_out


def main(video_dir: Path | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build final mp4 with a continuous human audio recording.")
    parser.add_argument("--fail-if-missing", action="store_true")
    args = parser.parse_args()
    build_human_audio_final(video_dir or Path.cwd(), fail_if_missing=args.fail_if_missing)
