# What's in a Name?

**Time, Place and Recorded Sex in American First Names**

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

Initial descriptive exploration is complete for the local state snapshot; clustering, TF-IDF and predictive models remain planned. We will justify assumptions, compare meaningful baselines and check sensitivity to analytical choices. Predictive preprocessing will use training data only. The contrasting studies of androgynous names cited in the proposal motivate RQ3; they do not predetermine our conclusions.

## Data and variables

- **[SSA national archive](https://www.ssa.gov/oact/babynames/names.zip):** one file per year; each observation is a **name × recorded sex × birth year** count. The year comes from the filename.
- **[SSA state archive](https://www.ssa.gov/oact/babynames/state/namesbystate.zip):** one file per state, including DC; each observation adds **state** to the national observation unit.
- **[Census regions and divisions](https://www.census.gov/programs-surveys/economic-census/guidance-geographies/levels.html):** a planned state-level lookup for regional comparisons, with its source and merge to be validated.

The local state files have been read with explicit column names and types in pandas and checked against their inventory hashes. Their original download date and exact official release remain unresolved. National data and the archive READMEs still need to be acquired and documented with source URLs, access dates and checksums.

The fields cover **text** (`name`), **categorical** (`sex`, `state`), **temporal** (`year`, stored as an integer) and **numerical** (`count`) variables. National data have four analytical fields including the filename-derived year; state data have five. See the [data dictionary](docs/data_dictionary.md). Derived shares, ranks, female shares, decades and spelling features will serve specific research questions, rather than simply increase the number of columns.

SSA counts originate from Social Security card applications, not a complete census of births. Every proportion will state its denominator: a share of published SSA counts is not automatically a share of all births. See the [publication limits](https://www.ssa.gov/oact/babynames/limits.html), [data qualifications](https://www.ssa.gov/oact/babynames/background.html) and [project data guide](data/README.md).

## Workflow and deliverables

This is the timetable in the submitted proposal; scheduled dates do not establish completion.

The [course requirements](docs/course_requirements.md) separately record the
official milestones, grading and submission rules supplied by the group. The
project is **70% of the total course grade**: proposal 10%, update 10%, video
25% and final report 25%. Stages 1–5 below are our internal work plan.

| Stage | Dates, 2026 | Expected output |
|---|---|---|
| **1. Acquire and prepare** | 20 Oct–2 Nov | Verified sources, data dictionary, quality audit and reproducible prepared data |
| **2. Explore** | 3–15 Nov | Descriptive statistics, focused figures and preliminary interpretations |
| **Project update** | **16 Nov** | `update_AJ.html` (preferably Quarto), or PDF with separate code; preparation, initial analysis and preliminary findings |
| **3. Analyse and model** | 17 Nov–5 Dec | Justified methods, validation and robustness checks |
| **4. Interpret and write** | 6–14 Dec | Integrated findings, discussion and limitations |
| **5. Review and present** | 15–20 Dec | Reproducibility checks, slides and a video of at most ten minutes |
| **Final submission** | **21 Dec** | `final_AJ.qmd` and `final_AJ.html` with code hidden but available; slides and a public Google Drive video link |

See also the [short requirements summary](docs/project_requirements.md) for submission formats, dataset recommendations and grading details.

The proposed roles are one lead for preparation/report integration and one for each research dimension, with joint review of methods and conclusions. The group will agree individual assignments.

## Current status and Phase 1 completion

**Verified locally on 14 November 2026:** the [setup](notebooks/00_setup.ipynb), [preparation](notebooks/01_state_preparation.ipynb) and [EDA](notebooks/02_state_eda.ipynb) notebooks executed successfully in the project's `.venv` kernel, and all seven inventory unit tests passed. Preparation retained **6,696,687 rows** from **51 files**, covering all 50 states plus DC over **1910–2025**, with **330,978,761 published counts**. All structural checks passed, including duplicate-key and coverage checks for **11,832 state–sex–year groups**. The **1,811 placeholder-like records** flagged for review were retained. Raw-file hashes were unchanged and the prepared CSV passed its export/reload comparison.

The earlier [acquisition-and-audit notebook](notebooks/01_data_acquisition_and_audit.ipynb) is retained for release identification and input checks. Its [9 November audit note](docs/data_audit.md) records that session's download and access limitations, rather than the current state-preparation results.

Prepared data and the preparation audit are in `data/processed/`; initial EDA figures, CSV tables and the [update source](reports/update_AJ.qmd) are available in `reports/`. HTML rendering and visual review are separate checks. Original acquisition provenance, national data and the regional lookup remain unresolved, so **Stage 1 is not globally complete**. This local status does not establish publication to GitHub.

- [x] **Local state coverage:** file inventory, checksums, row counts, observed years and state–sex–year group coverage verified.
- [x] **State data dictionary and audit:** types, unique keys, missing fields, invalid codes, year/count bounds and unusual entries checked with documented treatment.
- [x] **State interpretation rules:** published-count denominators, alphabetical rank tie-breaking, spelling preservation and suppression handling documented. Missing name records were not filled with zeros.
- [x] **State preparation:** all source rows retained; decade, name length, published share and rank added; saved data reloaded and compared with the prepared table.
- [ ] **Acquisition provenance:** establish the original download date and exact official release for the local state files.
- [ ] **National data:** acquire and audit the official national release before making national comparisons.
- [ ] **Regional lookup:** source a Census mapping and validate its many-to-one join, including DC, before regional comparisons.

Initial state EDA is now available. TF-IDF, clustering and predictive modelling remain for the later analysis stage.

## Report format and interpretation

The [update source](reports/update_AJ.qmd) adapts the supplied [course template](https://github.com/Elwin-Freudiger/project-template): **Abstract → Introduction → Data → EDA → Analysis → Conclusion → References**. Analysis includes the proposed methods and their rationale. Each figure and analysis should answer a question, explain its interpretation and cite its sources.

Our `reports/` folder contains the main `.qmd`, a generated preparation summary, manually maintained EDA text, figures and tables. Quarto renders the source as standalone HTML; rendering and visual review must pass before submission. TinyTeX is needed only if producing PDF.

The update requires data description, initial analysis and preliminary findings:
submit `update_<group_name>.html` on **16 November** (a PDF with separate code
is also allowed for the update). The final requires both
`final_<group_name>.qmd` and `final_<group_name>.html` on **21 December**, with
code hidden but available for reproducibility. The presentation requires
slides and a publicly accessible Google Drive link to a video of at most ten
minutes. See the [submission details](docs/course_requirements.md).

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

Open `notebooks/00_setup.ipynb` to check the environment and paths; it does not validate data. Then run the preparation and EDA notebooks in order. A fresh clone has no datasets: see the [data guide](data/README.md). Direct dependencies are pandas, JupyterLab and Matplotlib. Direct versions are pinned, but this is not a full environment lock.

The successful local runs used `.venv` with **Python 3.12.0, pandas 2.3.3 and Matplotlib 3.11.2**. On **14 November 2026**, PyCharm was configured to use the project's `.venv/bin/python`, and `00_setup.ipynb` ran successfully. When switching machines, select that machine's project `.venv` interpreter and notebook kernel.

Work on short task branches from up-to-date `main`, agree notebook ownership, and review small commits together before merging. Keep raw data unchanged and exclude datasets, `.venv` and personal settings from commits. Restart and run notebooks in order before sharing; see [state preparation](notebooks/01_state_preparation.ipynb) and [EDA](notebooks/02_state_eda.ipynb).
