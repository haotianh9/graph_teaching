# Chapter 5 Video: Barabási–Albert Networks

## Working title

**How Do Hubs Emerge? The Barabási–Albert Model**

## Core message

Many real networks contain hubs: a few nodes have far more links than most others.
The Barabási–Albert model explains this through two minimal ingredients:

1. **Growth**: the network expands one node at a time.
2. **Preferential attachment**: new nodes are more likely to connect to already well-connected nodes.

Together, these mechanisms generate hub-dominated, scale-free-like networks.

## Target length

First prototype: 3–5 minutes.
Final polished version: 6–8 minutes.

## Visual language

- Nodes are circles.
- Node size represents degree.
- Hubs are highlighted in yellow.
- Newly added nodes are highlighted in red.
- Candidate attachment links are drawn as faint lines.
- Thicker candidate lines mean higher attachment probability.
- BA networks are compared against Erdős–Rényi random networks.

## Mathematical core

Preferential attachment probability:

\[
\Pi_i = \frac{k_i}{\sum_j k_j}
\]

where:

- \(k_i\) is the degree of node \(i\),
- \(\Pi_i\) is the probability that a new node connects to node \(i\).

Interpretation:

> The more links a node already has, the more likely it is to receive new links.

This is the “rich-get-richer” mechanism.

---

# Scene 1: Hook — Why do hubs appear?

## Goal

Introduce the puzzle.

## Visual

Show two networks side by side:

- Left: random network.
- Right: Barabási–Albert network.

The BA network should visibly contain hubs.

## Narration draft

Most networks are not uniform.
In many real systems — the web, citation networks, social networks, infrastructure networks — some nodes become hubs.

A random network gives us some variation, but it does not naturally explain why a few nodes become dramatically more connected than the rest.

So the question is:

**Where do hubs come from?**

## On-screen text

- “Random network”
- “Network with hubs”
- “Why do hubs emerge?”

## Animation notes

1. Fade in title.
2. Create random network on the left.
3. Create BA-like network on the right.
4. Highlight the largest hub.
5. Bring in question text at the bottom.

---

# Scene 2: Ingredient 1 — Growth

## Goal

Show that real networks are not born all at once.

## Visual

Start with a tiny seed graph.
Add one node at a time.

## Narration draft

The first ingredient is growth.

Many real networks are not static.
The web grows as new pages appear.
Citation networks grow as new papers are published.
Social networks grow as new users join.

So instead of assuming a fixed number of nodes, we let the network grow one node at a time.

## On-screen text

- “Ingredient 1: Growth”
- “Add one node at a time”

## Animation notes

1. Start from 3 connected nodes.
2. Add new nodes one by one.
3. Each new node forms links to existing nodes.
4. Keep the animation simple and clear.

---

# Scene 3: Ingredient 2 — Preferential Attachment

## Goal

Explain the rule that new nodes prefer high-degree nodes.

## Visual

Show an existing network.
Show a new red node outside it.
Draw faint candidate lines from the new node to existing nodes.

Candidate lines to high-degree nodes should be thicker.

## Narration draft

The second ingredient is preferential attachment.

When a new node joins the network, it does not choose existing nodes uniformly at random.
Instead, it is more likely to connect to nodes that already have many links.

Mathematically, the probability of choosing node \(i\) is proportional to its degree:

\[
\Pi_i = \frac{k_i}{\sum_j k_j}
\]

This creates a positive feedback loop:

A node with more links is more visible.
Because it is more visible, it attracts more links.
And because it attracts more links, it becomes even more visible.

This is the rich-get-richer mechanism.

## On-screen text

- “Ingredient 2: Preferential attachment”
- “Higher degree → higher probability”
- \(\Pi_i = k_i / \sum_j k_j\)

## Animation notes

1. Show a small network.
2. Highlight the hub.
3. Add a new red node.
4. Draw candidate lines to old nodes.
5. Make the line width proportional to degree.
6. Convert the strongest candidate lines into actual edges.

---

# Scene 4: Building the BA Model

## Goal

Show the full process.

## Visual

Start from a small connected graph.
Repeatedly add nodes using preferential attachment.

## Narration draft

Now we combine the two ingredients.

Start with a small connected seed network.
At every step:

1. Add a new node.
2. Connect it to \(m\) existing nodes.
3. Choose those existing nodes with probability proportional to their degree.

After many repetitions, hubs appear naturally.

They were not manually inserted.
They emerge from the growth rule.

## On-screen text

- “Growth + preferential attachment”
- “Hubs emerge from the rule”

## Animation notes

1. Animate the first few added nodes slowly.
2. Then speed up.
3. As the network grows, scale node size by degree.
4. Highlight the largest hub near the end.

---

# Scene 5: BA vs Random Network

## Goal

Compare BA networks to random networks.

## Visual

Side-by-side comparison:

- Left: Erdős–Rényi random graph.
- Right: BA graph.

Below each network, show a rank-degree plot:

- x-axis: rank
- y-axis: degree
- BA should show a more uneven curve.

## Narration draft

The difference becomes clear when we compare a BA network with a random network of similar size and density.

The random network has some variation, but most nodes have similar degrees.

The BA network is much more heterogeneous.
A small number of nodes collect many links, while most nodes remain weakly connected.

This is the structural signature of preferential attachment.

## On-screen text

- “Random graph”
- “Barabási–Albert graph”
- “Degree heterogeneity”
- “Hubs are emergent”

## Animation notes

1. Show ER graph.
2. Show BA graph.
3. Highlight top hubs.
4. Fade in rank-degree plots.
5. Emphasize the steeper BA curve.

---

# Scene 6: Takeaway

## Goal

Summarize the lesson.

## Visual

Three cards:

1. Growth
2. Preferential attachment
3. Hubs / scale-free structure

## Narration draft

The Barabási–Albert model shows that complex network structure can emerge from very simple rules.

Growth adds new nodes.

Preferential attachment gives popular nodes an advantage.

Together, they generate hubs and broad degree distributions.

This does not explain every property of every real network, but it gives a minimal mechanism for why hubs are so common.

## On-screen text

- “Growth”
- “Preferential attachment”
- “Emergent hubs”
- “Simple rules → complex networks”

---

# First implementation target

The first prototype should include these Manim scenes:

1. `BAOpening`
2. `BAGrowth`
3. `BAPreferentialAttachment`
4. `BABuildingTheModel`
5. `BAComparison`
6. `BATakeaway`

Render each scene separately while developing:

```bash
manim -pql main.py BAOpening
manim -pql main.py BAGrowth
manim -pql main.py BAPreferentialAttachment
manim -pql main.py BABuildingTheModel
manim -pql main.py BAComparison
manim -pql main.py BATakeaway
```

---

# Version 0.1 render checklist

Version 0.1 focuses on making every scene render. Beauty, narration, smoother
transitions, refined layouts, degree-plot polish, pacing, sound, and camera work
are deferred to later versions.

## Scene entrypoints

1. `BAOpening`
2. `BAGrowth`
3. `BAPreferentialAttachment`
4. `BABuildingTheModel`
5. `BAComparison`
6. `BATakeaway`

## Render commands

Run from this folder after activating the Manim conda environment:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim

for scene in BAOpening BAGrowth BAPreferentialAttachment BABuildingTheModel BAComparison BATakeaway; do
  manim -ql main.py "$scene"
done
```

Render scenes sequentially. Parallel Manim renders can race while writing and
cleaning `media/Tex`.

## Current status

- Verified on 2026-05-04 with the sequential low-quality render loop above.
- All six scenes render to `media/videos/main/480p15/`.
- `BAGrowth` and `BABuildingTheModel` use render-safe graph snapshots for
  topology changes.

---

# Version 0.2 equation and mechanism notes

Version 0.2 should keep the v0.1 render stability and add clearer mathematical
signposts where they help the story.

Historical note: this v0.2 section records the broader prototype math pass.
For the current v1.0 Video 1 scope, the detailed algorithm equations are moved
to `../video5_2/`, and the visible Video 1 math is kept light.

## Equations to show when applicable

Growth:

\[
N(t) = N_0 + t
\]

If every new node adds \(m\) edges:

\[
E(t) = E_0 + mt
\]

Preferential attachment:

\[
\Pi_i(t) = \frac{k_i(t)}{\sum_j k_j(t)}
\]

For an undirected network, \(\sum_j k_j(t) = 2E(t)\), so:

\[
\Pi_i(t) = \frac{k_i(t)}{2E(t)}
\]

Expected degree gain for node \(i\) when the new node makes \(m\) links:

\[
\mathbb{E}[\Delta k_i(t)] = m\Pi_i(t)
= m\frac{k_i(t)}{\sum_j k_j(t)}
\]

Degree heterogeneity / comparison scene:

\[
k_{(1)} \ge k_{(2)} \ge \cdots \ge k_{(N)}
\]

where \(k_{(r)}\) is the degree of the node at rank \(r\). This is what the
rank-degree plot displays.

## How to verify the mechanism in code

The BA generator in `main.py` implements preferential attachment directly:

```python
degrees = np.array([G.degree(v) for v in old_nodes], dtype=float)
probabilities = degrees / degrees.sum()
target = rng.choice(old_nodes, p=probabilities)
```

This matches the equation \(\Pi_i = k_i / \sum_j k_j\):

- `degrees` stores each existing node's \(k_i\).
- `degrees.sum()` stores \(\sum_j k_j\).
- `probabilities` stores all \(\Pi_i\) values and sums to 1.
- `rng.choice(..., p=probabilities)` samples targets using those probabilities.
- The `targets` set prevents duplicate links from the same new node.

For v0.2, the animation should make this visible by showing degree values or
probability weights for a few candidate nodes before drawing the chosen links.

## Version 0.2 implementation status

Verified on 2026-05-04.

Implemented in `main.py`:

- Added `ba_growth_trace`, which records each step's before/after graph,
  new node, selected targets, degrees \(k_i\), probabilities \(\Pi_i\), and
  degree sum.
- The generator computes probabilities only as
  `probabilities = degrees / degrees.sum()` and checks that they sum to 1.
- `BAPreferentialAttachment` now uses the stored trace probabilities for
  candidate line widths, target labels, and the final selected edges.
- Growth scenes highlight new nodes in red and selected targets in green.
- `BABuildingTheModel` now uses early slow steps plus milestone snapshots
  instead of rendering every single growth step.
- Main graph layouts now use deterministic layout dictionaries instead of
  implicit `"spring"` layouts.

Equations shown by scene:

- `BAGrowth`: \(N(t)=N_0+t\), \(E(t)=E_0+mt\).
- `BAPreferentialAttachment`: \(\Pi_i=k_i/\sum_j k_j\),
  \(\sum_i\Pi_i=1\), and \(\mathbb{E}[\Delta k_i]=m\Pi_i\).
- `BABuildingTheModel`: \(\Pi_i(t)=k_i(t)/\sum_j k_j(t)\) and
  \(\sum_j k_j(t)=2E(t)\).
- `BAComparison`: \(k_{(1)} \ge k_{(2)} \ge \cdots \ge k_{(N)}\).
- `BATakeaway`: \(N(t)=N_0+t\) and \(\Pi_i=k_i/\sum_j k_j\).

Render verification:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
python -m py_compile main.py

python - <<'PY'
from main import ba_growth_trace
import numpy as np

trace = ba_growth_trace(n_final=25, m=2, seed=8)
for step in trace["steps"]:
    assert np.isclose(sum(step["probabilities"].values()), 1.0)
    assert len(step["targets"]) == 2
    assert all(t in step["degrees"] for t in step["targets"])
print("BA trace invariants passed")
PY
```

On the Dropbox/Windows mount, Manim can fail when deleting temporary TeX/SVG
files in the local `media/` directory. The v0.2 render was verified by putting
Manim's media directory on the Linux filesystem and then copying the final mp4
files back to this folder:

```bash
rm -rf /tmp/chapter5_manim_media

for scene in BAOpening BAGrowth BAPreferentialAttachment BABuildingTheModel BAComparison BATakeaway; do
  manim --media_dir /tmp/chapter5_manim_media -ql main.py "$scene"
done

mkdir -p media/videos/main/480p15
for scene in BAOpening BAGrowth BAPreferentialAttachment BABuildingTheModel BAComparison BATakeaway; do
  cp "/tmp/chapter5_manim_media/videos/main/480p15/${scene}.mp4" "media/videos/main/480p15/${scene}.mp4"
done
```

All six v0.2 mp4 files are available in `media/videos/main/480p15/`.

---

# Video 1 scope reset for Chapter 5 split

This folder is now specifically:

**Video 1 — How do hubs emerge?**

Keep this video focused on the conceptual mechanism:

1. random networks vs hub networks,
2. growth,
3. preferential attachment,
4. one first BA simulation,
5. BA vs random comparison.

Do not expand this video into the precise algorithm lecture. The following
belong in `../video5_2/`:

- exact model definition,
- role of \(m\),
- initial condition,
- finite-size effects,
- different realizations,
- the edge count equation \(E(t)=E_0+mt\),
- the identity \(\sum_j k_j(t)=2E(t)\),
- expected gain \(\mathbb{E}[\Delta k_i(t)] = m\Pi_i(t)\).

For Video 1, the visible math should stay light:

- `BAGrowth`: \(N(t)=N_0+t\).
- `BAPreferentialAttachment`: \(\Pi_i=k_i/\sum_j k_j\) and
  \(\sum_i\Pi_i=1\).
- `BABuildingTheModel`: \(\Pi_i(t)=k_i(t)/\sum_j k_j(t)\).
- `BAComparison`: rank-degree profiles, with
  \(k_{(1)} \ge k_{(2)} \ge \cdots \ge k_{(N)}\).

# Version 0.3 direction

Version 0.3 starts the teaching-video layer:

- add short on-screen narration captions;
- make growth/simulation transitions feel less abrupt;
- add a live rank-degree profile during the first BA simulation;
- keep sound, voice recording, and camera polish for Version 1.0.

## Current v0.3 implementation notes

Implemented in `main.py`:

- `make_caption(...)` creates subtitle-style narration captions.
- `BAOpening`, `BAGrowth`, `BAPreferentialAttachment`, and
  `BABuildingTheModel` now include narration captions.
- `BAGrowth` keeps only \(N(t)=N_0+t\), so the scene stays about growth rather
  than the precise \(m\)-edge algorithm.
- `BAPreferentialAttachment` keeps only the probability rule and normalization.
- `BABuildingTheModel` now includes a compact live rank-degree plot so students
  can see hubs appearing in the degree profile, not only in the node-link graph.

## Video 1 timing target

Target final length: **4-6 minutes**.

Prototype render length can be shorter because scenes are rendered separately,
but the script should fit this pacing:

1. Hook / puzzle: 35-45 seconds.
2. Growth ingredient: 45-55 seconds.
3. Preferential attachment ingredient: 60-75 seconds.
4. First BA simulation: 60-80 seconds.
5. BA vs random comparison: 45-60 seconds.
6. Takeaway: 25-35 seconds.

This gives enough time to explain the mechanism without drifting into Video 2.

## Draft narration script

`BAOpening`:
Most networks are not uniform. In many systems, a few nodes collect many more
links than the rest. A random graph gives some variation, but the hub pattern is
much stronger in growing networks. So the question is: why do hubs appear?

`BAGrowth`:
The first ingredient is growth. The network is not created all at once. It
expands as new nodes arrive, one step at a time.

`BAPreferentialAttachment`:
The second ingredient is preferential attachment. A new node is more likely to
connect to a node that already has many links. The thicker candidate lines show
larger probabilities, and the selected targets use those same probabilities.

`BABuildingTheModel`:
Now repeat the two local rules. Add a new node, connect it to existing nodes,
and give high-degree nodes an advantage. After many repetitions, hubs appear
without being manually placed.

`BAComparison`:
Compared with a random network of similar size and density, the BA network has
a more uneven degree profile. A small number of nodes become much more
connected than the rest.

`BATakeaway`:
The lesson is that simple local rules can generate complex network structure.
Growth plus preferential attachment gives a minimal mechanism for hubs.

## v0.3 render checklist

Run from `video5_1`:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
python -m py_compile main.py

rm -rf /tmp/chapter5_video5_1_v03
for scene in BAOpening BAGrowth BAPreferentialAttachment BABuildingTheModel BAComparison BATakeaway; do
  manim --media_dir /tmp/chapter5_video5_1_v03 -ql main.py "$scene"
done
```

After visual QA, copy the final mp4s back:

```bash
mkdir -p media/videos/main/480p15
for scene in BAOpening BAGrowth BAPreferentialAttachment BABuildingTheModel BAComparison BATakeaway; do
  cp "/tmp/chapter5_video5_1_v03/videos/main/480p15/${scene}.mp4" "media/videos/main/480p15/${scene}.mp4"
done
```

---

# Version 1.0 combined video plan and status

Version 1.0 turns the separate prototype scenes into one combined Video 1:

**Video 5.1 — How Do Hubs Emerge?**

Target combined length: **4-6 minutes**.

Final combined output:

```text
media/videos/video5_1_final_480p15.mp4
```

## v1.0 implementation status

Implemented in `main.py`:

- Added paced caption replacement through `replace_caption(...)`.
- Caption replacement fades the old caption out before fading the next one in,
  so caption beats do not stack during transitions.
- Expanded scene timing with narration beats rather than anonymous pauses.
- Kept Video 1 math light:
  \(N(t)=N_0+t\), \(\Pi_i=k_i/\sum_j k_j\), and rank-degree ordering.
- Kept detailed algorithm material in `../video5_2/note.md`.
- Updated `BATakeaway` with high-contrast yellow directional arrows and lifted
  the final message above the bottom video-control area.

## v1.0 script and timing table

| Scene | Target | Narration text | Main visual beats |
|---|---:|---|---|
| `BAOpening` | 35-45s | Many real networks are not uniform. A random graph has variation, but growing networks can develop much stronger hubs. The puzzle is to explain where those hubs come from. | Title, random graph, growing graph, hub rings, question. |
| `BAGrowth` | 40-50s | The first ingredient is growth. The network is not born all at once. New nodes arrive over time, so the node count increases. Growth sets the stage, but we still need a target rule. | Growth equation, node counter, red new nodes, green selected targets. |
| `BAPreferentialAttachment` | 55-70s | The second ingredient is preferential attachment. New nodes are more likely to choose nodes that already have many links. Wider candidate lines mean larger probabilities. The sampled targets become real edges. | Probability equation, candidate lines, probability labels, selected targets, rich-get-richer text. |
| `BABuildingTheModel` | 65-85s | Combine growth with preferential attachment. At each step, add one node and choose targets by degree. Early choices matter. A few nodes pull ahead, and hubs appear without being inserted by hand. | Rule list, live graph, live rank-degree profile, milestone snapshots, final hubs. |
| `BAComparison` | 45-60s | Compare the BA network with a random network of similar density. The random network is relatively even. The BA network is more heterogeneous, and the rank-degree plots summarize this pattern. | ER graph, BA graph, hub rings, heterogeneity message, rank-degree plots. |
| `BATakeaway` | 30-40s | Growth plus preferential attachment gives a minimal mechanism for hubs. Simple local rules can generate complex network structure. | Three cards, visible yellow arrows, key equations, final message. |

## v1.0 render and combine workflow

Run from `video5_1`:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
python -m py_compile main.py

rm -rf /tmp/chapter5_video5_1_v10
for scene in BAOpening BAGrowth BAPreferentialAttachment BABuildingTheModel BAComparison BATakeaway; do
  manim --media_dir /tmp/chapter5_video5_1_v10 -ql main.py "$scene"
done
```

Combine the six scene renders:

```bash
cat > /tmp/chapter5_video5_1_v10/concat.txt <<'EOF'
file '/tmp/chapter5_video5_1_v10/videos/main/480p15/BAOpening.mp4'
file '/tmp/chapter5_video5_1_v10/videos/main/480p15/BAGrowth.mp4'
file '/tmp/chapter5_video5_1_v10/videos/main/480p15/BAPreferentialAttachment.mp4'
file '/tmp/chapter5_video5_1_v10/videos/main/480p15/BABuildingTheModel.mp4'
file '/tmp/chapter5_video5_1_v10/videos/main/480p15/BAComparison.mp4'
file '/tmp/chapter5_video5_1_v10/videos/main/480p15/BATakeaway.mp4'
EOF

ffmpeg -y -f concat -safe 0 \
  -i /tmp/chapter5_video5_1_v10/concat.txt \
  -c copy media/videos/video5_1_final_480p15.mp4
```

Copy scene mp4s back after QA:

```bash
mkdir -p media/videos/main/480p15
for scene in BAOpening BAGrowth BAPreferentialAttachment BABuildingTheModel BAComparison BATakeaway; do
  cp "/tmp/chapter5_video5_1_v10/videos/main/480p15/${scene}.mp4" "media/videos/main/480p15/${scene}.mp4"
done
```

## v1.0 acceptance checklist

- All six scenes render sequentially.
- `media/videos/video5_1_final_480p15.mp4` exists.
- Combined duration is between 4 and 6 minutes.
- `BATakeaway` arrows are clearly visible at 480p.
- Contact sheets and selected full-size frames show no major text, equation,
  plot, card, or caption collisions.

## v1.0 render status

Verified on 2026-05-04 in the `manim` conda environment.

| Scene | Rendered duration | Status |
|---|---:|---|
| `BAOpening` | 38.2s | Rendered |
| `BAGrowth` | 42.3s | Rendered |
| `BAPreferentialAttachment` | 64.0s | Rendered |
| `BABuildingTheModel` | 71.2s | Rendered |
| `BAComparison` | 53.5s | Rendered |
| `BATakeaway` | 40.0s | Rendered |
| Combined mp4 | 309.3s | Rendered |

Final combined output:

```text
media/videos/video5_1_final_480p15.mp4
```

Visual QA checked selected full-size frames and contact sheets for
`BABuildingTheModel`, `BAComparison`, and `BATakeaway`. The final takeaway
arrows are thick yellow directional connectors, and the BA simulation final
message no longer collides with a bottom caption.

Opening visual update on 2026-05-04:

- Replaced the opening Erdős-Rényi sample with a connected random graph, so no
  isolated node appears far from the rest of the cloud.
- Loosened the opening graph layouts with a larger spring spacing, making both
  the random and growing graph clouds less compact.
- Rebuilt `media/videos/main/480p15/BAOpening.mp4` and the combined
  `media/videos/video5_1_final_480p15.mp4`.

## v1.0 full narration transcript for review

Book anchor: Chapter 5 of *Network Science* frames the BA model as the
combination of two mechanisms that random networks lack: network growth and
preferential attachment. The chapter defines the model by adding new nodes over
time and choosing their targets with probability proportional to degree,
\(\Pi_i = k_i / \sum_j k_j\). This transcript keeps Video 5.1 focused on that
conceptual mechanism; model-definition details, derivation, and limitations
remain for Videos 5.2-5.3.

Sources used for alignment:

- <https://www.networksciencebook.com/chapter/5>
- <https://barabasi.com/f/622.pdf>

Target voice pace: about 135-145 words per minute. Current combined video:
309.3 seconds, about 5 minutes 9 seconds.

| Scene | Rendered duration | Approx. words | Speaking goal |
|---|---:|---:|---|
| `BAOpening` | 38.2s | 80-95 | Hook: random networks miss strong hubs. |
| `BAGrowth` | 42.3s | 90-105 | Ingredient 1: networks grow over time. |
| `BAPreferentialAttachment` | 64.0s | 140-155 | Ingredient 2: degree becomes attachment probability. |
| `BABuildingTheModel` | 71.2s | 155-175 | Repeat the two rules and watch hubs emerge. |
| `BAComparison` | 53.5s | 115-130 | Compare BA heterogeneity with random linking. |
| `BATakeaway` | 40.0s | 80-95 | Summarize and point to the next videos. |

### `BAOpening`

Chapter 5 starts from a simple mismatch. Random networks can have degree
variation, but in many real systems the variation is much stronger. A few
webpages, papers, people, airports, or proteins collect many more links than
typical nodes. Those unusually connected nodes are hubs. If links were placed
uniformly at random, hubs would be rare and weak. So the question for this
video is not just: what does a hub look like? The question is: what process can
make hubs appear?

### `BAGrowth`

The first missing ingredient is growth. Real networks are not usually drawn all
at once. A citation network grows when new papers appear. The web grows when
new pages are published. A collaboration network grows when new people or
projects enter. In the BA picture we mark this with \(N(t)=N_0+t\): at each
step one new node joins the existing network. Growth matters because early nodes
have more time to receive links. But growth alone does not tell us where the new
links go. For that we need a second rule.

### `BAPreferentialAttachment`

The second ingredient is preferential attachment. When a new node arrives, it
does not choose all existing nodes equally. Nodes that already have many links
are more visible, easier to find, or more attractive targets. The model
expresses that idea with
\[
\Pi_i = \frac{k_i}{\sum_j k_j}.
\]
The numerator is the degree of node \(i\). The denominator adds up the degrees
of all current nodes, turning those degrees into probabilities. So a node with
twice as many links gets twice the chance of receiving the next link. This is
probabilistic, not deterministic. Low-degree nodes can still be chosen; they are
just less likely. The thin candidate lines show smaller probabilities, and the
thick lines show larger ones. Only the sampled targets become real edges. This
is the local rule behind the rich-get-richer effect.

### `BABuildingTheModel`

Now we combine the two rules and repeat them. Start with a small connected seed.
Add one new node. Give it a few links. Choose its targets using preferential
attachment. Then do it again. At the beginning the network is small, so each
random choice is visible. A node that is chosen once has a higher degree, which
makes it a little more likely to be chosen again. That extra link increases its
advantage for future steps. Over many repetitions, small early differences are
amplified. Nobody labels a node as a hub in advance. The hub emerges from the
feedback loop. The rank-degree plot tells the same story numerically: most nodes
stay near the low-degree end, while a few nodes pull away at the top. That is
the conceptual point of the Barabasi-Albert model: simple local decisions can
create global structure.

### `BAComparison`

To see why this matters, compare the BA network with a random network of similar
size and density. The random graph still has some high-degree nodes, because
randomness always creates variation. But the variation is relatively mild: the
degree profile drops more gradually. In the BA network, preferential attachment
concentrates links more strongly. A few nodes become visibly larger hubs, and
the rank-degree curve bends downward faster. This is why the BA mechanism is
useful as a first explanation of hub formation. It does not claim every real
network is exactly BA. It gives a minimal process that can create the kind of
heterogeneity random linking struggles to produce.

### `BATakeaway`

The message is simple. Growth gives nodes different histories. Preferential
attachment turns those histories into different chances of receiving future
links. Together they produce a rich-get-richer process, and hubs can emerge
without any central planner. This is the first step of Chapter 5: a mechanism
for how hubs appear. In the next videos, we can make the model precise, derive
the power law, and then ask what the BA model explains and what it misses.

---

## 2026-05-06 bilingual 720p export

Current review output:

```text
media/videos/video5_1_bilingual_final_720p30.mp4
```

Length: **329.2s**, about **5 minutes 29 seconds**.

This export supersedes the earlier English-only 480p draft for review.
The editable bilingual transcript is:

```text
transcript_draft.md
```

Changes in this pass:

- Added bilingual English/Chinese screen captions and bilingual key labels.
- Exported at `-qm` Manim quality: **720p30**.
- Added the first in-video citation when the Barabási-Albert model is first
  mentioned:
  Barabási and Albert, *Science* 286, 509-512 (1999).
- Clarified that \(\Pi_i\) does not set the new node's initial number of links;
  in the demo, the new node brings a fixed two links as part of the model setup,
  and \(\Pi_i\) chooses their existing targets.
- Removed the Video 5.1 takeaway reference to the role of \(m\); that belongs
  in Video 5.2.
- Added a final reference card with the Network Science book URL and the course
  GitHub repository URL.

Current scene durations:

| Scene | Duration |
|---|---:|
| `BAOpening` | 38.1s |
| `BAGrowth` | 52.5s |
| `BAPreferentialAttachment` | 71.1s |
| `BABuildingTheModel` | 70.6s |
| `BAComparison` | 53.3s |
| `BATakeaway` | 43.6s |

Verification:

- `python -m py_compile main.py` passed.
- All six scenes rendered sequentially at 720p30.
- `ffmpeg` concat produced the combined bilingual mp4.
- Selected 720p frames checked for the opening question, paper citation,
  target-selection annotation, comparison plots, and final takeaway arrows.

---

## 2026-05-06 Chinese TTS timing test

Current Chinese-audio timing-test output:

```text
media/videos/video5_1_zh_audio_test_720p30.mp4
```

Length: **432.2s**, about **7 minutes 12 seconds**.

Current 1.5x review output:

```text
media/videos/video5_1_zh_audio_test_720p30_1p5x.mp4
```

Length: **288.3s**, about **4 minutes 48 seconds**.

This 1.5x file speeds up both video and audio together with `setpts=PTS/1.5`
and `atempo=1.5`, so the narration remains synchronized with the visuals.

This is intentionally a timing-test render, not the final voiced version. The
full Chinese transcript is longer than the current 5.4-minute visual edit, so
the mux script preserves the full audio and freezes each scene's final frame
when the narration runs longer than the visual.

Generated audio files:

```text
assets/audio/zh/*.mp3
assets/audio/zh/*.txt
```

Workflow scripts:

```text
scripts/generate_chinese_audio.py
scripts/mux_chinese_audio.py
```

Commands:

```bash
source /home/haotian/miniconda3/etc/profile.d/conda.sh
conda activate manim
python scripts/generate_chinese_audio.py
python scripts/mux_chinese_audio.py
```

Scene timing comparison:

| Scene | Visual duration | Chinese TTS duration |
|---|---:|---:|
| `BAOpening` | 38.1s | 47.8s |
| `BAGrowth` | 52.5s | 67.8s |
| `BAPreferentialAttachment` | 71.1s | 114.4s |
| `BABuildingTheModel` | 70.6s | 86.0s |
| `BAComparison` | 53.3s | 67.5s |
| `BATakeaway` | 43.6s | 48.8s |

Implication:

- The Chinese narration needs either a shorter audio script or a longer visual
  edit.
- `BAPreferentialAttachment` is the largest mismatch and should be trimmed or
  split into more visual beats first.
- The project is now ready for separate recorded audio: replace the matching
  mp3 files in `assets/audio/zh/`, then rerun `scripts/mux_chinese_audio.py`.

Visual cleanup in this pass:

- Kept the Barabási-Albert model name and paper citation in English only on
  screen.
- Kept bilingual captions where they help explain the concept.

---

## 2026-05-10 end reference card

All Chapter 5 movie endings should include:

```text
Network Science book
https://www.networksciencebook.com/

Course code and teaching materials
https://github.com/haotianh9/graph_teaching
```

Implemented in:

- `video5_1/main.py`: `make_reference_end_card()` and `BATakeaway`
- `video5_2/main.py`: `make_reference_end_card()` and `BAAlgorithmTakeaway`

Updated outputs:

```text
media/videos/video5_1_bilingual_final_720p30.mp4
media/videos/video5_1_zh_audio_test_720p30.mp4
media/videos/video5_1_zh_audio_test_720p30_1p5x.mp4
```

---

## 2026-05-11 recorded Chinese narration alignment

Recorded narration supplied by instructor:

```text
media/audio/audio1359157491.m4a
```

Recorded audio duration: **363.6s**, about **6 minutes 4 seconds**.

Transcription workflow:

```bash
python scripts/transcribe_recorded_audio_whisper.py --model base
python scripts/align_recorded_audio.py
```

The Whisper `base` model was used for the first pass. It is good enough for
scene-level alignment, but it misrecognizes some technical words, so both raw
and cleaned review transcripts are saved.

Transcript outputs:

```text
media/audio/transcripts/audio1359157491_zh_transcript.json
media/audio/transcripts/audio1359157491_zh_transcript.txt
media/audio/transcripts/audio1359157491_zh_transcript.srt
media/audio/transcripts/audio1359157491_zh_transcript.md
media/audio/transcripts/audio1359157491_scene_transcript_review.md
```

Alignment outputs:

```text
media/audio/recorded_segments/
media/audio/transcripts/audio1359157491_alignment.json
media/audio/transcripts/audio1359157491_alignment.md
media/videos/main/720p30_recorded_aligned/
media/videos/video5_1_recorded_audio_aligned_720p30.mp4
```

Final aligned video duration: **384.8s**, about **6 minutes 25 seconds**.

Scene-level alignment:

| Scene | Recorded audio | Original video | Alignment |
|---|---:|---:|---|
| `BAOpening` | 52.0s | 38.1s | video slowed to audio |
| `BAGrowth` | 80.0s | 52.5s | video slowed to audio |
| `BAPreferentialAttachment` | 108.0s | 71.1s | video slowed to audio |
| `BABuildingTheModel` | 56.0s | 70.6s | video sped up to audio |
| `BAComparison` | 45.0s | 53.3s | video sped up to audio |
| `BATakeaway` | 22.6s | 43.6s | visual kept full length; audio padded with silence |

Notes for next pass:

- The recorded narration includes discussion of the new node's initial degree
  and says this will be discussed in the next lesson. This is now aligned in
  `BAPreferentialAttachment`/`BATakeaway`; if Video 5.1 should avoid this
  entirely, the audio should be rerecorded or this section should be edited
  out.
- `BAGrowth` and `BAPreferentialAttachment` required the largest slowdowns, so
  these two scenes would benefit from additional visual beats if we polish this
  version further.
