from pathlib import Path
import sys

NETWORKSCIENCE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NETWORKSCIENCE_ROOT))

from video_pipeline.tts import generate_chinese_audio


if __name__ == "__main__":
    generate_chinese_audio(Path(__file__).resolve().parents[1])
