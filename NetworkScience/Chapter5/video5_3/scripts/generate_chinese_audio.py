from pathlib import Path
import re

from gtts import gTTS


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


FORMULA_SPEECH = {
    r"\(\Pi_i \propto \eta_i k_i\)": "Pi i 正比于艾塔 i 乘以 k i",
    r"\(\Pi_i \propto k_i A(\mathrm{age}_i)\)": "Pi i 正比于 k i 乘以年龄函数 A",
    r"\(\Pi_i \propto k_i^\alpha\)": "Pi i 正比于 k i 的 alpha 次方",
    r"\(\gamma=3\)": "伽马等于三",
    r"\(\gamma\)": "伽马",
    r"\(\alpha=1\)": "alpha 等于一",
    r"\(\alpha<1\)": "alpha 小于一",
    r"\(\alpha>1\)": "alpha 大于一",
    r"\(p\)": "p",
    r"\(C\)": "C",
}


def extract_chinese_sections(transcript_path):
    text = transcript_path.read_text(encoding="utf-8")
    sections = {}
    for scene in SCENES:
        pattern = rf"## {scene}\s+(?:### 中文\s+)?(.*?)(?=\n## |\Z)"
        match = re.search(pattern, text, flags=re.S)
        if not match:
            raise ValueError(f"Missing Chinese transcript section for {scene}")
        scene_text = match.group(1).strip()
        for formula, spoken in FORMULA_SPEECH.items():
            scene_text = scene_text.replace(formula, spoken)
        sections[scene] = re.sub(r"\s+", " ", scene_text)
    return sections


def main():
    base = Path(__file__).resolve().parents[1]
    transcript_path = base / "transcript_draft.md"
    output_dir = base / "assets" / "audio" / "zh"
    output_dir.mkdir(parents=True, exist_ok=True)

    sections = extract_chinese_sections(transcript_path)
    for scene, text in sections.items():
        mp3_path = output_dir / f"{scene}.mp3"
        txt_path = output_dir / f"{scene}.txt"
        txt_path.write_text(text + "\n", encoding="utf-8")
        print(f"Generating {mp3_path.relative_to(base)}")
        gTTS(text=text, lang="zh-CN", slow=False, timeout=25).save(mp3_path)
        print(f"Wrote {mp3_path.relative_to(base)}", flush=True)


if __name__ == "__main__":
    main()
