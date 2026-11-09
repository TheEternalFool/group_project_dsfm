# Phase 1 acquisition and audit status

**Status: 9 November 2026 — real-data audit not completed.**

## What is available

- `notebooks/01_data_acquisition_and_audit.ipynb` provides source acquisition, provenance recording, non-overwriting extraction, schema/quality checks and local audit outputs.
- `docs/data_dictionary.md` defines expected observation units, fields and interpretation issues.
- `docs/project_requirements.md` records the submission requirements and dataset recommendations supplied by the group.

## What prevented a real run

Both official archive URLs returned **HTTP 403 Forbidden** to automated download attempts:

- https://www.ssa.gov/oact/babynames/names.zip
- https://www.ssa.gov/oact/babynames/state/namesbystate.zip

The local project folder was also inaccessible to this Codex session. The October setup documented 51 state files, but their current contents were not read for this task. The temporary October backup was no longer available. Consequently, no actual row totals, year coverage, missing-value rates, duplicate counts, release checksums or successful data-validation results are asserted here.

## How to complete this first task

1. Update the local checkout from GitHub's `main`.
2. Open the official archive links in a browser and save `names.zip` and `namesbystate.zip` in `data/raw/archives/` (create this folder if absent). Keep the actual download dates. If existing extracted files are available, they can be inspected without a ZIP, but archive provenance will remain unverified.
3. Open `notebooks/01_data_acquisition_and_audit.ipynb` with the project's Python environment and run it in order. Set `DOWNLOAD_MISSING = False` if using only local inputs.
4. If an archive differs from an existing raw file, investigate the release difference; the notebook deliberately does not replace that file.
5. Review `ssa_audit.json` and `ssa_file_audit.csv` in the new UTC timestamp folder printed by the notebook under `data/processed/audit/`. If every file fails to parse, that run contains only JSON errors. Earlier folders remain separate. Replace this status note with the observed results, unresolved issues and approved preparation decisions. Missing inputs must remain labelled **not audited**.

The notebook has no completed research findings saved in it. Data and machine-specific audit outputs remain local and ignored by Git.

## Code verification, not dataset findings

Checked with Python 3.12.14 and the project's pandas 2.3.3 dependency:

- Notebook format validation and targeted synthetic checks passed: missing fields, invalid values, duplicate keys, incomplete coverage, mixed archive membership, checksum changes, raw-file collisions and separation of outputs across runs.
- All cells executed in fresh kernels for two cases: no local inputs and small synthetic national/state archives, with downloads disabled. Missing inputs remained **not audited**; incomplete synthetic datasets required review.

These checks establish code behaviour only. They do not validate the SSA datasets or demonstrate performance on the full releases.

## Scope remaining within Phase 1

After reviewing real audit results, agree and implement any necessary preparation, define share denominators and missing/suppression rules, and validate the Census lookup before regional comparisons. Produce reproducible prepared data and verify a fresh-session run. Acquisition and an audit alone do not complete every Phase 1 criterion.
