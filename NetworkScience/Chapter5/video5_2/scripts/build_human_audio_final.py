from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


SCENE_TIMINGS = [
    ("BAAlgorithmDefinition", 0.0, 79.0),
    ("BARoleOfM", 79.0, 132.0),
    ("BAContinuumSetup", 132.0, 207.0),
    ("BADegreeGrowthEquation", 207.0, 303.0),
    ("BABirthTimeDistribution", 303.0, 329.0),
    ("BAPowerLawExponent", 329.0, 371.0),
    ("BAExponentRegimeMap", 371.0, 450.0),
    ("BASimulationSanityCheck", 450.0, 487.0),
    ("BATheoryTakeaway", 487.0, 509.1),
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
    parser = argparse.ArgumentParser(description="Build Video 5.2 with one continuous human audio recording.")
    parser.add_argument("--video-dir", default="media/videos/main/720p30")
    parser.add_argument("--audio", default="media/audio/audio1593684705.m4a")
    parser.add_argument("--work-dir", default="media/videos/main/720p30_human_audio_segments")
    parser.add_argument("--final-out", default="media/videos/video5_2_human_audio_final_720p30.mp4")
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
    silent_video = work_dir / "video5_2_human_silent_720p30.mp4"
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
