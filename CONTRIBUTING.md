# Contributing

A short guide for the four of us. Everything lives on one branch, `main`.

## 1. First-time setup

```bash
git clone git@github.com:TheEternalFool/group_project_dsfm.git
cd group_project_dsfm
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
python scripts/download_data.py && python scripts/build_dataset.py
```

See the README for the HTTP 403 workaround if SSA blocks the download.

## 2. Daily workflow (single `main` branch)

```bash
git pull --rebase                 # always start from the latest main
# ... work ...
pytest && ruff check .            # must pass before pushing
git add <files>
git commit -m "Add female-share trajectory plot"
git pull --rebase                 # pick up teammates' commits again
git push
```

- Pull before you start and again just before you push.
- Commit small, coherent steps with a message in the imperative
  (`Fix rank ties in add_popularity`). Push often so others see your work.
- GitHub Actions runs the tests on every push to `main`; if the badge turns
  red, fix it before doing anything else.

## 3. Who works where

To keep conflicts rare, each person owns separate files:

| Area | Files |
|---|---|
| Data pipeline | `src/names_project/data.py`, `preprocessing.py`, `scripts/`, `docs/data-*.md` |
| RQ1 Time | `notebooks/01_time.ipynb`, `report/sections/_rq1_time.qmd` |
| RQ2 Place | `notebooks/02_place.ipynb`, `report/sections/_rq2_place.qmd` |
| RQ3 Recorded sex | `notebooks/03_sex.ipynb`, `report/sections/_rq3_sex.qmd` |
| Report | `report/report.qmd`, `_introduction.qmd`, `_data.qmd`, `_eda.qmd`, `_conclusion.qmd` |

Shared modules (`features.py`, `modelling.py`, `visualisation.py`): add new
functions rather than changing existing ones, and tell the group when you
change a function someone else uses.

## 4. What never goes in a commit

- Data files (`data/raw/`, `data/processed/` are ignored by git).
- Rendered HTML and notebook outputs with large images. Clear notebook outputs
  before committing (Jupyter: *Edit → Clear All Outputs*).

## 5. Reviewing each other's work

There are no pull requests, so review happens after the push: skim the new
commits on GitHub (*Commits* tab) for your area's neighbours, and check the
statistics (normalisation, leakage, baselines, uncertainty) and wording
against AGENTS.md. Raise problems in the group chat or as a GitHub issue.

## 6. Resolving conflicts

If `git pull --rebase` reports a conflict:

1. Open each listed file and keep the correct parts between `<<<<<<<`,
   `=======` and `>>>>>>>`; delete the markers.
2. `git add <file>` then `git rebase --continue`.
3. Run `pytest`, then `git push`.

Stuck? `git rebase --abort` returns you to where you were. Conflicts in
`.ipynb` files are painful: avoid two people editing the same notebook, and
move reusable code into `src/names_project/` early.

## 7. Where code goes

| Kind of work | Location |
|---|---|
| Exploration, quick plots | `notebooks/0X_*.ipynb` |
| Anything the report depends on | `src/names_project/` with a test in `tests/` |
| Pipeline steps run from the command line | `scripts/` |
| Figures used in the report | saved with `visualisation.save_figure` into `report/figures/` |
