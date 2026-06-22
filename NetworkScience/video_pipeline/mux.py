from __future__ import annotations

from pathlib import Path

from .common import load_config, probe_duration, render_subdir, run, scene_names, write_concat_file


def mux_scene(video_path: Path, audio_path: Path, output_path: Path) -> None:
    video_duration = probe_duration(video_path)
    audio_duration = probe_duration(audio_path)
    target_duration = max(video_duration, audio_duration) + 0.35
    output_path.parent.mkdir(parents=True, exist_ok=True)

    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            video_path,
            "-i",
            audio_path,
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={target_duration:.3f}[v];"
            f"[1:a]apad=pad_dur={target_duration:.3f}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-t",
            f"{target_duration:.3f}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            output_path,
        ]
    )


def mux_chinese_audio(video_dir: Path) -> Path:
    config = load_config(video_dir)
    subdir = render_subdir(config)
    video_scene_dir = video_dir / "media" / "videos" / "main" / subdir
    audio_dir = video_dir / getattr(config, "TTS_AUDIO_DIR", "assets/audio/zh")
    mux_dir = video_dir / "media" / "videos" / "main" / f"{subdir}_zh_tts"
    final_path = video_dir / getattr(config, "TTS_FINAL_OUT", f"media/videos/{config.VIDEO_ID}_zh_tts_review_720p30.mp4")

    muxed_paths: list[Path] = []
    for scene in scene_names(config):
        video_path = video_scene_dir / f"{scene}.mp4"
        audio_path = audio_dir / f"{scene}.mp3"
        if not video_path.exists():
            raise FileNotFoundError(video_path)
        if not audio_path.exists():
            raise FileNotFoundError(audio_path)
        output_path = mux_dir / f"{scene}.mp4"
        mux_scene(video_path, audio_path, output_path)
        muxed_paths.append(output_path)

    list_path = video_dir / "media" / "videos" / f"{config.VIDEO_ID}_concat_list.txt"
    write_concat_file(muxed_paths, list_path)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", list_path, "-c", "copy", final_path])
    print(f"Wrote {final_path.relative_to(video_dir)}", flush=True)
    return final_path


def main(video_dir: Path | None = None) -> None:
    mux_chinese_audio(video_dir or Path.cwd())

