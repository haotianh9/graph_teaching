from pathlib import Path
import sys

NETWORKSCIENCE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NETWORKSCIENCE_ROOT))

from video_pipeline.human_audio import build_human_audio_final


if __name__ == "__main__":
    build_human_audio_final(Path(__file__).resolve().parents[1])
