from __future__ import annotations

import math

import networkx as nx
import numpy as np
from manim import *


BG = "#050609"
LOW = BLUE_C
MID = GREEN_C
HIGH = YELLOW
ALERT = RED_C
MUTED = GREY_B


def add_title(scene: Scene, title: str, font_size: int = 44) -> VGroup:
    title_obj = Tex(title, font_size=font_size).to_edge(UP, buff=0.25)
    rule = Line(LEFT * 6.45, RIGHT * 6.45, color=WHITE, stroke_width=2).next_to(title_obj, DOWN, buff=0.14)
    scene.play(Write(title_obj), Create(rule), run_time=0.9)
    return VGroup(title_obj, rule)


def reference_card(chapter_url: str) -> VGroup:
    header = Text("References", font_size=32, color=HIGH)
    book = VGroup(
        Text("Network Science book, Chapter 6", font_size=20),
        Text(chapter_url, font_size=16, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    repo = VGroup(
        Text("Course code and teaching materials", font_size=20),
        Text("https://github.com/haotianh9/graph_teaching", font_size=16, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    content = VGroup(book, repo).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    frame = RoundedRectangle(width=8.7, height=1.75, corner_radius=0.12, color=MUTED, stroke_width=1.4)
    content.move_to(frame.get_center()).align_to(frame, LEFT).shift(RIGHT * 0.42)
    return VGroup(header, VGroup(frame, content)).arrange(DOWN, buff=0.22)


def fit_color(value: float, low: float = 0.5, high: float = 2.5):
    alpha = max(0.0, min(1.0, (value - low) / (high - low)))
    return interpolate_color(LOW, HIGH, alpha)


def normalize_layout(graph: nx.Graph, seed: int, scale: float, center=ORIGIN) -> dict[int, np.ndarray]:
    pos = nx.spring_layout(graph, seed=seed, k=0.85 / math.sqrt(max(len(graph), 1)), iterations=120)
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


def graph_mobject(graph: nx.Graph, etas: dict[int, float] | None = None, seed: int = 1, scale: float = 4.0, center=ORIGIN) -> Graph:
    layout = normalize_layout(graph, seed=seed, scale=scale, center=center)
    degrees = dict(graph.degree())
    max_degree = max(degrees.values()) if degrees else 1
    vertex_config = {}
    for node in graph.nodes():
        eta = etas.get(node, 1.0) if etas else 1.0
        vertex_config[node] = {
            "radius": 0.065 + 0.16 * math.sqrt(degrees[node] / max_degree),
            "fill_color": fit_color(eta),
            "fill_opacity": 0.95,
            "stroke_color": WHITE,
            "stroke_width": 1.0,
        }
    return Graph(
        list(graph.nodes()),
        list(graph.edges()),
        layout=layout,
        vertex_config=vertex_config,
        edge_config={"stroke_color": GREY_B, "stroke_width": 1.1, "stroke_opacity": 0.42},
    )


def node_ring(graph_obj: Graph, node: int, color=HIGH, radius_buff: float = 0.12) -> Circle:
    dot = graph_obj.vertices[node]
    return Circle(radius=dot.radius + radius_buff, color=color, stroke_width=4).move_to(dot.get_center())


def small_badge(text: str, color=HIGH) -> VGroup:
    label = Text(text, font_size=23, color=color)
    box = RoundedRectangle(
        width=label.width + 0.42,
        height=label.height + 0.25,
        corner_radius=0.1,
        color=color,
        stroke_width=2,
    )
    return VGroup(box, label)
