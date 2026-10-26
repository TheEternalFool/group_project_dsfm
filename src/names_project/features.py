"""Engineered variables: name text features, trajectories and diversity.

These are *derived* from the original SSA variables (name, sex, year, state,
count). They help answer the research questions but do not add independent
information to the dataset; see docs/data-dictionary.md.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

VOWELS = set("aeiouy")


def name_text_features(names: pd.Series) -> pd.DataFrame:
    """Simple orthographic features for a series of names."""
    lower = names.astype("string").str.lower()
    return pd.DataFrame(
        {
            "name": names.values,
            "length": lower.str.len().astype("int16").values,
            "n_vowels": lower.map(lambda s: sum(ch in VOWELS for ch in s)).astype("int16").values,
            "first_letter": lower.str[0].values,
            "last_letter": lower.str[-1].values,
            "ends_in_vowel": lower.str[-1].isin(list(VOWELS)).values,
        }
    )


def char_ngram_vectorizer(ngram_range: tuple[int, int] = (1, 3), min_df: int = 5) -> TfidfVectorizer:
    """Character n-gram vectoriser with word boundaries (``^`` and ``$``).

    Names are wrapped in boundary markers so that prefixes and suffixes are
    distinguished from inner letter sequences. Fit it on training names only.
    """
    return TfidfVectorizer(
        analyzer="char",
        ngram_range=ngram_range,
        min_df=min_df,
        lowercase=True,
        preprocessor=lambda s: f"^{s.lower()}$",
        sublinear_tf=True,
    )


def trajectory_features(df: pd.DataFrame, share_col: str = "share") -> pd.DataFrame:
    """Summarise each (name, sex) popularity trajectory over time.

    Expects one row per name, sex and year with ``count`` and ``share_col``.
    ``mean_year`` is the birth-weighted mean year of birth of bearers.
    """
    g = df.sort_values("year").groupby(["name", "sex"], observed=True)
    peak_idx = df.groupby(["name", "sex"], observed=True)[share_col].idxmax()
    peaks = df.loc[peak_idx, ["name", "sex", "year", share_col]].rename(
        columns={"year": "peak_year", share_col: "peak_share"}
    )
    weighted_year = (df["year"].astype("float64") * df["count"]).groupby([df["name"], df["sex"]], observed=True).sum()
    summary = pd.DataFrame(
        {
            "first_year": g["year"].min(),
            "last_year": g["year"].max(),
            "years_in_use": g["year"].nunique(),
            "total_count": g["count"].sum(),
        }
    )
    summary["mean_year"] = weighted_year / summary["total_count"]
    return summary.reset_index().merge(peaks, on=["name", "sex"], how="left")


def diversity(counts: pd.Series | np.ndarray, top_k: int = 10) -> dict[str, float]:
    """Diversity of one count distribution (e.g. one state-year-sex).

    Returns Shannon entropy (nats), effective number of names (exp entropy),
    Herfindahl-Hirschman index, and the share held by the ``top_k`` names.
    Suppression of rare names biases all of these towards concentration.
    """
    c = np.asarray(counts, dtype="float64")
    c = c[c > 0]
    if c.size == 0:
        return {"entropy": np.nan, "effective_names": np.nan, "hhi": np.nan, f"top{top_k}_share": np.nan}
    p = c / c.sum()
    entropy = float(-(p * np.log(p)).sum())
    return {
        "entropy": entropy,
        "effective_names": float(np.exp(entropy)),
        "hhi": float((p**2).sum()),
        f"top{top_k}_share": float(np.sort(p)[::-1][:top_k].sum()),
    }


def diversity_by(df: pd.DataFrame, by: list[str], top_k: int = 10) -> pd.DataFrame:
    """Apply :func:`diversity` to each group of ``by``."""
    rows = [
        {**dict(zip(by, key, strict=True)), **diversity(group["count"], top_k)}
        for key, group in df.groupby(by, observed=True)
    ]
    return pd.DataFrame(rows)


def jensen_shannon(p: pd.Series, q: pd.Series) -> float:
    """Jensen-Shannon distance (base 2, in [0, 1]) between two count vectors.

    ``p`` and ``q`` are indexed by name; missing names count as zero.
    """
    from scipy.spatial.distance import jensenshannon

    aligned = pd.concat([p, q], axis=1).fillna(0).to_numpy(dtype="float64")
    return float(jensenshannon(aligned[:, 0], aligned[:, 1], base=2))
