# Chapter 5 Video 5.2 Notes

Working title:

**Video 5.2 — 从连接规则到幂律：BA 模型为什么给出 \(\gamma=3\)？**

English working title: **From Attachment Rules to Power Laws: Why the BA
Model Gives \(\gamma=3\)**

## Scope

This video merges the former standalone algorithm video and the former
continuum-derivation video. The old `video5_2` was too broad and repeated
ideas from Video 5.1, so the final sequence now keeps only the algorithm
details needed for the derivation.

Included:

- precise BA loop;
- what \(m\) changes and what it does not change;
- \(k_{\mathrm{new}}(t^+)=m\);
- \(\langle k\rangle\approx 2m\);
- continuum approximation;
- degree-growth equation;
- conversion from birth time to degree distribution;
- derivation of \(p(k)\sim k^{-3}\);
- why \(\gamma=3\) is a regime boundary;
- simulation sanity check.

Excluded from the final rendered sequence:

- full seed-graph comparison;
- finite-size comparison as its own scene;
- multiple-realization comparison as its own scene.

Those prototype scenes remain in `main.py` for reference, but they are not in
the current render/mux scene order.

## Scene List

1. `BAAlgorithmDefinition`
   - Inputs: final size \(N\), attachment number \(m\), connected seed \(G_0\).
   - Loop: add node, compute degrees, compute probabilities, sample \(m\)
     targets, add edges.

2. `BARoleOfM`
   - Shows \(m=1,2,4\).
   - Explains that \(m\) fixes the birth degree and density:
     \(k_{\mathrm{new}}(t^+)=m\), \(\langle k\rangle\approx 2m\).
   - Emphasizes that \(m\) does not choose targets or hub identity.

3. `BAContinuumSetup`
   - Moves from random steps to expected growth.
   - Derives the preferential-attachment denominator directly from total
     degree:
     \(\sum_j k_j(t)=2E(t)=2(E_0+mt)\approx 2mt\).
   - Then derives average degree from that total-degree sum:
     \(\langle k\rangle(t)=\frac{1}{N(t)}\sum_j k_j(t)=2E(t)/N(t)\to2m\).
   - Then inserts \(\Pi_i(t)=k_i(t)/\sum_j k_j(t)\) into
     \(d\bar{k}_i/dt=m\Pi_i(t)\).
   - Current layout makes the equation block larger and uses the checklist as
     secondary context.

4. `BADegreeGrowthEquation`
   - Emphasizes that the differential equation describes expected degree, not
     an exact single-run trajectory.
   - Defines \(\bar{k}_i(t)=\mathbb{E}[k_i(t)]\).
   - Derives \(\frac{d\bar{k}_i}{dt}=\bar{k}_i/(2t)\).
   - Uses the birth condition \(\bar{k}_i(t_i)=m\).
   - Shows \(\bar{k}_i(t)=m(t/t_i)^{1/2}\).

5. `BABirthTimeDistribution`
   - Converts \(k_i(t)\) into a statement about birth time:
     \(t_i=m^2t/k_i^2\).

6. `BAPowerLawExponent`
   - Derives \(p(k)\sim k^{-3}\) under the continuum approximation.

7. `BAExponentRegimeMap`
   - Places \(\gamma=3\) on the degree-exponent regime map.
   - Notes that \(2<\gamma<3\) has divergent \(\langle k^2\rangle\) and
     ultra-small distances, while \(\gamma>3\) has finite \(\langle k^2\rangle\)
     and small-world scaling.
   - Uses an original simplified diagram adapted from Network Science,
     Chapter 4, degree exponent:
     `https://networksciencebook.com/chapter/4#degree-exponent`.

8. `BASimulationSanityCheck`
   - Shows that finite simulations are noisy but still heavy-tailed.

9. `BATheoryTakeaway`
   - Summarizes algorithm \(\rightarrow\) degree growth \(\rightarrow\)
     distribution.
   - Ends with the Network Science book and GitHub reference card.

## Render Workflow

Run from `NetworkScience/Chapter5/video5_2`.

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
PYTHONPYCACHEPREFIX=/tmp/chapter5_pycache python -m py_compile main.py scripts/*.py
```

Invariant check:

```bash
python - <<'PY'
from main import ba_growth_trace
import numpy as np

trace = ba_growth_trace(n_final=40, m=3, seed=12)
for step in trace["steps"]:
    assert np.isclose(sum(step["probabilities"].values()), 1.0)
    assert len(step["targets"]) == 3
    assert all(t in step["degrees"] for t in step["targets"])
print("Video 5.2 BA trace invariants passed")
PY
```

Render sequentially into `/tmp`, then copy scene mp4s back:

```bash
rm -rf /tmp/chapter5_video5_2_merged
for scene in BAAlgorithmDefinition BARoleOfM BAContinuumSetup BADegreeGrowthEquation BABirthTimeDistribution BAPowerLawExponent BAExponentRegimeMap BASimulationSanityCheck BATheoryTakeaway; do
  manim --media_dir /tmp/chapter5_video5_2_merged -qm main.py "$scene"
done

mkdir -p media/videos/main/720p30
for scene in BAAlgorithmDefinition BARoleOfM BAContinuumSetup BADegreeGrowthEquation BABirthTimeDistribution BAPowerLawExponent BAExponentRegimeMap BASimulationSanityCheck BATheoryTakeaway; do
  cp "/tmp/chapter5_video5_2_merged/videos/main/720p30/${scene}.mp4" \
    "media/videos/main/720p30/${scene}.mp4"
done
```

Generate Chinese TTS and combine:

```bash
python scripts/generate_chinese_audio.py
python scripts/mux_chinese_audio.py
```

Final review output:

```text
media/videos/video5_2_zh_tts_review_720p30.mp4
```

Human-audio final build:

```bash
python scripts/build_human_audio_final.py
```

Human recording:

```text
media/audio/audio1593684705.m4a
```

Human-audio final output:

```text
media/videos/video5_2_human_audio_final_720p30.mp4
```

Current human-audio scene alignment:

| Scene | Audio time | Spoken content |
|---|---:|---|
| `BAAlgorithmDefinition` | 0:00-1:19 | Intro, algorithm inputs, algorithm loop. |
| `BARoleOfM` | 1:19-2:12 | What \(m\) fixes and the observation \(\langle k\rangle\approx2m\). |
| `BAContinuumSetup` | 2:12-3:27 | \(N(t)\), \(E(t)\), total degree denominator, large-\(t\) approximation. |
| `BADegreeGrowthEquation` | 3:27-5:03 | Expected degree growth and solving the differential equation. |
| `BABirthTimeDistribution` | 5:03-5:29 | Older birth time means larger expected degree. |
| `BAPowerLawExponent` | 5:29-6:11 | CDF-to-PDF step and \(p(k)\sim k^{-3}\). |
| `BAExponentRegimeMap` | 6:11-7:30 | \(\gamma=3\) as a critical boundary. |
| `BASimulationSanityCheck` | 7:30-8:07 | Finite simulation and noisy high-degree tail. |
| `BATheoryTakeaway` | 8:07-8:29 | Next video transition and reference card. |

Current visual-sync pass:

- Key equations and visual objects are highlighted using exact scene-relative
  intervals derived from `media/audio/transcription/audio1593684705.tsv`.
- Each active scene is rendered to exactly the corresponding human-audio
  segment duration, so the final mux no longer depends on end-padding to fill
  large timing gaps.
- The continuum frame now derives average degree only after the total-degree
  sum:
  \(\sum_j k_j(t)=2E(t)\), then
  \(\langle k\rangle(t)=\frac{1}{N(t)}\sum_j k_j(t)=2E(t)/N(t)\to2m\).
- The beat map is saved in `assets/timing/human_audio_beats.json`.

## Current Review Status

Verified on 2026-05-24 for the merged three-video Chapter 5 sequence.

- `main.py` and `scripts/*.py` compile.
- BA probability invariants pass for `n_final=40`, `m=3`, `seed=12`.
- The nine active scenes render at 720p30.
- Chinese TTS review audio is generated in `assets/audio/zh/`.
- Human-audio final uses `media/audio/audio1593684705.m4a`.
- The final review/final mp4s have both video and audio streams.
- The human-audio final was refreshed with transcription-timed equation
  highlights.
- Spot-checked frames from the \(m\) scene and birth-time scene are readable at
  720p30.
- Spot-checked the revised continuum frame, exponent frame, and final
  reference card after the visual-sync pass.

TTS review duration: about 7 minutes 37 seconds.

Human-audio final duration: about 8 minutes 29 seconds.
