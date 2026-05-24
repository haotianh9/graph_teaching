from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont
import networkx as nx

from public_metadata import (
    COVER_FOOTER,
    COVER_LEFT_LABEL,
    COVER_OUTPUTS,
    COVER_RIGHT_LABEL,
    COVER_SUBTITLE,
    COVER_TITLE,
)


BG = (6, 7, 10)
WHITE = (245, 245, 238)
GREY = (150, 154, 160)
BLUE = (79, 190, 220)
YELLOW = (242, 207, 91)
GREEN = (124, 202, 112)
RED = (238, 105, 92)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/mnt/c/Windows/Fonts/msyhbd.ttc" if bold else "/mnt/c/Windows/Fonts/msyh.ttc",
        "/mnt/c/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def transform_layout(pos, cx, cy, scale):
    return {
        node: (
            cx + scale * float(point[0]),
            cy + scale * float(point[1]),
        )
        for node, point in pos.items()
    }


def draw_network(draw, graph, pos, highlight_nodes=(), cluster_nodes=(), edge_color=(80, 85, 92), alpha=125):
    highlight_nodes = set(highlight_nodes)
    cluster_nodes = set(cluster_nodes)
    degrees = dict(graph.degree())
    max_degree = max(degrees.values()) if degrees else 1

    edge_rgba = edge_color + (alpha,)
    for u, v in graph.edges():
        draw.line([pos[u], pos[v]], fill=edge_rgba, width=2)

    for node in sorted(graph.nodes(), key=lambda n: degrees[n]):
        x, y = pos[node]
        if node in highlight_nodes:
            color = YELLOW
        elif node in cluster_nodes:
            color = GREEN
        else:
            color = BLUE
        radius = 4 + 14 * math.sqrt(degrees[node] / max_degree)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color + (235,), outline=WHITE + (220,), width=2)


def make_clustered_graph():
    graph = nx.connected_caveman_graph(4, 12)
    graph.add_edges_from([(0, 12), (12, 24), (24, 36), (6, 18), (18, 30)])
    return nx.convert_node_labels_to_integers(graph)


def draw_text_fit(draw, xy, text, max_width, start_size, fill, bold=False, min_size=18):
    size = start_size
    while size >= min_size:
        candidate = font(size, bold=bold)
        bbox = draw.textbbox(xy, text, font=candidate)
        if bbox[2] - bbox[0] <= max_width:
            draw.text(xy, text, font=candidate, fill=fill)
            return candidate
        size -= 2
    candidate = font(min_size, bold=bold)
    draw.text(xy, text, font=candidate, fill=fill)
    return candidate


def make_cover(width, height, output):
    base = Path(__file__).resolve().parents[1]
    output = base / "assets" / "cover" / output
    output.parent.mkdir(parents=True, exist_ok=True)

    random.seed(7)
    img = Image.new("RGBA", (width, height), BG + (255,))
    draw = ImageDraw.Draw(img, "RGBA")

    # Subtle panel glow.
    glow_y = int(height * 0.55)
    for radius, opacity in [(330, 22), (250, 30), (170, 38)]:
        r = int(radius * min(width / 1280, height / 720))
        draw.ellipse((int(width * 0.15) - r, glow_y - r, int(width * 0.15) + r, glow_y + r), fill=(35, 92, 120, opacity))
        draw.ellipse((int(width * 0.84) - r, glow_y - r, int(width * 0.84) + r, glow_y + r), fill=(70, 120, 70, opacity))

    ba = nx.barabasi_albert_graph(72, 2, seed=12)
    network_y = int(height * 0.55)
    network_scale = min(width * 0.18, height * 0.30)
    ba_pos = transform_layout(nx.spring_layout(ba, seed=4, k=0.25, iterations=120), int(width * 0.27), network_y, network_scale)
    ba_hubs = [n for n, _ in sorted(ba.degree(), key=lambda item: item[1], reverse=True)[:4]]
    draw_network(draw, ba, ba_pos, highlight_nodes=ba_hubs)

    real = make_clustered_graph()
    real_pos = transform_layout(nx.spring_layout(real, seed=9, k=0.30, iterations=120), int(width * 0.74), network_y, network_scale * 1.03)
    cluster_nodes = list(range(0, 12)) + list(range(12, 24))
    draw_network(draw, real, real_pos, cluster_nodes=cluster_nodes, edge_color=(80, 110, 85), alpha=145)

    margin_x = int(width * 0.055)
    title_y = int(height * 0.065)
    subtitle_y = title_y + int(height * 0.12)
    draw_text_fit(draw, (margin_x, title_y), COVER_TITLE, int(width * 0.88), int(height * 0.097), WHITE, bold=True)
    draw_text_fit(draw, (margin_x + 4, subtitle_y), COVER_SUBTITLE, int(width * 0.88), int(height * 0.047), YELLOW)

    label_font_size = int(height * 0.038)
    box_h = int(height * 0.086)
    box_y = int(height * 0.825)
    left_box = (int(width * 0.075), box_y, int(width * 0.43), box_y + box_h)
    right_box = (int(width * 0.55), box_y, int(width * 0.925), box_y + box_h)
    draw.rounded_rectangle(left_box, radius=18, fill=BG + (230,), outline=YELLOW + (245,), width=3)
    draw_text_fit(draw, (left_box[0] + 26, box_y + int(box_h * 0.22)), COVER_LEFT_LABEL, left_box[2] - left_box[0] - 52, label_font_size, YELLOW, bold=True)
    draw.rounded_rectangle(right_box, radius=18, fill=BG + (230,), outline=GREEN + (245,), width=3)
    draw_text_fit(draw, (right_box[0] + 26, box_y + int(box_h * 0.22)), COVER_RIGHT_LABEL, right_box[2] - right_box[0] - 52, label_font_size, GREEN, bold=True)

    draw_text_fit(
        draw,
        (margin_x, int(height * 0.93)),
        COVER_FOOTER,
        int(width * 0.70),
        int(height * 0.033),
        GREY,
    )

    img.convert("RGB").save(output, quality=95)
    print(output)


def main():
    for spec in COVER_OUTPUTS:
        make_cover(spec["width"], spec["height"], spec["filename"])


if __name__ == "__main__":
    main()
