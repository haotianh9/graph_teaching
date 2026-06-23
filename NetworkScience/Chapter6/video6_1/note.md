# Chapter 6 Fitness Inference Production Note

Title: 如何推断 Fitness? 从 Bianconi-Barabasi 模型到增长数据

Status: v0.1 renderable/review prototype.

## Scope

This video starts Chapter 6 as a direct continuation of Chapter 5.3. It gives a
brief reminder of the Bianconi-Barabasi fitness model, then focuses mainly on
how fitness can be inferred from growth histories.

Core equation:

\[
\Pi_i=\frac{\eta_i k_i}{\sum_j \eta_j k_j}.
\]

Inference equation:

\[
\ln \bar{k}_i(t)=\beta(\eta_i)\ln t+B_i,
\qquad
\beta(\eta_i)=\frac{\eta_i}{C}.
\]

\(\bar{k}_i(t)\) is the continuum expected degree. The constant \(C\) is a
network-level normalization determined by the fitness distribution
\(\rho(\eta)\), not a second per-node parameter. Taking the logarithm of
\(\bar{k}_i(t)=m(t/t_i)^{\eta_i/C}\) gives
\(B_i=\ln m-\beta(\eta_i)\ln t_i\).

Real-data teaching proxy:

\[
\widehat{\beta}_i=\mathrm{slope}\left[\log(c_i(\tau)+1)\ \mathrm{vs.}\ \log(\tau+1)\right],
\qquad
\widehat{\eta}_i=\widehat{\beta}_i/\langle\widehat{\beta}\rangle.
\]

The real-data demo uses the SNAP HEP-TH citation network. Raw downloads live
under ignored `assets/data/snap_hepth/`; the small derived fitting summary is
tracked under `data/`.

## Scenes

1. `FitnessOpening` — brief bridge from Chapter 5 and model reminder.
2. `FitnessRule` — show the fitness-weighted probability rule.
3. `FitnessGrowthDerivation` — derive \(\beta(\eta)=\eta/C\) and the log-log equation.
4. `FitnessInferenceOpening` — shift from model parameter to data estimate.
5. `LogLogSlope` — explain slope as effective fitness.
6. `GrowthHistoryComparison` — show why early popularity can mislead.
7. `CitationImpact` — discuss citation fitness plus aging/visibility.
8. `RealDataFitnessFit` — fit effective growth fitness on dated HEP-TH citation histories.
9. `PredictionWorkflow` — summarize the data workflow.
10. `FitnessTakeaway` — summarize and point to condensation/phase transition.

## Real-Data Fit

Run this before rendering if `data/fitness_fit_results.json` needs to be
regenerated:

```bash
python scripts/fit_hepth_fitness.py
```

Current derived results:

- dataset: SNAP HEP-TH citation network;
- total citation edges in source file: 352,807;
- dated usable citation edges after ID normalization: 80,400;
- papers passing the simple fitting threshold: 1,271;
- mean \(\widehat{\beta}\): 1.668;
- median \(\widehat{\beta}\): 1.557.

This is intentionally presented as an effective growth-fitness teaching proxy.
It is not the full scientific-impact model, because citation aging, fields, and
observation windows still matter.

## Shared Pipeline Commands

Run from this folder:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim

PYTHONPYCACHEPREFIX=/tmp/chapter6_pycache python -m py_compile \
  main.py video_config.py scripts/*.py ../../video_pipeline/*.py

python scripts/build_all.py
```

For a quicker rebuild after editing only metadata or the continuous human-audio
timing, keep the existing rendered scene mp4s and run:

```bash
python scripts/build_all.py --skip-render --skip-tts --skip-tts-mux
```

Expected outputs:

```text
media/videos/video6_1_zh_tts_review_720p30.mp4
media/videos/video6_1_human_audio_final_720p30.mp4
assets/cover/video6_1_cover_16x9.jpg
assets/cover/video6_1_cover_4x3.jpg
video_description.md
```

The public title, short description, references, and both cover ratios are
generated from `video_config.py`.

The human-audio final uses the configured speech cleanup chain:

```text
highpass=f=80,lowpass=f=9000,afftdn=nf=-32,loudnorm=I=-16:TP=-1.5:LRA=11
```

This keeps the original `.m4a` untouched and applies filtering only when the
final mp4 is assembled.

## Acceptance Checklist

- all ten scenes render at 720p30;
- Chinese TTS review video exists and has video/audio streams;
- human-audio final video exists and has video/audio streams once
  `HUMAN_AUDIO_PATH` is configured;
- `RealDataFitnessFit` shows the HEP-TH fitting result and the estimator caveat;
- cover outputs include 16:9 and 4:3 images;
- `video_description.md` is generated from `video_config.py`;
- generated `media/`, `assets/`, and `__pycache__/` files remain ignored.

## References

- Network Science book, Chapter 6:
  https://networksciencebook.com/chapter/6#bianconi-model
- Bianconi and Barabasi, *Competition and multiscaling in evolving networks*,
  Europhysics Letters 54, 436-442 (2001).
- SNAP HEP-TH citation network:
  https://snap.stanford.edu/data/cit-HepTh.html
- Course repository:
  https://github.com/haotianh9/graph_teaching
