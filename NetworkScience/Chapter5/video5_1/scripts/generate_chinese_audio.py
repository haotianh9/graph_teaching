from __future__ import annotations

import argparse
import re
from pathlib import Path

from gtts import gTTS


SCENE_ORDER = [
    "BAOpening",
    "BAGrowth",
    "BAPreferentialAttachment",
    "BABuildingTheModel",
    "BAComparison",
    "BATakeaway",
]


FORMULA_SPEECH = {
    r"\Pi_i = \frac{k_i}{\sum_j k_j}.": "Pi i 等于 k i 除以所有 k j 的和。",
    r"\Pi_i = \frac{k_i}{\sum_j k_j}": "Pi i 等于 k i 除以所有 k j 的和。",
    r"N(t)=N_0+t": "N t 等于 N 零加 t",
}


def extract_chinese_sections(transcript_path: Path) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_scene: str | None = None
    current_language: str | None = None

    for raw_line in transcript_path.read_text(encoding="utf-8").splitlines():
        scene_match = re.match(r"^##\s+(BA\w+)\s*$", raw_line)
        if scene_match:
            current_scene = scene_match.group(1)
            current_language = None
            sections.setdefault(current_scene, [])
            continue

        if raw_line.startswith("### "):
            current_language = "zh" if raw_line.strip() == "### 中文" else None
            continue

        if current_scene and current_language == "zh":
            sections[current_scene].append(raw_line)

    return {
        scene: "\n".join(lines).strip()
        for scene, lines in sections.items()
        if "\n".join(lines).strip()
    }


def clean_for_tts(markdown_text: str) -> str:
    text = markdown_text

    text = re.sub(
        r"\\\(\s*N\(t\)\s*=\s*N_0\s*\+\s*t\s*\\\)",
        "N t 等于 N 零加 t",
        text,
    )
    text = re.sub(r"\\\(i\\\)", "i", text)
    text = re.sub(
        r"\\\[\s*\\Pi_i\s*=\s*\\frac\{k_i\}\{\\sum_j k_j\}\.?\s*\\\]",
        "Pi i 等于 k i 除以所有 k j 的和。",
        text,
        flags=re.DOTALL,
    )

    for formula, spoken in FORMULA_SPEECH.items():
        text = text.replace(formula, spoken)

    text = re.sub(r"\\\((.*?)\\\)", lambda match: FORMULA_SPEECH.get(match.group(1), ""), text)
    text = text.replace(r"\[", "").replace(r"\]", "")
    text = text.replace("Barabasi-Albert", "Barabasi Albert")
    text = text.replace("BA", "B A")
    text = text.replace("*Science*", "Science")
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", "，").replace(" :", "：")
    return text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Chinese draft TTS audio from transcript_draft.md."
    )
    parser.add_argument("--transcript", default="transcript_draft.md")
    parser.add_argument("--out-dir", default="assets/audio/zh")
    parser.add_argument("--lang", default="zh-CN")
    args = parser.parse_args()

    transcript_path = Path(args.transcript)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sections = extract_chinese_sections(transcript_path)
    missing = [scene for scene in SCENE_ORDER if scene not in sections]
    if missing:
        raise SystemExit(f"Missing Chinese transcript sections: {', '.join(missing)}")

    for scene in SCENE_ORDER:
        spoken_text = clean_for_tts(sections[scene])
        text_path = out_dir / f"{scene}.txt"
        audio_path = out_dir / f"{scene}.mp3"
        text_path.write_text(spoken_text + "\n", encoding="utf-8")
        gTTS(text=spoken_text, lang=args.lang, slow=False).save(str(audio_path))
        print(f"{scene}: wrote {audio_path}")


if __name__ == "__main__":
    main()
