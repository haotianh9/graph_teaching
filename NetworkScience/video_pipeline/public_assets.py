from __future__ import annotations

import math
import random
import re
from pathlib import Path
from types import ModuleType

import networkx as nx
from PIL import Image, ImageDraw, ImageFont

from .common import load_config


BG = (6, 7, 10)
WHITE = (245, 245, 238)
GREY = (150, 154, 160)
BLUE = (79, 190, 220)
YELLOW = (242, 207, 91)
GREEN = (124, 202, 112)
RED = (238, 105, 92)


GREEK_TEXT_REPLACEMENTS = {
    "beta": "β",
    "eta": "η",
    "gamma": "γ",
}


def public_text(text: str) -> str:
    """Normalize public-facing Greek names to symbols for covers/descriptions."""
    def replace(match: re.Match[str]) -> str:
        return GREEK_TEXT_REPLACEMENTS[match.group(0).lower()]

    return re.sub(r"\b(beta|eta|gamma)\b", replace, text, flags=re.IGNORECASE)


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


def draw_text_fit(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, max_width: int, start_size: int, fill, bold: bool = False, min_size: int = 18) -> None:
    size = start_size
    while size >= min_size:
        candidate = font(size, bold=bold)
        bbox = draw.textbbox(xy, text, font=candidate)
        if bbox[2] - bbox[0] <= max_width:
            draw.text(xy, text, font=candidate, fill=fill)
            return
        size -= 2
    draw.text(xy, text, font=font(min_size, bold=bold), fill=fill)


def transform_layout(pos, cx: int, cy: int, scale: float):
    return {node: (cx + scale * float(point[0]), cy + scale * float(point[1])) for node, point in pos.items()}


def draw_network(draw: ImageDraw.ImageDraw, graph: nx.Graph, pos, high_nodes=(), fit_nodes=()) -> None:
    high_nodes = set(high_nodes)
    fit_nodes = set(fit_nodes)
    degrees = dict(graph.degree())
    max_degree = max(degrees.values()) if degrees else 1
    for u, v in graph.edges():
        draw.line([pos[u], pos[v]], fill=(75, 105, 120, 120), width=2)
    for node in sorted(graph.nodes(), key=lambda n: degrees[n]):
        x, y = pos[node]
        color = YELLOW if node in high_nodes else GREEN if node in fit_nodes else BLUE
        radius = 4 + 13 * math.sqrt(degrees[node] / max_degree)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color + (235,), outline=WHITE + (220,), width=2)


def make_default_cover(video_dir: Path, config: ModuleType, width: int, height: int, filename: str) -> Path:
    output = video_dir / "assets" / "cover" / filename
    output.parent.mkdir(parents=True, exist_ok=True)

    random.seed(getattr(config, "COVER_SEED", 11))
    img = Image.new("RGBA", (width, height), BG + (255,))
    draw = ImageDraw.Draw(img, "RGBA")

    for radius, opacity, center_x, color in [
        (360, 24, 0.22, (35, 92, 120)),
        (310, 26, 0.76, (96, 105, 45)),
    ]:
        r = int(radius * min(width / 1280, height / 720))
        cx = int(width * center_x)
        cy = int(height * 0.55)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (opacity,))

    graph = nx.barabasi_albert_graph(95, 2, seed=getattr(config, "COVER_SEED", 11))
    pos = transform_layout(
        nx.spring_layout(graph, seed=getattr(config, "COVER_SEED", 11), k=0.22, iterations=120),
        int(width * 0.70),
        int(height * 0.53),
        min(width * 0.27, height * 0.36),
    )
    degrees = dict(graph.degree())
    hubs = [node for node, _ in sorted(degrees.items(), key=lambda item: item[1], reverse=True)[:5]]
    fit_nodes = [node for node, _ in sorted(degrees.items(), key=lambda item: item[1], reverse=True)[5:12]]
    draw_network(draw, graph, pos, high_nodes=hubs, fit_nodes=fit_nodes)

    margin_x = int(width * 0.055)
    title_y = int(height * 0.075)
    draw_text_fit(draw, (margin_x, title_y), public_text(getattr(config, "COVER_TITLE")), int(width * 0.88), int(height * 0.085), WHITE, bold=True)
    draw_text_fit(draw, (margin_x + 4, title_y + int(height * 0.105)), public_text(getattr(config, "COVER_SUBTITLE")), int(width * 0.80), int(height * 0.045), YELLOW)

    box_y = int(height * 0.80)
    box_h = int(height * 0.09)
    labels = [
        (public_text(getattr(config, "COVER_LEFT_LABEL", "model")), YELLOW, int(width * 0.075), int(width * 0.37)),
        (public_text(getattr(config, "COVER_RIGHT_LABEL", "data")), GREEN, int(width * 0.40), int(width * 0.70)),
    ]
    for text, color, left, right in labels:
        draw.rounded_rectangle((left, box_y, right, box_y + box_h), radius=18, fill=BG + (230,), outline=color + (245,), width=3)
        draw_text_fit(draw, (left + 22, box_y + int(box_h * 0.22)), text, right - left - 44, int(height * 0.037), color, bold=True)

    draw_text_fit(draw, (margin_x, int(height * 0.93)), public_text(getattr(config, "COVER_FOOTER", "")), int(width * 0.70), int(height * 0.032), GREY)
    img.convert("RGB").save(output, quality=95)
    print(output)
    return output


def write_video_description(video_dir: Path, config: ModuleType) -> Path:
    references = "\n\n".join(f"{label}:\n{url}" for label, url in getattr(config, "REFERENCES", []))
    text = f"""# {getattr(config, 'VIDEO_LABEL', video_dir.name)} Description

## Suggested Title

{public_text(getattr(config, 'SUGGESTED_TITLE'))}

## Short Description

{public_text(getattr(config, 'SHORT_DESCRIPTION'))}

## References

{references}
"""
    output = video_dir / "video_description.md"
    output.write_text(text, encoding="utf-8")
    print(output)
    return output


def build_public_assets(video_dir: Path) -> list[Path]:
    config = load_config(video_dir)
    generated: list[Path] = []
    for spec in getattr(config, "COVER_OUTPUTS"):
        generated.append(make_default_cover(video_dir, config, int(spec["width"]), int(spec["height"]), spec["filename"]))
    generated.append(write_video_description(video_dir, config))
    return generated


def main(video_dir: Path | None = None) -> None:
    build_public_assets(video_dir or Path.cwd())
