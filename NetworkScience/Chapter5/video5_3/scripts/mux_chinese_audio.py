from pathlib import Path
import subprocess


SCENES = [
    "BAWhatItExplains",
    "BAVisualDifference",
    "BAClusteringComparison",
    "BATriadicClosure",
    "BAExponentQuestion",
    "BAFitness",
    "BAAging",
    "BANonlinearAttachment",
    "BAExtensionsTakeaway",
]


def duration_seconds(path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def run(cmd):
    print(" ".join(str(part) for part in cmd))
    subprocess.run([str(part) for part in cmd], check=True)


def mux_scene(video_path, audio_path, output_path):
    video_duration = duration_seconds(video_path)
    audio_duration = duration_seconds(audio_path)
    target_duration = max(video_duration, audio_duration) + 0.35
    output_path.parent.mkdir(parents=True, exist_ok=True)

    run(
        [
            "ffmpeg",
            "-y",
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


def concat_videos(scene_paths, final_path, list_path):
    list_path.write_text(
        "".join(f"file '{path.resolve()}'\n" for path in scene_paths),
        encoding="utf-8",
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_path,
            "-c",
            "copy",
            final_path,
        ]
    )


def main():
    base = Path(__file__).resolve().parents[1]
    video_dir = base / "media" / "videos" / "main" / "720p30"
    audio_dir = base / "assets" / "audio" / "zh"
    mux_dir = base / "media" / "videos" / "main" / "720p30_zh_tts"
    final_path = base / "media" / "videos" / "video5_3_zh_tts_review_720p30.mp4"

    muxed_paths = []
    for scene in SCENES:
        video_path = video_dir / f"{scene}.mp4"
        audio_path = audio_dir / f"{scene}.mp3"
        output_path = mux_dir / f"{scene}.mp4"
        if not video_path.exists():
            raise FileNotFoundError(video_path)
        if not audio_path.exists():
            raise FileNotFoundError(audio_path)
        mux_scene(video_path, audio_path, output_path)
        muxed_paths.append(output_path)

    concat_videos(muxed_paths, final_path, base / "media" / "videos" / "video5_3_concat_list.txt")
    print(f"Wrote {final_path.relative_to(base)}")


if __name__ == "__main__":
    main()
