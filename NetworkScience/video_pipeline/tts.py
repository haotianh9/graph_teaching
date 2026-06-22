from __future__ import annotations

import re
from pathlib import Path

from .common import load_config, scene_names


def extract_sections(transcript_path: Path, scenes: list[str], formula_speech: dict[str, str]) -> dict[str, str]:
    text = transcript_path.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    for scene in scenes:
        pattern = rf"## {re.escape(scene)}\s+(?:### 中文\s+)?(.*?)(?=\n## |\Z)"
        match = re.search(pattern, text, flags=re.S)
        if not match:
            raise ValueError(f"Missing transcript section for {scene}")
        section_text = match.group(1).strip()
        for formula, spoken in formula_speech.items():
            section_text = section_text.replace(formula, spoken)
        sections[scene] = re.sub(r"\s+", " ", section_text)
    return sections


def generate_chinese_audio(video_dir: Path) -> None:
    from gtts import gTTS

    config = load_config(video_dir)
    transcript_path = video_dir / getattr(config, "TRANSCRIPT_PATH", "transcript_draft.md")
    output_dir = video_dir / getattr(config, "TTS_AUDIO_DIR", "assets/audio/zh")
    output_dir.mkdir(parents=True, exist_ok=True)

    sections = extract_sections(
        transcript_path,
        scene_names(config),
        getattr(config, "FORMULA_SPEECH", {}),
    )
    for scene, text in sections.items():
        mp3_path = output_dir / f"{scene}.mp3"
        txt_path = output_dir / f"{scene}.txt"
        txt_path.write_text(text + "\n", encoding="utf-8")
        print(f"Generating {mp3_path.relative_to(video_dir)}", flush=True)
        gTTS(text=text, lang=getattr(config, "TTS_LANG", "zh-CN"), slow=False, timeout=25).save(mp3_path)


def main(video_dir: Path | None = None) -> None:
    generate_chinese_audio(video_dir or Path.cwd())
