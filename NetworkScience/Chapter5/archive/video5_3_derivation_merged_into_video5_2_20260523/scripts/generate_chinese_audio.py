from __future__ import annotations

import argparse
import re
from pathlib import Path

from gtts import gTTS


SCENE_ORDER = [
    "BAContinuumSetup",
    "BADegreeGrowthEquation",
    "BABirthTimeDistribution",
    "BAPowerLawExponent",
    "BASimulationSanityCheck",
    "BATheoryTakeaway",
]


FORMULA_SPEECH = {
    r"\(P(k)\sim k^{-3}\)": "P k 正比于 k 的负三次方",
    r"\(\frac{dk_i}{dt}=m\Pi_i(t)\)": "d k i 除以 d t 等于 m 乘以 Pi i t",
    r"\(\sum_j k_j(t)\approx 2mt\)": "所有节点度的和约等于二 m t",
    r"\(\frac{dk_i}{dt}=\frac{k_i}{2t}\)": "d k i 除以 d t 等于 k i 除以二 t",
    r"\(k_i(t_i)=m\)": "k i 在 t i 时刻等于 m",
    r"\(k_i(t)=m\left(\frac{t}{t_i}\right)^{1/2}\)": "k i t 等于 m 乘以 t 除以 t i 的二分之一次方",
    r"\(t_i=\frac{m^2t}{k_i^2}\)": "t i 等于 m 平方乘以 t 除以 k i 平方",
    r"\(P(k_i(t)<k)=1-\frac{m^2}{k^2}\)": "累积分布等于一减去 m 平方除以 k 平方",
    r"\(p(k)\sim 2m^2k^{-3}\)": "p k 正比于二 m 平方乘以 k 的负三次方",
    r"\(p(k)\sim k^{-3}\)": "p k 正比于 k 的负三次方",
}


def extract_chinese_sections(transcript_path: Path) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_scene: str | None = None
    current_language: str | None = None
    for raw_line in transcript_path.read_text(encoding="utf-8").splitlines():
        scene_match = re.match(r"^##\s+(\w+)\s*$", raw_line)
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
    for formula, spoken in FORMULA_SPEECH.items():
        text = text.replace(formula, spoken)
    text = re.sub(r"\\\[(.*?)\\\]", "", text, flags=re.DOTALL)
    text = re.sub(r"\\\((.*?)\\\)", "", text)
    text = text.replace("BA", "B A")
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Chinese TTS audio for Video 5.3.")
    parser.add_argument("--transcript", default="transcript_draft.md")
    parser.add_argument("--out-dir", default="assets/audio/zh")
    parser.add_argument("--lang", default="zh-CN")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sections = extract_chinese_sections(Path(args.transcript))
    missing = [scene for scene in SCENE_ORDER if scene not in sections]
    if missing:
        raise SystemExit(f"Missing Chinese transcript sections: {', '.join(missing)}")

    for scene in SCENE_ORDER:
        spoken_text = clean_for_tts(sections[scene])
        (out_dir / f"{scene}.txt").write_text(spoken_text + "\n", encoding="utf-8")
        gTTS(text=spoken_text, lang=args.lang, slow=False).save(str(out_dir / f"{scene}.mp3"))
        print(f"{scene}: wrote {out_dir / f'{scene}.mp3'}")


if __name__ == "__main__":
    main()
