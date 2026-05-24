from manim import *
from pathlib import Path
import networkx as nx
import numpy as np


NODE_COLOR = BLUE_C
HUB_COLOR = YELLOW
EDGE_COLOR = GREY_B
FITNESS_COLOR = ORANGE
AGING_COLOR = GREY_B
NETWORK_SCIENCE_BOOK_URL = "https://www.networksciencebook.com/"
GITHUB_REPO_URL = "https://github.com/haotianh9/graph_teaching"


CLUSTERING_EXAMPLES = [
    {
        "name": "C. elegans",
        "real": 0.186,
        "ba": 0.064,
    },
    {
        "name": "Facebook",
        "real": 0.606,
        "ba": 0.038,
    },
    {
        "name": "Collab.",
        "real": 0.644,
        "ba": 0.001,
    },
]


def make_caption(text, font_size=23, color=WHITE, buff=0.2):
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
    box = RoundedRectangle(width=8.7, height=2.7, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.8)
    body.move_to(box.get_center())
    card = VGroup(title, VGroup(box, body)).arrange(DOWN, buff=0.38)
    card.move_to(ORIGIN)
    return card


def spring_layout_3d(G, seed=1, scale=3.0, k=None, iterations=80):
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=iterations)
    return {node: np.array([scale * pos[node][0], scale * pos[node][1], 0.0]) for node in G.nodes()}


def top_degree_nodes(G, top=1):
    return [node for node, _ in sorted(G.degree(), key=lambda item: item[1], reverse=True)[:top]]


def make_node_ring(graph, node, color=YELLOW, radius_buff=0.06, stroke_width=3.5):
    vertex = graph.vertices[node]
    radius = max(vertex.width, vertex.height) / 2 + radius_buff
    ring = Circle(radius=radius, stroke_color=color, stroke_width=stroke_width)
    ring.move_to(vertex.get_center())
    return ring


def make_node_rings(graph, nodes, color=YELLOW, radius_buff=0.06, stroke_width=3.5):
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


def find_triangle_nodes(G):
    for u in G.nodes():
        neighbors = list(G.neighbors(u))
        for i, v in enumerate(neighbors):
            for w in neighbors[i + 1:]:
                if G.has_edge(v, w):
                    return [u, v, w]
    return []


def make_triangle_highlight(graph, triangle, color=GREEN_C):
    if len(triangle) != 3:
        return VGroup()
    centers = [graph.vertices[node].get_center() for node in triangle]
    edges = VGroup(
        Line(centers[0], centers[1], stroke_color=color, stroke_width=4),
        Line(centers[1], centers[2], stroke_color=color, stroke_width=4),
        Line(centers[2], centers[0], stroke_color=color, stroke_width=4),
    )
    rings = make_node_rings(graph, triangle, color=color, radius_buff=0.045, stroke_width=3)
    return VGroup(edges, rings)


def fallback_clustered_graph():
    G = nx.connected_caveman_graph(4, 14)
    G.add_edges_from([(0, 14), (14, 28), (28, 42)])
    return nx.convert_node_labels_to_integers(G)


def load_facebook_ego_sample(max_nodes=70):
    path = Path(__file__).resolve().parents[2] / "Data" / "facebook_combined.txt"
    if not path.exists():
        return fallback_clustered_graph()

    G = nx.read_edgelist(path, nodetype=int)
    candidates = [
        node
        for node, degree in G.degree()
        if 35 <= degree <= max_nodes - 1
    ]
    best_node = None
    best_score = -1
    for node in candidates:
        ego = nx.ego_graph(G, node, radius=1)
        if ego.number_of_nodes() > max_nodes:
            continue
        score = nx.average_clustering(ego) * ego.number_of_nodes()
        if score > best_score:
            best_node = node
            best_score = score

    if best_node is None:
        return fallback_clustered_graph()

    sample = nx.ego_graph(G, best_node, radius=1)
    sample.remove_edges_from(nx.selfloop_edges(sample))
    return nx.convert_node_labels_to_integers(sample)


def make_graph_mobject(
    G,
    layout=None,
    hub_nodes=None,
    color_overrides=None,
    min_radius=0.025,
    max_radius=0.12,
    edge_color=GREY_A,
    edge_width=1.15,
    edge_opacity=0.52,
):
    if layout is None:
        layout = spring_layout_3d(G)
    if hub_nodes is None:
        hub_nodes = []
    if color_overrides is None:
        color_overrides = {}
    degrees = dict(G.degree())
    max_degree = max(max(degrees.values()) if degrees else 1, 1)
    vertex_config = {}
    for node in G.nodes():
        fraction = degrees[node] / max_degree
        vertex_config[node] = {
            "radius": min_radius + (max_radius - min_radius) * fraction,
            "fill_color": color_overrides.get(node, HUB_COLOR if node in hub_nodes else NODE_COLOR),
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
            "stroke_color": edge_color,
            "stroke_width": edge_width,
            "stroke_opacity": edge_opacity,
        },
    )


def boxed_text(title, body, color=WHITE, width=3.2, height=2.0):
    title_mob = Text(title, font_size=25, color=color)
    body_mob = Text(body, font_size=20, color=WHITE)
    if body_mob.width > width - 0.4:
        body_mob.scale_to_fit_width(width - 0.4)
    content = VGroup(title_mob, body_mob).arrange(DOWN, buff=0.18)
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=2)
    content.move_to(box.get_center())
    return VGroup(box, content)


def change_limit_card(title, lines, color=WHITE, width=3.15, height=1.65):
    title_mob = Text(title, font_size=21, color=color)
    body = VGroup(*[Text(line, font_size=17, color=WHITE) for line in lines])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    if content.width > width - 0.3:
        content.scale_to_fit_width(width - 0.3)
    if content.height > height - 0.25:
        content.scale_to_fit_height(height - 0.25)
    box = RoundedRectangle(width=width, height=height, corner_radius=0.10, stroke_color=color, stroke_width=1.8)
    content.move_to(box.get_center())
    return VGroup(box, content)


def make_highlight_outline(mobject, color=YELLOW, buff=0.045, stroke_width=2.4):
    outline = SurroundingRectangle(
        mobject,
        color=color,
        buff=buff,
        stroke_width=stroke_width,
    )
    outline.set_z_index(50)
    return outline


def sync_highlight(scene, mobject, start, end, color=YELLOW, buff=0.045, stroke_width=2.4):
    if scene.time < start:
        scene.wait(start - scene.time)
    duration = max(end - max(scene.time, start), 0.08)
    outline = make_highlight_outline(mobject, color=color, buff=buff, stroke_width=stroke_width)
    scene.add(outline)
    scene.wait(duration)
    scene.remove(outline)


def sync_multi_highlight(scene, mobjects, start, end, color=YELLOW, buff=0.035, stroke_width=2.2):
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
    if scene.time < start:
        scene.wait(start - scene.time)
    scene.wait(max(end - max(scene.time, start), 0.08))


class BAWhatItExplains(Scene):
    def construct(self):
        title = Title("BA vs Real Networks")
        G = nx.barabasi_albert_graph(85, 2, seed=15)
        graph = make_graph_mobject(
            G,
            layout=spring_layout_3d(G, seed=4, scale=2.55, k=0.24),
            hub_nodes=top_degree_nodes(G, top=4),
            min_radius=0.025,
            max_radius=0.14,
            edge_width=1.1,
            edge_opacity=0.5,
        )
        graph.scale_to_fit_width(4.85)
        if graph.height > 5.25:
            graph.scale_to_fit_height(5.25)
        graph.move_to(LEFT * 4.35 + DOWN * 0.32)
        hub_rings = make_node_rings(graph, top_degree_nodes(G, top=4), color=YELLOW)

        question = Text(
            "What does BA explain,\nand what does it miss?",
            font_size=30,
            line_spacing=0.85,
            color=YELLOW,
        )
        bullets = VGroup(
            Text("explains: hubs and heavy tails", font_size=24, color=GREEN_C),
            Text("misses: strong local clustering", font_size=24, color=RED_C),
            Text("extensions add missing mechanisms", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        if question.width > 5.05:
            question.scale_to_fit_width(5.05)
        if bullets.width > 5.05:
            bullets.scale_to_fit_width(5.05)
        right_column = VGroup(question, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.58)
        right_column.move_to(RIGHT * 3.65 + UP * 0.35)
        caption = make_caption("BA is a baseline: powerful enough to create hubs, but not the whole story.")

        self.add(title, graph, hub_rings, question, bullets, caption)
        sync_pause(self, 0.0, 14.0)
        sync_pause(self, 14.0, 18.0)
        sync_pause(self, 18.0, 22.0)


class BAVisualDifference(Scene):
    def construct(self):
        title = Title("BA Model vs Real Network")

        real = load_facebook_ego_sample(max_nodes=45)
        ba = nx.barabasi_albert_graph(real.number_of_nodes(), 2, seed=23)

        ba_graph = make_graph_mobject(
            ba,
            layout=spring_layout_3d(ba, seed=9, scale=2.15, k=0.28, iterations=90),
            hub_nodes=top_degree_nodes(ba, top=2),
            min_radius=0.025,
            max_radius=0.12,
            edge_width=1.2,
            edge_opacity=0.58,
        )
        ba_rings = make_node_rings(ba_graph, top_degree_nodes(ba, top=2), color=YELLOW)
        ba_group = VGroup(ba_graph, ba_rings)

        triangle = find_triangle_nodes(real)
        real_graph = make_graph_mobject(
            real,
            layout=spring_layout_3d(real, seed=12, scale=2.15, k=0.23, iterations=100),
            color_overrides={node: GREEN_C for node in triangle},
            min_radius=0.024,
            max_radius=0.09,
            hub_nodes=[],
            edge_width=1.05,
            edge_opacity=0.46,
        )
        triangle_highlight = make_triangle_highlight(real_graph, triangle, color=GREEN_C)
        real_group = VGroup(real_graph, triangle_highlight)

        ba_panel = VGroup(
            Text("BA baseline", font_size=28, color=YELLOW),
            ba_group,
            Text("hubs from preferential attachment", font_size=20),
            Text("weak local triangle closure", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.18)

        real_panel = VGroup(
            Text("real Facebook sample", font_size=28, color=YELLOW),
            real_group,
            Text("higher local clustering", font_size=20),
            Text("community structure is visible", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.18)

        panels = VGroup(ba_panel, real_panel).arrange(RIGHT, buff=0.85)
        panels.scale(0.9).next_to(title, DOWN, buff=0.45)

        caption = make_caption(
            "The real sample has local clustered groups; BA gives hubs but misses much of this geometry."
        )

        self.add(title, ba_panel, real_panel, caption)
        sync_pause(self, 0.0, 9.0)
        sync_pause(self, 9.0, 16.0)
        sync_pause(self, 16.0, 21.0)
        sync_pause(self, 21.0, 28.0)
        sync_pause(self, 28.0, 32.0)


class BATriadicClosure(Scene):
    def construct(self):
        title = Title("Extension 1: Triad Formation")
        equation = VGroup(
            Text("Holme-Kim style triad formation (2002)", font_size=23, color=YELLOW),
            MathTex(
                r"\text{after PA: link to a target neighbor with probability }p",
                font_size=31,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.06)
        equation.next_to(title, DOWN, buff=0.18)

        target = Circle(radius=0.28, fill_color=HUB_COLOR, fill_opacity=1, stroke_color=WHITE)
        neighbor_a = Circle(radius=0.20, fill_color=NODE_COLOR, fill_opacity=1, stroke_color=WHITE)
        neighbor_b = Circle(radius=0.20, fill_color=NODE_COLOR, fill_opacity=1, stroke_color=WHITE)
        new_node = Circle(radius=0.22, fill_color=RED_C, fill_opacity=1, stroke_color=WHITE)

        target.move_to(LEFT * 0.9 + UP * 0.35)
        neighbor_a.move_to(RIGHT * 0.75 + UP * 1.05)
        neighbor_b.move_to(RIGHT * 0.75 + DOWN * 0.35)
        new_node.move_to(LEFT * 3.1 + DOWN * 0.35)

        existing_edges = VGroup(
            Line(target.get_center(), neighbor_a.get_center(), stroke_color=GREY_A, stroke_width=3.2),
            Line(target.get_center(), neighbor_b.get_center(), stroke_color=GREY_A, stroke_width=3.2),
        )
        pa_edge = Line(new_node.get_center(), target.get_center(), stroke_color=YELLOW, stroke_width=5.0)
        closure_edge = Line(new_node.get_center(), neighbor_a.get_center(), stroke_color=GREEN_C, stroke_width=5.0)
        triangle = Polygon(
            new_node.get_center(),
            target.get_center(),
            neighbor_a.get_center(),
            stroke_color=GREEN_C,
            stroke_width=3.0,
            fill_color=GREEN_C,
            fill_opacity=0.12,
        )

        labels = VGroup(
            Text("new node", font_size=19, color=RED_C).next_to(new_node, DOWN, buff=0.16),
            Text("PA target", font_size=19, color=YELLOW).next_to(target, DOWN, buff=0.16),
            Text("target's neighbor", font_size=19, color=GREEN_C).next_to(neighbor_a, UP, buff=0.16),
        )
        mechanism = VGroup(existing_edges, pa_edge, closure_edge, triangle, target, neighbor_a, neighbor_b, new_node, labels)
        mechanism.next_to(equation, DOWN, buff=0.38).shift(LEFT * 1.65)

        steps = VGroup(
            Text("1. PA chooses a target", font_size=21, color=YELLOW),
            Text("2. connect to target's neighbor", font_size=21, color=GREEN_C),
            Text("3. raises clustering C", font_size=21, color=GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        steps.next_to(mechanism, RIGHT, buff=0.34)
        if steps.get_right()[0] > config.frame_width / 2 - 0.45:
            steps.shift(LEFT * (steps.get_right()[0] - (config.frame_width / 2 - 0.45)))

        effects = VGroup(
            change_limit_card(
                "Can change",
                ["clustering coefficient C", "local closure"],
                color=GREEN_C,
            ),
            change_limit_card(
                "Cannot by itself",
                ["set exponent γ", "change degree tail"],
                color=RED_C,
            ),
        ).arrange(RIGHT, buff=0.45)
        effects.next_to(VGroup(mechanism, steps), DOWN, buff=0.30)

        caption = make_caption("Triad formation changes clustering C; it is not mainly an exponent-control mechanism.")

        self.add(title, equation, existing_edges, pa_edge, closure_edge, triangle, target, neighbor_a, neighbor_b, new_node, labels, steps, effects, caption)
        sync_pause(self, 0.0, 7.0)
        sync_pause(self, 7.0, 19.0)
        sync_pause(self, 19.0, 25.0)
        sync_pause(self, 25.0, 34.0)
        sync_pause(self, 34.0, 36.0)


class BAExponentQuestion(Scene):
    def construct(self):
        title = Title(r"Can Extensions Change $\gamma$?")
        formula = MathTex(r"P(k) \sim k^{-3}", font_size=58, color=YELLOW)
        gamma_note = VGroup(
            Text("standard BA", font_size=25, color=GREY_A),
            MathTex(r"\gamma = 3", font_size=46, color=YELLOW),
            Text("critical exponent", font_size=25, color=GREY_A),
        ).arrange(DOWN, buff=0.12)
        question = Text("Which extensions change the exponent?", font_size=30, color=WHITE)
        question2 = Text("Which extensions change clustering C?", font_size=28, color=GREEN_C)

        center = VGroup(formula, gamma_note).arrange(RIGHT, buff=1.15)
        center.next_to(title, DOWN, buff=0.85)
        questions = VGroup(question, question2).arrange(DOWN, buff=0.28)
        questions.next_to(center, DOWN, buff=0.65)

        caption = make_caption("After clustering, the second axis is the degree-distribution exponent.")

        self.add(title, formula, gamma_note, questions, caption)
        sync_pause(self, 0.0, 15.0)
        sync_pause(self, 15.0, 19.0)
        sync_pause(self, 19.0, 27.0)


class BAFitness(Scene):
    def construct(self):
        title = Title("Extension 2: Fitness")
        equation = MathTex(r"\Pi_i \propto \eta_i k_i", font_size=42, color=YELLOW)
        equation.next_to(title, DOWN, buff=0.18)
        baseline = Text(
            "standard BA: current degree k controls attraction",
            font_size=22,
            color=GREY_A,
        )
        baseline.next_to(equation, DOWN, buff=0.14)

        nodes = VGroup()
        labels = VGroup()
        positions = [LEFT * 3 + DOWN * 0.35, LEFT * 1 + UP * 0.35, RIGHT * 1 + DOWN * 0.1, RIGHT * 3 + UP * 0.30]
        fitness_values = [0.6, 1.0, 1.8, 2.5]
        for idx, (pos, eta) in enumerate(zip(positions, fitness_values)):
            radius = 0.22 + 0.08 * eta
            node = Circle(radius=radius, fill_color=FITNESS_COLOR if eta > 1.5 else NODE_COLOR, fill_opacity=1, stroke_color=WHITE)
            node.move_to(pos)
            label = MathTex(r"\eta=" + f"{eta:.1f}", font_size=25).next_to(node, DOWN, buff=0.15)
            nodes.add(node)
            labels.add(label)
        arrows = VGroup(
            *[
                Arrow(DOWN * 1.8, node.get_center(), buff=0.18, color=YELLOW if i >= 2 else GREY_B, stroke_width=4)
                for i, node in enumerate(nodes)
            ]
        )
        mechanism = VGroup(nodes, labels, arrows)
        mechanism.scale(0.76).next_to(baseline, DOWN, buff=0.24)

        effects = VGroup(
            change_limit_card(
                "Can change",
                ["exponent γ", "degree tail"],
                color=GREEN_C,
            ),
            change_limit_card(
                "Cannot by itself",
                ["clustering coefficient C", "local closure"],
                color=RED_C,
            ),
        ).arrange(RIGHT, buff=0.45)
        effects.next_to(mechanism, DOWN, buff=0.30)

        caption = make_caption("Fitness can change γ and the tail, but it does not create clustering C by itself.")

        self.add(title, equation, baseline, nodes, labels, arrows, effects, caption)
        sync_pause(self, 0.0, 14.0)
        sync_pause(self, 14.0, 26.0)
        sync_pause(self, 26.0, 34.0)
        sync_pause(self, 34.0, 38.0)


class BAAging(Scene):
    def construct(self):
        title = Title("Extension 3: Aging")
        equation = MathTex(r"\Pi_i \propto k_i A(\mathrm{age}_i)", font_size=40, color=YELLOW)
        equation.next_to(title, DOWN, buff=0.18)

        timeline = NumberLine(x_range=[0, 10, 1], length=7.6, include_numbers=False)
        timeline.next_to(equation, DOWN, buff=0.85)
        old_nodes = VGroup(*[Circle(radius=0.16, fill_color=AGING_COLOR, fill_opacity=1).move_to(timeline.n2p(x)) for x in [1, 2, 3]])
        middle_nodes = VGroup(*[Circle(radius=0.18, fill_color=NODE_COLOR, fill_opacity=1).move_to(timeline.n2p(x)) for x in [5, 6]])
        new_nodes = VGroup(*[Circle(radius=0.2, fill_color=YELLOW, fill_opacity=1).move_to(timeline.n2p(x)) for x in [8, 9]])
        labels = VGroup(
            Text("old: less active", font_size=22, color=GREY_A).next_to(timeline.n2p(2), DOWN, buff=0.35),
            Text("recent: more visible", font_size=22, color=YELLOW).next_to(timeline.n2p(8.5), DOWN, buff=0.35),
        )
        timeline_group = VGroup(timeline, old_nodes, middle_nodes, new_nodes, labels)

        effects = VGroup(
            change_limit_card(
                "Can change",
                ["effective γ", "tail cutoff"],
                color=GREEN_C,
            ),
            change_limit_card(
                "Cannot by itself",
                ["high clustering C", "local closure"],
                color=RED_C,
            ),
        ).arrange(RIGHT, buff=0.45)
        effects.next_to(timeline_group, DOWN, buff=0.35)

        caption = make_caption("Aging can change effective γ, but it does not directly create high clustering C.")

        self.add(title, equation, timeline, old_nodes, middle_nodes, new_nodes, labels, effects, caption)
        sync_pause(self, 0.0, 10.0)
        sync_pause(self, 10.0, 22.0)
        sync_pause(self, 22.0, 34.0)
        sync_pause(self, 34.0, 41.0)
        sync_pause(self, 41.0, 45.0)


class BANonlinearAttachment(Scene):
    def construct(self):
        title = Title("Extension 4: Nonlinear Attachment")
        equation = MathTex(r"\Pi_i \propto k_i^\alpha", font_size=44, color=YELLOW)
        equation.next_to(title, DOWN, buff=0.18)

        panels = VGroup(
            boxed_text("alpha < 1", "stretched tail; weak hubs", color=BLUE_C, width=3.05, height=1.55),
            boxed_text("alpha = 1", "standard BA: γ = 3", color=YELLOW, width=3.05, height=1.55),
            boxed_text("alpha > 1", "condensation; winner-take-all", color=RED_C, width=3.05, height=1.55),
        ).arrange(RIGHT, buff=0.45)
        panels.next_to(equation, DOWN, buff=0.45)

        effects = VGroup(
            change_limit_card(
                "Can change",
                ["exponent γ", "tail regime"],
                color=GREEN_C,
                width=3.65,
                height=1.35,
            ),
            change_limit_card(
                "Cannot by itself",
                ["clustering coefficient C", "local closure"],
                color=RED_C,
                width=3.65,
                height=1.35,
            ),
        ).arrange(RIGHT, buff=0.55)
        effects.next_to(panels, DOWN, buff=0.35)

        caption = make_caption("Nonlinearity is the most direct way to change the BA γ=3 conclusion.")

        self.add(title, equation, panels, effects, caption)
        sync_pause(self, 0.0, 17.0)
        sync_pause(self, 17.0, 25.0)
        sync_pause(self, 25.0, 35.0)
        sync_pause(self, 35.0, 44.0)


class BARealNetworkLimitations(Scene):
    def construct(self):
        title = Title("Real Networks Have More Structure")
        cards = VGroup(
            boxed_text("Clustering", "high local clustering", color=GREEN_C),
            boxed_text("Communities", "modular structure", color=BLUE_C),
            boxed_text("Direction", "in-links and out-links differ", color=ORANGE),
            boxed_text("Change", "nodes and edges can disappear", color=RED_C),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.55))
        cards.scale(0.85).next_to(title, DOWN, buff=0.65)
        caption = make_caption("BA is a baseline; real network data often needs extra mechanisms.")

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.1), run_time=1.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(4.0)


class BAClusteringComparison(Scene):
    def construct(self):
        title = Title("Clustering Across Domains")

        axis = VGroup(
            Line(LEFT * 4.6, RIGHT * 4.6, stroke_color=GREY_B, stroke_width=2),
            Line(LEFT * 4.6, LEFT * 4.6 + UP * 3.0, stroke_color=GREY_B, stroke_width=2),
        )
        axis.shift(DOWN * 2.0)
        y_axis_label = Text("clustering coefficient C", font_size=20, color=YELLOW)
        y_axis_label.rotate(PI / 2)
        y_axis_label.next_to(axis[1], LEFT, buff=0.58)

        y_ticks = VGroup()
        for value in [0.0, 0.3, 0.6]:
            y = axis[0].get_y() + value / 0.7 * 3.0
            tick = Line(LEFT * 4.72 + UP * y, LEFT * 4.52 + UP * y, stroke_color=GREY_B, stroke_width=1.5)
            label = Text(f"{value:.1f}", font_size=18, color=GREY_A).next_to(tick, LEFT, buff=0.08)
            guide = DashedLine(LEFT * 4.5 + UP * y, RIGHT * 4.5 + UP * y, stroke_color=GREY_D, stroke_width=0.8)
            y_ticks.add(guide, tick, label)

        bars = VGroup()
        labels = VGroup()
        values = VGroup()
        x_positions = [-2.8, 0.0, 2.8]
        bar_width = 0.32
        max_c = 0.7
        scale_height = 3.0
        baseline_y = axis[0].get_y()
        for x, example in zip(x_positions, CLUSTERING_EXAMPLES):
            group_label = Text(example["name"], font_size=20, color=WHITE)
            group_label.move_to(np.array([x, baseline_y - 0.35, 0]))
            labels.add(group_label)
            for offset, key, color in [(-0.22, "ba", BLUE_C), (0.22, "real", YELLOW)]:
                height = max(0.035, example[key] / max_c * scale_height)
                bar = Rectangle(width=bar_width, height=height, fill_color=color, fill_opacity=0.9, stroke_width=0)
                bar.move_to(np.array([x + offset, baseline_y + height / 2, 0]))
                bars.add(bar)
                value = Text(f"{example[key]:.2f}", font_size=16, color=color)
                value.next_to(bar, UP, buff=0.06)
                values.add(value)

        legend = VGroup(
            VGroup(Square(0.16, fill_color=BLUE_C, fill_opacity=0.9, stroke_width=0), Text("same-N BA", font_size=18)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.16, fill_color=YELLOW, fill_opacity=0.9, stroke_width=0), Text("network data", font_size=18)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.45)
        legend.next_to(title, DOWN, buff=0.40)

        note = Text(
            "real networks across domains; BA baselines use the same N and close average degree.",
            font_size=19,
            color=GREY_A,
        )
        if note.width > config.frame_width - 1.0:
            note.scale_to_fit_width(config.frame_width - 1.0)
        note.next_to(labels, DOWN, buff=0.30)

        real_bars = VGroup(bars[1], bars[3], bars[5])
        ba_bars = VGroup(bars[0], bars[2], bars[4])
        self.add(title, legend, axis, y_axis_label, y_ticks, bars, values, labels, note)
        sync_pause(self, 0.0, 18.0)
        sync_pause(self, 18.0, 29.0)
        sync_pause(self, 29.0, 37.0)
        sync_pause(self, 37.0, 43.0)
        sync_pause(self, 43.0, 49.0)


class BAExtensionsTakeaway(Scene):
    def construct(self):
        title = Title("Takeaway")
        summary = VGroup(
            Text("BA is a baseline for hub formation", font_size=29, color=YELLOW),
            Text("Extensions move the model toward real networks", font_size=28, color=GREEN_C),
            Text("fit the mechanism, not only the curve", font_size=26, color=GREY_A),
            Text("Next: Chapter 6, network growth", font_size=27, color=BLUE_C),
        ).arrange(DOWN, buff=0.28)
        summary.next_to(title, DOWN, buff=0.72)
        reference_card = make_reference_end_card()
        reference_card.scale(0.86).to_edge(DOWN, buff=0.25)

        self.add(title, summary, reference_card)
        sync_pause(self, 0.0, 8.0)
        sync_pause(self, 8.0, 21.0)
        sync_pause(self, 21.0, 30.0)
        sync_pause(self, 30.0, 33.4)
