# Chapter 6 Condensation and Phase Transitions

Title: 从凝聚到相变：演化网络的拓扑如何被动力学改变？

Status: v0.4 review prototype.

## Scope

This section follows the fitness model discussion and starts from time-history
based estimated-fitness distributions. The first is the HEP-TH citation-growth
fit from `video6_1`. The second is a lightweight Web-domain visibility proxy
from Common Crawl domain-level Web Graph PageRank snapshots. It then asks what
the whole fitness distribution does to network topology.

Core flow:

```text
HEP-TH fitted effective-fitness distribution
-> Common Crawl Web-domain visibility proxy
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

1. `FitnessDistributionOpening` — start from fitted HEP-TH
   \(\widehat{\eta}\) and Common Crawl Web-domain \(\widehat{\eta}_{web}\)
   proxy distributions, and explain why static networks alone do not measure
   fitness.
2. `TwoOutcomesOrderParameter` — compare fit-get-rich and condensation using
   \(s_{\max}\).
3. `CondensationAsPhaseTransition` — use a compact schematic after Network
   Science Fig. 6.8 to compare high/low-temperature Fermi and Bose gases, then
   map network nodes to energy levels and links to Bose-like particles before
   introducing condensation.
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
  mechanisms. The opening can use fitted HEP-TH and Common Crawl Web-domain
  proxy distributions as motivation, but should not repeat the full inference
  workflow.
- Be explicit that the Web-domain chart is a doable teaching proxy. The book's
  Web example is page-level Web document fitness; the local chart uses
  domain-level Common Crawl snapshots and PageRank visibility dynamics.
- Use Greek symbols directly in public text: \(\eta,\rho,\gamma,\nu\).
- Add Chinese only for key concepts, not every explanatory phrase:
  fitness distribution / 适应度分布, order parameter / 序参量,
  condensation / 凝聚, phase transition / 相变, initial attractiveness /
  初始吸引力, internal links / 内部连边, node deletion / 节点删除, aging / 老化.
- Use fixed scene zones for title, equations, diagrams, and captions to avoid
  text collisions.

## Empirical Check: Does Eq. 6.22 Fit?

The book gives a theoretical fitness-density family

\[
\rho(\eta)=(1-\zeta)(1-\eta)^{-\zeta}, \qquad 0\le \eta \le 1.
\]

This should be treated as a stylized analytic family, not as a claim that any
measured fitness distribution must exactly have this form. Our fitted
quantities are teaching proxies:

- HEP-TH: \(\widehat{\eta}=\widehat{\beta}/\langle\widehat{\beta}\rangle\).
- Web: \(\widehat{\eta}_{web}\) from domain-level Common Crawl PageRank
  snapshot growth.

They are not naturally bounded by 1, so fitting Eq. 6.22 requires an extra
normalization. The reproducible check is in:

```text
scripts/fit_condensation_family.py
data/condensation_family_fit.json
```

Main result:

| Data proxy | Normalization | Fit quality | Fitted \(\zeta\) |
|---|---|---:|---:|
| HEP-TH citation | literal sample max, all bins | poor, binned KS \(\approx 0.31\) | \(-1.19\) |
| HEP-TH citation | shape-only min-max, all bins | rough, binned KS \(\approx 0.17\) | \(-2.13\) |
| HEP-TH citation | shape-only min-max, top 25% | better tail fit, binned KS \(\approx 0.05\) | \(-3.39\) |
| Common Crawl Web proxy | literal sample max, all bins | poor, binned KS \(\approx 0.48\) | \(-0.03\) |
| Common Crawl Web proxy | shape-only min-max, all bins | weak, binned KS \(\approx 0.30\) | \(-1.76\) |
| Common Crawl Web proxy | shape-only min-max, top 25% | rough tail fit, binned KS \(\approx 0.12\) | \(-5.42\) |

Interpretation:

- The empirical proxy distributions do **not** strictly satisfy Eq. 6.22.
- If Eq. 6.22 is used only as a rough tail-shape approximation, the HEP-TH
  proxy suggests \(\zeta\approx -2\) to \(-3\), equivalently
  \(\rho(\eta)=(1+\theta)(1-\eta)^\theta\) with
  \(\theta=-\zeta\approx 2\) to \(3\).
- The Web-domain proxy is more truncated and less reliable for this specific
  fit; it is useful pedagogically but should not be used to claim a precise
  \(\zeta\).
- A better condensation test is not only fitting \(\rho(\eta)\), but simulating
  the Bianconi-Barabasi process with the empirical/proxy distribution and
  checking whether \(s_{\max}(t)=k_{\max}(t)/\sum_j k_j(t)\) stays finite.

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

- Network Science book, Chapter 6.3 measuring fitness:
  https://networksciencebook.com/chapter/6#measuring-fitness
- Network Science book, Chapter 6.4-6.5:
  https://networksciencebook.com/chapter/6#bose-einstein-condensation
- Network Science book, Figure 6.8:
  https://networksciencebook.com/#figure-6-8
- Kong, Sarshar, and Roychowdhury, *Experience versus talent shapes the
  structure of the Web*, PNAS 105, 13724-13729 (2008).
- Common Crawl Web Graphs:
  https://commoncrawl.org/web-graphs
- Common Crawl Web Graph statistics:
  https://commoncrawl.github.io/cc-webgraph-statistics/
- Bianconi and Barabasi, *Bose-Einstein condensation in complex networks*,
  Physical Review Letters 86, 5632-5635 (2001).
- SNAP HEP-TH citation network:
  https://snap.stanford.edu/data/cit-HepTh.html
- Course repository:
  https://github.com/haotianh9/graph_teaching
