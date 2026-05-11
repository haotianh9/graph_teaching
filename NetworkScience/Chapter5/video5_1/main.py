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
CHINESE_FONT = "Noto Sans SC"
NETWORK_SCIENCE_BOOK_URL = "https://www.networksciencebook.com/"
GITHUB_REPO_URL = "https://github.com/haotianh9/graph_teaching"


# ============================================================
# Helper functions
# ============================================================

def ba_growth_trace(n_final=50, m=2, seed=1):
    """
    Generate a Barabási-Albert growth trace manually.

    Each step records the graph before/after adding a node, the selected
    targets, the degrees k_i, and Pi_i = k_i / sum_j k_j.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    if n_final < m + 1:
        raise ValueError("n_final must be at least m + 1")

    rng = np.random.default_rng(seed)

    # Initial seed: complete graph with m + 1 nodes.
    G = nx.complete_graph(m + 1)
    graphs = [G.copy()]
    steps = []

    for new_node in range(m + 1, n_final):
        before = G.copy()
        old_nodes = list(G.nodes())
        degrees = np.array([G.degree(v) for v in old_nodes], dtype=float)
        # Preferential attachment equation: Pi_i = k_i / sum_j k_j.
        probabilities = degrees / degrees.sum()
        if not np.isclose(probabilities.sum(), 1.0):
            raise ValueError("Preferential attachment probabilities must sum to 1.")

        targets = set()
        while len(targets) < m:
            target = rng.choice(old_nodes, p=probabilities)
            targets.add(int(target))

        G.add_node(new_node)
        for target in targets:
            G.add_edge(new_node, target)

        after = G.copy()
        graphs.append(after)
        steps.append(
            {
                "before": before,
                "after": after,
                "new_node": new_node,
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

    return {
        "initial": graphs[0],
        "graphs": graphs,
        "steps": steps,
    }


def ba_growth_sequence(n_final=50, m=2, seed=1):
    """
    Generate a Barabási-Albert graph sequence manually.

    Returns a list of NetworkX graphs:
    G_0, G_1, ..., G_T
    """
    return ba_growth_trace(n_final=n_final, m=m, seed=seed)["graphs"]


def spring_layout_3d(G, seed=1, scale=3.0, k=None, iterations=50):
    """
    Return a Manim-compatible 3D layout dictionary from NetworkX spring_layout.
    """
    pos_2d = nx.spring_layout(G, seed=seed, k=k, iterations=iterations)
    return {
        v: np.array([scale * pos_2d[v][0], scale * pos_2d[v][1], 0.0])
        for v in G.nodes()
    }


def make_node_ring(graph, node, color=YELLOW, radius_buff=0.08, stroke_width=4):
    """
    Draw a ring around one displayed graph vertex.
    """
    vertex = graph.vertices[node]
    radius = max(vertex.width, vertex.height) / 2 + radius_buff
    ring = Circle(radius=radius)
    ring.set_stroke(color=color, width=stroke_width)
    ring.move_to(vertex.get_center())
    return ring


def make_node_rings(graph, nodes, color=YELLOW, radius_buff=0.08, stroke_width=4):
    """
    Draw rings around several displayed graph vertices.
    """
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


def outside_label_direction(point, center=ORIGIN):
    """
    Pick a stable label direction away from the graph center.
    """
    vector = point - center
    if np.linalg.norm(vector) < 0.1:
        return UP
    if abs(vector[0]) >= abs(vector[1]):
        return RIGHT if vector[0] >= 0 else LEFT
    return UP if vector[1] >= 0 else DOWN


def subset_layout(layout, nodes):
    """
    Keep only positions for the given subset of nodes.
    """
    return {v: layout[v] for v in nodes if v in layout}


def make_caption(text, chinese_text=None, font_size=24, color=TEXT_COLOR, buff=0.18):
    """
    Make a bottom narration caption with a subtle backing rectangle.

    If chinese_text is supplied, show English and Chinese together.
    """
    if chinese_text is not None:
        english = Text(text, font_size=font_size * 0.76, color=GREY_A)
        chinese = Text(
            chinese_text,
            font_size=font_size * 0.82,
            color=color,
            font=CHINESE_FONT,
        )
        caption = VGroup(english, chinese).arrange(DOWN, buff=0.05)
    else:
        caption = Text(text, font_size=font_size, color=color)

    max_width = config.frame_width - 1.0
    if caption.width > max_width:
        caption.scale_to_fit_width(max_width)

    background = BackgroundRectangle(
        caption,
        color=BLACK,
        fill_opacity=0.72,
        buff=0.14,
    )
    group = VGroup(background, caption)
    group.to_edge(DOWN, buff=buff)
    return group


def replace_caption(
    scene,
    current_caption,
    text,
    chinese_text=None,
    wait_time=4.0,
    font_size=24,
):
    """
    Replace the bottom narration caption and hold it for script pacing.
    """
    next_caption = make_caption(text, chinese_text=chinese_text, font_size=font_size)
    if current_caption is None:
        scene.play(FadeIn(next_caption), run_time=0.6)
    else:
        scene.play(FadeOut(current_caption), run_time=0.3)
        scene.play(FadeIn(next_caption), run_time=0.3)
    if wait_time > 0:
        scene.wait(wait_time)
    return next_caption


def make_reference_end_card():
    """
    Shared final reference card for Chapter 5 videos.
    """
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


def top_degree_nodes(G, top=1):
    """
    Return the top-degree node IDs.
    """
    ranked = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    return [node for node, degree in ranked[:top]]


def make_graph_mobject(
    G,
    layout=None,
    layout_scale=3.0,
    highlight_nodes=None,
    hub_nodes=None,
    min_radius=0.055,
    max_radius=0.18,
    edge_opacity=0.45,
    edge_width=1.4,
):
    """
    Convert a NetworkX graph into a Manim Graph mobject.

    Node radius scales with degree.
    Selected nodes can be highlighted.
    """
    if highlight_nodes is None:
        highlight_nodes = {}

    if hub_nodes is None:
        hub_nodes = []

    degrees = dict(G.degree())
    max_degree = max(degrees.values()) if len(degrees) > 0 else 1
    max_degree = max(max_degree, 1)

    vertex_config = {}
    for v in G.nodes():
        degree_fraction = degrees[v] / max_degree
        radius = min_radius + (max_radius - min_radius) * degree_fraction

        color = NODE_COLOR
        if v in hub_nodes:
            color = HUB_COLOR
        if v in highlight_nodes:
            color = highlight_nodes[v]

        vertex_config[v] = {
            "radius": radius,
            "fill_color": color,
            "fill_opacity": 1.0,
            "stroke_color": WHITE,
            "stroke_width": 0.8,
        }

    edge_config = {
        "stroke_color": EDGE_COLOR,
        "stroke_width": edge_width,
        "stroke_opacity": edge_opacity,
    }

    if layout is None:
        layout = "spring"

    graph = Graph.from_networkx(
        G,
        layout=layout,
        layout_scale=layout_scale,
        labels=False,
        vertex_config=vertex_config,
        edge_config=edge_config,
    )

    return graph


def make_rank_degree_plot(G, title_text, width=4.0, height=2.0):
    """
    Make a simple rank-degree curve.

    x-axis: rank
    y-axis: degree
    """
    degrees = np.array(sorted([d for _, d in G.degree()], reverse=True), dtype=float)
    n = len(degrees)

    if n == 0:
        degrees = np.array([0.0])
        n = 1

    max_degree = max(float(np.max(degrees)), 1.0)

    axes = Axes(
        x_range=[1, n, max(1, n // 4)],
        y_range=[0, max_degree + 1, max(1, int(max_degree // 3) or 1)],
        x_length=width,
        y_length=height,
        tips=False,
        axis_config={
            "include_numbers": False,
            "stroke_width": 1.5,
        },
    )

    points = [
        axes.c2p(rank, degree)
        for rank, degree in zip(np.arange(1, n + 1), degrees)
    ]

    curve = VMobject()
    curve.set_points_as_corners(points)
    curve.set_stroke(YELLOW, width=3)

    title = Text(title_text, font_size=22) if title_text else VGroup()
    if title_text:
        title.next_to(axes, UP, buff=0.15)

    x_label = Text("rank", font_size=18)
    x_label.next_to(axes.x_axis, DOWN, buff=0.15)

    y_label = Text("degree", font_size=18)
    y_label.rotate(PI / 2)
    y_label.next_to(axes.y_axis, LEFT, buff=0.15)

    return VGroup(title, axes, curve, x_label, y_label)


def make_simulation_degree_plot(G):
    """
    Compact rank-degree plot used during the first BA simulation.
    """
    plot = make_rank_degree_plot(G, "degree profile", width=2.65, height=1.15)
    plot.scale(0.76)
    plot.to_corner(DL, buff=0.45)
    plot.shift(UP * 1.0 + RIGHT * 0.15)
    return plot


def same_density_er_graph(reference_graph, seed=1):
    """
    Create an Erdős-Rényi graph with approximately the same expected density
    as a reference graph.
    """
    n = reference_graph.number_of_nodes()
    e = reference_graph.number_of_edges()

    if n <= 1:
        return nx.Graph()

    p = 2 * e / (n * (n - 1))
    return nx.gnp_random_graph(n, p, seed=seed)


# ============================================================
# Scene 1: Hook
# ============================================================

class BAOpening(Scene):
    def construct(self):
        title = Text("Why do hubs appear?", font_size=46)
        title_cn = Text("枢纽节点如何出现？", font_size=30, font=CHINESE_FONT)
        subtitle = Text("Chapter 5: growth and preferential attachment", font_size=24)
        subtitle_cn = Text("第五章：增长与优先连接", font_size=21, font=CHINESE_FONT)
        header = VGroup(title, title_cn, subtitle, subtitle_cn).arrange(DOWN, buff=0.08)
        header.to_edge(UP)

        n = 45
        m = 2

        ba = ba_growth_trace(n_final=n, m=m, seed=4)["graphs"][-1]
        er = same_density_er_graph(ba, seed=22)

        ba_hub = top_degree_nodes(ba, top=1)
        er_hub = top_degree_nodes(er, top=1)
        er_layout = spring_layout_3d(er, seed=28, scale=2.7, k=0.34, iterations=90)
        ba_layout = spring_layout_3d(ba, seed=15, scale=2.7, k=0.34, iterations=90)

        er_graph = make_graph_mobject(
            er,
            layout=er_layout,
            hub_nodes=er_hub,
            edge_opacity=0.35,
        )
        ba_graph = make_graph_mobject(
            ba,
            layout=ba_layout,
            hub_nodes=ba_hub,
            edge_opacity=0.35,
        )

        er_label = VGroup(
            Text("Random graph", font_size=26),
            Text("随机网络", font_size=21, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.04)
        ba_label = VGroup(
            Text("Growing network", font_size=26),
            Text("增长网络", font_size=21, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.04)

        left = VGroup(er_graph, er_label).arrange(DOWN, buff=0.25)
        right = VGroup(ba_graph, ba_label).arrange(DOWN, buff=0.25)

        comparison = VGroup(left, right).arrange(RIGHT, buff=0.95)
        comparison.scale(0.84).shift(DOWN * 0.35)

        er_hub_ring = make_node_rings(er_graph, er_hub, color=YELLOW)
        ba_hub_ring = make_node_rings(ba_graph, ba_hub, color=YELLOW)

        caption = None
        question = VGroup(
            Text("Why do some nodes become hubs?", font_size=31, color=YELLOW),
            Text("为什么有些节点会变成枢纽？", font_size=24, color=YELLOW, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.06)
        question.to_edge(DOWN)

        self.play(Write(header))
        caption = replace_caption(
            self,
            caption,
            "Chapter 4 showed that real systems differ from random networks.",
            "第四章说明了真实系统和随机网络的不同。",
            wait_time=4.0,
        )
        self.play(Create(er_graph), FadeIn(er_label), run_time=2.0)
        caption = replace_caption(
            self,
            caption,
            "Random graphs have variation, but strong hubs are uncommon.",
            "随机图也有差异，但强枢纽并不常见。",
            wait_time=5.5,
        )
        self.play(Create(ba_graph), FadeIn(ba_label), run_time=2.0)
        caption = replace_caption(
            self,
            caption,
            "Real networks often contain nodes with far more links than usual.",
            "真实网络中常有少数节点拥有远多于普通节点的连接。",
            wait_time=5.5,
        )
        self.play(Create(er_hub_ring), Create(ba_hub_ring), run_time=0.8)
        caption = replace_caption(
            self,
            caption,
            "The question is what dynamics can make those hubs appear.",
            "问题是：什么样的动力学过程会让枢纽自然出现？",
            wait_time=5.5,
        )
        self.play(
            FadeOut(caption),
            FadeOut(comparison),
            FadeOut(er_hub_ring),
            FadeOut(ba_hub_ring),
            Write(question),
            run_time=0.9,
        )
        self.wait(7.5)


# ============================================================
# Scene 2: Growth
# ============================================================

class BAGrowth(Scene):
    def construct(self):
        title = Title("Ingredient 1: Growth")
        caption = None

        trace = ba_growth_trace(n_final=13, m=2, seed=2)
        sequence = trace["graphs"]
        final_graph = sequence[-1]
        final_layout = spring_layout_3d(final_graph, seed=7, scale=3.0)
        formula = MathTex(r"N(t)=N_0+t", font_size=30)
        formula.next_to(title, DOWN, buff=0.38)
        formula.to_edge(RIGHT, buff=0.75)
        citation_intro = VGroup(
            Text("Barabási–Albert model", font_size=31, color=YELLOW),
            Text(
                "Original paper: Barabási & Albert, Science 286, 509-512 (1999)",
                font_size=17,
                color=GREY_A,
            ),
        ).arrange(DOWN, buff=0.06)
        citation_intro.next_to(title, DOWN, buff=0.22)
        citation_intro.to_edge(LEFT, buff=0.7)

        current_G = sequence[0]
        current_layout = subset_layout(final_layout, current_G.nodes())
        graph = make_graph_mobject(current_G, layout=current_layout)
        graph_snapshot = VGroup(graph)

        node_counter = Text(
            f"N = {current_G.number_of_nodes()}, E = {current_G.number_of_edges()}",
            font_size=30,
        )
        node_counter.next_to(title, DOWN, buff=0.25)

        self.play(Write(title), FadeIn(citation_intro))
        caption = replace_caption(
            self,
            caption,
            "A useful model for this phenomenon is the Barabási-Albert model.",
            "一个很好的描述这个现象的模型就是 Barabási-Albert model。",
            wait_time=8.0,
        )
        self.play(FadeOut(citation_intro), Write(formula), run_time=0.8)
        caption = replace_caption(
            self,
            caption,
            "The first missing ingredient is growth.",
            "第一个缺失的成分是增长。",
            wait_time=5.5,
        )
        self.play(Create(graph_snapshot), Write(node_counter))
        caption = replace_caption(
            self,
            caption,
            "The network is not born all at once.",
            "真实网络通常不是一次性画出来的。",
            wait_time=6.5,
        )

        for step_number, step_info in enumerate(trace["steps"]):
            G = step_info["after"]
            new_node = step_info["new_node"]
            targets = step_info["targets"]
            layout = subset_layout(final_layout, G.nodes())

            new_graph = make_graph_mobject(
                G,
                layout=layout,
                hub_nodes=targets,
                highlight_nodes={new_node: NEW_NODE_COLOR},
            )
            rings = VGroup(
                make_node_rings(new_graph, targets, color=TARGET_COLOR),
                make_node_rings(new_graph, [new_node], color=NEW_NODE_COLOR),
            )
            new_snapshot = VGroup(new_graph, rings)
            new_counter = Text(
                f"N = {G.number_of_nodes()}, E = {G.number_of_edges()}",
                font_size=30,
            )
            new_counter.next_to(title, DOWN, buff=0.25)

            run_time = 0.8 if step_number < 3 else 0.58
            self.remove(node_counter)
            self.add(new_counter)
            self.play(
                FadeOut(graph_snapshot, shift=DOWN * 0.05),
                FadeIn(new_snapshot, shift=DOWN * 0.05),
                run_time=run_time,
                rate_func=smooth,
            )
            graph_snapshot = new_snapshot
            node_counter = new_counter
            if step_number == 2:
                caption = replace_caption(
                    self,
                    caption,
                    "New nodes arrive over time, so the node count increases.",
                    "新节点会随时间加入，所以节点数不断增加。",
                    wait_time=5.0,
                )
            if step_number == 6:
                caption = replace_caption(
                    self,
                    caption,
                    "This simple growth rule sets the stage for hubs.",
                    "这个简单的增长规则为枢纽的出现搭好了舞台。",
                    wait_time=5.0,
                )

        caption = replace_caption(
            self,
            caption,
            "Growth alone is not enough; we still need a rule for where new edges go.",
            "只有增长还不够；我们还需要说明新来的边应该连向哪里。",
            wait_time=7.0,
        )
        self.play(FadeOut(caption), run_time=0.5)
        self.wait(1.0)


# ============================================================
# Scene 3: Preferential attachment
# ============================================================

class BAPreferentialAttachment(Scene):
    def construct(self):
        title = Title("Ingredient 2: Preferential Attachment")
        formula = MathTex(r"\Pi_i = \frac{k_i}{\sum_j k_j}", font_size=38)
        normalization = MathTex(r"\sum_i \Pi_i = 1", font_size=28)
        formula_block = VGroup(formula, normalization)
        formula_block.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        formula_block.to_corner(UL).shift(DOWN * 0.95 + RIGHT * 0.35)

        caption = None

        trace = ba_growth_trace(n_final=13, m=2, seed=3)
        step = trace["steps"][-1]
        G = step["before"]
        hub_nodes = top_degree_nodes(G, top=2)
        layout = spring_layout_3d(G, seed=5, scale=2.45)

        graph = make_graph_mobject(
            G,
            layout=layout,
            hub_nodes=hub_nodes,
            edge_opacity=0.4,
        )
        graph.shift(RIGHT * 0.85 + DOWN * 0.5)

        self.play(Write(title))
        self.play(Write(formula_block))
        caption = replace_caption(
            self,
            caption,
            "The second ingredient is preferential attachment.",
            "第二个成分是优先连接。",
            wait_time=5.5,
        )
        self.play(Create(graph), run_time=2.0)
        caption = replace_caption(
            self,
            caption,
            "A new node is more likely to choose nodes that already have many links.",
            "新节点更可能选择已经拥有很多连接的节点。",
            wait_time=7.0,
        )

        # New node placed outside the existing network.
        new_dot = Dot(color=NEW_NODE_COLOR, radius=0.11)
        new_dot.move_to(RIGHT * 4.25 + DOWN * 1.45)
        new_label = VGroup(
            Text("new node", font_size=20, color=NEW_NODE_COLOR),
            Text("新节点", font_size=18, color=NEW_NODE_COLOR, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.03)
        new_label.next_to(new_dot, DOWN, buff=0.15)
        new_ring = Circle(radius=0.19)
        new_ring.set_stroke(color=NEW_NODE_COLOR, width=4)
        new_ring.move_to(new_dot.get_center())
        new_degree_note = VGroup(
            Text("demo choice: 2 links", font_size=18, color=GREY_A),
            Text("Pi chooses the targets", font_size=18, color=GREY_A),
            Text("本例固定：2 条连接", font_size=16, color=GREY_A, font=CHINESE_FONT),
            Text("公式只选择目标节点", font_size=16, color=GREY_A, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.04)
        new_degree_note.next_to(new_label, DOWN, buff=0.16)
        new_degree_note.shift(LEFT * 0.08)

        self.play(FadeIn(new_dot), FadeIn(new_label), Create(new_ring))
        caption = replace_caption(
            self,
            caption,
            "The equation does not set the new node's initial number of links.",
            "这个公式并不决定新节点的初始连接数。",
            wait_time=5.0,
        )
        self.play(FadeIn(new_degree_note), run_time=0.8)
        caption = replace_caption(
            self,
            caption,
            "Here, the demo fixes two new links; Pi chooses their existing targets.",
            "在本例中，新节点固定带来两条连接；Pi 只选择这些连接的已有目标。",
            wait_time=6.5,
        )

        # Candidate line widths come from the same Pi_i values used for sampling.
        degrees = step["degrees"]
        probabilities = step["probabilities"]
        max_probability = max(probabilities.values())

        candidate_lines = VGroup()
        for node in G.nodes():
            start = new_dot.get_center()
            end = graph.vertices[node].get_center()

            probability_fraction = probabilities[node] / max_probability
            width = 0.7 + 4.2 * probability_fraction
            opacity = 0.15 + 0.45 * probability_fraction

            line = Line(start, end)
            line.set_stroke(
                color=TARGET_COLOR if node in step["targets"] else FAINT_COLOR,
                width=width,
                opacity=opacity,
            )
            candidate_lines.add(line)

        self.play(LaggedStartMap(Create, candidate_lines, lag_ratio=0.04), run_time=2.0)
        caption = replace_caption(
            self,
            caption,
            "The wider candidate lines are the more likely choices.",
            "候选线越粗，表示被选择的概率越高。",
            wait_time=7.0,
        )

        ranked_by_probability = sorted(
            probabilities,
            key=lambda node: probabilities[node],
            reverse=True,
        )
        displayed_nodes = []
        for node in step["targets"] + ranked_by_probability:
            if node not in displayed_nodes:
                displayed_nodes.append(node)
            if len(displayed_nodes) == 3:
                break

        probability_labels = VGroup()
        graph_center = graph.get_center()
        for node in displayed_nodes:
            label = MathTex(
                rf"k_{{{node}}}={degrees[node]},\ \Pi_{{{node}}}={probabilities[node]:.2f}",
                font_size=19,
            )
            label.add_background_rectangle(color=BLACK, opacity=0.75, buff=0.06)
            direction = outside_label_direction(
                graph.vertices[node].get_center(),
                center=graph_center,
            )
            label.next_to(graph.vertices[node], direction, buff=0.14)
            probability_labels.add(label)

        target_rings = make_node_rings(
            graph,
            step["targets"],
            color=TARGET_COLOR,
            radius_buff=0.1,
            stroke_width=5,
        )
        selected_lines = VGroup()
        for target in step["targets"]:
            selected_line = Line(new_dot.get_center(), graph.vertices[target].get_center())
            selected_line.set_stroke(color=TARGET_COLOR, width=5, opacity=1.0)
            selected_lines.add(selected_line)

        self.play(FadeIn(probability_labels), Create(target_rings), run_time=1.0)
        caption = replace_caption(
            self,
            caption,
            "The labels show the actual degree and probability values.",
            "这些标签显示的是实际的度和概率值。",
            wait_time=6.5,
        )
        self.play(Create(selected_lines), run_time=1.0)
        self.bring_to_front(probability_labels, target_rings, new_dot, new_label, new_ring, new_degree_note)
        caption = replace_caption(
            self,
            caption,
            "The sampled targets become the real new edges.",
            "最后，只有被抽样选中的目标会变成真实的边。",
            wait_time=6.5,
        )

        rich_get_richer = VGroup(
            Text("rich get richer", font_size=32, color=YELLOW),
            Text("富者愈富", font_size=25, color=YELLOW, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.04)
        rich_get_richer.next_to(formula_block, DOWN, buff=0.25)
        rich_get_richer.to_edge(LEFT, buff=0.5)

        self.play(Write(rich_get_richer))
        caption = replace_caption(
            self,
            caption,
            "This feedback loop is the rich-get-richer mechanism.",
            "这就是“富者愈富”效应背后的反馈机制。",
            wait_time=7.0,
        )
        self.play(FadeOut(caption), run_time=0.5)
        self.wait(1.0)


# ============================================================
# Scene 4: Building the BA model
# ============================================================

class BABuildingTheModel(Scene):
    def construct(self):
        title = Title("Growth + Preferential Attachment")
        rule = VGroup(
            Text("1. Add one new node", font_size=26),
            Text("2. Connect it to existing nodes", font_size=26),
            Text("3. Prefer high-degree targets", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rule.to_corner(UL).shift(DOWN * 0.8)
        formula = MathTex(r"\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}", font_size=28)
        formula.next_to(rule, DOWN, aligned_edge=LEFT, buff=0.35)
        caption = None

        trace = ba_growth_trace(n_final=55, m=2, seed=8)
        sequence = trace["graphs"]
        final_G = sequence[-1]
        final_layout = spring_layout_3d(final_G, seed=11, scale=2.75)

        current_G = sequence[0]
        graph = make_graph_mobject(
            current_G,
            layout=subset_layout(final_layout, current_G.nodes()),
        )
        graph.shift(RIGHT * 1.15 + DOWN * 0.45)
        graph_snapshot = VGroup(graph)
        degree_plot = make_simulation_degree_plot(current_G)

        counter = Text(
            f"N = {current_G.number_of_nodes()}, E = {current_G.number_of_edges()}",
            font_size=26,
        )
        counter.next_to(title, DOWN, buff=0.22)
        counter.to_edge(RIGHT, buff=0.8)

        self.play(Write(title))
        caption = replace_caption(
            self,
            caption,
            "Now combine growth with preferential attachment.",
            "现在把增长和优先连接合在一起。",
            wait_time=5.5,
            font_size=23,
        )
        self.play(
            FadeIn(rule),
            Write(formula),
            Create(graph_snapshot),
            Create(degree_plot),
            Write(counter),
        )
        caption = replace_caption(
            self,
            caption,
            "At each step, add one node and choose targets by degree.",
            "每一步加入一个新节点，并按度来选择连接目标。",
            wait_time=6.5,
            font_size=23,
        )

        milestone_indices = [0, 1, 2, 3, 4, 5, 8, 14, 24, 39, len(trace["steps"]) - 1]
        seen_indices = set()
        selected_steps = []
        for idx in milestone_indices:
            if idx not in seen_indices:
                selected_steps.append((idx, trace["steps"][idx]))
                seen_indices.add(idx)

        for idx, step_info in selected_steps:
            G = step_info["after"]
            new_node = step_info["new_node"]
            targets = step_info["targets"]
            hubs = top_degree_nodes(G, top=1)

            new_graph = make_graph_mobject(
                G,
                layout=subset_layout(final_layout, G.nodes()),
                hub_nodes=hubs,
                highlight_nodes={new_node: NEW_NODE_COLOR},
                edge_opacity=0.42,
            )
            new_graph.shift(RIGHT * 1.15 + DOWN * 0.45)
            rings = VGroup(
                make_node_rings(new_graph, targets, color=TARGET_COLOR),
                make_node_rings(new_graph, [new_node], color=NEW_NODE_COLOR),
            )
            new_snapshot = VGroup(new_graph, rings)

            new_counter = Text(
                f"N = {G.number_of_nodes()}, E = {G.number_of_edges()}",
                font_size=26,
            )
            new_counter.next_to(title, DOWN, buff=0.22)
            new_counter.to_edge(RIGHT, buff=0.8)
            new_degree_plot = make_simulation_degree_plot(G)

            rt = 0.7 if idx < 6 else 0.95

            self.remove(counter)
            self.add(new_counter)
            self.play(
                FadeOut(graph_snapshot, shift=DOWN * 0.04),
                FadeIn(new_snapshot, shift=DOWN * 0.04),
                Transform(degree_plot, new_degree_plot),
                run_time=rt,
                rate_func=smooth,
            )
            graph_snapshot = new_snapshot
            counter = new_counter
            if idx == 2:
                caption = replace_caption(
                    self,
                    caption,
                    "Early choices matter because selected nodes gain more visibility.",
                    "早期选择很重要，因为被选中的节点会变得更可见。",
                    wait_time=6.0,
                    font_size=23,
                )
            if idx == 5:
                caption = replace_caption(
                    self,
                    caption,
                    "A node with more links has more chances to receive the next link.",
                    "连接越多的节点，获得下一条连接的机会也越多。",
                    wait_time=7.0,
                    font_size=23,
                )
            if idx == 14:
                caption = replace_caption(
                    self,
                    caption,
                    "The rank-degree curve begins to bend: a few nodes pull ahead.",
                    "秩-度曲线开始弯曲：少数节点逐渐拉开差距。",
                    wait_time=7.5,
                    font_size=23,
                )
            if idx == 39:
                caption = replace_caption(
                    self,
                    caption,
                    "After many repetitions, hubs are visible in the graph and the plot.",
                    "重复很多次之后，图和曲线中都能看到枢纽。",
                    wait_time=8.0,
                    font_size=23,
                )

        final_hubs = top_degree_nodes(final_G, top=3)
        final_graph = make_graph_mobject(
            final_G,
            layout=final_layout,
            hub_nodes=final_hubs,
            edge_opacity=0.38,
        )
        final_graph.shift(RIGHT * 1.15 + DOWN * 0.45)
        final_hub_rings = make_node_rings(
            final_graph,
            final_hubs,
            color=YELLOW,
            radius_buff=0.1,
            stroke_width=5,
        )
        final_snapshot = VGroup(final_graph, final_hub_rings)
        final_degree_plot = make_simulation_degree_plot(final_G)

        takeaway = VGroup(
            Text("Hubs emerge from the rule", font_size=29, color=YELLOW),
            Text("枢纽从规则中涌现", font_size=23, color=YELLOW, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.05)
        takeaway.to_edge(DOWN, buff=0.35)

        self.play(
            FadeOut(caption),
            FadeOut(graph_snapshot, shift=DOWN * 0.04),
            FadeIn(final_snapshot, shift=DOWN * 0.04),
            Transform(degree_plot, final_degree_plot),
            run_time=1.0,
            rate_func=smooth,
        )
        self.play(Write(takeaway))
        self.wait(8.5)
        self.wait(2.0)


# ============================================================
# Scene 5: BA vs ER comparison
# ============================================================

class BAComparison(Scene):
    def construct(self):
        title = Title("BA Network vs Random Network")
        caption = None

        n = 90
        m = 2

        ba = ba_growth_trace(n_final=n, m=m, seed=10)["graphs"][-1]
        er = same_density_er_graph(ba, seed=20)

        ba_hubs = top_degree_nodes(ba, top=3)
        er_hubs = top_degree_nodes(er, top=3)
        er_layout = spring_layout_3d(er, seed=21, scale=2.25)
        ba_layout = spring_layout_3d(ba, seed=22, scale=2.25)

        er_graph = make_graph_mobject(
            er,
            layout=er_layout,
            hub_nodes=er_hubs,
            edge_opacity=0.25,
            min_radius=0.035,
            max_radius=0.13,
        )
        ba_graph = make_graph_mobject(
            ba,
            layout=ba_layout,
            hub_nodes=ba_hubs,
            edge_opacity=0.25,
            min_radius=0.035,
            max_radius=0.17,
        )

        er_label = VGroup(
            Text("Erdős–Rényi", font_size=23),
            Text("随机网络", font_size=18, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.03)
        ba_label = VGroup(
            Text("Barabási–Albert", font_size=23),
            Text("BA 网络", font_size=18, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.03)

        er_group = VGroup(er_label, er_graph).arrange(DOWN, buff=0.15)
        ba_group = VGroup(ba_label, ba_graph).arrange(DOWN, buff=0.15)

        graph_row = VGroup(er_group, ba_group).arrange(RIGHT, buff=1.0)
        graph_row.scale(0.58)
        graph_row.next_to(title, DOWN, buff=0.18)
        er_hub_rings = make_node_rings(er_graph, er_hubs, color=YELLOW, radius_buff=0.06)
        ba_hub_rings = make_node_rings(ba_graph, ba_hubs, color=YELLOW, radius_buff=0.06)

        er_plot = make_rank_degree_plot(er, "", width=3.7, height=1.45)
        ba_plot = make_rank_degree_plot(ba, "", width=3.7, height=1.45)

        plot_row = VGroup(er_plot, ba_plot).arrange(RIGHT, buff=1.15)
        plot_row.scale(0.56)
        plot_row.to_edge(DOWN, buff=0.5)
        rank_equation = MathTex(
            r"k_{(1)} \ge k_{(2)} \ge \cdots \ge k_{(N)}",
            font_size=22,
        )

        message = Text(
            "Preferential attachment creates stronger degree heterogeneity",
            font_size=20,
            color=YELLOW,
        )
        message_cn = Text(
            "优先连接会产生更强的度异质性",
            font_size=18,
            color=YELLOW,
            font=CHINESE_FONT,
        )
        message = VGroup(message, message_cn).arrange(DOWN, buff=0.04)
        message.next_to(graph_row, DOWN, buff=0.2)
        rank_equation.next_to(message, DOWN, buff=0.1)
        if rank_equation.get_bottom()[1] < plot_row.get_top()[1] + 0.25:
            plot_row.next_to(rank_equation, DOWN, buff=0.3)
            plot_row.to_edge(DOWN, buff=0.35)

        self.play(Write(title))
        caption = replace_caption(
            self,
            caption,
            "Now compare the BA network with a random network of similar density.",
            "现在把 BA 网络和密度相近的随机网络进行比较。",
            wait_time=5.5,
        )
        self.play(Create(er_graph), FadeIn(er_label), run_time=2.0)
        caption = replace_caption(
            self,
            caption,
            "The random network has degree variation, but it is relatively even.",
            "随机网络也有度的差异，但整体相对均匀。",
            wait_time=6.0,
        )
        self.play(Create(ba_graph), FadeIn(ba_label), run_time=2.0)
        caption = replace_caption(
            self,
            caption,
            "The BA network is more heterogeneous because attachment was biased.",
            "BA 网络更异质，因为连接目标带有偏好。",
            wait_time=6.0,
        )
        self.play(Create(er_hub_rings), Create(ba_hub_rings), run_time=0.8)
        caption = replace_caption(
            self,
            caption,
            "The highlighted nodes show where the largest degrees concentrate.",
            "高亮节点显示了最大的度集中在哪里。",
            wait_time=6.0,
        )
        self.play(Write(message))
        self.play(Write(rank_equation))
        caption = replace_caption(
            self,
            caption,
            "The rank-degree plots summarize the same pattern numerically.",
            "秩-度图用数字总结了同一个模式。",
            wait_time=5.0,
        )
        self.play(FadeOut(caption), run_time=0.5)
        self.play(Create(er_plot), Create(ba_plot), run_time=2.0)
        self.wait(8.5)


# ============================================================
# Scene 6: Takeaway
# ============================================================

class BATakeaway(Scene):
    def construct(self):
        title = Text("The Barabási–Albert Model", font_size=40)
        title.to_edge(UP)

        card1 = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.18)
        card2 = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.18)
        card3 = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.18)

        text1 = VGroup(
            Text("Growth", font_size=30),
            Text("增长", font_size=23, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.06)
        text2 = VGroup(
            Text("Preferential\nattachment", font_size=26, line_spacing=0.8),
            Text("优先连接", font_size=21, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.05)
        text3 = VGroup(
            Text("Emergent\nhubs", font_size=26, line_spacing=0.8),
            Text("涌现的枢纽", font_size=21, font=CHINESE_FONT),
        ).arrange(DOWN, buff=0.05)

        group1 = VGroup(card1, text1)
        group2 = VGroup(card2, text2)
        group3 = VGroup(card3, text3)

        text1.move_to(card1.get_center())
        text2.move_to(card2.get_center())
        text3.move_to(card3.get_center())

        cards = VGroup(group1, group2, group3).arrange(RIGHT, buff=0.78)
        cards.move_to(UP * 0.25)
        key_equations = MathTex(
            r"N(t)=N_0+t",
            r"\quad",
            r"\Pi_i=\frac{k_i}{\sum_j k_j}",
            font_size=30,
        )
        key_equations.next_to(cards, DOWN, buff=0.4)

        arrow1 = Arrow(
            group1.get_right(),
            group2.get_left(),
            buff=0.08,
            stroke_width=8,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.45,
        )
        arrow2 = Arrow(
            group2.get_right(),
            group3.get_left(),
            buff=0.08,
            stroke_width=8,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.45,
        )

        final_message = VGroup(
            Text(
                "Simple local rules can generate complex network structure",
                font_size=25,
                color=YELLOW,
            ),
            Text(
                "简单的局部规则可以产生复杂的网络结构",
                font_size=21,
                color=YELLOW,
                font=CHINESE_FONT,
            ),
        ).arrange(DOWN, buff=0.06)
        final_message.next_to(key_equations, DOWN, buff=0.45)

        self.play(Write(title))
        self.wait(3.0)
        self.play(FadeIn(group1))
        self.wait(4.0)
        self.play(Create(arrow1), FadeIn(group2))
        self.wait(5.0)
        self.play(Create(arrow2), FadeIn(group3))
        self.wait(5.0)
        self.play(Write(key_equations))
        self.wait(5.0)
        self.play(Write(final_message))
        self.wait(5.0)

        reference_card = make_reference_end_card()
        self.play(
            FadeOut(title),
            FadeOut(cards),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(key_equations),
            FadeOut(final_message),
            run_time=0.8,
        )
        self.play(FadeIn(reference_card), run_time=0.8)
        self.wait(6.0)
