"""Cleaning and reshaping of the raw SSA tables.

All popularity measures are normalised by the *published* births of the same
year and sex (and state). Because names under 5 occurrences are suppressed,
these denominators are slightly smaller than true births, and the gap is
largest in small states and recent, more diverse years.
"""

from __future__ import annotations

import pandas as pd


def tidy_types(df: pd.DataFrame) -> pd.DataFrame:
    """Give the raw columns compact, explicit dtypes and a stable order."""
    out = df.copy()
    out["name"] = out["name"].astype("string")
    out["sex"] = pd.Categorical(out["sex"], categories=["F", "M"])
    out["year"] = out["year"].astype("int16")
    out["count"] = out["count"].astype("int32")
    if "state" in out:
        out["state"] = out["state"].astype("category")
    keys = [c for c in ["state", "year", "sex"] if c in out]
    return out.sort_values(keys + ["count", "name"], ascending=[True] * len(keys) + [False, True]).reset_index(
        drop=True
    )


def add_popularity(df: pd.DataFrame, group: list[str] | None = None) -> pd.DataFrame:
    """Add ``share``, ``per_million`` and ``rank`` within each group.

    ``group`` defaults to year and sex (plus state when present). ``rank`` is
    1 for the most common name; ties share the lowest rank.
    """
    if group is None:
        group = [c for c in ["state", "year", "sex"] if c in df]
    out = df.copy()
    totals = out.groupby(group, observed=True)["count"].transform("sum")
    out["share"] = out["count"] / totals
    out["per_million"] = out["share"] * 1e6
    out["rank"] = out.groupby(group, observed=True)["count"].rank(method="min", ascending=False).astype("int32")
    return out


def add_decade(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["decade"] = (out["year"] // 10 * 10).astype("int16")
    return out


def female_share(df: pd.DataFrame, by: list[str] | None = None) -> pd.DataFrame:
    """Combine F and M rows into one row per name (and ``by`` keys).

    Returns columns ``count_f``, ``count_m``, ``total`` and ``female_share``.
    A name missing for one sex in a year gets a count of 0 for that sex, but
    note this really means "fewer than 5 recorded", not "none".
    """
    by = by if by is not None else [c for c in ["state", "year"] if c in df]
    wide = (
        df.pivot_table(index=by + ["name"], columns="sex", values="count", aggfunc="sum", fill_value=0, observed=True)
        .reindex(columns=["F", "M"], fill_value=0)
        .rename(columns={"F": "count_f", "M": "count_m"})
        .reset_index()
    )
    wide.columns.name = None
    wide["total"] = wide["count_f"] + wide["count_m"]
    wide["female_share"] = wide["count_f"] / wide["total"]
    return wide


def add_regions(df: pd.DataFrame, regions: pd.DataFrame) -> pd.DataFrame:
    """Merge Census region and division onto a frame with a ``state`` column."""
    out = df.merge(regions[["state", "region", "division"]], on="state", how="left", validate="many_to_one")
    if out["region"].isna().any():
        missing = sorted(out.loc[out["region"].isna(), "state"].astype(str).unique())
        raise ValueError(f"States without a Census region: {missing}")
    out["region"] = out["region"].astype("category")
    out["division"] = out["division"].astype("category")
    return out


def apply_min_count(df: pd.DataFrame, min_total: int, by: str = "name") -> pd.DataFrame:
    """Keep only names whose total count over the frame reaches ``min_total``.

    Used for trajectory analyses, where very rare names give noisy shares.
    Always report the threshold and run sensitivity checks with other values.
    """
    totals = df.groupby(by, observed=True)["count"].transform("sum")
    return df.loc[totals >= min_total].reset_index(drop=True)


def build_national(raw: pd.DataFrame) -> pd.DataFrame:
    """Raw national table -> analysis table with popularity measures."""
    return add_decade(add_popularity(tidy_types(raw)))


def build_state(raw: pd.DataFrame, regions: pd.DataFrame | None = None) -> pd.DataFrame:
    """Raw state table -> analysis table with popularity measures and regions."""
    out = add_decade(add_popularity(tidy_types(raw)))
    if regions is not None:
        out = add_regions(out, regions)
    return out
