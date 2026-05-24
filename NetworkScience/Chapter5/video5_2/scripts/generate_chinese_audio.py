from __future__ import annotations

import argparse
import re
from pathlib import Path

from gtts import gTTS


SCENE_ORDER = [
    "BAAlgorithmDefinition",
    "BARoleOfM",
    "BAContinuumSetup",
    "BADegreeGrowthEquation",
    "BABirthTimeDistribution",
    "BAPowerLawExponent",
    "BAExponentRegimeMap",
    "BASimulationSanityCheck",
    "BATheoryTakeaway",
]


FORMULA_SPEECH = {
    r"\(N(t)=N_0+t\)": "N t 等于 N 零加 t",
    r"\(E(t)=E_0+mt\)": "E t 等于 E 零加 m t",
    r"\(\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}\)": "Pi i t 等于 k i t 除以所有 k j t 的和",
    r"\(\langle k\rangle\approx 2m\)": "平均度约等于二 m",
    r"\(\langle k\rangle(t)=\frac{2E(t)}{N(t)}=\frac{2(E_0+mt)}{N_0+t}\)": "平均度 t 等于二 E t 除以 N t，也就是二倍 E 零加 m t，除以 N 零加 t",
    r"\(\sum_j k_j(t)=2E(t)=2(E_0+mt)\)": "所有 k j t 的和等于二 E t，也就是二倍 E 零加 m t",
    r"\(\sum_j k_j(t)=N(t)\langle k\rangle(t)\approx 2mt\)": "所有 k j t 的和等于 N t 乘以平均度 t，约等于二 m t",
    r"\(\frac{d\bar{k}_i}{dt}=m\Pi_i(t)\)": "k i 上横线对 t 的导数等于 m 乘以 Pi i t",
    r"\(k_{\mathrm{new}}(t^+)=m\)": "新节点出生时的度等于 m",
    r"\(k_i(t)=m(t/t_i)^{1/2}\)": "k i t 等于 m 乘以 t 除以 t i 的二分之一次方",
    r"\(p(k)\sim k^{-3}\)": "p k 正比于 k 的负三次方",
    r"\(\gamma=3\)": "伽马等于三",
    r"\(\langle k^2\rangle\)": "k 平方的平均",
    r"\(\langle d\rangle\sim\ln\ln N\)": "平均距离正比于 ln ln N",
    r"\(\langle d\rangle\sim\ln N\)": "平均距离正比于 ln N",
    r"\(\bar{k}_i(t)=\mathbb{E}[k_i(t)]\)": "k i 上横线 t 表示 k i t 的期望",
    r"\(\frac{d\bar{k}_i}{dt}=m\frac{\bar{k}_i}{2mt}\)": "k i 上横线对 t 的导数等于 m 乘以 k i 上横线除以二 m t",
    r"\(\frac{d\bar{k}_i}{dt}=\frac{\bar{k}_i}{2t}\)": "k i 上横线对 t 的导数等于 k i 上横线除以二 t",
    r"\(\bar{k}_i(t_i)=m\)": "k i 上横线在出生时间 t i 等于 m",
    r"\(\bar{k}_i(t)=m(t/t_i)^{1/2}\)": "k i 上横线 t 等于 m 乘以 t 除以 t i 的二分之一次方",
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
    text = text.replace("Barabasi-Albert", "Barabasi Albert")
    text = text.replace("BA", "B A")
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Chinese TTS audio for Video 5.2.")
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
        (out_dir / f"{scene}.txt").write_text(spoken_text + "\n", encoding="utf-8")
        gTTS(text=spoken_text, lang=args.lang, slow=False, timeout=25).save(str(out_dir / f"{scene}.mp3"))
        print(f"{scene}: wrote {out_dir / f'{scene}.mp3'}", flush=True)


if __name__ == "__main__":
    main()
