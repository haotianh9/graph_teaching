from manim import *
import networkx as nx
import numpy as np


NODE_COLOR = BLUE_C
HUB_COLOR = YELLOW
EDGE_COLOR = GREY_B
TEXT_COLOR = WHITE
FAINT_COLOR = GREY_C
NETWORK_SCIENCE_BOOK_URL = "https://www.networksciencebook.com/"
GITHUB_REPO_URL = "https://github.com/haotianh9/graph_teaching"


def make_caption(text, font_size=23, color=TEXT_COLOR, buff=0.2):
    caption = Text(text, font_size=font_size, color=color)
    max_width = config.frame_width - 1.0
    if caption.width > max_width:
        caption.scale_to_fit_width(max_width)
    background = BackgroundRectangle(caption, color=BLACK, fill_opacity=0.72, buff=0.14)
    group = VGroup(background, caption)
    group.to_edge(DOWN, buff=buff)
    return group


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


def spring_layout_3d(G, seed=1, scale=3.0, k=None, iterations=80):
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=iterations)
    return {
        node: np.array([scale * pos[node][0], scale * pos[node][1], 0.0])
        for node in G.nodes()
    }


def top_degree_nodes(G, top=1):
    return [node for node, _ in sorted(G.degree(), key=lambda item: item[1], reverse=True)[:top]]


def make_graph_mobject(G, layout=None, hub_nodes=None, min_radius=0.03, max_radius=0.13):
    if layout is None:
        layout = spring_layout_3d(G)
    if hub_nodes is None:
        hub_nodes = []

    degrees = dict(G.degree())
    max_degree = max(max(degrees.values()) if degrees else 1, 1)
    vertex_config = {}
    for node in G.nodes():
        degree_fraction = degrees[node] / max_degree
        radius = min_radius + (max_radius - min_radius) * degree_fraction
        vertex_config[node] = {
            "radius": radius,
            "fill_color": HUB_COLOR if node in hub_nodes else NODE_COLOR,
            "fill_opacity": 1.0,
            "stroke_color": WHITE,
            "stroke_width": 0.6,
        }

    return Graph.from_networkx(
        G,
        layout=layout,
        labels=False,
        vertex_config=vertex_config,
        edge_config={
            "stroke_color": EDGE_COLOR,
            "stroke_width": 0.8,
            "stroke_opacity": 0.24,
        },
    )


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
            Text("1. Track one node i", font_size=25),
            Text("2. Replace random jumps by expected growth", font_size=25),
            Text("3. Treat time and degree as continuous", font_size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bullets.to_edge(LEFT, buff=0.8).shift(DOWN * 0.35)

        equations = VGroup(
            MathTex(r"\frac{dk_i}{dt}=m\Pi_i(t)", font_size=38),
            MathTex(r"\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}", font_size=36),
            MathTex(r"\sum_j k_j(t)\approx 2mt", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        equations.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.35)

        caption = make_caption("Continuum theory turns the stochastic algorithm into an approximate differential equation.")

        self.play(Write(title))
        self.play(FadeIn(bullets), run_time=1.1)
        self.play(Write(equations), FadeIn(caption), run_time=1.6)
        self.wait(4.0)


class BADegreeGrowthEquation(Scene):
    def construct(self):
        title = Title("Degree Growth of One Node")
        derivation = VGroup(
            MathTex(r"\frac{dk_i}{dt}=m\frac{k_i}{2mt}", font_size=38),
            MathTex(r"\frac{dk_i}{dt}=\frac{k_i}{2t}", font_size=40, color=YELLOW),
            MathTex(r"k_i(t_i)=m", font_size=36),
        ).arrange(DOWN, buff=0.32)
        derivation.to_edge(LEFT, buff=0.9).shift(DOWN * 0.1)

        axes = Axes(
            x_range=[1, 10, 3],
            y_range=[0, 4, 1],
            x_length=4.1,
            y_length=2.6,
            tips=False,
            axis_config={"include_numbers": False},
        )
        curve = axes.plot(lambda x: 1.0 * np.sqrt(x / 1.5), x_range=[1.5, 10], color=YELLOW)
        start_dot = Dot(axes.c2p(1.5, 1.0), color=GREEN_C)
        label = MathTex(r"k_i(t)=m\left(\frac{t}{t_i}\right)^{1/2}", font_size=34)
        plot_group = VGroup(axes, curve, start_dot, label)
        label.next_to(axes, UP, buff=0.15)
        plot_group.to_edge(RIGHT, buff=0.85).shift(DOWN * 0.05)

        caption = make_caption("Older nodes have had more time to grow, but growth is sublinear in time.")

        self.play(Write(title))
        self.play(Write(derivation), run_time=1.7)
        self.play(Create(axes), Create(curve), FadeIn(start_dot), Write(label), FadeIn(caption), run_time=1.5)
        self.wait(4.0)


class BABirthTimeDistribution(Scene):
    def construct(self):
        title = Title("Birth Time Becomes Degree")
        left = VGroup(
            Text("Nodes arrive roughly uniformly in time", font_size=25, color=YELLOW),
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

        caption = make_caption("The degree distribution comes from asking how many nodes were born early enough.")

        self.play(Write(title))
        self.play(FadeIn(left), run_time=1.2)
        self.play(Create(timeline), FadeIn(dots), FadeIn(old_label), FadeIn(young_label), Create(arrow), FadeIn(caption), run_time=1.5)
        self.wait(4.0)


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

        caption = make_caption("The BA exponent is 3 under the continuum approximation.")

        self.play(Write(title))
        self.play(Write(equations), run_time=1.8)
        self.play(Create(axes), Create(curve), FadeIn(label), FadeIn(caption), run_time=1.4)
        self.wait(4.5)


class BASimulationSanityCheck(Scene):
    def construct(self):
        title = Title("Simulation Sanity Check")
        G = nx.barabasi_albert_graph(500, 2, seed=9)
        layout = spring_layout_3d(G, seed=6, scale=2.3, k=0.13, iterations=80)
        graph = make_graph_mobject(
            G,
            layout=layout,
            hub_nodes=top_degree_nodes(G, top=3),
            min_radius=0.01,
            max_radius=0.075,
        )
        graph.scale(0.95).to_edge(LEFT, buff=0.35).shift(DOWN * 0.1)

        degree_values = [degree for _, degree in G.degree()]
        plot = make_log_log_points(degree_values, width=3.5, height=2.3)
        plot.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.1)
        plot_title = Text("log-log degree counts", font_size=22, color=YELLOW).next_to(plot, UP, buff=0.2)

        caption = make_caption("Finite simulations are noisy, but the high-degree tail is visibly heavy.")

        self.play(Write(title))
        self.play(FadeIn(graph), run_time=1.6)
        self.play(FadeIn(plot), FadeIn(plot_title), FadeIn(caption), run_time=1.3)
        self.wait(4.5)


class BATheoryTakeaway(Scene):
    def construct(self):
        title = Title("What the Derivation Says")
        card_font_size = 22
        cards = VGroup(
            VGroup(
                Text("Continuum approx.", font_size=card_font_size, color=YELLOW),
                Text("random jumps", font_size=card_font_size),
                Text("expected growth", font_size=card_font_size),
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

        self.play(Write(title))
        self.play(FadeIn(boxes), run_time=1.4)
        self.play(FadeIn(next_line), run_time=0.7)
        self.wait(3.0)
        self.play(FadeOut(title), FadeOut(boxes), FadeOut(next_line), run_time=0.8)
        self.play(FadeIn(reference_card), run_time=0.8)
        self.wait(5.0)
