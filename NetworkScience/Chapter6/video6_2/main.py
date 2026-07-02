from __future__ import annotations

import json
import sys
from pathlib import Path

import networkx as nx
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chapter6_manim_utils import ALERT, BG, HIGH, LOW, MID, MUTED, add_title, graph_mobject, node_ring, small_badge


WHITEISH = "#F3F0E8"
ZH_FONT = "Noto Sans SC"
FITNESS_FIT_PATH = Path(__file__).resolve().parents[1] / "video6_1" / "data" / "fitness_fit_results.json"
WEB_PROXY_PATH = Path(__file__).resolve().parent / "data" / "commoncrawl_web_fitness_proxy.json"


def scale_free_graph(n: int = 78) -> nx.Graph:
    return nx.barabasi_albert_graph(n, 2, seed=31)


def condensed_graph(n: int = 78) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from((0, node) for node in range(1, n))
    for start in range(1, n, 10):
        cluster = list(range(start, min(start + 10, n)))
        for idx, node in enumerate(cluster[:-1]):
            graph.add_edge(node, cluster[idx + 1])
        if len(cluster) > 4:
            graph.add_edge(cluster[0], cluster[3])
            graph.add_edge(cluster[2], cluster[-1])
    return graph


def simple_graph(points: list[np.ndarray], edges: list[tuple[int, int]], node_colors=None, edge_color=MUTED) -> VGroup:
    node_colors = node_colors or {}
    edge_group = VGroup()
    node_group = VGroup()
    for u, v in edges:
        edge_group.add(Line(points[u], points[v], color=edge_color, stroke_width=3, stroke_opacity=0.65))
    for idx, point in enumerate(points):
        node_group.add(
            Circle(
                radius=0.13,
                color=WHITE,
                fill_color=node_colors.get(idx, LOW),
                fill_opacity=0.95,
                stroke_width=1.4,
            ).move_to(point)
        )
    return VGroup(edge_group, node_group)


def share_bar(label: str, value: float, color, width: float = 3.2) -> VGroup:
    if label.startswith("$") and label.endswith("$"):
        text = MathTex(label.strip("$"), font_size=24, color=WHITE)
    else:
        text = Text(label, font_size=20, color=WHITE)
    base = Rectangle(width=width, height=0.22, color=MUTED, stroke_width=1.1)
    fill = Rectangle(width=width * value, height=0.22, color=color, fill_color=color, fill_opacity=0.9, stroke_width=0)
    fill.align_to(base, LEFT)
    pct = Text(f"{int(value * 100)}%", font_size=20, color=color).next_to(base, RIGHT, buff=0.14)
    return VGroup(text, VGroup(base, fill), pct).arrange(RIGHT, buff=0.16)


def equation_label(tex: str, color=HIGH, size=38) -> MathTex:
    return MathTex(tex, font_size=size, color=color)


def concept_label(en: str, zh: str, color=HIGH, en_size: int = 25, zh_size: int = 22) -> VGroup:
    return VGroup(
        Text(en, font_size=en_size, color=color),
        Text(zh, font_size=zh_size, color=color, font=ZH_FONT),
    ).arrange(DOWN, buff=0.05)


def compact_note(text: str, color=WHITE, size: int = 22) -> Text:
    return Text(text, font_size=size, color=color)


def load_eta_distribution() -> dict:
    if FITNESS_FIT_PATH.exists():
        return json.loads(FITNESS_FIT_PATH.read_text(encoding="utf-8"))["eta_distribution"]
    return {
        "bin_edges": [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 3.0],
        "density": [0.12, 0.64, 1.0, 0.84, 0.50, 0.29, 0.13, 0.08, 0.04, 0.03, 0.0, 0.0, 0.0],
        "counts": [46, 224, 344, 288, 173, 101, 45, 27, 12, 9, 1, 0, 1],
        "quantiles": {"p50": 0.934, "p90": 1.476, "p99": 2.083},
    }


def load_web_proxy_distribution() -> dict:
    if WEB_PROXY_PATH.exists():
        return json.loads(WEB_PROXY_PATH.read_text(encoding="utf-8"))["eta_web_proxy_distribution"]
    return {
        "bin_edges": [0.65, 0.72, 0.78, 0.85, 0.92, 0.98, 1.05, 1.12, 1.18, 1.25, 1.32, 1.38, 1.45],
        "density": [0.0, 0.02, 0.13, 0.28, 0.78, 1.0, 0.57, 0.19, 0.04, 0.05, 0.03, 0.0],
        "counts": [0, 5, 30, 63, 175, 224, 127, 42, 9, 10, 6, 1],
        "quantiles": {"p50": 1.0, "p90": 1.119, "p99": 1.366},
    }


def distribution_chart(
    distribution: dict,
    x_tex: str,
    count_text: str,
    median_text: str,
    p90_text: str,
    tick_values: list[float],
    width: float = 4.6,
    height: float = 2.1,
) -> VGroup:
    edges = distribution["bin_edges"]
    density = distribution["density"]
    counts = distribution["counts"]
    quantiles = distribution["quantiles"]

    axis_color = WHITE
    x0, y0 = -width / 2, -height / 2
    eta_min = float(edges[0])
    eta_max = float(edges[-1])

    x_axis = Line([x0, y0, 0], [x0 + width, y0, 0], color=axis_color, stroke_width=2)
    y_axis = Line([x0, y0, 0], [x0, y0 + height, 0], color=axis_color, stroke_width=2)
    bars = VGroup()
    for left, right, value, count in zip(edges[:-1], edges[1:], density, counts):
        bar_left = x0 + width * (float(left) - eta_min) / (eta_max - eta_min)
        bar_right = x0 + width * (float(right) - eta_min) / (eta_max - eta_min)
        bar_width = max(0.03, bar_right - bar_left - 0.025)
        bar_height = height * float(value)
        color = interpolate_color(LOW, HIGH, min(1.0, max(0.0, (float(left) - eta_min) / max(eta_max - eta_min, 1e-6))))
        bar = Rectangle(
            width=bar_width,
            height=bar_height,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.92,
        ).move_to([bar_left + bar_width / 2, y0 + bar_height / 2, 0])
        bars.add(bar)

    def x_for_eta(value: float) -> float:
        return x0 + width * (value - eta_min) / (eta_max - eta_min)

    median_x = x_for_eta(float(quantiles["p50"]))
    p90_x = x_for_eta(float(quantiles["p90"]))
    median = VGroup(
        DashedLine([median_x, y0, 0], [median_x, y0 + height * 0.98, 0], color=WHITE, stroke_width=2),
        MathTex(median_text, font_size=18, color=WHITE),
    )
    median[1].next_to(median[0], UP, buff=0.06).shift(LEFT * 0.08)
    p90 = VGroup(
        DashedLine([p90_x, y0, 0], [p90_x, y0 + height * 0.7, 0], color=HIGH, stroke_width=2),
        MathTex(p90_text, font_size=18, color=HIGH),
    )
    p90[1].next_to(p90[0], UP, buff=0.06).shift(RIGHT * 0.08)

    x_label = MathTex(x_tex, font_size=24, color=HIGH).next_to(x_axis.get_end(), RIGHT, buff=0.1).shift(DOWN * 0.03)
    y_label = Text("count", font_size=17, color=MUTED).rotate(PI / 2).next_to(y_axis, LEFT, buff=0.12)
    ticks = VGroup()
    for value in tick_values:
        x = x_for_eta(value)
        ticks.add(Line([x, y0 - 0.05, 0], [x, y0 + 0.05, 0], color=axis_color, stroke_width=2))
        ticks.add(Text(f"{value:g}", font_size=14, color=MUTED).move_to([x, y0 - 0.23, 0]))
    count_label = Text(count_text, font_size=17, color=WHITE).next_to(VGroup(x_axis, y_axis), UP, buff=0.18).align_to(y_axis, LEFT)
    return VGroup(x_axis, y_axis, ticks, bars, median, p90, x_label, y_label, count_label)


def eta_distribution_chart() -> VGroup:
    return distribution_chart(
        load_eta_distribution(),
        r"\widehat{\eta}",
        "1,271 fitted papers",
        r"\mathrm{median}\ 0.93",
        r"90\%\leq 1.48",
        [0.5, 1.0, 1.5, 2.0, 2.5],
    )


def web_proxy_chart() -> VGroup:
    data = load_web_proxy_distribution()
    domain_count = 695
    if WEB_PROXY_PATH.exists():
        domain_count = json.loads(WEB_PROXY_PATH.read_text(encoding="utf-8"))["domain_count"]
    return distribution_chart(
        data,
        r"\widehat{\eta}_{\mathrm{web}}",
        f"{domain_count:,} fitted domains",
        r"\mathrm{median}\ 1.00",
        r"90\%\leq 1.12",
        [0.7, 0.9, 1.1, 1.3],
    )


def condensation_reference_card() -> VGroup:
    header = Text("References", font_size=31, color=HIGH)
    book = VGroup(
        Text("Network Science book, Chapter 6.4-6.5", font_size=19),
        Text("https://networksciencebook.com/chapter/6#bose-einstein-condensation", font_size=15, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    paper = VGroup(
        Text("Bianconi and Barabasi, Bose-Einstein condensation in complex networks", font_size=19),
        Text("Phys. Rev. Lett. 86, 5632-5635 (2001)", font_size=15, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    repo = VGroup(
        Text("Course code and teaching materials", font_size=19),
        Text("https://github.com/haotianh9/graph_teaching", font_size=15, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    content = VGroup(book, paper, repo).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = RoundedRectangle(width=10.2, height=2.55, corner_radius=0.12, color=MUTED, stroke_width=1.4)
    content.move_to(frame.get_center()).align_to(frame, LEFT).shift(RIGHT * 0.42)
    return VGroup(header, VGroup(frame, content)).arrange(DOWN, buff=0.2)


class FitnessDistributionOpening(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Start from Real Time Histories", font_size=41)

        heading = VGroup(
            concept_label("estimated effective fitness", "估计的有效适应度", HIGH, en_size=25, zh_size=23),
            compact_note("doable proxies from growth histories, not one static graph", WHITE, size=20),
        ).arrange(DOWN, buff=0.08).to_edge(UP, buff=1.2)

        citation_panel = VGroup(
            Text("Citation histories", font_size=24, color=HIGH),
            Text("SNAP HEP-TH papers", font_size=18, color=WHITE),
            eta_distribution_chart(),
        ).arrange(DOWN, buff=0.08).move_to(LEFT * 3.15 + DOWN * 0.42)

        web_panel = VGroup(
            Text("Web-domain snapshots", font_size=24, color=HIGH),
            Text("Common Crawl top domains", font_size=18, color=WHITE),
            web_proxy_chart(),
        ).arrange(DOWN, buff=0.08).move_to(RIGHT * 3.15 + DOWN * 0.42)

        bottom = VGroup(
            compact_note("Book anchor: page-level Web documents; here: domain-level Common Crawl PageRank snapshots.", HIGH, size=18),
            compact_note("Static edge lists show topology, not fitness; we need time histories.", WHITE, size=19),
            MathTex(r"\rho(\eta)\ \mathrm{can\ decide:\ fit\!-\!get\!-\!rich\ or\ condensation}", font_size=25, color=HIGH),
        ).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.2)

        self.play(FadeIn(heading), run_time=1.0)
        self.play(FadeIn(citation_panel), run_time=1.2)
        self.play(FadeIn(web_panel), run_time=1.2)
        self.play(FadeIn(bottom), run_time=0.8)
        self.wait(2.1)


class TwoOutcomesOrderParameter(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Same Rule, Two Macroscopic Outcomes", font_size=40)

        left_graph = scale_free_graph()
        right_graph = condensed_graph()
        left_obj = graph_mobject(left_graph, seed=4, scale=3.05, center=LEFT * 3.25 + DOWN * 0.35)
        right_obj = graph_mobject(right_graph, seed=8, scale=3.05, center=RIGHT * 3.25 + DOWN * 0.35)
        left_degrees = dict(left_graph.degree())
        left_hubs = [node for node, _ in sorted(left_degrees.items(), key=lambda item: item[1], reverse=True)[:4]]
        right_obj.vertices[0].set_fill(ALERT)
        rings = VGroup(*(node_ring(left_obj, node, HIGH) for node in left_hubs), node_ring(right_obj, 0, ALERT, radius_buff=0.25))

        left_title = VGroup(
            concept_label("scale-free", "无标度相", HIGH, en_size=25, zh_size=21),
            compact_note("several hubs coexist", WHITE, size=19),
        ).arrange(DOWN, buff=0.04).move_to(LEFT * 3.25 + UP * 2.3)
        right_title = VGroup(
            concept_label("condensed phase", "凝聚相", ALERT, en_size=25, zh_size=21),
            compact_note("one super-hub dominates", WHITE, size=19),
        ).arrange(DOWN, buff=0.04).move_to(RIGHT * 3.25 + UP * 2.3)

        order_label = concept_label("order parameter", "序参量", HIGH, en_size=22, zh_size=20)
        order = MathTex(r"s_{\max}(t)=\frac{k_{\max}(t)}{\sum_j k_j(t)}", font_size=35, color=WHITE)
        bars = VGroup(
            share_bar(r"$s_{\max}\to 0$", 0.12, HIGH),
            share_bar(r"$s_{\max}\ \mathrm{finite}$", 0.58, ALERT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        order_group = VGroup(order_label, order, bars).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(left_title), Create(left_obj), run_time=1.3)
        self.play(FadeIn(right_title), Create(right_obj), run_time=1.3)
        self.play(FadeIn(rings), FadeIn(order_group), run_time=1.1)
        self.wait(2.1)


class CondensationAsPhaseTransition(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Condensation Is a Topological Phase Transition", font_size=38)

        hierarchy = VGroup(
            concept_label("hub hierarchy", "hub 层级", HIGH, en_size=25, zh_size=21),
            compact_note("no finite-share winner", WHITE, size=20),
            MathTex(r"s_{\max}(t)\rightarrow 0", font_size=36, color=HIGH),
        ).arrange(DOWN, buff=0.14).move_to(LEFT * 3.45 + UP * 1.05)

        winner = VGroup(
            concept_label("condensation", "凝聚", ALERT, en_size=25, zh_size=22),
            compact_note("finite link share", WHITE, size=20),
            MathTex(r"s_{\max}(t)>0", font_size=36, color=ALERT),
        ).arrange(DOWN, buff=0.14).move_to(RIGHT * 3.45 + UP * 1.05)

        mapping = VGroup(
            VGroup(MathTex(r"\eta_i=e^{-\beta_T\epsilon_i}", font_size=35, color=HIGH), compact_note("higher fitness -> lower energy", MUTED, size=20)).arrange(DOWN, buff=0.06),
            VGroup(compact_note("links", LOW, size=22), Arrow(LEFT, RIGHT, color=MUTED, stroke_width=4), compact_note("particles", LOW, size=22)).arrange(RIGHT, buff=0.16),
            VGroup(compact_note("super-hub", ALERT, size=22), Arrow(LEFT, RIGHT, color=MUTED, stroke_width=4), compact_note("lowest energy", ALERT, size=22)).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)

        arrow = Arrow(hierarchy.get_right(), winner.get_left(), color=ALERT, stroke_width=7, buff=0.35)
        label = concept_label("phase transition", "相变", ALERT, en_size=22, zh_size=20).next_to(arrow, UP, buff=0.15)

        self.play(FadeIn(hierarchy), run_time=1.0)
        self.play(Create(arrow), FadeIn(label), FadeIn(winner), run_time=1.1)
        self.play(FadeIn(mapping), run_time=1.2)
        self.wait(2.1)


class RuleToTopology(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Microscopic Rules Leave Macroscopic Traces", font_size=42)

        top = VGroup(
            small_badge("rule", LOW),
            Arrow(LEFT, RIGHT, color=MUTED, stroke_width=5),
            small_badge("competition", HIGH),
            Arrow(LEFT, RIGHT, color=MUTED, stroke_width=5),
            small_badge("topology", ALERT),
        ).arrange(RIGHT, buff=0.22).shift(UP * 1.55)

        types = VGroup(
            VGroup(
                concept_label("Type 1", "参数调节", HIGH, en_size=23, zh_size=20),
                compact_note("degree exponent changes", MUTED, size=18),
            ).arrange(DOWN, buff=0.1),
            VGroup(
                concept_label("Type 2", "结构修正", MID, en_size=23, zh_size=20),
                compact_note("cutoff or saturation", MUTED, size=18),
            ).arrange(DOWN, buff=0.1),
            VGroup(
                concept_label("Type 3", "相变", ALERT, en_size=23, zh_size=20),
                compact_note("scale-free can break", MUTED, size=18),
            ).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.8).shift(DOWN * 0.55)

        cap = Text("Rule change -> topology change", font_size=26, color=HIGH).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(top), run_time=1.0)
        self.play(FadeIn(types), run_time=1.2)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(2.1)


class InitialAttractiveness(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Initial Attractiveness: Smooth Exponent Tuning", font_size=38)

        formulas = VGroup(
            concept_label("initial attractiveness", "初始吸引力", HIGH, en_size=24, zh_size=21),
            MathTex(r"\Pi(k)\sim A+k", font_size=44, color=HIGH),
            MathTex(r"\gamma=3+\frac{A}{m}", font_size=44, color=WHITE),
            compact_note("zero-degree nodes still have a chance", MUTED, size=22),
        ).arrange(DOWN, buff=0.13).shift(UP * 1.25)

        left = VGroup(
            Text("A = 0", font_size=28, color=LOW),
            compact_note("standard PA", WHITE, size=22),
            share_bar("hub advantage", 0.78, LOW, width=2.6),
        ).arrange(DOWN, buff=0.22).shift(LEFT * 3.1 + DOWN * 1.15)
        right = VGroup(
            Text("A > 0", font_size=28, color=HIGH),
            compact_note("small nodes get chances", WHITE, size=22),
            share_bar("hub advantage", 0.48, HIGH, width=2.6),
        ).arrange(DOWN, buff=0.22).shift(RIGHT * 3.1 + DOWN * 1.15)
        verdict = Text("smooth tuning, not winner-takes-all", font_size=25, color=HIGH).to_edge(DOWN, buff=0.43)

        self.play(FadeIn(formulas), run_time=1.2)
        self.play(FadeIn(left), FadeIn(right), run_time=1.2)
        self.play(FadeIn(verdict), run_time=0.8)
        self.wait(2.1)


class InternalLinksAcceleratedGrowth(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Internal Links and Accelerated Growth", font_size=40)

        points = [LEFT * 0.8, RIGHT * 0.8, UP * 0.7, DOWN * 0.7, LEFT * 1.5 + DOWN * 0.2, RIGHT * 1.5 + UP * 0.2]
        pref_edges = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 5), (2, 5), (0, 4)]
        rand_edges = [(0, 4), (1, 5), (2, 3), (0, 2), (1, 3), (4, 5)]
        pref = VGroup(
            concept_label("internal links", "内部连边", HIGH, en_size=23, zh_size=20),
            simple_graph(points, pref_edges, {0: HIGH, 1: HIGH, 2: MID}),
            compact_note("hub-to-hub reinforcement", WHITE, size=19),
        ).arrange(DOWN, buff=0.16)
        random = VGroup(
            concept_label("random links", "随机连边", LOW, en_size=23, zh_size=20),
            simple_graph(points, rand_edges, {3: MID, 5: MID}),
            compact_note("closer to random mixing", WHITE, size=19),
        ).arrange(DOWN, buff=0.16)
        panels = VGroup(pref, random).arrange(RIGHT, buff=1.15).shift(UP * 0.35)

        accel = VGroup(
            MathTex(r"m(t)=m_0t^\theta", font_size=38, color=HIGH),
            compact_note("accelerated growth / 加速增长", HIGH, size=23),
            compact_note("average degree can increase over time", MUTED, size=21),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.42)

        self.play(FadeIn(panels), run_time=1.3)
        self.play(FadeIn(accel), run_time=1.0)
        self.wait(2.2)


class NodeDeletionPhaseMap(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Node Deletion Can Destroy Scale-Free Structure", font_size=38)

        axes = Axes(
            x_range=[0, 1, 0.5],
            y_range=[0, 1, 0.5],
            x_length=7.0,
            y_length=4.2,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
        ).shift(LEFT * 1.35 + DOWN * 0.25)
        xlab = MathTex(r"A\ \text{initial attractiveness}", font_size=23, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.14)
        ylab = MathTex(r"r\ \text{removal rate}", font_size=23, color=MUTED).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.17)

        boundary = axes.plot(lambda x: 0.72 - 0.45 * x + 0.06 * np.sin(5 * x), x_range=[0.05, 0.95], color=ALERT, stroke_width=5)
        region1 = concept_label("scale-free", "无标度", HIGH, en_size=25, zh_size=20).move_to(axes.c2p(0.25, 0.30))
        region2 = Text("stretched\nexponential", font_size=22, color=MID, line_spacing=0.8).move_to(axes.c2p(0.62, 0.58))
        region3 = Text("exponential", font_size=27, color=ALERT).move_to(axes.c2p(0.78, 0.83))
        critical = Text("critical boundary", font_size=20, color=ALERT).move_to(axes.c2p(0.46, 0.76))
        rates = VGroup(
            concept_label("node deletion", "节点删除", ALERT, en_size=25, zh_size=21),
            Text("r < 1: growth wins", font_size=21, color=HIGH),
            Text("r = 1: balance", font_size=21, color=WHITE),
            Text("r > 1: decline", font_size=21, color=ALERT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.65).shift(DOWN * 0.2)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=0.9)
        self.play(Create(boundary), FadeIn(region1), FadeIn(region2), FadeIn(region3), FadeIn(critical), run_time=1.2)
        self.play(FadeIn(rates), run_time=0.8)
        self.wait(2.3)


class AgingRegimes(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Aging Is Another Control Parameter", font_size=41)

        formula = VGroup(
            concept_label("aging", "老化", HIGH, en_size=24, zh_size=21),
            MathTex(r"\tau_i=t-t_i", font_size=36, color=WHITE),
            MathTex(r"\Pi(k_i,\tau_i)\sim k_i\tau_i^{-\nu}", font_size=42, color=HIGH),
        ).arrange(DOWN, buff=0.1).shift(UP * 1.65)

        def panel(title: str, subtitle: str, points, edges, color) -> VGroup:
            graph = simple_graph(points, edges, {0: color}, edge_color=MUTED)
            graph[1][0].scale(1.55)
            return VGroup(
                Text(title, font_size=25, color=color),
                graph,
                Text(subtitle, font_size=19, color=WHITE),
            ).arrange(DOWN, buff=0.16)

        star_points = [ORIGIN, UP * 0.8, DOWN * 0.8, LEFT * 0.75, RIGHT * 0.75, UL * 0.65, DR * 0.65]
        star_edges = [(0, i) for i in range(1, 7)]
        hierarchy_points = [LEFT * 0.8, ORIGIN, RIGHT * 0.8, UP * 0.7, DOWN * 0.7, LEFT * 1.2 + DOWN * 0.2, RIGHT * 1.2 + UP * 0.2]
        hierarchy_edges = [(0, 1), (1, 2), (1, 3), (1, 4), (0, 5), (2, 6), (3, 6)]
        chain_points = [LEFT * 1.1, LEFT * 0.65, LEFT * 0.2, RIGHT * 0.25, RIGHT * 0.7, RIGHT * 1.15]
        chain_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

        panels = VGroup(
            panel(r"ν < 0", "old nodes favored", star_points, star_edges, ALERT),
            panel(r"ν = 0", "BA-like hierarchy", hierarchy_points, hierarchy_edges, HIGH),
            panel(r"ν > 1", "recent nodes dominate", chain_points, chain_edges, LOW),
        ).arrange(RIGHT, buff=0.75).scale(0.9).shift(DOWN * 0.65)
        cap = Text("aging can preserve, weaken, or break scale-free structure", font_size=24, color=HIGH).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(formula), run_time=1.0)
        self.play(FadeIn(panels), run_time=1.4)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(2.1)


class DynamicsTakeaway(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_title(self, "Topology Follows Dynamics", font_size=44)

        rows = [
            ("fitness distribution / 适应度分布", "fit-get-rich or condensation", HIGH),
            ("initial attractiveness / 初始吸引力", "γ increases; hubs weaken", MID),
            ("internal links / 内部连边", "density and reinforcement change", LOW),
            ("node deletion / 节点删除", "cutoff or exponential transition", ALERT),
            ("aging / 老化", "old hubs fade; scale-free can break", ALERT),
            ("accelerated growth / 加速增长", "average degree changes over time", HIGH),
        ]
        table_rows = VGroup()
        for mechanism, effect, color in rows:
            table_rows.add(
                VGroup(
                    Text(mechanism, font_size=18, color=color, font=ZH_FONT),
                    Text(effect, font_size=18, color=WHITE),
                ).arrange(RIGHT, buff=0.5).align_to(ORIGIN, LEFT)
            )
        table = table_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).shift(UP * 1.0 + LEFT * 0.45)
        conclusion = VGroup(
            Text("not one universal power law", font_size=23, color=MUTED),
            concept_label("topology follows dynamics", "拓扑跟随动力学", HIGH, en_size=27, zh_size=23),
        ).arrange(DOWN, buff=0.1).next_to(table, DOWN, buff=0.25)
        refs = condensation_reference_card().scale(0.54).to_edge(DOWN, buff=0.15)

        self.play(FadeIn(table), run_time=1.2)
        self.play(FadeIn(conclusion), run_time=0.9)
        self.play(FadeIn(refs), run_time=0.9)
        self.wait(2.1)
