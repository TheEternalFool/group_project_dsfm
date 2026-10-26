# What's in a Name?

**Time, Place and Sex in American First Names, 1880–2025**

Group AJ · Data Science Methods for Management · University of Lausanne (UNIL)

[![tests](https://github.com/TheEternalFool/group_project_dsfm/actions/workflows/tests.yml/badge.svg)](https://github.com/TheEternalFool/group_project_dsfm/actions/workflows/tests.yml)

## The question

> How have American first-name patterns evolved across time, geography and
> recorded sex categories, and what demographic information can names
> reliably convey?

| | Sub-question | Main data | Core methods |
|---|---|---|---|
| **RQ1 Time** | What historical popularity patterns do American first names follow, and how informative is a name's spelling about the period in which it was popular? | National, 1880–2025 | Normalised time series, trajectory clustering, character n-gram regression (split by name) |
| **RQ2 Place** | How distinctive are first-name distributions across US states, and have regional naming preferences become more similar over time? | State, 1910–2025 | Diversity indices, TF-IDF on state-decade documents, Jensen–Shannon distance to the national profile |
| **RQ3 Recorded sex** | How have associations between first names and SSA-recorded sex changed over time, and how reliably can these changes be anticipated from historical naming patterns? | National (and state) | Female-share trajectories, classification with a temporal hold-out, uncertainty analysis |

The story runs **Time → Place → Recorded sex → What can names reliably
reveal?** Details are in [docs/research-plan.md](docs/research-plan.md) and
[docs/methodology.md](docs/methodology.md).

## Data

All data come from the US Social Security Administration (public domain):

- National file: <https://www.ssa.gov/oact/babynames/names.zip> (1880–)
- State file: <https://www.ssa.gov/oact/babynames/state/namesbystate.zip> (1910–)
- Documentation: <https://www.ssa.gov/oact/babynames/limits.html>

plus the US Census Bureau region/division table committed in
[data/external/](data/external/). Raw and processed data are **not**
committed. Variables are described in
[docs/data-dictionary.md](docs/data-dictionary.md) and the latest audit is in
[docs/data-audit.md](docs/data-audit.md).

## Setup

Requires Python 3.11+ and, for the report, [Quarto](https://quarto.org).

```bash
git clone git@github.com:TheEternalFool/group_project_dsfm.git
cd group_project_dsfm
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # installs src/names_project in editable mode
pytest                             # should pass without any data
```

> If the repository sits in iCloud Drive, OneDrive or Dropbox, create the
> virtual environment outside the synced folder (for example
> `python3 -m venv ~/venvs/dsfm`) to avoid syncing thousands of files.

## Reproducing the data

```bash
python scripts/download_data.py              # downloads + extracts into data/raw/
python scripts/build_dataset.py              # validates, writes data/processed/*.parquet
python scripts/audit_data.py --out docs/data-audit.md
```

SSA's website sometimes answers scripted downloads with **HTTP 403**. If that
happens, open the zip URL in a browser, save it as `data/raw/names.zip` or
`data/raw/namesbystate.zip`, and run `download_data.py` again; it will extract
the file you saved.

Expected layout after these steps:

```
data/raw/names/yob1880.txt ... yob2025.txt
data/raw/namesbystate/AK.TXT ... WY.TXT
data/processed/national.parquet, national_female_share.parquet, state.parquet
```

## Rendering the report

```bash
cd report
quarto render report.qmd          # writes report/report.html
```

## Repository layout

```
.github/            CI workflow and pull-request template
data/raw/           downloaded SSA files (ignored by git)
data/processed/     Parquet tables built by scripts/build_dataset.py (ignored)
data/external/      small committed reference tables (Census regions)
docs/               research plan, data dictionary, methodology, data audit
notebooks/          exploratory notebooks, one per research question
src/names_project/  reusable, tested code (data, preprocessing, features, modelling, visualisation, audit)
scripts/            command-line entry points for the pipeline
tests/              pytest suite on small synthetic fixtures
report/             Quarto report (report.qmd + sections/, figures/, references.bib)
```

## Working together

Branches, commits, pull requests and reviews are described in
[CONTRIBUTING.md](CONTRIBUTING.md). Methodological safeguards that every
contributor (human or AI assistant) should follow are in
[AGENTS.md](AGENTS.md).

## Deadlines

| Date | Deliverable |
|---|---|
| 16 November 2026 | Project update: Quarto HTML with data description, preprocessing, initial EDA and preliminary findings |
| 21 December 2026 | Final reproducible `.qmd` + HTML report, slides, video (≤ 10 min) |

## Licence

Code under the MIT licence (see [LICENSE](LICENSE)). SSA data are public domain.
