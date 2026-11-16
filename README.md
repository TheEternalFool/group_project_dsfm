# What's in a Name?

**Time, Place and Recorded Sex in American First Names**

Data Science Methods for Management · HEC Lausanne · Group AJ

**Group members:** Komivi Assiamua, Selorm Fiadonu, Carles González Saña,
Héctor Honrubia Gonzalez.

We study how American first names vary across time, states and recorded sex.
The research questions concern popularity life cycles, geographical differences
and changes in name–sex associations.

## Report and reference documents

- **Project update:** [HTML](reports/update_AJ.html) · [PDF](reports/update_AJ.pdf) · [Quarto source](reports/update_AJ.qmd)
- [Data dictionary](docs/data_dictionary.md): fields, preparation rules and limitations.
- [Course requirements](docs/course_requirements.md): deadlines, submission formats and marking rubric.
- [Project proposal](docs/project_proposal.pdf).

## Data and analysis

| Dataset | Period | Files | Records |
|---|---|---:|---:|
| National | 1880–2025 | 146 | 2,181,032 |
| State, including DC | 1910–2025 | 51 | 6,696,687 |

The EDA addresses all three research questions: national popularity life
cycles and spelling, state naming profiles and convergence, and changes in
name–sex associations. Clustering and predictive models are the next steps.

Raw and processed data are excluded from Git. Download the
[SSA national](https://www.ssa.gov/oact/babynames/names.zip) and
[state](https://www.ssa.gov/oact/babynames/state/namesbystate.zip) archives;
preserve their documentation and place the extracted files here:

```text
data/raw/national/names/yobYYYY.txt
data/raw/state/XX.TXT
```

National files directly under `data/raw/national/` are also supported.
Keep raw files unchanged. Missing published records are not automatically
zero, and national counts must not be added to state counts.

## Run the project

Use Python 3.12 and select the project `.venv` as the notebook kernel.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, create the environment with `py -3.12 -m venv .venv` and activate
it with `.venv\Scripts\Activate.ps1`.

Run these notebooks in order:

1. [00_setup.ipynb](notebooks/00_setup.ipynb): display the environment and paths.
2. [01_state_preparation.ipynb](notebooks/01_state_preparation.ipynb): load, inspect and prepare both datasets.
3. [02_state_eda.ipynb](notebooks/02_state_eda.ipynb): analyse all three research questions using national and state data; generate the report's seven figures and supporting tables.

Prepared CSVs go to `data/processed/`; figures and result tables go to
`reports/`. With [Quarto](https://quarto.org/) installed, render the report
from the repository root:

```bash
quarto render reports/update_AJ.qmd
```

The report narrative and EDA interpretation are maintained in
`reports/update_AJ.qmd`. Check them against notebook outputs after analysis
changes. The PDF is exported from the rendered HTML; inspect both formats
after report changes.
