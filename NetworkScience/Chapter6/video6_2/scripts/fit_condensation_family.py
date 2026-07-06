from __future__ import annotations

import json
import math
from pathlib import Path

from scipy.optimize import minimize_scalar


VIDEO_DIR = Path(__file__).resolve().parents[1]
CHAPTER_DIR = VIDEO_DIR.parent
HEP_FIT_PATH = CHAPTER_DIR / "video6_1" / "data" / "fitness_fit_results.json"
WEB_PROXY_PATH = VIDEO_DIR / "data" / "commoncrawl_web_fitness_proxy.json"
OUT_PATH = VIDEO_DIR / "data" / "condensation_family_fit.json"


def load_distributions() -> list[dict]:
    hep = json.loads(HEP_FIT_PATH.read_text(encoding="utf-8"))["eta_distribution"]
    web_summary = json.loads(WEB_PROXY_PATH.read_text(encoding="utf-8"))
    web = web_summary["eta_web_proxy_distribution"]
    return [
        {
            "name": "HEP-TH citation effective fitness proxy",
            "distribution": hep,
            "n_total": sum(hep["counts"]),
            "caveat": "Uses binned eta_hat = beta_hat / mean(beta_hat), not a direct intrinsic fitness measurement.",
        },
        {
            "name": "Common Crawl Web-domain visibility proxy",
            "distribution": web,
            "n_total": web_summary["domain_count"],
            "caveat": "Uses domain-level PageRank growth proxy; not page-level Web document fitness.",
        },
    ]


def binned_counts(dist: dict, n_total: int, normalization: str, tail: str | None = None) -> tuple[list[tuple[float, float, float]], float, float]:
    edges = [float(value) for value in dist["bin_edges"]]
    counts = [float(value) for value in dist["counts"]]
    min_value = float(dist.get("min", edges[0]))
    max_value = float(dist.get("max", edges[-1]))
    missing_upper = max(0.0, float(n_total) - sum(counts))

    raw_bins = [(left, right, count) for left, right, count in zip(edges[:-1], edges[1:], counts)]
    if missing_upper and edges[-1] < max_value:
        raw_bins.append((edges[-1], max_value, missing_upper))

    if tail is not None:
        threshold = float(dist["quantiles"][tail])
        trimmed = []
        for left, right, count in raw_bins:
            if right <= threshold:
                continue
            adjusted_left = max(left, threshold)
            fraction = (right - adjusted_left) / (right - left) if right > left else 1.0
            trimmed.append((adjusted_left, right, count * fraction))
        raw_bins = trimmed
        min_value = threshold

    if normalization == "sample_max":
        transform = lambda value: value / max_value
        bins: list[tuple[float, float, float]] = []
        first = max(0.0, min(1.0, transform(raw_bins[0][0]))) if raw_bins else 0.0
        if first > 0:
            bins.append((0.0, first, 0.0))
    elif normalization == "sample_minmax":
        transform = lambda value: (value - min_value) / (max_value - min_value)
        bins = []
    else:
        raise ValueError(f"Unknown normalization: {normalization}")

    for left, right, count in raw_bins:
        a = max(0.0, min(1.0, transform(left)))
        b = max(0.0, min(1.0, transform(right)))
        if b > a:
            bins.append((a, b, count))
    if bins and bins[-1][1] < 1.0:
        bins.append((bins[-1][1], 1.0, 0.0))
    return bins, min_value, max_value


def fit_zeta(bins: list[tuple[float, float, float]]) -> dict:
    """Fit rho(eta)=(1-zeta)(1-eta)^(-zeta), eta in [0,1]."""

    def bin_probability(left: float, right: float, zeta: float) -> float:
        power = 1.0 - zeta
        p_left = (1.0 - left) ** power if left < 1.0 else 0.0
        p_right = (1.0 - right) ** power if right < 1.0 else 0.0
        return max(p_left - p_right, 1e-300)

    def nll(zeta: float) -> float:
        if zeta >= 0.999:
            return 1e99
        return -sum(count * math.log(bin_probability(left, right, zeta)) for left, right, count in bins if count > 0)

    result = minimize_scalar(nll, bounds=(-10.0, 0.99), method="bounded", options={"xatol": 1e-8})
    zeta = float(result.x)
    n_obs = sum(count for _, _, count in bins)
    cumulative = 0.0
    max_cdf_error = 0.0
    mean_cdf_error = 0.0
    used = 0
    expected_bins = []
    chi2 = 0.0
    for left, right, count in bins:
        expected = n_obs * bin_probability(left, right, zeta)
        expected_bins.append(
            {
                "left": round(left, 4),
                "right": round(right, 4),
                "observed": round(count, 3),
                "expected": round(expected, 3),
            }
        )
        if expected > 1e-6:
            chi2 += (count - expected) ** 2 / expected
        cumulative += count
        empirical_cdf = cumulative / n_obs if n_obs else 0.0
        model_cdf = 1.0 - (1.0 - right) ** (1.0 - zeta) if right < 1.0 else 1.0
        error = abs(empirical_cdf - model_cdf)
        max_cdf_error = max(max_cdf_error, error)
        mean_cdf_error += error
        used += 1

    return {
        "zeta": round(zeta, 4),
        "equivalent_positive_exponent_theta": round(-zeta, 4),
        "n_binned_observations": round(n_obs, 3),
        "max_binned_cdf_error": round(max_cdf_error, 4),
        "mean_binned_cdf_error": round(mean_cdf_error / max(used, 1), 4),
        "chi_square_binned": round(chi2, 3),
        "expected_bins": expected_bins,
    }


def main() -> None:
    results = {
        "model": "rho(eta)=(1-zeta)(1-eta)^(-zeta), eta in [0,1]",
        "interpretation_note": (
            "The fitted video quantities are teaching proxies and are not naturally bounded by 1. "
            "The 'sample_max' normalization maps eta_hat/max(eta_hat) into [0,1] and tests the formula most literally, "
            "but it is strongly affected by selection/truncation. The 'sample_minmax' normalization tests only whether "
            "the observed shape resembles the theoretical family after removing the observed lower cutoff."
        ),
        "fits": [],
    }
    for item in load_distributions():
        dataset_result = {"name": item["name"], "caveat": item["caveat"], "fits": []}
        dist = item["distribution"]
        for normalization in ["sample_max", "sample_minmax"]:
            for tail in [None, "p75", "p90"]:
                bins, min_value, max_value = binned_counts(dist, item["n_total"], normalization=normalization, tail=tail)
                if sum(count for _, _, count in bins) < 5:
                    continue
                fit = fit_zeta(bins)
                fit.update(
                    {
                        "normalization": normalization,
                        "tail": tail or "all",
                        "raw_min_used": round(min_value, 4),
                        "raw_max_used": round(max_value, 4),
                    }
                )
                dataset_result["fits"].append(fit)
        results["fits"].append(dataset_result)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(VIDEO_DIR)}")
    for dataset in results["fits"]:
        print(dataset["name"])
        for fit in dataset["fits"]:
            if fit["tail"] in {"all", "p75", "p90"} and fit["normalization"] == "sample_minmax":
                print(
                    f"  {fit['normalization']} tail={fit['tail']}: "
                    f"zeta={fit['zeta']}, theta={fit['equivalent_positive_exponent_theta']}, "
                    f"KS~{fit['max_binned_cdf_error']}"
                )


if __name__ == "__main__":
    main()
