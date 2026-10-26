"""Leakage-safe splits, baselines and uncertainty helpers.

Two rules from docs/methodology.md are enforced here:

* Unseen-name generalisation (RQ1 spelling -> period): split by complete
  name, so no name appears in both train and test.
* Temporal prediction (RQ3 shifts in female share): train only on years up
  to a cut-off and evaluate on later years.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

from names_project import RANDOM_STATE


def split_by_name(
    df: pd.DataFrame, test_size: float = 0.2, name_col: str = "name", random_state: int = RANDOM_STATE
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Train/test split where every name falls entirely on one side."""
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(splitter.split(df, groups=df[name_col]))
    return df.iloc[train_idx].copy(), df.iloc[test_idx].copy()


def temporal_split(df: pd.DataFrame, cutoff_year: int, year_col: str = "year") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Rows with year <= cutoff go to train, later rows go to test."""
    return df[df[year_col] <= cutoff_year].copy(), df[df[year_col] > cutoff_year].copy()


def bootstrap_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metric: Callable[[np.ndarray, np.ndarray], float],
    n_boot: int = 1000,
    alpha: float = 0.05,
    random_state: int = RANDOM_STATE,
) -> tuple[float, float, float]:
    """Point estimate and percentile bootstrap interval for a test metric."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    rng = np.random.default_rng(random_state)
    n = len(y_true)
    stats = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        stats[b] = metric(y_true[idx], y_pred[idx])
    lo, hi = np.quantile(stats, [alpha / 2, 1 - alpha / 2])
    return float(metric(y_true, y_pred)), float(lo), float(hi)


def compare_to_baseline(scores: dict[str, float], baseline_key: str = "baseline") -> pd.DataFrame:
    """Tabulate model scores next to the baseline and their difference."""
    base = scores[baseline_key]
    return pd.DataFrame(
        [{"model": k, "score": v, "diff_vs_baseline": v - base} for k, v in scores.items()]
    ).sort_values("score", ascending=False, ignore_index=True)
