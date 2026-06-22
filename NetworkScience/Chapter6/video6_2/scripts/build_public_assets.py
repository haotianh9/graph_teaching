from pathlib import Path
import sys

NETWORKSCIENCE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NETWORKSCIENCE_ROOT))

from video_pipeline.public_assets import build_public_assets


if __name__ == "__main__":
    build_public_assets(Path(__file__).resolve().parents[1])
