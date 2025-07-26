# src/powerball_suite/analysis/latent_sets.py
"""Discover ‘latent’ ball‑sets by clustering one‑hot drawings."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE

WHITE_BALLS = list(range(1, 70))  # 1–69 inclusive


# ───────────────────────── IO ──────────────────────────


def load_white_balls(csv_path: str | Path) -> tuple[pd.Series, np.ndarray]:
    """Load the CSV and return (dates, one‑hot‑matrix[ n_draws × 69 ])."""
    df = pd.read_csv(csv_path)

    # Pick the first 5 integer columns → assumed to be the white balls
    white_cols = [c for c in df.columns if df[c].dtype.kind in "iu"][:5]
    if len(white_cols) != 5:
        raise ValueError(
            f"Expected 5 integer columns (white balls) but found {len(white_cols)}."
        )

    one_hot = np.zeros((len(df), len(WHITE_BALLS)), dtype=int)
    for i, row in enumerate(df[white_cols].to_numpy()):
        one_hot[i, row - 1] = 1  # Balls are 1‑based in the data

    date_col = df["date"] if "date" in df.columns else pd.Series(range(len(df)))
    return date_col, one_hot


# ──────────────────── Core discovery ───────────────────


def discover_sets(
    csv_path: str | Path,
    eps: float = 1.5,
    min_samples: int = 8,
    perplexity: int = 40,
    plot: bool = True,
) -> pd.DataFrame:
    """Return a DataFrame[date, cluster] after t‑SNE → DBSCAN."""
    dates, X = load_white_balls(csv_path)

    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        metric="cosine",
        random_state=0,
    ).fit_transform(X)

    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(tsne)

    if plot:
        _, ax = plt.subplots(figsize=(7, 6))
        scatter = ax.scatter(tsne[:, 0], tsne[:, 1], c=labels, cmap="tab20", s=30)
        ax.set(
            title="Latent clusters (possible ball‑sets)",
            xlabel="t‑SNE dim 1",
            ylabel="t‑SNE dim 2",
        )
        plt.colorbar(scatter, ax=ax, label="cluster id")
        plt.tight_layout()
        plt.show()

    return pd.DataFrame({"date": dates, "cluster": labels})


# ───────────────────────── CLI ─────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m powerball_suite.analysis.latent_sets",
        description="Cluster Powerball drawings into latent ball‑sets.",
    )
    p.add_argument("csv", type=Path, help="Cleaned Powerball CSV (≥ 5 white‑ball cols)")
    p.add_argument("--eps", type=float, default=1.5, help="DBSCAN ε (default 1.5)")
    p.add_argument(
        "--min-samples", type=int, default=8, help="DBSCAN min_samples (default 8)"
    )
    p.add_argument(
        "--perplexity",
        type=int,
        default=40,
        help="t‑SNE perplexity (default 40 — works well for ~1 k rows)",
    )
    p.add_argument(
        "--no-plot",
        dest="plot",
        action="store_false",
        help="Skip the scatter plot (headless / CI runs)",
    )
    return p


def main() -> None:
    args = _build_parser().parse_args()

    clusters = discover_sets(
        csv_path=args.csv,
        eps=args.eps,
        min_samples=args.min_samples,
        perplexity=args.perplexity,
        plot=args.plot,
    )

    out_path = Path(args.csv).with_name("draws_with_cluster_labels.csv")
    clusters.to_csv(out_path, index=False)
    print(f"✓ wrote {out_path.relative_to(Path.cwd())}")
    print(clusters.cluster.value_counts(dropna=False).sort_index())


if __name__ == "__main__":
    main()
