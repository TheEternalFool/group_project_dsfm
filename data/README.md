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
│   ├── state/       Original state files and their source README
│   └── national/    Original national files and their source README
└── processed/       Outputs of documented preparation steps
```

At setup on 26 October, the national and processed directories contained only
`.gitkeep` placeholders. Git uses these empty files to retain the folder layout.
Current local contents could not be verified in the 9 November session.

The sampled state files are comma-separated and have no header. The expected
column order to verify during inspection is:

```text
state, sex, year, name, count
```

The existing files' original download date, release and full year coverage have
not yet been established. National files and the SSA archive readme were not
present in the 26 October working copy. Do not describe the national data as acquired or
assume that the local files already include 2025.

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

Read the [expected-schema dictionary](../docs/data_dictionary.md) and [current audit status](../docs/data_audit.md). No real-data audit results are currently claimed.
