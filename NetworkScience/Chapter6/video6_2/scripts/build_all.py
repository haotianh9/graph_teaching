from pathlib import Path
import sys

NETWORKSCIENCE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NETWORKSCIENCE_ROOT))

from video_pipeline.build_all import main


if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1])
