# Data

## Current local files

At setup on 26 October 2026, this working copy contained 51 state-level text
files, including `CA.TXT`, `NY.TXT` and `DC.TXT`. They have been moved from
`data/` to `data/raw/state/`, with their contents verified unchanged.
They remain local and are excluded from Git. A fresh clone receives the folder
placeholders and source instructions, without the datasets.

```text
data/
├── raw/
│   ├── state/       Local original state files; source README still missing
│   └── national/    Reserved for official national files; not acquired yet
└── processed/       Outputs of documented preparation steps
```

The national directory still contains only its `.gitkeep` placeholder.
The preparation notebook generates `state_names.csv.gz` and `state_audit.json`
in the processed directory. EDA outputs are saved in `reports/figures/` and
`reports/tables/`.

On **9 November 2026**, a reproducible inventory verified all 51 local state
files: **6,696,687 records**, covering **1910–2025**, with all 50 states plus DC.
All files passed the inventory's parsing and code checks and remained
byte-for-byte unchanged. See the [inventory record](../docs/data_inventory/README.md),
[per-file checksums and coverage](../docs/data_inventory/files.csv), and
[machine-readable summary](../docs/data_inventory/summary.json).

The state files are comma-separated and have no header. Their verified
column order is:

```text
state, sex, year, name, count
```

The state preparation audit was rerun successfully on **14 November 2026**:
all **11,832 state–sex–year groups** were present, with no structural failures
or duplicate keys. The **6,696,687 rows** sum to **330,978,761 published counts**.
It retained all rows, including **1,811 placeholder-like records** flagged for
review, and added decade, name length, within-group published share and rank
with alphabetical tie-breaking. All 51 raw-file hashes remained unchanged;
the exported CSV was reloaded and verified. Initial state EDA also executed,
producing report figures and CSV tables.

The existing files' original download date and exact release remain unknown.
Group coverage does not establish coverage of all names or all births.
National files, the SSA archive README and a sourced regional lookup remain
absent. The completed state audit does not close those outstanding tasks.

To regenerate the inventory with the project environment activated, run:

```bash
python src/ssa_inventory.py --datasets state
```

## Fit with the course recommendations

The course recommends at least 1,000 observations and 8–12 variables with a
mix of numeric, categorical, temporal and text fields. Our state data exceeds
the row recommendation and includes all four broad types, but has only **five
raw fields**. The prepared table has **nine columns**, including four useful
derived fields; the sourced geographical lookup remains planned. Derived
columns are not independent new information. We justify each addition and the
suitability of these aggregate longitudinal records. See the
[course requirements and project implications](../docs/course_requirements.md)
for the full recommendations and the distinction from mandatory deliverables.

## Official sources

- [SSA documentation and publication limits](https://www.ssa.gov/oact/babynames/limits.html)
- [State data archive](https://www.ssa.gov/oact/babynames/state/namesbystate.zip)
- [National data archive](https://www.ssa.gov/oact/babynames/names.zip)

A fresh clone will contain this README, not the data. When acquiring the data,
download the relevant official archive and preserve its README. State files
belong in `data/raw/state/`; national files belong in `data/raw/national/`.
Record the source URL, download date, archive checksum and
observed year coverage so the group can identify which release it used. Agree
on the same release before comparing results, and do not overwrite the existing
files during inspection.

Keep the source data unchanged. Save future transformed datasets separately,
in `data/processed/`, and document how they were produced.
Data files and downloaded archive READMEs are ignored by Git. This project
README and the `.gitkeep` placeholders remain versionable.

SSA suppresses some rare-name records to protect privacy. A missing name from
a published file must not automatically be treated as zero occurrences. See
the official documentation above before choosing denominators or handling
absent records.

## First acquisition and audit notebook

Use [notebook 01](../notebooks/01_data_acquisition_and_audit.ipynb) to identify releases and inspect the actual files. If automated downloads are refused, create `data/raw/archives/` if absent, save the two official ZIPs there as `names.zip` and `namesbystate.zip`, then rerun. It preserves raw files, records checksums and writes local evidence in a separate UTC timestamp folder for each run under `data/processed/audit/`. Existing extracted files can be inspected with unverified archive provenance explicitly recorded; files absent from the selected ZIP are flagged for review.

Read the [expected-schema dictionary](../docs/data_dictionary.md) and the [9 November acquisition-audit note](../docs/data_audit.md). That earlier notebook's real-data run remains unverified; the separate state preparation and EDA notebooks produced the verified results described above.
