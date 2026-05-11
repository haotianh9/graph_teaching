from __future__ import annotations

import json
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

# Boundaries inferred from the recorded narration transcript.
SCENE_BOUNDARIES = {
    "BAOpening": (0.0, 52.0),
    "BAGrowth": (52.0, 132.0),
    "BAPreferentialAttachment": (132.0, 240.0),
    "BABuildingTheModel": (240.0, 296.0),
    "BAComparison": (296.0, 341.0),
    "BATakeaway": (341.0, None),
}


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
    root = Path(".")
    audio_path = root / "media/audio/audio1359157491.m4a"
    video_dir = root / "media/videos/main/720p30"
    segment_dir = root / "media/audio/recorded_segments"
    scene_out_dir = root / "media/videos/main/720p30_recorded_aligned"
    final_out = root / "media/videos/video5_1_recorded_audio_aligned_720p30.mp4"
    report_path = root / "media/audio/transcripts/audio1359157491_alignment.json"
    report_md_path = root / "media/audio/transcripts/audio1359157491_alignment.md"

    segment_dir.mkdir(parents=True, exist_ok=True)
    scene_out_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    final_out.parent.mkdir(parents=True, exist_ok=True)

    full_audio_duration = probe_duration(audio_path)
    report = {
        "audio": str(audio_path),
        "audio_duration": full_audio_duration,
        "mode": (
            "Scene-level alignment. The first five scene videos are retimed to "
            "their recorded narration segments. BATakeaway keeps the full visual "
            "duration so the reference card remains readable."
        ),
        "scenes": [],
    }

    muxed_paths: list[Path] = []
    for scene in SCENE_ORDER:
        start, end = SCENE_BOUNDARIES[scene]
        if end is None:
            end = full_audio_duration
        audio_duration = end - start
        video_path = video_dir / f"{scene}.mp4"
        segment_path = segment_dir / f"{scene}.m4a"
        scene_output = scene_out_dir / f"{scene}.mp4"

        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-ss",
                f"{start:.3f}",
                "-to",
                f"{end:.3f}",
                "-i",
                str(audio_path),
                "-vn",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                str(segment_path),
            ]
        )

        video_duration = probe_duration(video_path)
        measured_audio_duration = probe_duration(segment_path)

        if scene == "BATakeaway":
            output_duration = max(video_duration, measured_audio_duration)
            video_pad = max(0.0, measured_audio_duration - video_duration)
            audio_pad = max(0.0, video_duration - measured_audio_duration)
            filter_spec = (
                f"[0:v]tpad=stop_mode=clone:stop_duration={video_pad:.3f},"
                f"trim=0:{output_duration:.3f},setpts=PTS-STARTPTS[v];"
                f"[1:a]apad=pad_dur={audio_pad:.3f},"
                f"atrim=0:{output_duration:.3f},asetpts=PTS-STARTPTS[a]"
            )
            speed_factor = 1.0
        else:
            output_duration = measured_audio_duration
            speed_factor = measured_audio_duration / video_duration
            filter_spec = (
                f"[0:v]setpts={speed_factor:.8f}*PTS,"
                f"trim=0:{output_duration:.3f},setpts=PTS-STARTPTS[v];"
                f"[1:a]atrim=0:{output_duration:.3f},asetpts=PTS-STARTPTS[a]"
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
                str(segment_path),
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
                "192k",
                str(scene_output),
            ]
        )

        muxed_paths.append(scene_output)
        report["scenes"].append(
            {
                "scene": scene,
                "audio_start": start,
                "audio_end": end,
                "audio_duration": measured_audio_duration,
                "video_duration_original": video_duration,
                "video_speed_factor": speed_factor,
                "output_duration": probe_duration(scene_output),
                "audio_segment": str(segment_path),
                "scene_output": str(scene_output),
            }
        )

    concat_file = scene_out_dir / "concat_recorded_aligned.txt"
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

    report["final_output"] = str(final_out)
    report["final_duration"] = probe_duration(final_out)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Video 5.1 Recorded Audio Alignment",
        "",
        f"Recorded audio: `{audio_path}`",
        f"Final output: `{final_out}`",
        f"Final duration: `{report['final_duration']:.1f}s`",
        "",
        "The first five scene videos are retimed to match the recorded narration "
        "segments. The final takeaway scene keeps its full visual duration so "
        "the end reference card remains readable.",
        "",
        "| Scene | Audio segment | Audio duration | Original video | Video factor | Output |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in report["scenes"]:
        lines.append(
            "| {scene} | {start:.1f}-{end:.1f}s | {aud:.1f}s | {vid:.1f}s | "
            "{factor:.3f} | {out:.1f}s |".format(
                scene=item["scene"],
                start=item["audio_start"],
                end=item["audio_end"],
                aud=item["audio_duration"],
                vid=item["video_duration_original"],
                factor=item["video_speed_factor"],
                out=item["output_duration"],
            )
        )
    report_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {report_path}")
    print(f"wrote {report_md_path}")
    print(f"wrote {final_out} ({report['final_duration']:.1f}s)")


if __name__ == "__main__":
    main()
