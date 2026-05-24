# Chapter 5 Video 5.3 Notes

Working title:

**Video 5.3 — BA 模型遗漏了什么？从 hub 到真实网络结构**

## Scope

This video closes the Chapter 5 BA sequence by explaining the model's strengths
and limitations.

Included:

- what BA captures: growth, preferential attachment, hubs, heavy-tailed degree
  heterogeneity;
- a side-by-side visual contrast between a BA sample and a local Facebook
  ego-network sample;
- clustering comparison between real networks across domains and same-\(N\)
  BA baselines;
- Holme-Kim style triad formation as the first extension for creating
  clustering;
- fitness: \(\Pi_i \propto \eta_i k_i\);
- aging: \(\Pi_i \propto k_i A(\mathrm{age}_i)\);
- nonlinear preferential attachment: \(\Pi_i \propto k_i^\alpha\);
- real-network limitations such as clustering, communities, directed links,
  and node/edge deletion.
- a clustering-coefficient comparison between BA baselines and real network
  examples.

Excluded:

- full derivations, which now belong to Video 5.2;
- detailed empirical case studies, which can be handled after the BA sequence.

## V0.1 Scene List

1. `BAWhatItExplains`
   - BA as a minimal mechanism for hub emergence.

2. `BAVisualDifference`
   - Shows a BA baseline next to a local Facebook sample loaded from
     `../../Data/facebook_combined.txt`.
   - Highlights BA hubs versus higher local clustering in the Facebook sample.

3. `BAClusteringComparison`
   - Compares average clustering \(C\) for same-\(N\) BA baselines and real
     networks across domains.
   - BA uses the same node count as each real network, with integer \(m\)
     chosen to match the real average degree as closely as possible.
   - Review values:
     - C. elegans: real \(C\approx0.186\), matched BA \(C\approx0.064\).
     - Facebook: real \(C\approx0.606\), matched BA \(C\approx0.038\).
     - Collaboration: real \(C\approx0.644\), matched BA \(C\approx0.001\).

4. `BATriadicClosure`
   - Introduces Holme-Kim style triad formation as a standard local mechanism
     for clustering.
   - After preferential attachment chooses a target, the new node also links
     to one of that target's neighbors with probability \(p\).
   - Can change the clustering coefficient \(C\).
   - Cannot by itself serve as the main mechanism for tuning the degree
     exponent \(\gamma\).

5. `BAFitness`
   - Adds intrinsic node attractiveness through
     \(\Pi_i \propto \eta_i k_i\).
   - Can change the degree-tail shape and move the model away from a fixed
     \(\gamma=3\).
   - Cannot by itself directly explain high clustering \(C\); any
     finite-sample change in measured \(C\) is indirect.

6. `BAAging`
   - Adds changing visibility through
     \(\Pi_i \propto k_i A(\mathrm{age}_i)\).
   - Can truncate the tail and change the effective exponent \(\gamma\)
     observed in finite data.
   - Cannot by itself directly explain high clustering \(C\); any
     finite-sample change in measured \(C\) is indirect.

7. `BANonlinearAttachment`
   - Shows how \(\Pi_i \propto k_i^\alpha\) changes regimes.
   - Can directly move the model away from the BA \(\gamma=3\) conclusion:
     \(\alpha<1\) weakens hubs, \(\alpha=1\) is standard BA, and
     \(\alpha>1\) can produce winner-take-all condensation.
   - Cannot by itself solve low clustering \(C\).

8. `BAExponentQuestion`
   - Separates the transition from clustering \(C\) to the exponent
     \(\gamma=3\) for the human-audio version.

9. `BAExtensionsTakeaway`
   - Summarizes BA as a baseline and ends with the Network Science book and
     GitHub repository references.

## Transcript and Audio

Human-audio aligned Chinese transcript:

```text
transcript_draft.md
```

Human recording:

```text
media/audio/audio1641536479.m4a
```

Human-audio final:

```text
media/videos/video5_3_human_audio_final_720p30.mp4
```

Generated Chinese TTS review audio:

```text
assets/audio/zh/
```

## Render and Review Workflow

Run from `NetworkScience/Chapter5/video5_3`.

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
PYTHONPYCACHEPREFIX=/tmp/chapter5_pycache python -m py_compile main.py scripts/*.py
```

Render sequentially into `/tmp`, then copy finished scene mp4s back:

```bash
rm -rf /tmp/chapter5_video5_3_v01
for scene in BAWhatItExplains BAVisualDifference BAClusteringComparison BATriadicClosure BAExponentQuestion BAFitness BAAging BANonlinearAttachment BAExtensionsTakeaway; do
  manim --media_dir /tmp/chapter5_video5_3_v01 -qm main.py "$scene"
done

mkdir -p media/videos/main/720p30
for scene in BAWhatItExplains BAVisualDifference BAClusteringComparison BATriadicClosure BAExponentQuestion BAFitness BAAging BANonlinearAttachment BAExtensionsTakeaway; do
  cp "/tmp/chapter5_video5_3_v01/videos/main/720p30/${scene}.mp4" \
    "media/videos/main/720p30/${scene}.mp4"
done
```

Generate Chinese TTS, mux each scene, and concatenate:

```bash
python scripts/generate_chinese_audio.py
python scripts/mux_chinese_audio.py
```

Final review output:

```text
media/videos/video5_3_zh_tts_review_720p30.mp4
```

For the human-audio final, render the aligned scene list and combine with the
single continuous human recording:

```bash
for scene in BAWhatItExplains BAVisualDifference BAClusteringComparison BATriadicClosure BAExponentQuestion BAFitness BAAging BANonlinearAttachment BAExtensionsTakeaway; do
  manim -qm main.py "$scene"
done

python scripts/build_human_audio_final.py
```

Generate public upload assets, including both cover ratios and the video
description:

```bash
python scripts/build_public_assets.py
```

Public asset outputs:

```text
assets/cover/video5_3_cover.png
assets/cover/video5_3_cover_16x9.png
assets/cover/video5_3_cover_4x3.png
video_description.md
```

The shared title, cover labels, description, and reference links live in:

```text
scripts/public_metadata.py
```

## Acceptance Checklist

- All nine scenes render with exit code `0`.
- The clustering comparison scene renders and uses the documented review
  values.
- The final review mp4 has both video and audio streams.
- Equations are visible and do not overlap major objects.
- The final reference card is readable.
- `media/` output stays ignored by Git.

## Current Human-Audio Alignment

| Scene | Audio interval | Focus |
|---|---:|---|
| `BAWhatItExplains` | 0:00-0:22 | BA vs real-network question. |
| `BAVisualDifference` | 0:22-0:54 | BA hubs versus Facebook clustering. |
| `BAClusteringComparison` | 0:54-1:43 | Real networks have much larger \(C\). |
| `BATriadicClosure` | 1:43-2:19 | Holme-Kim style triad formation. |
| `BAExponentQuestion` | 2:19-2:46 | Move to \(\gamma=3\). |
| `BAFitness` | 2:46-3:24 | Fitness changes node attractiveness. |
| `BAAging` | 3:24-4:09 | Aging changes visibility over time. |
| `BANonlinearAttachment` | 4:09-4:53 | Nonlinear attachment changes regimes. |
| `BAExtensionsTakeaway` | 4:53-5:26 | Summary, Chapter 6 transition, references. |

## Current V0.1 Review Status

Verified on 2026-05-24 in the `manim` conda environment after moving the
clustering comparison earlier, adding the triad-formation extension, and
cleaning up the extension cards so the "can/cannot" logic focuses on two
axes: degree exponent \(\gamma\) and clustering coefficient \(C\).

- `main.py` and `scripts/*.py` compile.
- All nine scenes render at 720p30.
- Chinese TTS review audio is generated in `assets/audio/zh/`.
- Final combined review mp4 has video and audio streams.
- Clustering comparison uses `clustering coefficient C` as the y-axis label
  and describes the examples as real networks across domains.
- The opening comparison scene keeps the BA graph and explanatory text in
  separate visual regions. Dynamic rectangle highlights are removed from the
  human-audio scenes; visual emphasis now comes from color, node rings, edges,
  cards, and bars.
- Graph-heavy scenes use brighter, thicker base edges so ordinary connections
  remain visible behind hub and clustering highlights.
- Final reference card frame is readable.

Final review file:

```text
media/videos/video5_3_zh_tts_review_720p30.mp4
```

Current duration after the \(\gamma\)/\(C\) axis cleanup and the expanded
aging clarification: about 9 minutes 03 seconds.

## Current Human-Audio Status

Verified on 2026-05-24 in the `manim` conda environment.

- The recorded Chinese audio `media/audio/audio1641536479.m4a` is used as one
  continuous final track.
- The human-audio final renders at 720p30 and has both video and audio
  streams.
- Dynamic rectangle highlight boxes are disabled in the human-audio final to
  avoid title/object mismatch; timing is kept through scene-relative waits.
- The \(\gamma=3\) transition is separated into its own scene so the logic
  moves cleanly from clustering to exponent-changing extensions.
- The public-asset pipeline generates the 16:9 cover, 4:3 cover,
  compatibility cover, and `video_description.md` from
  `scripts/public_metadata.py`.

Human-audio final:

```text
media/videos/video5_3_human_audio_final_720p30.mp4
```
