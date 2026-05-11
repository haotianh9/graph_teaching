# graph_teaching

Python tutorial code and Manim animations for graph theory and network
science teaching.

## Current Dependencies

The Chapter 5 animation workflow is built and tested in the `manim` conda
environment.

Core libraries and tools:

- Python 3
- Manim Community
- NumPy
- NetworkX
- FFmpeg and FFprobe
- LaTeX tools used by Manim for `MathTex`
- A Chinese font for bilingual captions, currently `Noto Sans SC`

Audio and review helpers:

- gTTS, used by `NetworkScience/Chapter5/video5_1/scripts/generate_chinese_audio.py`
- openai-whisper, used for recorded Chinese narration transcription
- faster-whisper, optional alternative transcription backend
- Optional `manim-voiceover[gtts]` for future in-scene voiceover timing
- Optional ImageMagick for contact-sheet visual checks

Typical setup:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
pip install gTTS
pip install faster-whisper
pip install "manim-voiceover[gtts]"  # optional
```

For the recorded-audio transcription pass, `openai-whisper` was installed in
the system Python with existing Torch dependencies:

```bash
python -m pip install --user --no-deps openai-whisper
```

Chapter 5 videos should render Manim scenes sequentially, because parallel
renders can race while writing shared `media/Tex` files.

## End References

Every finished movie should end with:

- Network Science book: https://www.networksciencebook.com/
- Course repository: https://github.com/haotianh9/graph_teaching

## References

1. [Network Science Book](https://www.networksciencebook.com/) by Albert-Laszlo Barabasi
2. [Dynamics and Bifurcation in Networks: Theory and Applications of Coupled Differential Equations](https://epubs.siam.org/doi/10.1137/1.9781611977332) by Martin Golubitsky and Ian Stewart
