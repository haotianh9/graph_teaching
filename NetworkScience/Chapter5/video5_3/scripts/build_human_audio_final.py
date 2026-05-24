from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


SCENE_TIMINGS = [
    ("BAWhatItExplains", 0.0, 22.0),
    ("BAVisualDifference", 22.0, 54.0),
    ("BAClusteringComparison", 54.0, 103.0),
    ("BATriadicClosure", 103.0, 139.0),
    ("BAExponentQuestion", 139.0, 166.0),
    ("BAFitness", 166.0, 204.0),
    ("BAAging", 204.0, 249.0),
    ("BANonlinearAttachment", 249.0, 293.0),
    ("BAExtensionsTakeaway", 293.0, 326.443),
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
    parser = argparse.ArgumentParser(description="Build Video 5.3 with one continuous human audio recording.")
    parser.add_argument("--video-dir", default="media/videos/main/720p30")
    parser.add_argument("--audio", default="media/audio/audio1641536479.m4a")
    parser.add_argument("--work-dir", default="media/videos/main/720p30_human_audio_segments")
    parser.add_argument("--final-out", default="media/videos/video5_3_human_audio_final_720p30.mp4")
    args = parser.parse_args()

    video_dir = Path(args.video_dir)
    audio_path = Path(args.audio)
    work_dir = Path(args.work_dir)
    final_out = Path(args.final_out)
    work_dir.mkdir(parents=True, exist_ok=True)
    final_out.parent.mkdir(parents=True, exist_ok=True)

    if not audio_path.exists():
        raise SystemExit(f"Missing human audio: {audio_path}")

    segment_paths: list[Path] = []
    for scene, start, end in SCENE_TIMINGS:
        target_duration = end - start
        video_path = video_dir / f"{scene}.mp4"
        output_path = work_dir / f"{scene}.mp4"
        if not video_path.exists():
            raise SystemExit(f"Missing rendered scene video: {video_path}")

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
                str(video_path),
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
                str(output_path),
            ]
        )
        segment_paths.append(output_path)
        print(f"{scene}: scene={video_duration:.1f}s target={target_duration:.1f}s")

    concat_file = work_dir / "concat_human_video.txt"
    concat_file.write_text(
        "".join(f"file '{path.resolve()}'\n" for path in segment_paths),
        encoding="utf-8",
    )
    silent_video = work_dir / "video5_3_human_silent_720p30.mp4"
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
            str(silent_video),
        ]
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(silent_video),
            "-i",
            str(audio_path),
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
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-shortest",
            str(final_out),
        ]
    )
    print(f"combined: {final_out} ({probe_duration(final_out):.1f}s)")


if __name__ == "__main__":
    main()
