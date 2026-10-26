# What's in a Name?

**Time, Place and Sex in American First Names, 1880–2025**

Data Science Methods for Management · University of Lausanne · Group AJ

How do American first names vary with the time, place and recorded sex of birth,
and how have these patterns evolved since 1880?

The three research dimensions are **time**, **place** and **recorded sex**.
1880–2025 is the intended study period; the coverage of the downloaded files
must be checked before reporting results.

## Current stage

**Phase 1: data acquisition and preparation, 20 October–2 November 2026.**
We are preparing to inspect the SSA datasets, understand their variables and
observation units, and document data-quality and preparation decisions.
The group will choose and carry out each analysis as the course progresses.

## Repository layout

```text
group_project_dsfm/
├── data/
│   ├── raw/
│   │   ├── state/             Original SSA state files (local only)
│   │   └── national/          Original SSA national files (not acquired yet)
│   ├── processed/             Prepared datasets (empty until preparation)
│   └── README.md              Sources, provenance and data-handling rules
├── notebooks/
│   ├── 00_setup.ipynb          Environment and project-path check
│   └── README.md              Notebook naming and working conventions
├── src/
│   └── README.md              Space for reusable Python functions
├── docs/
│   ├── project_proposal.pdf   Original group proposal
│   ├── archive/               Preserved initial PyCharm example
│   └── README.md              Project documentation guide
├── reports/
│   ├── figures/               Selected figures, once produced
│   └── README.md              Report sources and outputs, once produced
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

The 51 existing state files are now in `data/raw/state/`, with their contents
unchanged. Keep source data in `data/raw/` and write future prepared datasets to
`data/processed/`. These data files stay local; only their folder structure and
documentation are shared through Git.

Use notebooks to explain and explore, `src/` for functions reused across
notebooks, `docs/` for project documents and preparation decisions, and
`reports/` for outputs actually produced. Empty folders reserve these locations;
they do not imply that data have been acquired or analyses completed.

## Set up Python

Use **Python 3.12** as the shared reference version. Run these commands from the
repository root. Each group member creates their own `.venv`; it is not shared
through Git.

macOS / Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The two direct dependencies are **pandas** for tabular data and **JupyterLab** for
notebooks. Their versions are specified in `requirements.txt`; indirect
dependencies are resolved by pip. This is a starting environment, not a complete
lock of every dependency.

## Start working

On macOS / Linux, with the environment activated:

```bash
python -m jupyterlab
```

On Windows:

```powershell
.\.venv\Scripts\python.exe -m jupyterlab
```

Open `notebooks/00_setup.ipynb` and run its cells to check your interpreter and
paths. It does not load or analyse the datasets. In PyCharm, select this
repository's `.venv` as the project interpreter.

See [the notebook guide](notebooks/README.md) for naming, paths and working
conventions. Start a notebook for the task agreed by the group.

## Work together with Git

The shared branch on GitHub is `main`. For a new task, start from an up-to-date
`main` with a clean working tree and create a short, descriptive branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c yourname/data-inspection
```

Review `git status` and `git diff`, then add the specific files you intend to
share and make a small commit. Push your task branch and have another group
member review it before merging. Do not force-push or commit `.venv`, downloaded
datasets or personal editor settings.

See [data/README.md](data/README.md) for the official SSA sources and the status
of the local files.
