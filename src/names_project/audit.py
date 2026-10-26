"""Preliminary data-quality audit of the raw SSA tables.

Produces facts that the report's Data section needs (dimensions, types,
missing values, coverage) and quantifies how much of each table sits at the
SSA publication threshold of 5 occurrences.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from names_project.data import SSA_MIN_COUNT, validate_national, validate_state


def audit_frame(df: pd.DataFrame, kind: str) -> dict[str, Any]:
    """Compute audit statistics for a raw ``national`` or ``state`` table."""
    if kind not in {"national", "state"}:
        raise ValueError("kind must be 'national' or 'state'")
    years = sorted(df["year"].unique())
    expected_years = set(range(years[0], years[-1] + 1))
    at_min = df["count"] == SSA_MIN_COUNT
    near_min = df["count"] < 2 * SSA_MIN_COUNT
    sexes_per_name = df.groupby("name")["sex"].nunique()
    group = ["state", "year", "sex"] if kind == "state" else ["year", "sex"]
    names_per_group = df.groupby(group, observed=True)["name"].size()

    result: dict[str, Any] = {
        "kind": kind,
        "n_rows": len(df),
        "n_columns": df.shape[1],
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing": {c: int(n) for c, n in df.isna().sum().items()},
        "year_min": int(years[0]),
        "year_max": int(years[-1]),
        "n_years": len(years),
        "missing_years": sorted(expected_years - set(years)),
        "n_unique_names": int(df["name"].nunique()),
        "n_name_sex_pairs": int(df.groupby(["name", "sex"]).ngroups),
        "share_names_both_sexes": float((sexes_per_name > 1).mean()),
        "births_total": int(df["count"].sum()),
        "births_by_sex": {str(k): int(v) for k, v in df.groupby("sex")["count"].sum().items()},
        "count_min": int(df["count"].min()),
        "count_median": float(df["count"].median()),
        "count_max": int(df["count"].max()),
        "share_rows_at_threshold": float(at_min.mean()),
        "share_rows_below_10": float(near_min.mean()),
        "share_births_below_10": float(df.loc[near_min, "count"].sum() / df["count"].sum()),
        "names_per_group_median": float(names_per_group.median()),
        "validation_problems": validate_state(df) if kind == "state" else validate_national(df),
    }
    if kind == "state":
        per_state = df.groupby("state", observed=True).agg(rows=("count", "size"), births=("count", "sum"))
        result["n_states"] = int(df["state"].nunique())
        result["states"] = sorted(df["state"].astype(str).unique())
        result["rows_per_state_min"] = (str(per_state["rows"].idxmin()), int(per_state["rows"].min()))
        result["rows_per_state_max"] = (str(per_state["rows"].idxmax()), int(per_state["rows"].max()))
    return result


def threshold_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Per year: rows, births, and share of rows at the publication threshold."""
    return (
        df.assign(at_min=df["count"] == SSA_MIN_COUNT)
        .groupby("year")
        .agg(rows=("count", "size"), births=("count", "sum"), share_rows_at_threshold=("at_min", "mean"))
        .reset_index()
    )


def audit_to_markdown(audit: dict[str, Any], by_year: pd.DataFrame | None = None) -> str:
    """Render one audit dictionary as a Markdown section."""
    a = audit
    lines = [
        f"## {a['kind'].capitalize()} table",
        "",
        "| Statistic | Value |",
        "|---|---|",
        f"| Rows | {a['n_rows']:,} |",
        f"| Columns | {a['n_columns']} ({', '.join(f'`{c}`: {t}' for c, t in a['dtypes'].items())}) |",
        f"| Missing values | {sum(a['missing'].values())} |",
        f"| Years | {a['year_min']}-{a['year_max']} ({a['n_years']} years; missing: {a['missing_years'] or 'none'}) |",
    ]
    if a["kind"] == "state":
        lines += [
            f"| States | {a['n_states']} |",
            f"| Fewest rows | {a['rows_per_state_min'][0]} ({a['rows_per_state_min'][1]:,}) |",
            f"| Most rows | {a['rows_per_state_max'][0]} ({a['rows_per_state_max'][1]:,}) |",
        ]
    lines += [
        f"| Distinct names | {a['n_unique_names']:,} |",
        f"| Distinct name-sex pairs | {a['n_name_sex_pairs']:,} |",
        f"| Names recorded under both sexes (ever) | {a['share_names_both_sexes']:.1%} |",
        f"| Published births | {a['births_total']:,} |",
        f"| Published births by sex | {', '.join(f'{k}: {v:,}' for k, v in a['births_by_sex'].items())} |",
        f"| Count min / median / max | {a['count_min']} / {a['count_median']:g} / {a['count_max']:,} |",
        f"| Rows exactly at threshold (count = 5) | {a['share_rows_at_threshold']:.1%} |",
        f"| Rows with count < 10 | {a['share_rows_below_10']:.1%} |",
        f"| Births in rows with count < 10 | {a['share_births_below_10']:.2%} |",
        f"| Median names per {'state-' if a['kind'] == 'state' else ''}year-sex | {a['names_per_group_median']:g} |",
        f"| Validation problems | {'; '.join(a['validation_problems']) or 'none'} |",
        "",
    ]
    if by_year is not None:
        decades = by_year[by_year["year"] % 10 == 0]
        lines += [
            "Share of rows exactly at the publication threshold, every tenth year:",
            "",
            "| Year | Rows | Published births | Rows at threshold |",
            "|---|---|---|---|",
        ]
        lines += [
            f"| {r.year} | {r.rows:,} | {r.births:,} | {r.share_rows_at_threshold:.1%} |"
            for r in decades.itertuples()
        ]
        lines.append("")
    return "\n".join(lines)
