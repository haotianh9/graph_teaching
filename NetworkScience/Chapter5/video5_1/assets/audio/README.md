# Video 5.1 Audio Workflow

This folder stores external narration tracks for Video 5.1.

Current generated Chinese timing-test audio:

```text
assets/audio/zh/
```

Each scene has two files:

- `SCENE.mp3`: generated Chinese TTS audio.
- `SCENE.txt`: cleaned plain text sent to the TTS engine.

To regenerate Chinese TTS from `transcript_draft.md`:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
python scripts/generate_chinese_audio.py
```

To replace TTS with recorded audio later:

1. Record or export one mp3 per scene.
2. Use the same names:
   - `BAOpening.mp3`
   - `BAGrowth.mp3`
   - `BAPreferentialAttachment.mp3`
   - `BABuildingTheModel.mp3`
   - `BAComparison.mp3`
   - `BATakeaway.mp3`
3. Put them in `assets/audio/zh/`.
4. Run:

```bash
python scripts/mux_chinese_audio.py
```

The mux script preserves the full audio. If a scene audio file is longer than
the rendered scene, it freezes the final video frame until the narration ends.
This makes timing mismatches visible instead of cutting narration.
