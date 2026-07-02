from __future__ import annotations

import csv
import gzip
import json
import math
import urllib.request
from pathlib import Path

import numpy as np


VIDEO_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = VIDEO_DIR / "data"
DATA_BASE_URL = "https://data.commoncrawl.org/projects/hyperlinkgraph"

# Year-spaced releases keep the demo light and reduce overlap among quarterly
# rolling windows. These are domain-level graphs, not page-level histories.
RELEASES = [
    "cc-main-2018-feb-mar-apr",
    "cc-main-2019-feb-mar-apr",
    "cc-main-2020-feb-mar-may",
    "cc-main-2021-feb-apr-may",
    "cc-main-2022-may-jun-aug",
    "cc-main-2023-may-sep-nov",
    "cc-main-2024-apr-may-jun",
    "cc-main-2025-apr-may-jun",
    "cc-main-2026-apr-may-jun",
]


def reverse_domain(host_rev: str) -> str:
    return ".".join(reversed(host_rev.split(".")))


def fetch_top_domains(release: str, limit: int = 1000) -> list[dict]:
    url = f"{DATA_BASE_URL}/{release}/domain/{release}-domain-ranks.txt.gz"
    rows: list[dict] = []
    with urllib.request.urlopen(url, timeout=45) as response:
        with gzip.GzipFile(fileobj=response) as handle:
            header = handle.readline().decode("utf-8").strip().split("\t")
            for _ in range(limit):
                line = handle.readline()
                if not line:
                    break
                fields = dict(zip(header, line.decode("utf-8").strip().split("\t")))
                rows.append(
                    {
                        "release": release,
                        "domain": reverse_domain(fields["#host_rev"]),
                        "harmonicc_pos": int(fields["#harmonicc_pos"]),
                        "harmonicc_val": float(fields["#harmonicc_val"]),
                        "pr_pos": int(fields["#pr_pos"]),
                        "pr_val": float(fields["#pr_val"]),
                        "n_hosts": int(fields["#n_hosts"]),
                    }
                )
    return rows


def fit_domain_visibility(rows_by_release: list[list[dict]], min_points: int = 5) -> list[dict]:
    by_domain: dict[str, list[dict]] = {}
    release_index = {release: idx for idx, release in enumerate(RELEASES)}
    for rows in rows_by_release:
        for row in rows:
            by_domain.setdefault(row["domain"], []).append(row)

    fitted: list[dict] = []
    for domain, rows in by_domain.items():
        rows = sorted(rows, key=lambda row: release_index[row["release"]])
        if len(rows) < min_points:
            continue
        t = np.array([release_index[row["release"]] for row in rows], dtype=float)
        y = np.log(np.array([row["pr_val"] for row in rows], dtype=float) + 1e-12)
        if float(t.max() - t.min()) < 3:
            continue
        slope, intercept = np.polyfit(t, y, 1)
        multiplier = float(math.exp(slope))
        fitted.append(
            {
                "domain": domain,
                "points": len(rows),
                "first_release": rows[0]["release"],
                "last_release": rows[-1]["release"],
                "first_pr": rows[0]["pr_val"],
                "last_pr": rows[-1]["pr_val"],
                "first_rank": rows[0]["pr_pos"],
                "last_rank": rows[-1]["pr_pos"],
                "log_pr_slope": float(slope),
                "visibility_multiplier": multiplier,
            }
        )
    median_multiplier = float(np.median([row["visibility_multiplier"] for row in fitted]))
    for row in fitted:
        row["eta_web_proxy"] = row["visibility_multiplier"] / median_multiplier
    return fitted


def histogram(values: np.ndarray) -> dict:
    bins = np.linspace(0.65, 1.45, 13)
    counts, edges = np.histogram(values, bins=bins)
    return {
        "bin_edges": [round(float(value), 3) for value in edges],
        "counts": [int(value) for value in counts],
        "density": [round(float(value / max(counts.max(), 1)), 3) for value in counts],
    }


def write_outputs(fitted: list[dict], top_limit: int) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    values = np.array([row["eta_web_proxy"] for row in fitted], dtype=float)
    fastest = sorted(fitted, key=lambda row: row["eta_web_proxy"], reverse=True)[:8]
    slowest = sorted(fitted, key=lambda row: row["eta_web_proxy"])[:8]
    summary = {
        "dataset": "Common Crawl domain-level Web Graph top-rank snapshots",
        "source_url": "https://commoncrawl.org/web-graphs",
        "statistics_url": "https://commoncrawl.github.io/cc-webgraph-statistics/",
        "method": (
            "Stream the top domain rank rows from yearly Common Crawl Web Graph releases; "
            "fit slope of log(PageRank) vs release index for domains appearing in at least "
            "five top-1000 snapshots; normalize exp(slope) by the median. This is a "
            "lightweight visibility-growth proxy, not the page-level WWW fitness estimate "
            "from Kong, Sarshar, and Roychowdhury (2008)."
        ),
        "important_caveat": (
            "The Network Science book's WWW fitness distribution uses web-document time evolution. "
            "This teaching proxy uses domain-level top-rank snapshots, so it measures domain "
            "visibility dynamics rather than intrinsic page talent directly."
        ),
        "release_count": len(RELEASES),
        "top_domains_per_release": top_limit,
        "domain_count": len(fitted),
        "releases": RELEASES,
        "eta_web_proxy_distribution": {
            "label": "Common Crawl domain visibility growth proxy",
            "note": "eta_web_proxy = exp(slope(log PageRank)) / median multiplier",
            **histogram(values),
            "quantiles": {
                "p10": round(float(np.percentile(values, 10)), 3),
                "p25": round(float(np.percentile(values, 25)), 3),
                "p50": round(float(np.percentile(values, 50)), 3),
                "p75": round(float(np.percentile(values, 75)), 3),
                "p90": round(float(np.percentile(values, 90)), 3),
                "p95": round(float(np.percentile(values, 95)), 3),
                "p99": round(float(np.percentile(values, 99)), 3),
            },
            "min": round(float(values.min()), 3),
            "max": round(float(values.max()), 3),
        },
        "examples": {
            "fastest": [
                {
                    "domain": row["domain"],
                    "eta_web_proxy": round(row["eta_web_proxy"], 3),
                    "first_rank": row["first_rank"],
                    "last_rank": row["last_rank"],
                    "points": row["points"],
                }
                for row in fastest
            ],
            "slowest": [
                {
                    "domain": row["domain"],
                    "eta_web_proxy": round(row["eta_web_proxy"], 3),
                    "first_rank": row["first_rank"],
                    "last_rank": row["last_rank"],
                    "points": row["points"],
                }
                for row in slowest
            ],
        },
    }
    json_path = OUT_DIR / "commoncrawl_web_fitness_proxy.json"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    csv_path = OUT_DIR / "commoncrawl_web_fitness_proxy_examples.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["kind", "domain", "eta_web_proxy", "first_rank", "last_rank", "points"])
        writer.writeheader()
        for kind in ["fastest", "slowest"]:
            for row in summary["examples"][kind]:
                writer.writerow({"kind": kind, **row})

    print(f"Wrote {json_path.relative_to(VIDEO_DIR)}")
    print(f"Wrote {csv_path.relative_to(VIDEO_DIR)}")
    print(f"Fitted domains: {len(fitted)}")


def main() -> None:
    top_limit = 1000
    rows_by_release = []
    for release in RELEASES:
        print(f"Fetching {release}", flush=True)
        rows_by_release.append(fetch_top_domains(release, limit=top_limit))
    fitted = fit_domain_visibility(rows_by_release)
    write_outputs(fitted, top_limit)


if __name__ == "__main__":
    main()
