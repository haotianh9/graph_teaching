from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


SCENE_ORDER = [
    "BAOpening",
    "BAGrowth",
    "BAPreferentialAttachment",
    "BABuildingTheModel",
    "BAComparison",
    "BATakeaway",
]


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mux generated Chinese audio onto rendered Video 5.1 scenes."
    )
    parser.add_argument("--video-dir", default="media/videos/main/720p30")
    parser.add_argument("--audio-dir", default="assets/audio/zh")
    parser.add_argument("--scene-out-dir", default="media/videos/main/720p30_zh_audio")
    parser.add_argument("--final-out", default="media/videos/video5_1_zh_audio_test_720p30.mp4")
    args = parser.parse_args()

    video_dir = Path(args.video_dir)
    audio_dir = Path(args.audio_dir)
    scene_out_dir = Path(args.scene_out_dir)
    final_out = Path(args.final_out)
    scene_out_dir.mkdir(parents=True, exist_ok=True)
    final_out.parent.mkdir(parents=True, exist_ok=True)

    muxed_paths: list[Path] = []
    for scene in SCENE_ORDER:
        video_path = video_dir / f"{scene}.mp4"
        audio_path = audio_dir / f"{scene}.mp3"
        output_path = scene_out_dir / f"{scene}.mp4"

        if not video_path.exists():
            raise SystemExit(f"Missing rendered scene video: {video_path}")
        if not audio_path.exists():
            raise SystemExit(f"Missing generated audio: {audio_path}")

        video_duration = probe_duration(video_path)
        audio_duration = probe_duration(audio_path)
        output_duration = max(video_duration, audio_duration)
        video_pad = max(0.0, audio_duration - video_duration)
        audio_pad = max(0.0, video_duration - audio_duration)
        filter_spec = (
            f"[0:v]tpad=stop_mode=clone:stop_duration={video_pad:.3f},"
            f"trim=0:{output_duration:.3f},setpts=PTS-STARTPTS[v];"
            f"[1:a]apad=pad_dur={audio_pad:.3f},"
            f"atrim=0:{output_duration:.3f},asetpts=PTS-STARTPTS[a]"
        )

        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(video_path),
                "-i",
                str(audio_path),
                "-filter_complex",
                filter_spec,
                "-map",
                "[v]",
                "-map",
                "[a]",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                str(output_path),
            ]
        )
        muxed_paths.append(output_path)
        print(
            f"{scene}: video={video_duration:.1f}s audio={audio_duration:.1f}s "
            f"output={output_duration:.1f}s -> {output_path}"
        )

    concat_file = scene_out_dir / "concat_zh_audio.txt"
    concat_file.write_text(
        "".join(f"file '{path.resolve()}'\n" for path in muxed_paths),
        encoding="utf-8",
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(final_out),
        ]
    )
    print(f"combined: {final_out} ({probe_duration(final_out):.1f}s)")


if __name__ == "__main__":
    main()
