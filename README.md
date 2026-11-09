# What's in a Name?

**Time, Place and Sex in American First Names, 1880–2025**

Data Science Methods for Management · University of Lausanne · Group AJ

## Purpose and motivation

First names offer an accessible way to study demographic patterns: some endure across generations, others become brief fashions, and preferences differ across places and recorded sex categories. Understanding these associations also helps assess the limits of using names as demographic proxies in research, surveys or customer databases.

Using public US Social Security Administration (SSA) data, we will describe these patterns and investigate them through visualisation and selected statistical methods, following our [submitted proposal](docs/project_proposal.pdf).

> **Main question:** How do American first names vary with the time, place and recorded sex of birth, and how have these patterns evolved since 1880?

The intended coverage is **1880–2025 nationally** and **1910–2025 by state**, subject to checking the downloaded releases. Our narrative follows **time → place → recorded sex**.

## Research questions and planned methods

| Dimension | Question | Approach |
|---|---|---|
| **RQ1 · Time** | Do names follow identifiable popularity life cycles, and does spelling reveal when they were popular? | Explore and later cluster normalised popularity trajectories. Regress count-weighted mean birth year on character n-grams (short letter sequences), evaluating on names unseen during training. |
| **RQ2 · Place** | Do states have distinctive naming profiles, and have they converged towards a national pattern since 1910? | Explore state profiles and diversity. Later use TF-IDF on state–decade documents to identify distinctive names, and compare distributions with the national profile over matching periods and sex categories. |
| **RQ3 · Recorded sex** | Are changes in name–sex associations asymmetric or largely stable, and can spelling help anticipate later shifts? | Explore and later cluster female-share trajectories. Define a shift and test a classifier trained on earlier information against subsequent years. |

These are planned analyses. We will justify assumptions, compare meaningful baselines and check sensitivity to analytical choices. Predictive preprocessing will use training data only. The contrasting studies of androgynous names cited in the proposal motivate RQ3; they do not predetermine our conclusions.

## Data and variables

- **[SSA national archive](https://www.ssa.gov/oact/babynames/names.zip):** one file per year; each observation is a **name × recorded sex × birth year** count. The year comes from the filename.
- **[SSA state archive](https://www.ssa.gov/oact/babynames/state/namesbystate.zip):** one file per state, including DC; each observation adds **state** to the national observation unit.
- **[Census regions and divisions](https://www.census.gov/programs-surveys/economic-census/guidance-geographies/levels.html):** a planned state-level lookup for regional comparisons, with its source and merge to be validated.

We will download and extract the official ZIP archives, preserve their READMEs, and read the comma-separated files with explicit column names and types in pandas. No scraping or API is needed. Source URLs, access dates and checksums will identify each release.

The fields cover **text** (`name`), **categorical** (`sex`, `state`), **temporal** (`year`, stored as an integer) and **numerical** (`count`) variables. National data have four analytical fields including the filename-derived year; state data have five. See the [data dictionary](docs/data_dictionary.md). Derived shares, ranks, female shares, decades and spelling features will serve specific research questions, rather than simply increase the number of columns.

SSA counts originate from Social Security card applications, not a complete census of births. Every proportion will state its denominator: a share of published SSA counts is not automatically a share of all births. See the [publication limits](https://www.ssa.gov/oact/babynames/limits.html), [data qualifications](https://www.ssa.gov/oact/babynames/background.html) and [project data guide](data/README.md).

## Workflow and deliverables

This is the timetable in the submitted proposal; scheduled dates do not establish completion.

| Stage | Dates, 2026 | Expected output |
|---|---|---|
| **1. Acquire and prepare** | 20 Oct–2 Nov | Verified sources, data dictionary, quality audit and reproducible prepared data |
| **2. Explore** | 3–15 Nov | Descriptive statistics, focused figures and preliminary interpretations |
| **Project update** | **16 Nov** | `update_AJ.html` (preferably Quarto), or PDF with separate code; preparation, initial analysis and preliminary findings |
| **3. Analyse and model** | 17 Nov–5 Dec | Justified methods, validation and robustness checks |
| **4. Interpret and write** | 6–14 Dec | Integrated findings, discussion and limitations |
| **5. Review and present** | 15–20 Dec | Reproducibility checks, slides and a video of at most ten minutes |
| **Final submission** | **21 Dec** | `final_AJ.qmd` and `final_AJ.html` with code hidden but available; slides and a public Google Drive video link |

The project contributes **70% of the total course grade**: proposal 10%, update 10%, video 25%, final report 25%. See the [course requirements](docs/project_requirements.md) for submission formats, dataset recommendations and grading details.

The proposed roles are one lead for preparation/report integration and one for each research dimension, with joint review of methods and conclusions. The group will agree individual assignments.

## Current status and Phase 1 completion

**Checked on 9 November 2026:** the acquisition-and-audit notebook, expected-schema dictionary and course requirements are available. The setup record documents 51 local state files, but automated SSA downloads returned HTTP 403 and the local data were inaccessible to this session. **No real-data audit has been completed.** Start with [notebook 01](notebooks/01_data_acquisition_and_audit.ipynb) and read the [audit status](docs/data_audit.md); the checklist below remains open.

Before EDA on the relevant dataset, complete and document:

- [ ] **Provenance and coverage:** national/state releases, source URLs, access dates, checksums, file inventory, actual years, geographical coverage and row counts.
- [ ] **Data dictionary and audit:** observation units, types and unique keys; checks for missing values, duplicate keys, invalid codes, implausible years/counts and unusual entries, with justified treatment.
- [ ] **Interpretation rules:** spelling distinctions, suppression versus true zeros, popularity denominators, rank ties and minimum-count rules. A missing opposite-sex record must not automatically yield a female share of 0 or 1. State counts need not sum to national counts.
- [ ] **Reproducible preparation:** a notebook or script that preserves raw files, applies documented transformations, saves outputs and basic EDA measures to `data/processed/`, records before/after checks and reruns from a clean session using relative paths.
- [ ] **Regional lookup:** a sourced Census mapping and a validated many-to-one join, including DC, without unmatched states or duplicated observations. This is required for regional comparisons, not for exploring national trends.

These are completion criteria, not recorded achievements. Once the relevant inputs pass them, move to focused EDA. TF-IDF, clustering and modelling-specific features belong to the later analysis stage.

## Report format and interpretation

We will adapt the supplied [course template](https://github.com/Elwin-Freudiger/project-template): **Abstract → Introduction → Data → EDA → Methods, where applicable → Findings and discussion → Conclusion → References**, with supporting appendices. Each figure and analysis should answer a question, explain its interpretation and cite its sources.

Our `reports/` folder corresponds to the template's `report/`. Its `report.qmd`, `sections/` and `references.bib` will be adapted there when assembling the report; those files are not present yet. The template permits `venv`; Quarto will be needed for rendering, and TinyTeX only for PDF output.

Interpretation will address rare-name suppression, incomplete early historical coverage, binary recorded-sex categories, possible recording errors and spelling variants treated as separate names. Findings concern aggregate associations, with no causal claims about parental choices or inference about an individual's identity.

## Repository and getting started

```text
data/raw/state/       Original SSA state files, kept local
data/raw/national/    Original SSA national files, kept local
data/processed/       Reproducibly prepared datasets, kept local
notebooks/            Step-by-step analysis and explanations
src/                  Reusable Python functions
docs/                 Proposal and methodological documentation
reports/figures/      Selected figures for the report
requirements.txt      Current Python dependencies
```

Use **Python 3.12**, from the repository root:

**macOS / Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Open `notebooks/00_setup.ipynb` to check the environment and paths, then `notebooks/01_data_acquisition_and_audit.ipynb` for the first Phase 1 task. A fresh clone has no datasets: see the [data guide](data/README.md). Current direct dependencies are pandas and JupyterLab; add visualisation/modelling libraries when needed. Direct versions are pinned, but this is not a full environment lock.

Work on short task branches from up-to-date `main`, agree notebook ownership, and review small commits together before merging. Keep raw data unchanged and exclude datasets, `.venv` and personal settings from commits. Restart and run notebooks in order before sharing; see the [notebook guide](notebooks/README.md).
