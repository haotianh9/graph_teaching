# Chapter 6 Video Plan

Chapter 5 ended with the main lesson of the Barabasi-Albert model: growth plus
preferential attachment can create hubs, but BA is only a baseline. Chapter 6
adds fitness and then asks what happens when evolving-network dynamics become
strong enough to change the network's qualitative phase.

Chapter 6 has exactly two videos:

```text
video6_1  infer fitness from growth data
video6_2  condensation and evolving-network phase transitions
```

## Video Sequence

### 6.1 — Inferring Fitness from Growth

This video gives only a short reminder of the Bianconi-Barabasi fitness model,
because the model was already introduced at the end of Chapter 5:

\[
\Pi_i=\frac{\eta_i k_i}{\sum_j \eta_j k_j}.
\]

The main focus is inference. Fitness is treated not only as a model parameter,
but as something that can be estimated from growth histories. The
central visual equation is

\[
\ln k_i(t)=\beta(\eta_i)\ln t+B_i.
\]

It explains why slope in a log-log growth plot estimates effective
fitness, why early popularity can mislead, and why citation data must account
for aging and observation windows.

### 6.2 — Condensation and Evolving-Network Phase Transitions

This video focuses on Chapter 6.4 and 6.5: Bose-Einstein condensation and
broader evolving-network mechanisms.

The key conceptual contrast is:

- fit-get-rich phase: fitter nodes grow faster, but the largest hub's share of
  all links vanishes as the network grows;
- condensed phase: one exceptionally fit node captures a finite fraction of all
  links.

The video introduces the Bose-gas mapping only at a teaching level:

\[
\varepsilon_i=-\frac{1}{\beta}\ln\eta_i,
\]

and uses the representative distribution

\[
\rho(\eta)=(\lambda+1)(1-\eta)^\lambda
\]

to explain how a fitness distribution can push the network across a phase
transition. The final section broadens to evolving-network mechanisms:
initial attractiveness, aging, deletion, internal links, and the general lesson
that topology follows dynamics.

## Shared Pipeline

Chapter 6 videos use `NetworkScience/video_pipeline/` for:

- sequential Manim rendering;
- Chinese TTS generation;
- scene audio muxing;
- final concat;
- optional human-audio muxing;
- title, 4:3 cover, and 16:9 cover generation;
- video description generation.

Each active video folder owns a small `video_config.py` and thin scripts in
`scripts/` that call the shared package.
