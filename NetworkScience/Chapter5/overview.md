# Chapter 5 Video Sequence

This chapter is now split into three videos. The old standalone algorithm
video and continuum-derivation video were merged so the sequence has less
repetition.

## Video 1 — How Do Hubs Emerge?

Folder: `video5_1`

Script job:

- pose the hub puzzle;
- show random networks vs hub networks;
- introduce growth;
- introduce preferential attachment;
- run the first BA simulation;
- compare BA vs random using a rank-degree profile.

Keep the math light:

\[
N(t)=N_0+t,
\qquad
\Pi_i=\frac{k_i}{\sum_j k_j}.
\]

## Video 2 — From BA Algorithm to Power Law

Folder: `video5_2`

Script job:

- define the algorithm precisely;
- explain the role of \(m\);
- show that \(k_{\mathrm{new}}(t^+)=m\);
- move from the stochastic algorithm to continuum theory;
- derive \(k_i(t)=m(t/t_i)^{1/2}\);
- convert birth times into the degree distribution;
- explain why the BA exponent is \(3\).

This video intentionally drops the former separate scenes on seed choice,
finite-size comparison, and different realizations from the main rendered
sequence. Those ideas can be folded into narration later if needed.

## Video 3 — What BA Explains and What It Misses

Folder: `video5_3`

Script job:

- explain what BA captures well;
- visually compare a BA baseline with a real-network sample;
- introduce fitness;
- introduce aging;
- introduce nonlinear preferential attachment;
- compare clustering coefficients;
- discuss real-network limitations.

Tone:

BA is a useful minimal model, not a complete description of every real network.

## Pacing Rule

Each video should have one main promise. If a scene needs more than one
promise, move the extra idea into narration, notes, or a later chapter.
