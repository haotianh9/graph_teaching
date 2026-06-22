from __future__ import annotations

import json
import math
from pathlib import Path

import networkx as nx
import numpy as np
from manim import *


BG = "#050609"
LOW_FITNESS = BLUE_C
HIGH_FITNESS = YELLOW
LATE = RED_C
SELECTED = GREEN_C
MUTED = GREY_B
DATA_PATH = Path(__file__).resolve().parent / "data" / "fitness_fit_results.json"
ZH_FONT = "Noto Sans SC"


def add_title(scene: Scene, title: str, font_size: int = 46) -> VGroup:
    title_obj = Tex(title, font_size=font_size).to_edge(UP, buff=0.25)
    rule = Line(LEFT * 6.45, RIGHT * 6.45, color=WHITE, stroke_width=2).next_to(title_obj, DOWN, buff=0.14)
    group = VGroup(title_obj, rule)
    scene.play(Write(title_obj), Create(rule), run_time=1.0)
    return group


def small_badge(text: str, color=HIGH_FITNESS) -> VGroup:
    label = Text(text, font_size=23, color=color)
    box = RoundedRectangle(
        width=label.width + 0.42,
        height=label.height + 0.25,
        corner_radius=0.1,
        color=color,
        stroke_width=2,
    )
    return VGroup(box, label)


def key_term(en: str, zh: str, color=HIGH_FITNESS, en_size: int = 24, zh_size: int = 20) -> VGroup:
    return VGroup(
        Text(en, font_size=en_size, color=color),
        Text(zh, font_size=zh_size, color=color, font=ZH_FONT),
    ).arrange(DOWN, buff=0.03)


def load_fitness_fit_results() -> dict:
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return {
        "dataset": "SNAP High-energy physics theory citation network",
        "source_url": "https://snap.stanford.edu/data/cit-HepTh.html",
        "papers_with_enough_timed_citations": 1271,
        "mean_beta_hat": 1.668,
        "median_beta_hat": 1.557,
        "important_caveat": "fallback values; run scripts/fit_hepth_fitness.py to regenerate",
        "examples": [
            {
                "label": "early burst",
                "paper_id": 9612223,
                "total_citations": 20,
                "beta_hat": 1.074,
                "eta_hat": 0.644,
                "early_share_first_2y": 0.75,
                "ages": [0.005, 0.238, 0.58, 0.83, 1.248, 1.648, 3.203, 4.86],
                "cumulative_citations": [1, 2, 7, 10, 14, 15, 17, 20],
            },
            {
                "label": "steady growth",
                "paper_id": 9607227,
                "total_citations": 41,
                "beta_hat": 1.661,
                "eta_hat": 0.996,
                "early_share_first_2y": 0.22,
                "ages": [0.312, 0.936, 1.993, 2.899, 3.833, 4.334, 4.901, 5.687],
                "cumulative_citations": [1, 5, 9, 15, 21, 30, 37, 41],
            },
            {
                "label": "late bloomer",
                "paper_id": 9406217,
                "total_citations": 25,
                "beta_hat": 3.921,
                "eta_hat": 2.351,
                "early_share_first_2y": 0.0,
                "ages": [3.337, 4.312, 4.83, 5.5, 5.821, 6.513, 6.968, 7.302],
                "cumulative_citations": [1, 3, 7, 9, 15, 18, 23, 25],
            },
        ],
        "sample_curves": [],
    }


def curve_from_points(axes: Axes, ages: list[float], citations: list[int], color, stroke_width=2.5, opacity=1.0) -> VMobject:
    points = [axes.c2p(math.log1p(age), math.log1p(count)) for age, count in zip(ages, citations)]
    curve = VMobject(color=color, stroke_width=stroke_width, stroke_opacity=opacity)
    curve.set_points_as_corners(points)
    return curve


def reference_card() -> VGroup:
    header = Text("References", font_size=34, color=HIGH_FITNESS)
    book = VGroup(
        Text("Network Science book, Chapter 6", font_size=20),
        Text("https://networksciencebook.com/chapter/6#measuring-fitness", font_size=16, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    data = VGroup(
        Text("SNAP HEP-TH citation network", font_size=20),
        Text("https://snap.stanford.edu/data/cit-HepTh.html", font_size=16, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    repo = VGroup(
        Text("Course code and teaching materials", font_size=20),
        Text("https://github.com/haotianh9/graph_teaching", font_size=16, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    paper = VGroup(
        Text("Bianconi and Barabasi fitness model", font_size=20),
        Text("Europhysics Letters 54, 436-442 (2001)", font_size=16, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    box = VGroup(paper, book, data, repo).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    frame = RoundedRectangle(width=9.4, height=3.05, corner_radius=0.14, color=MUTED, stroke_width=1.5)
    box.move_to(frame.get_center()).align_to(frame, LEFT).shift(RIGHT * 0.45)
    framed_content = VGroup(frame, box)
    group = VGroup(header, framed_content).arrange(DOWN, buff=0.22)
    return group


def normalize_layout(graph: nx.Graph, seed: int, scale: float, center=ORIGIN) -> dict[int, np.ndarray]:
    pos = nx.spring_layout(graph, seed=seed, k=0.72 / math.sqrt(max(len(graph), 1)), iterations=140)
    xs = np.array([point[0] for point in pos.values()])
    ys = np.array([point[1] for point in pos.values()])
    xmid = (xs.max() + xs.min()) / 2
    ymid = (ys.max() + ys.min()) / 2
    span = max(xs.max() - xs.min(), ys.max() - ys.min(), 1e-6)
    return {
        node: np.array(
            [
                center[0] + scale * (point[0] - xmid) / span,
                center[1] + scale * (point[1] - ymid) / span,
                0.0,
            ]
        )
        for node, point in pos.items()
    }


def fitness_color(eta: float, min_eta: float = 0.55, max_eta: float = 2.8):
    alpha = max(0.0, min(1.0, (eta - min_eta) / (max_eta - min_eta)))
    return interpolate_color(LOW_FITNESS, HIGH_FITNESS, alpha)


def fitness_growth_graph(n_final: int = 72, m: int = 2, seed: int = 61, late_node: int = 34, late_eta: float = 3.0):
    rng = np.random.default_rng(seed)
    graph = nx.complete_graph(m + 1)
    etas = {node: float(rng.uniform(0.55, 1.25)) for node in graph.nodes()}

    for new_node in range(m + 1, n_final):
        existing = list(graph.nodes())
        eta = late_eta if new_node == late_node else float(rng.uniform(0.55, 1.25))
        weights = np.array([etas[node] * graph.degree(node) for node in existing], dtype=float)
        probabilities = weights / weights.sum()
        targets = rng.choice(existing, size=m, replace=False, p=probabilities)
        graph.add_node(new_node)
        etas[new_node] = eta
        graph.add_edges_from((new_node, int(target)) for target in targets)
    return graph, etas, late_node


def graph_mobject(
    graph: nx.Graph,
    etas: dict[int, float] | None = None,
    late_node: int | None = None,
    seed: int = 1,
    scale: float = 4.2,
    center=ORIGIN,
    edge_opacity: float = 0.42,
) -> Graph:
    layout = normalize_layout(graph, seed=seed, scale=scale, center=center)
    degrees = dict(graph.degree())
    max_degree = max(degrees.values()) if degrees else 1
    vertex_config = {}
    for node in graph.nodes():
        eta = etas.get(node, 0.9) if etas else 0.9
        color = LATE if node == late_node else fitness_color(eta)
        radius = 0.075 + 0.16 * math.sqrt(degrees[node] / max_degree)
        vertex_config[node] = {
            "radius": radius,
            "fill_color": color,
            "fill_opacity": 0.95,
            "stroke_color": WHITE,
            "stroke_width": 1.0,
        }
    return Graph(
        list(graph.nodes()),
        list(graph.edges()),
        layout=layout,
        vertex_config=vertex_config,
        edge_config={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": edge_opacity},
    )


def node_ring(graph_obj: Graph, node: int, color=HIGH_FITNESS, radius_buff: float = 0.12) -> Circle:
    dot = graph_obj.vertices[node]
    return Circle(
        radius=dot.radius + radius_buff,
        color=color,
        stroke_width=4,
    ).move_to(dot.get_center())


def weighted_choice_panel() -> VGroup:
    title = VGroup(
        Text("all candidates have the same degree", font_size=25, color=WHITE),
        MathTex(r"k_i=4", font_size=34, color=HIGH_FITNESS),
    ).arrange(RIGHT, buff=0.28).move_to(UP * 1.85)

    source = Dot(DOWN * 2.0, radius=0.08, color=LATE)
    source_label = Text("new node", font_size=19, color=LATE).next_to(source, DOWN, buff=0.12)
    candidates = VGroup()
    arrows = VGroup()
    specs = [
        (LEFT * 3.05 + UP * 0.35, 0.7, LOW_FITNESS, 3),
        (UP * 0.65, 1.2, GREEN_C, 5),
        (RIGHT * 3.05 + UP * 0.35, 2.4, HIGH_FITNESS, 8),
    ]

    for point, eta, color, width in specs:
        core = Circle(radius=0.2, color=WHITE, fill_color=color, fill_opacity=0.95, stroke_width=2).move_to(point)
        offsets = [UP * 0.48, RIGHT * 0.48, DOWN * 0.48, LEFT * 0.48]
        leaves = VGroup(
            *(
                Circle(radius=0.07, color=MUTED, fill_color=MUTED, fill_opacity=0.85, stroke_width=1.0).move_to(
                    point + offset
                )
                for offset in offsets
            )
        )
        spokes = VGroup(*(Line(point, leaf.get_center(), color=MUTED, stroke_width=2.2) for leaf in leaves))
        mini_graph = VGroup(spokes, leaves, core)
        degree_label = MathTex(r"k_i=4", font_size=26, color=WHITE).next_to(mini_graph, UP, buff=0.16)
        eta_label = MathTex(fr"\eta_i={eta}", font_size=25, color=color).next_to(mini_graph, DOWN, buff=0.16)
        score = MathTex(fr"\eta_i k_i={eta * 4:.1f}", font_size=23, color=color).next_to(eta_label, DOWN, buff=0.06)
        candidate = VGroup(degree_label, mini_graph, eta_label, score)
        arrow = Arrow(
            source.get_center(),
            core.get_center(),
            buff=0.34,
            color=color,
            stroke_width=width,
            max_tip_length_to_length_ratio=0.16,
        )
        candidates.add(candidate)
        arrows.add(arrow)

    return VGroup(title, arrows, source, source_label, candidates)


class FitnessOpening(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Tex("Chapter 6: Inferring Fitness", font_size=52).to_edge(UP, buff=0.42)
        question = Text("Can intrinsic attractiveness be inferred from growth data?", font_size=31, color=HIGH_FITNESS).next_to(title, DOWN, buff=0.35)
        paper = Text("Bianconi-Barabasi fitness model (2001)", font_size=24, color=MUTED).next_to(question, DOWN, buff=0.18)

        graph, etas, late = fitness_growth_graph(n_final=56, seed=42, late_node=29)
        graph_obj = graph_mobject(graph, etas, late_node=late, seed=5, scale=4.2, center=LEFT * 3.35 + DOWN * 0.55)
        degrees = dict(graph.degree())
        hubs = [node for node, _ in sorted(degrees.items(), key=lambda item: item[1], reverse=True)[:3]]
        rings = VGroup(*(node_ring(graph_obj, node, HIGH_FITNESS) for node in hubs))
        late_ring = node_ring(graph_obj, late, LATE, radius_buff=0.18)

        ba = VGroup(
            Text("BA: degree alone drives attachment", font_size=26),
            Text("degree / 度", font_size=21, color=MUTED, font=ZH_FONT),
        ).arrange(DOWN, buff=0.06).shift(RIGHT * 3.1 + UP * 0.82)
        fitness = VGroup(
            Text("Fitness: degree x intrinsic attractiveness", font_size=26, color=HIGH_FITNESS),
            Text("fitness / 适应度", font_size=21, color=HIGH_FITNESS, font=ZH_FONT),
        ).arrange(DOWN, buff=0.06).next_to(ba, DOWN, buff=0.28)
        eq = MathTex(r"\Pi_i=\frac{\eta_i k_i}{\sum_j \eta_j k_j}", font_size=44, color=WHITE).next_to(fitness, DOWN, buff=0.42)
        legend = VGroup(
            Dot(color=LOW_FITNESS), Text("low fitness", font_size=20),
            Dot(color=HIGH_FITNESS), Text("high fitness", font_size=20),
            Dot(color=LATE), Text("late entrant", font_size=20),
        ).arrange(RIGHT, buff=0.12).next_to(eq, DOWN, buff=0.45)

        self.play(Write(title), FadeIn(question), FadeIn(paper), run_time=1.4)
        self.play(Create(graph_obj), FadeIn(rings), FadeIn(late_ring), run_time=2.0)
        self.play(FadeIn(ba), FadeIn(fitness), Write(eq), FadeIn(legend), run_time=1.6)
        self.wait(2.0)


class FitnessRule(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Fitness-Weighted Attachment")
        eq = MathTex(r"\Pi_i=\frac{\eta_i k_i}{\sum_j \eta_j k_j}", font_size=48).shift(UP * 2.15)
        terms = VGroup(
            key_term("fitness", "适应度", HIGH_FITNESS, en_size=22, zh_size=19),
            Text(r"η", font_size=25, color=HIGH_FITNESS),
            Text("×", font_size=24, color=MUTED),
            key_term("degree", "度", WHITE, en_size=22, zh_size=19),
            Text(r"k", font_size=25, color=WHITE),
            Text("→ attachment weight", font_size=22, color=MUTED),
        ).arrange(RIGHT, buff=0.16).next_to(eq, DOWN, buff=0.18)
        panel = weighted_choice_panel().scale(0.78).shift(DOWN * 0.85)

        self.play(Write(eq), FadeIn(terms), run_time=1.2)
        self.play(FadeIn(panel), run_time=1.6)
        self.wait(2.4)


class FitnessGrowthDerivation(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, r"Where Does $\beta(\eta)$ Come From?", font_size=43)

        left_title = VGroup(
            Text("continuum approximation", font_size=25, color=HIGH_FITNESS),
            Text("连续近似：看期望增长", font_size=22, color=HIGH_FITNESS, font=ZH_FONT),
        ).arrange(DOWN, buff=0.05)
        left_steps = VGroup(
            MathTex(r"\Pi_i(t)=\frac{\eta_i k_i(t)}{\sum_j \eta_j k_j(t)}", font_size=33),
            MathTex(r"\frac{d\bar{k}_i}{dt}=m\Pi_i(t)", font_size=33),
            MathTex(r"\sum_j \eta_j k_j(t)\approx Cmt", font_size=33, color=HIGH_FITNESS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        left_note = Text(
            "C is one network-level constant",
            font_size=20,
            color=MUTED,
        )
        left_group = VGroup(left_title, left_steps, left_note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        left_group.move_to(LEFT * 3.25 + UP * 0.25)

        right_title = VGroup(
            Text("solve the growth equation", font_size=25, color=HIGH_FITNESS),
            Text("解出增长轨迹", font_size=22, color=HIGH_FITNESS, font=ZH_FONT),
        ).arrange(DOWN, buff=0.05)
        right_steps = VGroup(
            MathTex(r"\frac{d\bar{k}_i}{dt}=\frac{\eta_i}{C}\frac{\bar{k}_i}{t}", font_size=33),
            MathTex(r"\bar{k}_i(t_i)=m", font_size=31, color=MUTED),
            MathTex(r"\bar{k}_i(t)=m\left(\frac{t}{t_i}\right)^{\eta_i/C}", font_size=34),
            MathTex(r"\beta(\eta_i)=\frac{\eta_i}{C}", font_size=36, color=HIGH_FITNESS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        right_group = VGroup(right_title, right_steps).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right_group.move_to(RIGHT * 3.25 + UP * 0.18)

        bottom = VGroup(
            MathTex(
                r"\ln \bar{k}_i(t)=\beta(\eta_i)\ln t+B_i",
                font_size=38,
                color=HIGH_FITNESS,
            ),
            MathTex(
                r"B_i=\ln m-\beta(\eta_i)\ln t_i",
                font_size=29,
                color=WHITE,
            ),
            Text(
                "β is the expected log-log slope; data estimate this slope from observed growth.",
                font_size=21,
                color=MUTED,
            ),
        ).arrange(DOWN, buff=0.07).to_edge(DOWN, buff=0.48)

        self.play(FadeIn(left_title), Write(left_steps[0]), run_time=1.0)
        self.play(Write(left_steps[1]), run_time=0.8)
        self.play(Write(left_steps[2]), FadeIn(left_note), run_time=0.9)
        self.play(FadeIn(right_title), TransformFromCopy(left_steps[1], right_steps[0]), run_time=1.0)
        self.play(Write(right_steps[1]), Write(right_steps[2]), run_time=1.0)
        self.play(Write(right_steps[3]), FadeIn(bottom), run_time=1.1)
        self.wait(2.3)


class FitnessInferenceOpening(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Inferring Fitness from Growth")

        formula = MathTex(r"\ln \bar{k}_i(t)=\beta(\eta_i)\ln t+B_i", font_size=42, color=HIGH_FITNESS).shift(UP * 2.1)
        beta_def = VGroup(
            VGroup(
                MathTex(r"\beta(\eta_i)=\frac{\eta_i}{C}", font_size=39, color=HIGH_FITNESS),
                Text("growth exponent", font_size=25, color=HIGH_FITNESS),
                Text("增长指数", font_size=23, color=HIGH_FITNESS, font=ZH_FONT),
            ).arrange(RIGHT, buff=0.24),
            Text("C is fixed by the fitness distribution ρ(η)", font_size=24, color=WHITE),
            Text("same fitness recovers BA: C = 2, β = 1/2", font_size=23, color=MUTED),
            MathTex(
                r"\eta_i\uparrow\quad\Rightarrow\quad\beta(\eta_i)\uparrow"
                r"\quad\Rightarrow\quad \bar{k}_i(t)\ \text{grows faster}",
                font_size=28,
                color=HIGH_FITNESS,
            ),
        ).arrange(DOWN, buff=0.12).next_to(formula, DOWN, buff=0.34)

        pipeline = VGroup(
            small_badge("data", LOW_FITNESS),
            Arrow(LEFT, RIGHT, color=MUTED, stroke_width=4),
            small_badge("growth curve", SELECTED),
            Arrow(LEFT, RIGHT, color=MUTED, stroke_width=4),
            small_badge("estimate β, then η", HIGH_FITNESS),
        ).arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=0.65)

        self.play(Write(formula), run_time=1.0)
        self.play(FadeIn(beta_def), run_time=1.0)
        self.play(FadeIn(pipeline), run_time=1.0)
        self.wait(2.1)


class LogLogSlope(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Log-Log Slope")

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=6.45,
            y_length=4.2,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
        ).shift(LEFT * 2.15 + DOWN * 0.55)
        xlab = Tex(r"$\ln t$", font_size=28, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.18)
        ylab = Tex(r"$\ln k_i(t)$", font_size=28, color=MUTED).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.2)
        line_low = axes.plot(lambda x: 0.65 * x + 0.7, x_range=[0.5, 5.5], color=LOW_FITNESS, stroke_width=5)
        line_high = axes.plot(lambda x: 1.08 * x + 0.4, x_range=[0.5, 5.0], color=HIGH_FITNESS, stroke_width=5)

        def legend_item(color, label: str) -> VGroup:
            return VGroup(
                Line(LEFT * 0.32, RIGHT * 0.32, color=color, stroke_width=5),
                Text(label, font_size=22, color=color),
            ).arrange(RIGHT, buff=0.14)

        legend = VGroup(
            legend_item(HIGH_FITNESS, "higher slope"),
            legend_item(LOW_FITNESS, "lower slope"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        formula = VGroup(
            MathTex(r"\text{slope}=\beta(\eta_i)", font_size=38, color=HIGH_FITNESS),
            MathTex(r"\beta(\eta_i)=\eta_i/C", font_size=34, color=WHITE),
            key_term("dynamic exponent", "动态增长指数", HIGH_FITNESS, en_size=22, zh_size=20),
            Text("estimated from the curve", font_size=21, color=MUTED),
        ).arrange(DOWN, buff=0.1).to_edge(RIGHT, buff=0.65).shift(UP * 1.2)
        legend.next_to(formula, DOWN, buff=0.35).align_to(formula, LEFT)
        note = Text("different slopes imply different expected growth rates", font_size=24, color=HIGH_FITNESS).to_edge(DOWN, buff=0.45)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=0.9)
        self.play(Create(line_low), Create(line_high), run_time=1.0)
        self.play(FadeIn(legend), Write(formula), FadeIn(note), run_time=0.9)
        self.wait(2.2)


class GrowthHistoryComparison(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Early Popularity Can Mislead")

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 8, 1],
            x_length=6.7,
            y_length=4.4,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
        ).shift(LEFT * 2.05 + DOWN * 0.55)
        fast_start = axes.plot(lambda x: 5.0 * (1 - np.exp(-0.75 * x)) + 0.2, x_range=[0.1, 10], color=LOW_FITNESS, stroke_width=5)
        slow_burn = axes.plot(lambda x: 0.38 * (x + 0.3) ** 1.25 + 0.4, x_range=[0.1, 10], color=HIGH_FITNESS, stroke_width=5)
        xlab = Text("time", font_size=21, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.18)
        ylab = Text("links / citations", font_size=21, color=MUTED).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.18)
        legend = VGroup(
            VGroup(
                Line(LEFT * 0.35, RIGHT * 0.35, color=LOW_FITNESS, stroke_width=5),
                Text("early burst", font_size=22, color=LOW_FITNESS),
            ).arrange(RIGHT, buff=0.16),
            Text("high early count; flatter long-run slope", font_size=19, color=MUTED),
            VGroup(
                Line(LEFT * 0.35, RIGHT * 0.35, color=HIGH_FITNESS, stroke_width=5),
                Text("slower start", font_size=22, color=HIGH_FITNESS),
            ).arrange(RIGHT, buff=0.16),
            Text("lower early count; steeper long-run slope", font_size=19, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_edge(RIGHT, buff=0.65).shift(UP * 0.4)
        cap = Text("Use the whole growth history, not one early snapshot.", font_size=24, color=LATE).to_edge(DOWN, buff=0.43)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=0.9)
        self.play(Create(fast_start), Create(slow_burn), run_time=1.1)
        self.play(FadeIn(legend), FadeIn(cap), run_time=0.9)
        self.wait(2.1)


class CitationImpact(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Citations: Fitness plus Time Decay")

        left = VGroup(
            Text("paper quality", font_size=24, color=HIGH_FITNESS),
            key_term("fitness", "适应度", HIGH_FITNESS, en_size=26, zh_size=22),
            MathTex(r"\eta_i", font_size=45, color=HIGH_FITNESS),
        ).arrange(DOWN, buff=0.12).shift(LEFT * 4.05 + UP * 0.4)
        middle = VGroup(
            key_term("aging", "老化", LATE, en_size=26, zh_size=22),
            Text("novelty decay", font_size=24, color=LATE),
            MathTex(r"A(t-t_i)", font_size=45, color=LATE),
        ).arrange(DOWN, buff=0.12).shift(UP * 0.4)
        right = VGroup(
            Text("observed", font_size=24, color=LOW_FITNESS),
            Text("citations", font_size=27, color=LOW_FITNESS),
            MathTex(r"k_i(t)", font_size=45, color=LOW_FITNESS),
        ).arrange(DOWN, buff=0.12).shift(RIGHT * 4.05 + UP * 0.4)
        arrows = VGroup(
            Arrow(left.get_right(), middle.get_left(), buff=0.25, color=MUTED, stroke_width=5),
            Arrow(middle.get_right(), right.get_left(), buff=0.25, color=MUTED, stroke_width=5),
        )
        note = VGroup(
            Text("A paper can be high fitness but receive attention only while it is visible.", font_size=25, color=WHITE),
            Text("Fitness inference must account for the observation window.", font_size=25, color=HIGH_FITNESS),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.48)

        self.play(FadeIn(left), FadeIn(middle), FadeIn(right), run_time=1.0)
        self.play(Create(arrows), run_time=0.8)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(2.3)


class RealDataFitnessFit(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Real Citation Data: Fitness Fitting")
        results = load_fitness_fit_results()
        examples = results["examples"]
        sample_curves = results.get("sample_curves", [])

        summary = VGroup(
            Text("SNAP HEP-TH citation data", font_size=24, color=WHITE),
            Text(
                f"{results['papers_with_enough_timed_citations']:,} fitted papers, dated subset",
                font_size=24,
                color=HIGH_FITNESS,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(LEFT, buff=0.55).shift(UP * 2.25)

        estimator = VGroup(
            MathTex(r"\widehat{\beta}_i=\mathrm{slope}", font_size=34, color=HIGH_FITNESS),
            MathTex(
                r"\log(c_i(\tau)+1)\ \mathrm{vs.}\ \log(\tau+1)",
                font_size=30,
                color=HIGH_FITNESS,
            ),
        ).arrange(DOWN, buff=0.08).to_edge(RIGHT, buff=0.62).shift(UP * 2.15)
        eta_norm = MathTex(
            r"\widehat{\eta}_i=\widehat{\beta}_i/\langle\widehat{\beta}\rangle",
            font_size=34,
            color=WHITE,
        ).next_to(estimator, DOWN, buff=0.18)

        axes = Axes(
            x_range=[0, 2.25, 0.5],
            y_range=[0, 4.05, 1],
            x_length=6.4,
            y_length=3.55,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
        ).shift(LEFT * 3.0 + DOWN * 0.7)
        xlab = Tex(r"$\log(\tau+1)$", font_size=24, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.18)
        ylab = Tex(r"$\log(c_i(\tau)+1)$", font_size=24, color=MUTED).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.18)

        grey_curves = VGroup()
        for sample in sample_curves[:28]:
            grey_curves.add(
                curve_from_points(
                    axes,
                    sample["ages"],
                    sample["cumulative_citations"],
                    color=GREY_B,
                    stroke_width=1.2,
                    opacity=0.28,
                )
            )

        colors = [LOW_FITNESS, SELECTED, LATE]
        highlighted = VGroup()
        for example, color in zip(examples, colors):
            curve = curve_from_points(
                axes,
                example["ages"],
                example["cumulative_citations"],
                color=color,
                stroke_width=5,
                opacity=1.0,
            )
            highlighted.add(curve)

        table_title = Text("three fitted papers", font_size=25, color=HIGH_FITNESS)
        header = VGroup(
            Text("type", font_size=18, color=MUTED),
            Text("cites", font_size=18, color=MUTED),
            MathTex(r"\widehat{\beta}", font_size=24, color=MUTED),
            MathTex(r"\widehat{\eta}", font_size=24, color=MUTED),
        ).arrange(RIGHT, buff=0.34)
        rows = VGroup()
        for example, color in zip(examples, colors):
            rows.add(
                VGroup(
                    Text(example["label"], font_size=19, color=color),
                    Text(str(example["total_citations"]), font_size=19, color=WHITE),
                    Text(f"{example['beta_hat']:.2f}", font_size=19, color=WHITE),
                    Text(f"{example['eta_hat']:.2f}", font_size=19, color=HIGH_FITNESS),
                ).arrange(RIGHT, buff=0.38)
            )
        table = VGroup(table_title, header, rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22
        ).to_edge(RIGHT, buff=0.82).shift(DOWN * 0.65)

        caveat = Text(
            "This is an effective growth-fitness proxy; citation aging still matters.",
            font_size=23,
            color=LATE,
        ).to_edge(DOWN, buff=0.42)

        self.play(FadeIn(summary), Write(estimator), FadeIn(eta_norm), run_time=1.2)
        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), FadeIn(grey_curves), run_time=1.2)
        self.play(Create(highlighted), FadeIn(table), run_time=1.5)
        self.play(FadeIn(caveat), run_time=0.8)
        self.wait(2.2)


class PredictionWorkflow(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "A Practical Inference Workflow")

        steps = VGroup(
            small_badge("1. collect time-stamped links", LOW_FITNESS),
            small_badge("2. align birth time t_i", SELECTED),
            small_badge("3. fit log-log growth slope", HIGH_FITNESS),
            small_badge("4. compare predicted future impact", LATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).shift(LEFT * 2.7 + UP * 0.25)

        axis = NumberLine(x_range=[0, 10, 1], length=5.3, color=WHITE).shift(RIGHT * 2.7 + DOWN * 0.2)
        dots = VGroup(*(Dot(axis.n2p(x), color=HIGH_FITNESS if x > 6 else LOW_FITNESS, radius=0.07) for x in [1, 2, 2.7, 4.4, 6.3, 7.2, 8.5, 9.4]))
        label = Text("link/citation events over time", font_size=24, color=MUTED).next_to(axis, UP, buff=0.45)
        cap = Text("Prediction is probabilistic: estimate growth tendency, not a guaranteed ranking.", font_size=24, color=HIGH_FITNESS).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(steps), run_time=1.2)
        self.play(Create(axis), FadeIn(dots), FadeIn(label), run_time=1.0)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(2.1)


class FitnessTakeaway(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Takeaway")
        bullets = VGroup(
            Text("model reminder: η x degree drives attachment", font_size=29, color=HIGH_FITNESS),
            Text("theory: β(η) = η / C is the expected growth exponent", font_size=27, color=WHITE),
            Text("inference: log-log slope estimates effective β(η)", font_size=27, color=WHITE),
            Text("early popularity is not the same as long-term impact", font_size=28, color=LATE),
            Text("Video 6.2: condensation and evolving-network phase transitions", font_size=26, color=BLUE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).shift(UP * 1.58)
        eq = MathTex(r"\ln \bar{k}_i(t)=\beta(\eta_i)\ln t+B_i", font_size=37).next_to(bullets, DOWN, buff=0.24)
        refs = reference_card().scale(0.58).to_edge(DOWN, buff=0.24)

        self.play(FadeIn(bullets, shift=UP * 0.2), Write(eq), run_time=1.5)
        self.wait(1.4)
        self.play(FadeOut(eq), FadeIn(refs), run_time=1.0)
        self.wait(2.2)
