from __future__ import annotations

import math
from pathlib import Path

import networkx as nx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1280
HEIGHT = 720
OUT_DIR = Path("assets/thumbnails")
PNG_OUT = OUT_DIR / "video5_1_thumbnail.png"
JPG_OUT = OUT_DIR / "video5_1_thumbnail.jpg"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/mnt/c/Windows/Fonts/msyhbd.ttc" if bold else "/mnt/c/Windows/Fonts/msyh.ttc",
        "/mnt/c/Windows/Fonts/simhei.ttf",
        "/home/haotian/.local/share/fonts/codex-cjk/NotoSansSC-VF.ttf",
        "/mnt/c/Windows/Fonts/NotoSansSC-VF.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default(size=size)


def draw_text_with_glow(
    image: Image.Image,
    position: tuple[int, int],
    text: str,
    font_obj: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    glow: tuple[int, int, int],
    radius: int = 5,
) -> None:
    glow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.text(position, text, font=font_obj, fill=(*glow, 210))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius))
    image.alpha_composite(glow_layer)
    ImageDraw.Draw(image).text(position, text, font=font_obj, fill=(*fill, 255))


def normalize_layout(layout: dict[int, np.ndarray], center: tuple[int, int], radius: int):
    points = np.array(list(layout.values()))
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    span = np.maximum(maxs - mins, 1e-6)
    result = {}
    for node, point in layout.items():
        xy = (point - mins) / span
        xy = (xy - 0.5) * 2
        result[node] = (
            int(center[0] + xy[0] * radius),
            int(center[1] + xy[1] * radius * 0.78),
        )
    return result


def draw_network(
    image: Image.Image,
    G: nx.Graph,
    layout: dict[int, tuple[int, int]],
    hub_nodes: list[int],
    dim: bool = False,
) -> None:
    edge_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    edge_draw = ImageDraw.Draw(edge_layer)
    edge_color = (115, 190, 210, 62) if not dim else (110, 135, 145, 42)
    for u, v in G.edges():
        edge_draw.line([layout[u], layout[v]], fill=edge_color, width=2)
    image.alpha_composite(edge_layer)

    degrees = dict(G.degree())
    max_degree = max(degrees.values())
    draw = ImageDraw.Draw(image)
    for node, (x, y) in sorted(layout.items(), key=lambda item: degrees[item[0]]):
        fraction = degrees[node] / max_degree
        radius = int(5 + 23 * math.sqrt(fraction))
        if node in hub_nodes:
            glow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow_layer)
            for extra, alpha in [(35, 34), (22, 54), (10, 95)]:
                glow_draw.ellipse(
                    [x - radius - extra, y - radius - extra, x + radius + extra, y + radius + extra],
                    fill=(255, 214, 87, alpha),
                )
            image.alpha_composite(glow_layer.filter(ImageFilter.GaussianBlur(10)))
            fill = (255, 211, 83, 255)
            outline = (255, 245, 180, 255)
        else:
            fill = (100, 210, 235, 235) if not dim else (95, 145, 155, 190)
            outline = (220, 250, 255, 130)
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=fill,
            outline=outline,
            width=2,
        )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (WIDTH, HEIGHT), (4, 7, 12, 255))

    # Subtle radial glow.
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r, alpha in [(620, 22), (450, 28), (290, 38)]:
        glow_draw.ellipse(
            [WIDTH - 160 - r, HEIGHT // 2 - r, WIDTH - 160 + r, HEIGHT // 2 + r],
            fill=(17, 93, 105, alpha),
        )
    image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))

    rng_seed = 12
    ba = nx.barabasi_albert_graph(80, 2, seed=rng_seed)
    er = nx.gnm_random_graph(80, ba.number_of_edges(), seed=rng_seed)
    ba_layout = normalize_layout(nx.spring_layout(ba, seed=4, k=0.24, iterations=100), (825, 385), 300)
    er_layout = normalize_layout(nx.spring_layout(er, seed=8, k=0.24, iterations=100), (260, 420), 165)
    ba_hubs = [node for node, _ in sorted(ba.degree(), key=lambda item: item[1], reverse=True)[:4]]
    er_hubs = [node for node, _ in sorted(er.degree(), key=lambda item: item[1], reverse=True)[:2]]

    draw_network(image, er, er_layout, er_hubs, dim=True)
    draw_network(image, ba, ba_layout, ba_hubs, dim=False)

    draw = ImageDraw.Draw(image)
    title_font = font(74, bold=True)
    subtitle_font = font(34)
    small_font = font(24)
    badge_font = font(22, bold=True)

    draw.rounded_rectangle([48, 42, 520, 90], radius=16, fill=(255, 212, 74, 235))
    draw.text((72, 53), "Network Science Chapter 5 · Video 1", font=badge_font, fill=(12, 14, 20, 255))

    draw_text_with_glow(
        image,
        (52, 115),
        "枢纽节点如何出现？",
        title_font,
        fill=(255, 255, 245),
        glow=(255, 206, 69),
        radius=7,
    )
    draw.text((58, 210), "How Do Hubs Emerge?", font=subtitle_font, fill=(190, 238, 247, 245))

    draw.rounded_rectangle([60, 592, 548, 656], radius=18, fill=(3, 7, 12, 170), outline=(255, 212, 74, 190), width=2)
    draw.text((84, 607), "Growth + preferential attachment", font=small_font, fill=(255, 244, 180, 255))

    arrow_draw = ImageDraw.Draw(image)
    arrow_draw.line([(542, 625), (675, 548)], fill=(255, 214, 88, 245), width=8)
    arrow_draw.polygon([(675, 548), (640, 548), (659, 578)], fill=(255, 214, 88, 245))

    image = image.convert("RGB")
    image.save(PNG_OUT)
    image.save(JPG_OUT, quality=94, optimize=True)
    print(f"wrote {PNG_OUT}")
    print(f"wrote {JPG_OUT}")


if __name__ == "__main__":
    main()
