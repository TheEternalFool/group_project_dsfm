"""Inventory SSA source files without changing them or treating missing rows as zeros.

Run from any directory using the script's absolute path. Relative CLI paths are
resolved against the caller's working directory; defaults use the repository.
This checks parseability and coverage, not duplicate keys or analytical fitness.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATES = set("AK AL AR AZ CA CO CT DC DE FL GA HI IA ID IL IN KS KY LA MA MD ME MI MN MO MS MT NC ND NE NH NJ NM NV NY OH OK OR PA RI SC SD TN TX UT VA VT WA WI WV WY".split())
FILE_PATTERNS = {
    "state": re.compile(r"([A-Z]{2})\.TXT"),
    "national": re.compile(r"yob([0-9]{4})\.txt"),
}
CSV_FIELDS = [
    "dataset", "relative_path", "sha256", "bytes", "row_count",
    "year_min", "year_max", "years_present", "sex_codes", "geographies",
]


class InventoryError(ValueError):
    """A source is missing or cannot be safely inventoried as SSA records."""


def source_files(directory: Path, dataset: str) -> list[Path]:
    """Recognise data files explicitly; permit only known metadata companions."""
    if not directory.is_dir():
        raise InventoryError(f"Missing {dataset} data directory: {directory}")
    files = []
    for path in sorted(directory.iterdir()):
        is_readme = "readme" in path.stem.lower() and path.suffix.lower() in {
            ".txt", ".pdf", ".md", ".html"
        }
        if path.is_file() and (path.name in {".gitkeep", ".DS_Store"} or is_readme):
            continue
        match = FILE_PATTERNS[dataset].fullmatch(path.name)
        if not path.is_file() or match is None:
            raise InventoryError(f"Unrecognised {dataset} directory entry: {path}")
        if dataset == "state" and match.group(1) not in STATES:
            raise InventoryError(f"Unknown state code in filename: {path}")
        files.append(path)
    if not files:
        raise InventoryError(f"No {dataset} data files in {directory}")
    return files


def inspect_file(path: Path, dataset: str) -> dict:
    """Count records and hash the exact same byte stream, with bounded memory."""
    match = FILE_PATTERNS[dataset].fullmatch(path.name)
    if match is None:
        raise InventoryError(f"Unrecognised {dataset} filename: {path}")
    expected_state = match.group(1) if dataset == "state" else None
    file_year = int(match.group(1)) if dataset == "national" else None
    years, sexes, geographies = set(), set(), set()
    digest = hashlib.sha256()
    byte_count = 0
    row_count = 0
    reader = None

    def decoded_lines(stream):
        nonlocal byte_count
        for raw_line in stream:
            digest.update(raw_line)
            byte_count += len(raw_line)
            yield raw_line.decode("utf-8")

    try:
        with path.open("rb") as stream:
            reader = csv.reader(decoded_lines(stream), strict=True)
            for row in reader:
                expected_columns = 5 if dataset == "state" else 3
                if len(row) != expected_columns:
                    raise ValueError(f"expected {expected_columns} columns, got {len(row)}")
                if dataset == "state":
                    state, sex, year_text, name, count_text = row
                    if state != expected_state or state not in STATES:
                        raise ValueError(f"state {state!r} does not match filename {expected_state!r}")
                    if not re.fullmatch(r"[0-9]{4}", year_text):
                        raise ValueError(f"invalid integer year {year_text!r}")
                    year = int(year_text)
                    geography = state
                else:
                    name, sex, count_text = row
                    year = file_year
                    geography = "US"
                if sex not in {"F", "M"}:
                    raise ValueError(f"invalid recorded sex {sex!r}")
                if not name or name != name.strip():
                    raise ValueError("empty name or surrounding whitespace")
                if not re.fullmatch(r"[0-9]+", count_text) or int(count_text) <= 0:
                    raise ValueError(f"count must be a positive integer, got {count_text!r}")
                years.add(year)
                sexes.add(sex)
                geographies.add(geography)
                row_count += 1
    except (ValueError, csv.Error) as exc:
        line = reader.line_num if reader is not None else 0
        raise InventoryError(f"{path}, line {line}: {exc}") from exc
    if not row_count:
        raise InventoryError(f"Empty data file: {path}")
    try:
        relative_path = path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        relative_path = f"{dataset}/{path.name}"
    return {
        "dataset": dataset,
        "relative_path": relative_path,
        "sha256": digest.hexdigest(),
        "bytes": byte_count,
        "row_count": row_count,
        "year_min": min(years),
        "year_max": max(years),
        "years_present": sorted(years),
        "sex_codes": sorted(sexes),
        "geographies": sorted(geographies),
    }


def inventory(state_dir: Path, national_dir: Path, selected: tuple[str, ...] = ("state", "national")) -> tuple[list[dict], dict]:
    """Return file inventory and observed coverage; do not write source files."""
    records = []
    datasets = {}
    directories = {"state": state_dir, "national": national_dir}
    for dataset in selected:
        directory = directories[dataset]
        entries = [inspect_file(path, dataset) for path in source_files(directory, dataset)]
        records.extend(entries)
        years = sorted({year for entry in entries for year in entry["years_present"]})
        geographies = sorted({code for entry in entries for code in entry["geographies"]})
        datasets[dataset] = {
            "file_count": len(entries),
            "row_count": sum(entry["row_count"] for entry in entries),
            "bytes": sum(entry["bytes"] for entry in entries),
            "observation_unit": (["state"] if dataset == "state" else []) + ["name", "sex", "year"],
            "year_min": min(years),
            "year_max": max(years),
            "years_present": years,
            "missing_years_within_observed_range": sorted(set(range(min(years), max(years) + 1)) - set(years)),
            "sex_codes": sorted({code for entry in entries for code in entry["sex_codes"]}),
            "geographies": geographies,
        }
        if dataset == "state":
            datasets[dataset]["missing_states_including_dc"] = sorted(STATES - set(geographies))
    summary = {
        "schema_version": 1,
        "datasets": datasets,
        "datasets_not_inventoried": sorted(set(directories) - set(selected)),
        "checks_performed": [
            "exact-byte SHA-256 and file sizes", "CSV field count and nonempty names",
            "integer years and positive integer counts", "F/M recorded-sex codes",
            "state codes consistent with filenames", "observed file, year and geographical coverage",
        ],
        "not_performed": [
            "duplicate-key audit", "full data-quality audit", "acquisition provenance verification",
            "suppression imputation", "data preparation", "EDA",
        ],
        "notes": [
            "Row counts describe published records, not births or counts summed across records.",
            "Missing years are checked only inside the observed dataset range; target coverage requires separate comparison.",
            "Dataset-level year coverage does not establish coverage of every state/sex/year combination.",
            "relative_path is repository-relative for repository inputs; external inputs use dataset/filename.",
            "README files and .gitkeep/.DS_Store companions are excluded from data row counts and hashes.",
        ],
    }
    return records, summary


def write_inventory(records: list[dict], summary: dict, output_dir: Path) -> None:
    """Save deterministic, reviewable metadata after all inputs pass parsing."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "files.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        for record in records:
            row = dict(record)
            for field in ("years_present", "sex_codes", "geographies"):
                row[field] = ";".join(str(value) for value in row[field])
            writer.writerow(row)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, default=PROJECT_ROOT / "data/raw/state")
    parser.add_argument("--national-dir", type=Path, default=PROJECT_ROOT / "data/raw/national")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "docs/data_inventory")
    parser.add_argument("--datasets", nargs="+", choices=("state", "national"), default=["state", "national"], help="Datasets to inventory; select state to inspect only existing local state files.")
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    for source in (args.state_dir.resolve(), args.national_dir.resolve()):
        if output == source or output.is_relative_to(source):
            parser.error("output directory must not be inside a raw input directory")
    try:
        selected = tuple(dict.fromkeys(args.datasets))
        records, summary = inventory(args.state_dir, args.national_dir, selected)
        write_inventory(records, summary, output)
    except (InventoryError, OSError) as exc:
        print(f"Inventory failed: {exc}", file=sys.stderr)
        return 1
    for dataset, details in summary["datasets"].items():
        print(f"{dataset}: {details['file_count']} files, {details['row_count']:,} rows, {details['year_min']}–{details['year_max']}")
    print(f"Wrote {output / 'files.csv'} and {output / 'summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
