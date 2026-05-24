from manim import *
import networkx as nx
import numpy as np


# ============================================================
# Visual constants
# ============================================================

NODE_COLOR = BLUE_C
HUB_COLOR = YELLOW
NEW_NODE_COLOR = RED
EDGE_COLOR = GREY_B
TEXT_COLOR = WHITE
FAINT_COLOR = GREY_C
TARGET_COLOR = GREEN_C
NETWORK_SCIENCE_BOOK_URL = "https://www.networksciencebook.com/"
GITHUB_REPO_URL = "https://github.com/haotianh9/graph_teaching"
DEGREE_EXPONENT_URL = "networksciencebook.com/chapter/4#degree-exponent"


# ============================================================
# BA helpers
# ============================================================

def ba_growth_trace(n_final=50, m=2, seed=1, initial_graph=None):
    """
    Generate a Barabasi-Albert growth trace.

    Each step records before/after graphs, selected targets, degrees k_i,
    and preferential attachment probabilities Pi_i = k_i / sum_j k_j.
    """
    if m < 1:
        raise ValueError("m must be at least 1")

    rng = np.random.default_rng(seed)

    if initial_graph is None:
        G = nx.complete_graph(m + 1)
    else:
        G = nx.convert_node_labels_to_integers(initial_graph.copy())
        if G.number_of_nodes() < m:
            raise ValueError("initial graph must have at least m nodes")
        if not nx.is_connected(G):
            raise ValueError("initial graph must be connected")

    if n_final < G.number_of_nodes():
        raise ValueError("n_final must be at least the initial graph size")

    if sum(dict(G.degree()).values()) <= 0:
        raise ValueError("initial graph must have positive degree sum")

    graphs = [G.copy()]
    steps = []
    next_node = G.number_of_nodes()

    while G.number_of_nodes() < n_final:
        before = G.copy()
        old_nodes = list(G.nodes())
        if len(old_nodes) < m:
            raise ValueError("need at least m existing nodes before sampling")

        degrees = np.array([G.degree(v) for v in old_nodes], dtype=float)
        probabilities = degrees / degrees.sum()
        if not np.isclose(probabilities.sum(), 1.0):
            raise ValueError("preferential attachment probabilities must sum to 1")

        targets = set()
        while len(targets) < m:
            target = rng.choice(old_nodes, p=probabilities)
            targets.add(int(target))

        new_node = next_node
        G.add_node(new_node)
        for target in targets:
            G.add_edge(new_node, target)

        after = G.copy()
        graphs.append(after)
        steps.append(
            {
                "before": before,
                "after": after,
                "new_node": int(new_node),
                "targets": sorted(targets),
                "degrees": {
                    int(node): int(degree)
                    for node, degree in zip(old_nodes, degrees)
                },
                "probabilities": {
                    int(node): float(probability)
                    for node, probability in zip(old_nodes, probabilities)
                },
                "degree_sum": float(degrees.sum()),
            }
        )
        next_node += 1

    return {"initial": graphs[0], "graphs": graphs, "steps": steps}


def ba_graph(n_final=50, m=2, seed=1, initial_graph=None):
    return ba_growth_trace(
        n_final=n_final,
        m=m,
        seed=seed,
        initial_graph=initial_graph,
    )["graphs"][-1]


def spring_layout_3d(G, seed=1, scale=3.0, k=None, iterations=60):
    pos_2d = nx.spring_layout(G, seed=seed, scale=1.0, k=k, iterations=iterations)
    return {
        v: np.array([scale * pos_2d[v][0], scale * pos_2d[v][1], 0.0])
        for v in G.nodes()
    }


def subset_layout(layout, nodes):
    return {v: layout[v] for v in nodes if v in layout}


def top_degree_nodes(G, top=1):
    ranked = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    return [node for node, degree in ranked[:top]]


# ============================================================
# Manim helpers
# ============================================================

def make_caption(text, font_size=23, color=TEXT_COLOR, buff=0.2):
    caption = Text(text, font_size=font_size, color=color)
    max_width = config.frame_width - 1.0
    if caption.width > max_width:
        caption.scale_to_fit_width(max_width)
    background = BackgroundRectangle(caption, color=BLACK, fill_opacity=0.72, buff=0.14)
    group = VGroup(background, caption)
    group.to_edge(DOWN, buff=buff)
    return group


def make_graph_mobject(
    G,
    layout=None,
    hub_nodes=None,
    highlight_nodes=None,
    min_radius=0.045,
    max_radius=0.16,
    edge_opacity=0.35,
    edge_width=1.1,
    edge_color=EDGE_COLOR,
):
    if hub_nodes is None:
        hub_nodes = []
    if highlight_nodes is None:
        highlight_nodes = {}
    if layout is None:
        layout = spring_layout_3d(G)

    degrees = dict(G.degree())
    max_degree = max(max(degrees.values()) if degrees else 1, 1)

    vertex_config = {}
    for node in G.nodes():
        degree_fraction = degrees[node] / max_degree
        radius = min_radius + (max_radius - min_radius) * degree_fraction

        color = NODE_COLOR
        if node in hub_nodes:
            color = HUB_COLOR
        if node in highlight_nodes:
            color = highlight_nodes[node]

        vertex_config[node] = {
            "radius": radius,
            "fill_color": color,
            "fill_opacity": 1.0,
            "stroke_color": WHITE,
            "stroke_width": 0.7,
        }

    edge_config = {
        "stroke_color": edge_color,
        "stroke_width": edge_width,
        "stroke_opacity": edge_opacity,
    }

    return Graph.from_networkx(
        G,
        layout=layout,
        labels=False,
        vertex_config=vertex_config,
        edge_config=edge_config,
    )


def make_node_ring(graph, node, color=YELLOW, radius_buff=0.07, stroke_width=4):
    vertex = graph.vertices[node]
    radius = max(vertex.width, vertex.height) / 2 + radius_buff
    ring = Circle(radius=radius)
    ring.set_stroke(color=color, width=stroke_width)
    ring.move_to(vertex.get_center())
    return ring


def make_node_rings(graph, nodes, color=YELLOW, radius_buff=0.07, stroke_width=4):
    return VGroup(
        *[
            make_node_ring(
                graph,
                node,
                color=color,
                radius_buff=radius_buff,
                stroke_width=stroke_width,
            )
            for node in nodes
        ]
    )


def make_rank_degree_plot(
    G,
    title_text="rank-degree",
    width=3.0,
    height=1.3,
    include_labels=True,
    stroke_width=3,
):
    degrees = np.array(sorted([d for _, d in G.degree()], reverse=True), dtype=float)
    if len(degrees) == 0:
        degrees = np.array([0.0])
    n = len(degrees)
    max_degree = max(float(np.max(degrees)), 1.0)

    axes = Axes(
        x_range=[1, n, max(1, n // 3)],
        y_range=[0, max_degree + 1, max(1, int(max_degree // 3) or 1)],
        x_length=width,
        y_length=height,
        tips=False,
        axis_config={"include_numbers": False, "stroke_width": 1.2},
    )

    points = [
        axes.c2p(rank, degree)
        for rank, degree in zip(np.arange(1, n + 1), degrees)
    ]
    curve = VMobject()
    curve.set_points_as_corners(points)
    curve.set_stroke(YELLOW, width=stroke_width)

    parts = [axes, curve]
    if title_text:
        title = Text(title_text, font_size=18)
        title.next_to(axes, UP, buff=0.12)
        parts.insert(0, title)

    if include_labels:
        x_label = Text("rank", font_size=15)
        x_label.next_to(axes.x_axis, DOWN, buff=0.1)
        y_label = Text("degree", font_size=15)
        y_label.rotate(PI / 2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.1)
        parts.extend([x_label, y_label])

    return VGroup(*parts)


def make_bullet_list(lines, font_size=24, line_buff=0.18):
    bullets = VGroup(
        *[Text(line, font_size=font_size) for line in lines]
    ).arrange(DOWN, aligned_edge=LEFT, buff=line_buff)
    return bullets


def make_reference_end_card():
    title = Text("References", font_size=38, color=YELLOW)
    book = VGroup(
        Text("Network Science book", font_size=25, color=WHITE),
        Text(NETWORK_SCIENCE_BOOK_URL, font_size=21, color=GREY_A),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    repo = VGroup(
        Text("Course code and teaching materials", font_size=25, color=WHITE),
        Text(GITHUB_REPO_URL, font_size=21, color=GREY_A),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body = VGroup(book, repo).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
    box = RoundedRectangle(
        width=8.7,
        height=2.7,
        corner_radius=0.12,
        stroke_color=GREY_B,
        stroke_width=1.8,
    )
    body.move_to(box.get_center())
    card = VGroup(title, VGroup(box, body)).arrange(DOWN, buff=0.38)
    card.move_to(ORIGIN)
    return card


def boxed_group(title, items, color=WHITE, width=4.2, height=2.6):
    title_mob = Text(title, font_size=28, color=color)
    body = make_bullet_list(items, font_size=22, line_buff=0.2)
    content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=2.0,
    )
    content.move_to(box.get_center())
    return VGroup(box, content)


def make_highlight_outline(mobject, color=YELLOW, buff=0.045, stroke_width=2.2):
    outline = SurroundingRectangle(
        mobject,
        color=color,
        buff=buff,
        stroke_width=stroke_width,
    )
    outline.set_z_index(50)
    return outline


def hold_highlight(scene, mobject, duration=2.0, color=YELLOW, buff=0.045, stroke_width=2.2):
    """Keep a visible highlight on the object for one narration beat."""
    outline = make_highlight_outline(mobject, color=color, buff=buff, stroke_width=stroke_width)
    fade_time = min(0.28, duration / 4)
    scene.play(FadeIn(outline), run_time=fade_time)
    scene.wait(max(duration - 2 * fade_time, 0.05))
    scene.play(FadeOut(outline), run_time=fade_time)


def sync_highlight(scene, mobject, start, end, color=YELLOW, buff=0.045, stroke_width=2.2):
    """Highlight an object during an exact scene-relative audio interval."""
    if scene.time < start:
        scene.wait(start - scene.time)

    duration = max(end - max(scene.time, start), 0.08)
    outline = make_highlight_outline(mobject, color=color, buff=buff, stroke_width=stroke_width)
    scene.add(outline)
    scene.wait(duration)
    scene.remove(outline)


def sync_multi_highlight(scene, mobjects, start, end, color=YELLOW, buff=0.035, stroke_width=2.0):
    """Highlight several targets with separate tight outlines."""
    if scene.time < start:
        scene.wait(start - scene.time)

    duration = max(end - max(scene.time, start), 0.08)
    outlines = VGroup(
        *[
            make_highlight_outline(mobject, color=color, buff=buff, stroke_width=stroke_width)
            for mobject in mobjects
        ]
    )
    scene.add(outlines)
    scene.wait(duration)
    scene.remove(outlines)


def sync_pause(scene, start, end):
    """Hold timing without drawing an extra visual highlight."""
    if scene.time < start:
        scene.wait(start - scene.time)
    scene.wait(max(end - max(scene.time, start), 0.08))


def finish_scene_at(scene, duration):
    if scene.time < duration:
        scene.wait(duration - scene.time)


# ============================================================
# Scene 1: Precise algorithm definition
# ============================================================

class BAAlgorithmDefinition(Scene):
    def construct(self):
        title = Title(r"From Attachment Rules to $k^{-3}$")

        inputs = boxed_group(
            "Inputs",
            [
                "final size N",
                "attachment number m",
                "connected seed graph G0",
            ],
            color=BLUE_C,
            width=4.1,
            height=2.25,
        )
        inputs.to_corner(UL, buff=0.55).shift(DOWN * 0.75)

        loop = make_bullet_list(
            [
                "1. add one new node",
                "2. compute existing degrees",
                "3. convert degrees to probabilities",
                "4. sample m distinct targets",
                "5. add the new edges",
            ],
            font_size=24,
            line_buff=0.16,
        )
        loop.next_to(inputs, DOWN, aligned_edge=LEFT, buff=0.35)

        equations = VGroup(
            MathTex(r"N(t)=N_0+t", font_size=32),
            MathTex(r"E(t)=E_0+mt", font_size=32),
            MathTex(r"\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        equations.to_corner(UR, buff=0.65).shift(DOWN * 0.85)

        trace = ba_growth_trace(n_final=8, m=2, seed=12)
        step = trace["steps"][2]
        before = step["before"]
        after = step["after"]
        layout = spring_layout_3d(after, seed=8, scale=2.2, k=0.9, iterations=80)
        before_graph = make_graph_mobject(
            before,
            layout=subset_layout(layout, before.nodes()),
            edge_opacity=0.45,
        )
        after_graph = make_graph_mobject(
            after,
            layout=layout,
            highlight_nodes={
                step["new_node"]: NEW_NODE_COLOR,
                **{target: TARGET_COLOR for target in step["targets"]},
            },
            edge_opacity=0.45,
        )
        rings = VGroup(
            make_node_ring(after_graph, step["new_node"], color=NEW_NODE_COLOR),
            make_node_rings(after_graph, step["targets"], color=TARGET_COLOR),
        )
        focus_rings = VGroup(rings[0], *rings[1])
        graph_group = VGroup(after_graph, rings)
        before_graph.move_to(RIGHT * 2.35 + DOWN * 0.7)
        graph_group.move_to(RIGHT * 2.35 + DOWN * 0.7)

        caption = make_caption(
            "The algorithm is a loop: add a node, then use degrees as probabilities."
        )

        self.add(title, inputs, equations, loop, graph_group, caption)
        sync_pause(self, 0.0, 24.0)
        sync_multi_highlight(self, focus_rings, 24.0, 32.0)
        sync_pause(self, 32.0, 63.0)
        sync_highlight(self, equations[2], 63.0, 68.0)
        sync_pause(self, 68.0, 74.0)
        sync_multi_highlight(self, focus_rings, 74.0, 79.0)
        finish_scene_at(self, 79.0)


# ============================================================
# Scene 2: Role of m
# ============================================================

class BARoleOfM(Scene):
    def construct(self):
        title = Title("The Role of m")
        equations = VGroup(
            MathTex(r"k_{\mathrm{new}}(t^+)=m", font_size=36),
            MathTex(r"\langle k\rangle \approx 2m", font_size=36),
        ).arrange(RIGHT, buff=0.75)
        equations.next_to(title, DOWN, buff=0.16)

        panels = []
        for idx, m in enumerate([1, 2, 4]):
            G = ba_graph(n_final=55, m=m, seed=20 + idx)
            hub = top_degree_nodes(G, top=1)
            layout = spring_layout_3d(G, seed=30 + idx, scale=1.65, k=0.32, iterations=80)
            graph = make_graph_mobject(
                G,
                layout=layout,
                hub_nodes=hub,
                min_radius=0.026,
                max_radius=0.105,
                edge_opacity=0.62,
                edge_width=1.35,
                edge_color=GREY_A,
            )
            rings = make_node_rings(graph, hub, color=YELLOW, radius_buff=0.06)
            graph_group = VGroup(graph, rings)

            label = Text(f"m = {m}", font_size=28, color=YELLOW)
            stats = VGroup(
                Text(f"N = {G.number_of_nodes()}", font_size=20),
                Text(f"E = {G.number_of_edges()}", font_size=20),
                MathTex(r"\langle k\rangle \approx " + str(2 * m), font_size=24),
            ).arrange(DOWN, buff=0.08)
            panel = VGroup(label, graph_group, stats).arrange(DOWN, buff=0.18)
            panels.append(panel)

        row = VGroup(*panels).arrange(RIGHT, buff=0.45)
        row.scale(0.78)
        row.next_to(equations, DOWN, buff=0.22)

        changes = VGroup(
            Text("m changes", font_size=22, color=GREEN_C),
            Text("birth degree | density | average degree", font_size=18),
        ).arrange(DOWN, buff=0.08)
        limits = VGroup(
            Text("m cannot set", font_size=22, color=RED_C),
            Text("targets | hub identity | clustering", font_size=18),
        ).arrange(DOWN, buff=0.08)
        comparison = VGroup(changes, limits).arrange(RIGHT, buff=0.45)
        comparison.next_to(row, DOWN, buff=0.12)

        caption = make_caption(
            "m sets how many edges arrive; preferential attachment still decides where they go."
        )

        self.add(title, equations, row, comparison, caption)
        sync_highlight(self, equations[0], 0.0, 21.0)
        sync_highlight(self, equations[0], 21.0, 28.0)
        sync_highlight(self, equations[1], 28.0, 36.0)
        sync_highlight(self, equations[1], 36.0, 47.0)
        sync_pause(self, 47.0, 50.0)
        sync_highlight(self, equations[1], 50.0, 52.0)
        finish_scene_at(self, 53.0)


# ============================================================
# Scene 3: Initial condition
# ============================================================

class BAInitialCondition(Scene):
    def construct(self):
        title = Title("The Initial Condition")
        subtitle = Text("The same rule can start from different connected seeds.", font_size=23)
        subtitle.next_to(title, DOWN, buff=0.42)

        seeds = [
            ("triangle seed", nx.complete_graph(3), 40),
            ("path seed", nx.path_graph(3), 41),
            ("complete seed", nx.complete_graph(4), 42),
        ]

        initial_panels = []
        final_panels = []
        for label_text, seed_graph, seed in seeds:
            final_graph = ba_graph(
                n_final=16,
                m=2,
                seed=seed,
                initial_graph=seed_graph,
            )
            final_layout = spring_layout_3d(final_graph, seed=seed, scale=1.6, k=0.55)
            initial = make_graph_mobject(
                seed_graph,
                layout=subset_layout(final_layout, seed_graph.nodes()),
                min_radius=0.07,
                max_radius=0.14,
                edge_opacity=0.5,
            )
            grown = make_graph_mobject(
                final_graph,
                layout=final_layout,
                hub_nodes=top_degree_nodes(final_graph, top=1),
                min_radius=0.045,
                max_radius=0.14,
                edge_opacity=0.32,
            )
            grown_ring = make_node_rings(grown, top_degree_nodes(final_graph, top=1))

            label = Text(label_text, font_size=24, color=YELLOW)
            initial_panels.append(VGroup(label.copy(), initial).arrange(DOWN, buff=0.2))
            final_panels.append(
                VGroup(label.copy(), VGroup(grown, grown_ring)).arrange(DOWN, buff=0.2)
            )

        initial_row = VGroup(*initial_panels).arrange(RIGHT, buff=0.7).scale(0.78)
        final_row = VGroup(*final_panels).arrange(RIGHT, buff=0.7).scale(0.78)
        initial_row.next_to(subtitle, DOWN, buff=0.95)
        final_row.move_to(initial_row)

        caption1 = make_caption("The seed graph controls the earliest steps.")
        caption2 = make_caption("After growth, the same preferential rule is driving all three networks.")

        self.play(Write(title), FadeIn(subtitle))
        self.play(FadeIn(initial_row), FadeIn(caption1), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(caption1), FadeOut(initial_row), FadeIn(final_row), run_time=1.2)
        self.play(FadeIn(caption2), run_time=0.5)
        self.wait(3.5)


# ============================================================
# Scene 4: Finite-size effects
# ============================================================

class BAFiniteSize(Scene):
    def construct(self):
        title = Title("Finite-Size Effects")
        subtitle = Text("Small BA networks have noisy tails.", font_size=28, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.18)

        panels = []
        for idx, n in enumerate([30, 100, 300]):
            G = ba_graph(n_final=n, m=2, seed=60)
            layout = spring_layout_3d(G, seed=70 + idx, scale=1.35, k=0.22, iterations=80)
            graph = make_graph_mobject(
                G,
                layout=layout,
                hub_nodes=top_degree_nodes(G, top=1),
                min_radius=0.015 if n >= 100 else 0.028,
                max_radius=0.09 if n >= 100 else 0.12,
                edge_opacity=0.11 if n >= 100 else 0.22,
                edge_width=0.45 if n >= 100 else 0.7,
            )
            rings = make_node_rings(
                graph,
                top_degree_nodes(G, top=1),
                radius_buff=0.04,
                stroke_width=3,
            )
            plot = make_rank_degree_plot(
                G,
                title_text="rank-degree",
                width=2.35,
                height=0.85,
                include_labels=False,
                stroke_width=2.0,
            )
            label = Text(f"N = {n}", font_size=24, color=YELLOW)
            panel = VGroup(label, VGroup(graph, rings), plot).arrange(DOWN, buff=0.15)
            panels.append(panel)

        row = VGroup(*panels).arrange(RIGHT, buff=0.42)
        row.scale(0.88)
        row.next_to(subtitle, DOWN, buff=0.35)

        caption = make_caption("More nodes make the degree profile easier to read, but the high-degree tail is still sparse.")

        self.play(Write(title), FadeIn(subtitle))
        self.play(LaggedStart(*[FadeIn(panel) for panel in row], lag_ratio=0.12), run_time=2.2)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(4.0)


# ============================================================
# Scene 5: Different realizations
# ============================================================

class BARealizations(Scene):
    def construct(self):
        title = Title("Different Realizations")
        subtitle = Text("Same N and m, different random target choices.", font_size=26)
        subtitle.next_to(title, DOWN, buff=0.18)

        panels = []
        for seed in [1, 2, 3, 4]:
            G = ba_graph(n_final=60, m=2, seed=seed)
            layout = spring_layout_3d(G, seed=90 + seed, scale=1.3, k=0.30, iterations=80)
            hub = top_degree_nodes(G, top=1)
            graph = make_graph_mobject(
                G,
                layout=layout,
                hub_nodes=hub,
                min_radius=0.025,
                max_radius=0.10,
                edge_opacity=0.22,
                edge_width=0.7,
            )
            rings = make_node_rings(graph, hub, radius_buff=0.05, stroke_width=3)
            label = Text(f"seed {seed}", font_size=22, color=YELLOW)
            panel = VGroup(label, VGroup(graph, rings)).arrange(DOWN, buff=0.1)
            panels.append(panel)

        grid = VGroup(*panels).arrange_in_grid(rows=2, cols=2, buff=(0.22, 0.75))
        grid.scale(0.74)
        grid.next_to(subtitle, DOWN, buff=0.12)

        caption = make_caption("The hub identity can change, but heterogeneous degrees remain.")

        self.play(Write(title), FadeIn(subtitle))
        self.play(LaggedStart(*[FadeIn(panel) for panel in grid], lag_ratio=0.08), run_time=2.2)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(4.0)


# ============================================================
# Scene 6: Algorithm takeaway
# ============================================================

class BAAlgorithmTakeaway(Scene):
    def construct(self):
        title = Title("What the Algorithm Fixes")

        fixed = boxed_group(
            "Fixed by the model",
            [
                "final size N",
                "attachment number m",
                "connected seed graph",
                "probability rule",
            ],
            color=GREEN_C,
            width=4.5,
            height=2.8,
        )

        random = boxed_group(
            "Random in each run",
            [
                "which targets are sampled",
                "which nodes become hubs",
                "exact graph shape",
            ],
            color=RED_C,
            width=4.5,
            height=2.8,
        )

        columns = VGroup(fixed, random).arrange(RIGHT, buff=0.65)
        columns.next_to(title, DOWN, buff=0.55)

        formula = MathTex(r"\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}", font_size=34)
        formula.next_to(columns, DOWN, buff=0.35)

        next_video = VGroup(
            Text("Next video:", font_size=28),
            MathTex(r"P(k)\sim k^{-3}", font_size=36, color=YELLOW),
        ).arrange(RIGHT, buff=0.2)
        next_video.next_to(formula, DOWN, buff=0.4)

        caption = make_caption("Video 2 makes the mechanism precise enough to simulate.")

        self.play(Write(title))
        self.play(FadeIn(columns), run_time=1.3)
        self.play(Write(formula), FadeIn(caption), run_time=1.0)
        self.play(FadeIn(next_video), run_time=0.8)
        self.wait(3.0)

        reference_card = make_reference_end_card()
        self.play(
            FadeOut(title),
            FadeOut(columns),
            FadeOut(formula),
            FadeOut(next_video),
            FadeOut(caption),
            run_time=0.8,
        )
        self.play(FadeIn(reference_card), run_time=0.8)
        self.wait(5.0)


# ============================================================
# Merged derivation scenes from the former Video 5.3
# ============================================================

def make_log_log_points(values, width=3.2, height=2.0):
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    data = sorted((k, c) for k, c in counts.items() if k > 0 and c > 0)
    xs = np.array([np.log10(k) for k, _ in data])
    ys = np.array([np.log10(c) for _, c in data])
    x_min, x_max = float(xs.min()), float(xs.max())
    y_min, y_max = float(ys.min()), float(ys.max())
    if x_min == x_max:
        x_max += 1
    if y_min == y_max:
        y_max += 1

    axes = Axes(
        x_range=[x_min, x_max, (x_max - x_min) / 2],
        y_range=[y_min, y_max, max((y_max - y_min) / 2, 0.2)],
        x_length=width,
        y_length=height,
        tips=False,
        axis_config={"include_numbers": False, "stroke_width": 1.2},
    )
    dots = VGroup(
        *[
            Dot(axes.c2p(np.log10(k), np.log10(c)), radius=0.04, color=YELLOW)
            for k, c in data
        ]
    )
    labels = VGroup(
        Text("log k", font_size=16).next_to(axes.x_axis, DOWN, buff=0.1),
        Text("log count", font_size=16).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.1),
    )
    return VGroup(axes, dots, labels)


class BAContinuumSetup(Scene):
    def construct(self):
        title = Title("From Algorithm to Continuum Theory")
        bullets = VGroup(
            Text("growth fixes totals", font_size=20),
            Text("track one node i", font_size=20),
            Text("replace jumps by expectation", font_size=20),
            Text("treat t and k as continuous", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bullets.to_edge(RIGHT, buff=0.58).shift(DOWN * 0.05)

        total_title = Text("Network totals", font_size=25, color=YELLOW)
        total_equations = VGroup(
            MathTex(r"N(t)=N_0+t,\quad E(t)=E_0+mt", font_size=31),
            MathTex(r"\sum_j k_j(t)=2E(t)", font_size=32),
            MathTex(
                r"\langle k\rangle(t)=\frac{1}{N(t)}\sum_j k_j(t)=\frac{2E(t)}{N(t)}\to 2m",
                font_size=28,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        total_group = VGroup(total_title, total_equations).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        node_title = Text("One node", font_size=25, color=YELLOW)
        node_equations = VGroup(
            MathTex(r"\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}", font_size=31),
            MathTex(r"\frac{d\bar{k}_i}{dt}=m\Pi_i(t)", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        node_group = VGroup(node_title, node_equations).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        equations = VGroup(total_group, node_group).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        if equations.height > 5.0:
            equations.scale_to_fit_height(5.0)
        if equations.width > 7.3:
            equations.scale_to_fit_width(7.3)
        equations.to_edge(LEFT, buff=0.55).shift(DOWN * 0.05)

        self.add(title, bullets, equations)
        sync_pause(self, 0.0, 10.0)
        sync_highlight(self, total_equations[0], 10.0, 24.0)
        sync_highlight(self, total_equations[0], 24.0, 42.0)
        sync_highlight(self, total_equations[1], 42.0, 60.0)
        sync_highlight(self, total_equations[2], 60.0, 74.0)
        sync_highlight(self, node_equations[0], 74.0, 75.0)
        finish_scene_at(self, 75.0)


class BADegreeGrowthEquation(Scene):
    def construct(self):
        title = Title("Expected Degree Growth")
        expectation_note = Text(
            "continuum curve = expected degree, not an exact single run",
            font_size=23,
            color=YELLOW,
        )
        expectation_note.next_to(title, DOWN, buff=0.18)

        derivation = VGroup(
            MathTex(r"\bar{k}_i(t)=\mathbb{E}[k_i(t)]", font_size=32),
            MathTex(r"\frac{d\bar{k}_i}{dt}=m\frac{\bar{k}_i}{2mt}", font_size=35),
            MathTex(r"\frac{d\bar{k}_i}{dt}=\frac{\bar{k}_i}{2t}", font_size=37),
            MathTex(r"\bar{k}_i(t_i)=m", font_size=33),
        ).arrange(DOWN, buff=0.22)
        derivation.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        axes = Axes(
            x_range=[1, 10, 3],
            y_range=[0, 4, 1],
            x_length=4.1,
            y_length=2.6,
            tips=False,
            axis_config={"include_numbers": False},
        )
        curve = axes.plot(lambda x: np.sqrt(x / 1.5), x_range=[1.5, 10], color=YELLOW)
        jump_points = [
            axes.c2p(1.5, 1.0),
            axes.c2p(2.4, 1.0),
            axes.c2p(2.4, 1.35),
            axes.c2p(4.1, 1.35),
            axes.c2p(4.1, 1.75),
            axes.c2p(6.5, 1.75),
            axes.c2p(6.5, 2.05),
            axes.c2p(9.0, 2.05),
        ]
        sample_path = VMobject()
        sample_path.set_points_as_corners(jump_points)
        sample_path.set_stroke(GREY_A, width=2.3, opacity=0.75)
        start_dot = Dot(axes.c2p(1.5, 1.0), color=GREEN_C)
        label = MathTex(r"\bar{k}_i(t)=m\left(\frac{t}{t_i}\right)^{1/2}", font_size=32)
        sample_key = VGroup(
            Line(LEFT * 0.18, RIGHT * 0.18, color=GREY_A, stroke_width=3),
            Text("one run jumps", font_size=18, color=GREY_A),
        ).arrange(RIGHT, buff=0.08)
        expected_key = VGroup(
            Line(LEFT * 0.18, RIGHT * 0.18, color=YELLOW, stroke_width=3),
            Text("expected curve", font_size=18, color=YELLOW),
        ).arrange(RIGHT, buff=0.08)
        legend = VGroup(sample_key, expected_key).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        plot_group = VGroup(axes, sample_path, curve, start_dot, label, legend)
        label.next_to(axes, UP, buff=0.15)
        legend.next_to(axes, DOWN, buff=0.14)
        legend.align_to(axes, LEFT).shift(RIGHT * 0.1)
        plot_group.to_edge(RIGHT, buff=0.85).shift(DOWN * 0.05)

        caption = make_caption("This differential equation describes the mean trend; individual degrees jump randomly.")

        self.add(title, expectation_note, derivation, axes, sample_path, curve, start_dot, label, legend, caption)
        sync_pause(self, 0.0, 8.0)
        sync_pause(self, 8.0, 23.0)
        sync_highlight(self, derivation[0], 23.0, 30.0)
        sync_highlight(self, derivation[1], 30.0, 59.0)
        sync_highlight(self, derivation[2], 59.0, 67.0)
        sync_highlight(self, derivation[2], 67.0, 82.0)
        sync_highlight(self, label, 82.0, 96.0)
        finish_scene_at(self, 96.0)


class BABirthTimeDistribution(Scene):
    def construct(self):
        title = Title("Birth Time Becomes Degree")
        left = VGroup(
            Text("Arrival times are roughly uniform", font_size=25, color=YELLOW),
            MathTex(r"k_i(t)=m\left(\frac{t}{t_i}\right)^{1/2}", font_size=34),
            MathTex(r"t_i=\frac{m^2t}{k_i^2}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        left.to_edge(LEFT, buff=0.8).shift(DOWN * 0.15)

        timeline = NumberLine(x_range=[0, 10, 1], length=5.0, include_numbers=False)
        dots = VGroup(*[Dot(timeline.n2p(x), radius=0.045, color=BLUE_C) for x in np.linspace(0.6, 9.4, 14)])
        old_label = Text("old nodes", font_size=20, color=YELLOW).next_to(timeline.n2p(1.0), DOWN, buff=0.25)
        young_label = Text("young nodes", font_size=20, color=GREY_A).next_to(timeline.n2p(9.0), DOWN, buff=0.25)
        arrow = Arrow(timeline.n2p(2.0) + UP * 0.5, timeline.n2p(2.0), buff=0.05, color=YELLOW)
        timeline_group = VGroup(timeline, dots, old_label, young_label, arrow)
        timeline_group.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)

        caption = make_caption("The degree distribution asks how many nodes were born early enough.")

        self.add(title, left, timeline_group, caption)
        sync_highlight(self, left[1], 0.0, 5.0)
        sync_highlight(self, timeline_group, 5.0, 23.0)
        sync_highlight(self, left[2], 23.0, 26.0)
        finish_scene_at(self, 26.0)


class BAPowerLawExponent(Scene):
    def construct(self):
        title = Title("The Exponent 3")
        equations = VGroup(
            MathTex(r"P(k_i(t)<k)=1-\frac{m^2}{k^2}", font_size=38),
            MathTex(r"p(k)=\frac{d}{dk}P(k_i(t)<k)", font_size=36),
            MathTex(r"p(k)\sim 2m^2k^{-3}", font_size=42, color=YELLOW),
        ).arrange(DOWN, buff=0.36)
        equations.to_edge(LEFT, buff=0.85).shift(DOWN * 0.15)

        axes = Axes(
            x_range=[1, 10, 2],
            y_range=[0, 1, 0.25],
            x_length=4.0,
            y_length=2.7,
            tips=False,
            axis_config={"include_numbers": False},
        )
        curve = axes.plot(lambda x: min(1, 2.0 * x ** -3), x_range=[1.25, 10], color=YELLOW)
        label = MathTex(r"k^{-3}", font_size=36, color=YELLOW).next_to(curve, UP, buff=0.05)
        plot_group = VGroup(axes, curve, label)
        plot_group.to_edge(RIGHT, buff=1.0).shift(DOWN * 0.05)

        caption = make_caption("Under the continuum approximation, the BA exponent is 3.")

        self.add(title, equations, plot_group, caption)
        sync_highlight(self, equations[0], 0.0, 16.0)
        sync_highlight(self, equations[1], 16.0, 21.0)
        sync_highlight(self, equations[2], 21.0, 34.0)
        sync_highlight(self, label, 34.0, 42.0)
        finish_scene_at(self, 42.0)


class BAExponentRegimeMap(Scene):
    def construct(self):
        title = Title(r"Why $\gamma=3$ Matters")
        subtitle = Text(
            "BA sits at the boundary between ultra-small and small-world regimes.",
            font_size=23,
            color=YELLOW,
        )
        subtitle.next_to(title, DOWN, buff=0.18)

        axis = NumberLine(
            x_range=[1, 4, 1],
            length=8.5,
            include_numbers=True,
            include_tip=True,
            font_size=24,
        )
        axis.shift(DOWN * 0.05)
        gamma_label = MathTex(r"\gamma", font_size=34, color=WHITE)
        gamma_label.next_to(axis, RIGHT, buff=0.15)

        tick2 = axis.n2p(2)
        tick3 = axis.n2p(3)
        left_end = axis.n2p(1)
        right_end = axis.n2p(4)

        anomalous = Rectangle(width=2.15, height=2.45, stroke_color=GREY_B, fill_color=GREY_E, fill_opacity=0.12)
        scale_free = Rectangle(width=2.8, height=2.45, stroke_color=PURPLE_B, fill_color=PURPLE_E, fill_opacity=0.15)
        random_like = Rectangle(width=2.8, height=2.45, stroke_color=GREEN_B, fill_color=GREEN_E, fill_opacity=0.15)
        anomalous.move_to((left_end + tick2) / 2 + UP * 1.0)
        scale_free.move_to((tick2 + tick3) / 2 + UP * 1.0)
        random_like.move_to((tick3 + right_end) / 2 + UP * 1.0)

        anomalous_title = Text("anomalous", font_size=22, color=GREY_B).next_to(anomalous.get_top(), DOWN, buff=0.2)
        scale_title = Text("scale-free", font_size=22, color=PURPLE_B).next_to(scale_free.get_top(), DOWN, buff=0.2)
        random_title = Text("random-like", font_size=22, color=GREEN_B).next_to(random_like.get_top(), DOWN, buff=0.2)

        scale_notes = VGroup(
            MathTex(r"2<\gamma<3", font_size=28, color=PURPLE_B),
            MathTex(r"\langle k\rangle\ \mathrm{finite}", font_size=24),
            MathTex(r"\langle k^2\rangle\ \mathrm{diverges}", font_size=24),
            MathTex(r"\langle d\rangle\sim \ln\ln N", font_size=24),
        ).arrange(DOWN, buff=0.13)
        scale_notes.move_to(scale_free.get_center()).shift(DOWN * 0.1)

        random_notes = VGroup(
            MathTex(r"\gamma>3", font_size=28, color=GREEN_B),
            MathTex(r"\langle k\rangle,\langle k^2\rangle\ \mathrm{finite}", font_size=23),
            MathTex(r"\langle d\rangle\sim \ln N", font_size=24),
        ).arrange(DOWN, buff=0.16)
        random_notes.move_to(random_like.get_center()).shift(DOWN * 0.05)

        anomalous_notes = VGroup(
            MathTex(r"\gamma<2", font_size=28, color=GREY_B),
            Text("not stable", font_size=18, color=GREY_B),
            Text("for large N", font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.16)
        anomalous_notes.move_to(anomalous.get_center())

        critical_line = DashedLine(tick3 + DOWN * 1.05, tick3 + UP * 2.0, color=YELLOW, dash_length=0.12)
        critical_dot = Dot(tick3, color=YELLOW, radius=0.07)
        critical_label = VGroup(
            MathTex(r"\gamma=3", font_size=30, color=YELLOW),
            Text("BA critical boundary", font_size=21, color=YELLOW),
            MathTex(r"\langle k^2\rangle\sim \ln N", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.1)
        critical_label.next_to(critical_line, DOWN, buff=0.25)

        caption = make_caption("The exponent is not just a fit number; it changes which moments and distances dominate.")
        source = Text(
            f"Regime map adapted from Network Science, Ch. 4: {DEGREE_EXPONENT_URL}",
            font_size=18,
            color=GREY_B,
        )
        source.next_to(caption, UP, buff=0.08)

        self.add(
            title,
            subtitle,
            anomalous,
            scale_free,
            random_like,
            anomalous_title,
            scale_title,
            random_title,
            axis,
            gamma_label,
            anomalous_notes,
            scale_notes,
            random_notes,
            critical_line,
            critical_dot,
            critical_label,
            source,
            caption,
        )
        sync_highlight(self, critical_label, 0.0, 15.0)
        sync_highlight(self, scale_notes, 15.0, 45.0, color=PURPLE_B)
        sync_highlight(self, random_notes, 45.0, 67.0, color=GREEN_B)
        sync_highlight(self, critical_label, 67.0, 76.0)
        sync_pause(self, 76.0, 79.0)
        finish_scene_at(self, 79.0)


class BASimulationSanityCheck(Scene):
    def construct(self):
        title = Title("Simulation Sanity Check")
        G = nx.barabasi_albert_graph(500, 2, seed=9)
        hubs = top_degree_nodes(G, top=3)
        layout = spring_layout_3d(G, seed=6, scale=2.3, k=0.13, iterations=80)
        graph = make_graph_mobject(
            G,
            layout=layout,
            hub_nodes=hubs,
            min_radius=0.01,
            max_radius=0.075,
            edge_opacity=0.24,
            edge_width=0.8,
        )
        graph.scale(0.95).to_edge(LEFT, buff=0.35).shift(DOWN * 0.1)
        hub_rings = make_node_rings(graph, hubs, color=YELLOW, radius_buff=0.035, stroke_width=2.4)

        degree_values = [degree for _, degree in G.degree()]
        plot = make_log_log_points(degree_values, width=3.5, height=2.3)
        plot.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.1)
        plot_title = Text("log-log degree counts", font_size=22, color=YELLOW).next_to(plot, UP, buff=0.2)

        caption = make_caption("Finite simulations are noisy, but the high-degree tail is visibly heavy.")

        self.add(title, graph, hub_rings, plot, plot_title, caption)
        sync_pause(self, 0.0, 5.0)
        sync_multi_highlight(self, hub_rings, 5.0, 21.0)
        sync_highlight(self, plot[1], 21.0, 35.0)
        sync_pause(self, 35.0, 37.0)
        finish_scene_at(self, 37.0)


class BATheoryTakeaway(Scene):
    def construct(self):
        title = Title("Algorithm to Power Law")
        card_font_size = 22
        cards = VGroup(
            VGroup(
                Text("Algorithm", font_size=card_font_size, color=YELLOW),
                MathTex(r"\Pi_i=\frac{k_i}{\sum_j k_j}", font_size=card_font_size),
            ).arrange(DOWN, buff=0.12),
            VGroup(
                Text("Degree growth", font_size=card_font_size, color=YELLOW),
                MathTex(r"k_i(t)=m(t/t_i)^{1/2}", font_size=card_font_size),
            ).arrange(DOWN, buff=0.12),
            VGroup(
                Text("Distribution", font_size=card_font_size, color=YELLOW),
                MathTex(r"p(k)\sim k^{-3}", font_size=card_font_size),
            ).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=0.55)
        boxes = VGroup()
        for card in cards:
            box = RoundedRectangle(width=3.75, height=1.65, corner_radius=0.12, stroke_color=GREY_B)
            card.move_to(box.get_center())
            boxes.add(VGroup(box, card))
        boxes.arrange(RIGHT, buff=0.22).next_to(title, DOWN, buff=1.0)

        next_line = Text("Next: what BA explains, and what it misses.", font_size=27, color=YELLOW)
        next_line.next_to(boxes, DOWN, buff=0.55)

        reference_card = make_reference_end_card()

        self.add(title, boxes, next_line)
        sync_multi_highlight(self, boxes, 0.0, 5.0)
        sync_pause(self, 5.0, 16.0)
        self.remove(title, boxes, next_line)
        self.add(reference_card)
        finish_scene_at(self, 22.1)
