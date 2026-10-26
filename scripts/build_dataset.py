"""Validate the raw SSA files and write processed Parquet tables.

Usage:
    python scripts/build_dataset.py

Outputs (in data/processed/, not committed):
    national.parquet          year, name, sex, count, share, per_million, rank, decade
    national_female_share.parquet   year, name, count_f, count_m, total, female_share
    state.parquet             state, year, name, sex, count, share, per_million, rank,
                              decade, region, division

A table whose raw files are missing is skipped with a message.
"""

from __future__ import annotations

import sys

from names_project import data, preprocessing


def main() -> int:
    paths = data.Paths()
    paths.processed.mkdir(parents=True, exist_ok=True)
    built = 0

    try:
        raw = data.load_national_raw()
    except FileNotFoundError as exc:
        print(f"[skip national] {exc}")
    else:
        problems = data.validate_national(raw)
        if problems:
            print("[error national] " + "; ".join(problems), file=sys.stderr)
            return 1
        national = preprocessing.build_national(raw)
        national.to_parquet(paths.processed / "national.parquet", index=False)
        preprocessing.female_share(national, by=["year"]).to_parquet(
            paths.processed / "national_female_share.parquet", index=False
        )
        print(f"[ok national] {len(national):,} rows")
        built += 1

    try:
        raw = data.load_state_raw()
    except FileNotFoundError as exc:
        print(f"[skip state] {exc}")
    else:
        problems = data.validate_state(raw)
        if problems:
            print("[error state] " + "; ".join(problems), file=sys.stderr)
            return 1
        state = preprocessing.build_state(raw, data.load_census_regions())
        state.to_parquet(paths.processed / "state.parquet", index=False)
        print(f"[ok state] {len(state):,} rows")
        built += 1

    return 0 if built else 1


if __name__ == "__main__":
    raise SystemExit(main())
