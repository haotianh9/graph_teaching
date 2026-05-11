from __future__ import annotations

import argparse
import json
from pathlib import Path

import whisper


def format_timestamp(seconds: float, srt: bool = False) -> str:
    millis = int(round(seconds * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    separator = "," if srt else "."
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{millis:03d}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transcribe recorded Chinese narration with OpenAI Whisper."
    )
    parser.add_argument("--audio", default="media/audio/audio1359157491.m4a")
    parser.add_argument("--out-dir", default="media/audio/transcripts")
    parser.add_argument("--model", default="small")
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    audio_path = Path(args.audio)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem

    model = whisper.load_model(args.model, device=args.device)
    result = model.transcribe(
        str(audio_path),
        language="zh",
        task="transcribe",
        verbose=False,
        fp16=args.device != "cpu",
    )

    segments = [
        {
            "id": int(segment["id"]),
            "start": float(segment["start"]),
            "end": float(segment["end"]),
            "text": segment["text"].strip(),
        }
        for segment in result["segments"]
    ]
    payload = {
        "audio": str(audio_path),
        "model": args.model,
        "language": result.get("language", "zh"),
        "duration": segments[-1]["end"] if segments else 0.0,
        "text": result.get("text", "").strip(),
        "segments": segments,
    }

    json_path = out_dir / f"{stem}_zh_transcript.json"
    txt_path = out_dir / f"{stem}_zh_transcript.txt"
    srt_path = out_dir / f"{stem}_zh_transcript.srt"
    md_path = out_dir / f"{stem}_zh_transcript.md"

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    txt_path.write_text(payload["text"] + "\n", encoding="utf-8")
    srt_path.write_text(
        "\n\n".join(
            "\n".join(
                [
                str(idx + 1),
                (
                    f"{format_timestamp(segment['start'], srt=True)} --> "
                    f"{format_timestamp(segment['end'], srt=True)}"
                ),
                segment["text"],
                ]
            )
            for idx, segment in enumerate(segments)
        )
        + "\n",
        encoding="utf-8",
    )
    md_path.write_text(
        "# Video 5.1 Recorded Chinese Transcript\n\n"
        f"Audio: `{audio_path}`\n\n"
        f"Model: `openai-whisper {args.model}`\n\n"
        "## Timestamped Transcript\n\n"
        + "\n".join(
            (
                f"- `{format_timestamp(segment['start'])}"
                f" - {format_timestamp(segment['end'])}` "
                f"{segment['text']}"
            )
            for segment in segments
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"wrote {json_path}")
    print(f"wrote {txt_path}")
    print(f"wrote {srt_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
