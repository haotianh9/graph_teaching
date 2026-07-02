from __future__ import annotations

import csv
import datetime as dt
import gzip
import json
import math
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np


VIDEO_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = VIDEO_DIR / "assets" / "data" / "snap_hepth"
OUT_DIR = VIDEO_DIR / "data"

URLS = {
    "cit-HepTh.txt.gz": "https://snap.stanford.edu/data/cit-HepTh.txt.gz",
    "cit-HepTh-dates.txt.gz": "https://snap.stanford.edu/data/cit-HepTh-dates.txt.gz",
}


def ensure_raw_data() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for filename, url in URLS.items():
        path = RAW_DIR / filename
        if path.exists():
            continue
        print(f"Downloading {url}", flush=True)
        urllib.request.urlretrieve(url, path)


def parse_dates(path: Path) -> dict[int, dt.date]:
    dates: dict[int, dt.date] = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            paper_id, date_text = line.split()[:2]
            try:
                date = dt.date.fromisoformat(date_text)
            except ValueError:
                continue
            dates[int(paper_id)] = date

            # SNAP notes that cross-listed papers can use ids of the form 11<true_id>.
            # The citation file often uses the unprefixed id, so keep both keys.
            if paper_id.startswith("11") and len(paper_id) == 9:
                dates[int(paper_id[2:])] = date
    return dates


def collect_citation_ages(edge_path: Path, dates: dict[int, dt.date]):
    by_cited: dict[int, list[float]] = defaultdict(list)
    stats = {
        "edges_total": 0,
        "edges_with_dates": 0,
        "edges_with_missing_dates": 0,
        "edges_with_negative_age": 0,
    }
    with gzip.open(edge_path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            citing_text, cited_text = line.split()[:2]
            citing = int(citing_text)
            cited = int(cited_text)
            stats["edges_total"] += 1

            citing_date = dates.get(citing)
            cited_date = dates.get(cited)
            if citing_date is None or cited_date is None:
                stats["edges_with_missing_dates"] += 1
                continue

            age_years = (citing_date - cited_date).days / 365.25
            if age_years < 0:
                stats["edges_with_negative_age"] += 1
                continue

            stats["edges_with_dates"] += 1
            by_cited[cited].append(age_years)
    return by_cited, stats


def fit_growth(by_cited: dict[int, list[float]], dates: dict[int, dt.date]):
    rows: list[dict] = []
    for paper_id, ages in by_cited.items():
        ages = sorted(ages)
        total = len(ages)
        if total < 8 or ages[-1] < 2.0:
            continue

        x = np.log1p(np.array(ages, dtype=float))
        y = np.log1p(np.arange(1, total + 1, dtype=float))
        if float(x.max() - x.min()) < 0.45:
            continue

        beta_hat, intercept = np.polyfit(x, y, 1)
        if not math.isfinite(float(beta_hat)):
            continue

        early_share = sum(age <= 2.0 for age in ages) / total
        rows.append(
            {
                "paper_id": paper_id,
                "date": dates[paper_id].isoformat() if paper_id in dates else "",
                "total_citations": total,
                "beta_hat": float(beta_hat),
                "intercept": float(intercept),
                "early_share_first_2y": float(early_share),
                "max_age_years": float(ages[-1]),
                "ages": ages,
            }
        )
    mean_beta = float(np.mean([row["beta_hat"] for row in rows]))
    for row in rows:
        row["eta_hat"] = row["beta_hat"] / mean_beta
    return rows, mean_beta


def downsample_curve(ages: list[float], max_points: int = 48) -> tuple[list[float], list[int]]:
    total = len(ages)
    if total <= max_points:
        indices = list(range(total))
    else:
        indices = sorted(set(np.linspace(0, total - 1, max_points, dtype=int).tolist()))
    return [round(float(ages[i]), 3) for i in indices], [i + 1 for i in indices]


def select_examples(rows: list[dict], mean_beta: float) -> list[dict]:
    candidates = [
        row
        for row in rows
        if row["total_citations"] >= 20 and row["max_age_years"] >= 4.0
    ]
    if len(candidates) < 3:
        raise RuntimeError("Not enough fitted papers for examples")

    early = max(
        candidates,
        key=lambda row: row["early_share_first_2y"]
        - 0.15 * row["eta_hat"]
        + min(row["total_citations"], 150) / 10000,
    )
    steady_pool = [
        row for row in candidates if 0.20 <= row["early_share_first_2y"] <= 0.65
    ]
    steady = min(
        steady_pool,
        key=lambda row: abs(row["eta_hat"] - 1.0)
        + 0.0005 * abs(row["total_citations"] - 70),
    )
    late = max(
        candidates,
        key=lambda row: row["eta_hat"]
        - 1.4 * row["early_share_first_2y"]
        + min(row["total_citations"], 150) / 15000,
    )

    labels = [
        ("early burst", early, "many citations arrive early, then growth slows"),
        ("steady growth", steady, "middle slope, citations keep accumulating"),
        ("late bloomer", late, "small early share, high fitted growth slope"),
    ]
    examples = []
    for label, row, note in labels:
        ages, cumulative = downsample_curve(row["ages"])
        examples.append(
            {
                "label": label,
                "paper_id": row["paper_id"],
                "date": row["date"],
                "total_citations": row["total_citations"],
                "beta_hat": round(row["beta_hat"], 3),
                "eta_hat": round(row["eta_hat"], 3),
                "early_share_first_2y": round(row["early_share_first_2y"], 3),
                "max_age_years": round(row["max_age_years"], 3),
                "note": note,
                "ages": ages,
                "cumulative_citations": cumulative,
            }
        )
    return examples


def select_sample_curves(rows: list[dict], seed: int = 11, count: int = 28) -> list[dict]:
    rng = np.random.default_rng(seed)
    pool = [
        row
        for row in rows
        if 10 <= row["total_citations"] <= 120 and row["max_age_years"] >= 3
    ]
    indices = rng.choice(len(pool), size=min(count, len(pool)), replace=False)
    samples = []
    for idx in indices:
        row = pool[int(idx)]
        ages, cumulative = downsample_curve(row["ages"], max_points=28)
        samples.append(
            {
                "paper_id": row["paper_id"],
                "beta_hat": round(row["beta_hat"], 3),
                "eta_hat": round(row["eta_hat"], 3),
                "ages": ages,
                "cumulative_citations": cumulative,
            }
        )
    return samples


def write_outputs(rows: list[dict], mean_beta: float, stats: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    betas = np.array([row["beta_hat"] for row in rows], dtype=float)
    etas = np.array([row["eta_hat"] for row in rows], dtype=float)
    examples = select_examples(rows, mean_beta)
    samples = select_sample_curves(rows)
    eta_bins = np.linspace(0.3, 3.0, 14)
    eta_counts, eta_edges = np.histogram(etas, bins=eta_bins)
    eta_distribution = {
        "label": "estimated effective fitness from HEP-TH citation growth",
        "note": "eta_hat = beta_hat / mean(beta_hat); this is a teaching proxy for effective growth fitness",
        "bin_edges": [round(float(value), 3) for value in eta_edges],
        "counts": [int(value) for value in eta_counts],
        "density": [round(float(value / max(eta_counts.max(), 1)), 3) for value in eta_counts],
        "quantiles": {
            "p10": round(float(np.percentile(etas, 10)), 3),
            "p25": round(float(np.percentile(etas, 25)), 3),
            "p50": round(float(np.percentile(etas, 50)), 3),
            "p75": round(float(np.percentile(etas, 75)), 3),
            "p90": round(float(np.percentile(etas, 90)), 3),
            "p95": round(float(np.percentile(etas, 95)), 3),
            "p99": round(float(np.percentile(etas, 99)), 3),
        },
        "min": round(float(etas.min()), 3),
        "max": round(float(etas.max()), 3),
    }

    summary = {
        "dataset": "SNAP High-energy physics theory citation network",
        "source_url": "https://snap.stanford.edu/data/cit-HepTh.html",
        "edge_file": URLS["cit-HepTh.txt.gz"],
        "date_file": URLS["cit-HepTh-dates.txt.gz"],
        "period": "January 1993 to April 2003, with dated papers beginning in 1992",
        "method": "Fit slope of log(c_i(age)+1) vs log(age+1) for papers with at least 8 dated citations and at least 2 years of observed citation age.",
        "important_caveat": "This is an effective growth-fitness teaching proxy, not the full citation-impact model with aging and field effects.",
        **stats,
        "papers_with_enough_timed_citations": len(rows),
        "mean_beta_hat": round(float(betas.mean()), 3),
        "median_beta_hat": round(float(np.median(betas)), 3),
        "p10_beta_hat": round(float(np.percentile(betas, 10)), 3),
        "p90_beta_hat": round(float(np.percentile(betas, 90)), 3),
        "eta_distribution": eta_distribution,
        "examples": examples,
        "sample_curves": samples,
    }

    json_path = OUT_DIR / "fitness_fit_results.json"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    csv_path = OUT_DIR / "fitness_fit_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "paper_id",
                "label",
                "date",
                "total_citations",
                "beta_hat",
                "eta_hat",
                "early_share_first_2y",
                "max_age_years",
                "note",
            ],
        )
        writer.writeheader()
        for example in examples:
            writer.writerow(
                {
                    key: example[key]
                    for key in writer.fieldnames
                    if key in example
                }
            )

    print(f"Wrote {json_path.relative_to(VIDEO_DIR)}")
    print(f"Wrote {csv_path.relative_to(VIDEO_DIR)}")
    print(f"Fitted papers: {len(rows)}")


def main() -> None:
    ensure_raw_data()
    dates = parse_dates(RAW_DIR / "cit-HepTh-dates.txt.gz")
    by_cited, stats = collect_citation_ages(RAW_DIR / "cit-HepTh.txt.gz", dates)
    rows, mean_beta = fit_growth(by_cited, dates)
    write_outputs(rows, mean_beta, stats)


if __name__ == "__main__":
    main()
