from pathlib import Path
import sys

NETWORKSCIENCE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NETWORKSCIENCE_ROOT))

from video_pipeline.render import render_scenes


if __name__ == "__main__":
    render_scenes(Path(__file__).resolve().parents[1])
