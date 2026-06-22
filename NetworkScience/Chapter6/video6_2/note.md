# Chapter 6 Condensation and Phase Transitions

Title: 从凝聚到相变：演化网络的拓扑如何被动力学改变？

Status: v0.4 review prototype.

## Scope

This section follows the fitness model discussion and shifts from measuring
single-node fitness to asking what the whole fitness distribution does to
network topology.

Core flow:

```text
fitness rule
-> fitness distribution
-> condensation as a finite-share phase
-> order parameter for topology
-> other evolving-network mechanisms
-> phase diagram viewpoint
```

The visible model reminder is:

\[
\Pi_i=\frac{\eta_i k_i}{\sum_j \eta_j k_j}.
\]

The key topology diagnostic is:

\[
s_{\max}(t)=\frac{k_{\max}(t)}{\sum_j k_j(t)}.
\]

Scale-free / fit-get-rich phase:

\[
s_{\max}(t)\to 0.
\]

Condensed phase:

\[
s_{\max}(t)>0
\]

in the large-network limit.

## Scenes

1. `FitnessDistributionOpening` — start from the network question, not the
   Bose-gas analogy.
2. `TwoOutcomesOrderParameter` — compare fit-get-rich and condensation using
   \(s_{\max}\).
3. `CondensationAsPhaseTransition` — introduce condensation and the brief
   Bose analogy.
4. `RuleToTopology` — generalize from condensation to microscopic rules
   leaving macroscopic traces.
5. `InitialAttractiveness` — show smooth exponent tuning,
   \(\Pi(k)\sim A+k\), \(\gamma=3+A/m\).
6. `InternalLinksAcceleratedGrowth` — show old-node links and
   \(m(t)=m_0t^\theta\).
7. `NodeDeletionPhaseMap` — show deletion as a clear phase-transition
   example.
8. `AgingRegimes` — show \(\nu\) regimes for aging.
9. `DynamicsTakeaway` — final synthesis and references.

## Visual Rules

- Do not use numbered video labels on screen or in public-facing text.
- Do not reuse the previous fitness-inference bridge visual.
- Keep this section focused on topology phases and evolving-network
  mechanisms, not on fitness fitting from empirical trajectories.
- Use Greek symbols directly in public text: \(\eta,\rho,\gamma,\nu\).
- Add Chinese only for key concepts, not every explanatory phrase:
  fitness distribution / 适应度分布, order parameter / 序参量,
  condensation / 凝聚, phase transition / 相变, initial attractiveness /
  初始吸引力, internal links / 内部连边, node deletion / 节点删除, aging / 老化.
- Use fixed scene zones for title, equations, diagrams, and captions to avoid
  text collisions.

## Commands

Run from this folder:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim

PYTHONPYCACHEPREFIX=/tmp/chapter6_pycache python -m py_compile \
  main.py video_config.py scripts/*.py ../chapter6_manim_utils.py ../../video_pipeline/*.py

python scripts/build_all.py
```

For a quick metadata-only rebuild, run:

```bash
python scripts/build_all.py --skip-render --skip-tts --skip-tts-mux --skip-human-audio
```

Expected outputs:

```text
media/videos/video6_2_zh_tts_review_720p30.mp4
assets/cover/video6_2_cover_16x9.jpg
assets/cover/video6_2_cover_4x3.jpg
video_description.md
```

The public title, short description, references, and both cover ratios are
generated from `video_config.py`.

## References

- Network Science book, Chapter 6.4-6.5:
  https://networksciencebook.com/chapter/6#bose-einstein-condensation
- Bianconi and Barabasi, *Bose-Einstein condensation in complex networks*,
  Physical Review Letters 86, 5632-5635 (2001).
- Course repository:
  https://github.com/haotianh9/graph_teaching
