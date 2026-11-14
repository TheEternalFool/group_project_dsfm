# Local SSA data inventory

**Inspected on 9 November 2026.** This step inventories the state files already
present in the project. It does not download, modify or prepare datasets.

The findings and next step below describe that inspection. Preparation and
EDA have since been completed for the local state snapshot; see the
[current project status](../../README.md#current-status-and-phase-1-completion)
and [report guide](../../reports/README.md).

## Verified coverage

| Measure | Observed result |
|---|---|
| Location | `data/raw/state/` |
| Data files | 51 `.TXT` files |
| Geography | All 50 US states plus DC; no missing state codes |
| Observation unit | State × name × recorded sex × birth year |
| Records | **6,696,687** CSV rows, not a count of births |
| Observed years | **1910–2025**, with no missing year at dataset level |
| Recorded-sex codes | `F`, `M` |
| Raw size | 137,756,141 bytes |
| National data | Not inventoried; `data/raw/national/` contains only `.gitkeep` |
| Prepared outputs | None yet |

[files.csv](files.csv) records every data file's exact-byte SHA-256, size, row
count, years and codes. [summary.json](summary.json) contains aggregate coverage
and explicitly lists checks not performed. These small metadata files can be
shared in Git; the source datasets remain ignored.

## Provenance: what is known and what is not

The existing project documentation identifies the files as SSA state data.
Their format is consistent with that description. The expected official source
is the [SSA state archive](https://www.ssa.gov/oact/babynames/state/namesbystate.zip),
linked from [SSA's download and publication-limits page](https://www.ssa.gov/oact/babynames/limits.html).
The source documentation was consulted on 9 November 2026.

The **original download date, original ZIP checksum and exact release are
unknown**. No SSA archive README accompanies these local files. The checksums
recorded here identify the files we actually have; they do not prove a match
to a particular official release. The inspection date is not a download date.

The confirmed end year is 2025. That alone does not identify the release,
because later releases may revise earlier counts. Resolving acquisition
provenance remains open, and national acquisition is deferred.

## Checks completed and limits

The inventory streamed all records and checked field counts, nonempty names
without surrounding whitespace, integer years, positive integer counts,
recorded-sex codes, and agreement between state codes and filenames. All files
passed those checks. An independent line count agrees with the record total.
SHA-256 checks before and after the run confirmed that all **51 raw files stayed
byte-for-byte unchanged**.

This is not the full quality audit. Duplicate keys, implausible years/counts,
unusual names, and coverage of each state–sex–year combination still require
checking. Dataset-wide year coverage does not establish every combination.
No rows were dropped, corrected, imputed or aggregated into analytical outputs.

SSA explains that privacy suppression omits some low-frequency records and
that state totals can therefore differ from national totals. An absent record
must not automatically become zero. Counts come from Social Security card
applications and have historical coverage and recording limitations; see
[SSA's data qualifications](https://www.ssa.gov/oact/babynames/background.html).

## Reproduce

With the project's Python environment activated, run from the repository root:

```bash
python src/ssa_inventory.py --datasets state
```

This regenerates `files.csv` and `summary.json` in this directory. Inputs default
to paths relative to the script's repository, so execution also works from
`notebooks/` using `python ../src/ssa_inventory.py --datasets state`.

The files are deterministic for the same inputs; they do not contain a changing
run timestamp. This README records the inspection date. For a separate run,
use `--output-dir /path/to/inventory`; never write metadata inside the raw data
directory. A failed parse returns a nonzero exit code without generating a new
inventory. If prior outputs exist, they remain a historical snapshot, not
evidence of a successful rerun.

Validation on 9 November used the existing project `.venv` with Python 3.12.0.
A separate run launched from `notebooks/` produced byte-identical CSV and JSON
outputs to the repository-root run. PyCharm's environment-discovery tool
reported no project modules, so these checks used the existing local environment
without changing IDE settings.

When national files are acquired, omitting `--datasets state` inventories both
datasets and fails explicitly if either dataset is absent. Do not describe
state sums as a substitute for the missing national data.

Seven small fixture tests check exact-byte hashes, counts, year gaps, malformed
inputs, missing files, state-only operation, deterministic outputs and raw-folder
protection:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

**Next step:** document the data dictionary and perform the full state-data
quality audit before creating prepared outputs or starting EDA.
