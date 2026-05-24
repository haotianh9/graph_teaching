# Chapter 5 Video 5.3 Notes

Working title: **Why \(P(k)\sim k^{-3}\)**

Goal for V0.1: make a rough but renderable derivation video with Chinese TTS
timing. This is the math-heavy Chapter 5 video.

## Scope

Include:

- continuum approximation;
- expected degree growth \(dk_i/dt\);
- solution \(k_i(t)=m(t/t_i)^{1/2}\);
- birth-time-to-degree conversion;
- \(p(k)\sim k^{-3}\);
- finite simulation sanity check.

Keep out:

- fitness, aging, nonlinear preferential attachment, and real-network
  limitations. Those now belong to Video 5.3.

## Scene List

1. `BAContinuumSetup`
2. `BADegreeGrowthEquation`
3. `BABirthTimeDistribution`
4. `BAPowerLawExponent`
5. `BASimulationSanityCheck`
6. `BATheoryTakeaway`

## Render And Review Workflow

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
PYTHONPYCACHEPREFIX=/tmp/chapter5_pycache python -m py_compile main.py scripts/*.py

rm -rf /tmp/chapter5_video5_3_v01
for scene in BAContinuumSetup BADegreeGrowthEquation BABirthTimeDistribution BAPowerLawExponent BASimulationSanityCheck BATheoryTakeaway; do
  manim --media_dir /tmp/chapter5_video5_3_v01 -qm main.py "$scene"
done

mkdir -p media/videos/main/720p30
for scene in BAContinuumSetup BADegreeGrowthEquation BABirthTimeDistribution BAPowerLawExponent BASimulationSanityCheck BATheoryTakeaway; do
  cp "/tmp/chapter5_video5_3_v01/videos/main/720p30/${scene}.mp4" \
    "media/videos/main/720p30/${scene}.mp4"
done

python scripts/generate_chinese_audio.py
python scripts/mux_chinese_audio.py
```

Review output target:

```text
media/videos/video5_3_zh_tts_review_720p30.mp4
```

## Acceptance Checklist

- All six scenes render with exit code `0`.
- The final review mp4 has both video and audio streams.
- Equations are visible and do not overlap major objects.
- The final reference card is readable.
- `media/` output stays ignored by Git.

## Current V0.1 Review Status

Verified on 2026-05-12 in the `manim` conda environment.

- `main.py` and `scripts/*.py` compile.
- All six scenes render at 720p30.
- Chinese TTS review audio is generated in `assets/audio/zh/`.
- Final combined review mp4 has video and audio streams.
- Final reference card frame is readable.

Final review file:

```text
media/videos/video5_3_zh_tts_review_720p30.mp4
```

Duration: about 4 minutes 18 seconds.
