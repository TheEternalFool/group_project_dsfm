# Contributing

A short guide for the four of us. When in doubt, open a pull request early
and ask in its comments.

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

## 2. Branches

`main` always holds reviewed work. Never commit to it directly.

| Branch | Owner area |
|---|---|
| `feature/data-pipeline` | download, cleaning, data dictionary, audit |
| `feature/rq1-time` | RQ1 notebook, features and report section |
| `feature/rq2-place` | RQ2 notebook, features and report section |
| `feature/rq3-sex` | RQ3 notebook, features and report section |
| `feature/quarto-report` | report skeleton, introduction, conclusion, styling |

For smaller pieces use `feature/<area>-<short-description>` or
`fix/<short-description>`.

```bash
git switch main && git pull
git switch -c feature/rq1-time       # or: git switch feature/rq1-time
```

## 3. Commits

- Commit small, coherent steps with a message in the imperative:
  `Add female-share trajectory plot`, `Fix rank ties in add_popularity`.
- Never commit data files, rendered HTML or notebook outputs with large
  embedded images. Clear notebook outputs before committing
  (Jupyter: *Edit → Clear All Outputs*).
- Run `pytest` and `ruff check .` before pushing.

## 4. Pull requests

```bash
git push -u origin feature/rq1-time
```

Then open a PR into `main` on GitHub. Fill in the template: what changed,
how it was checked, and any methodological decision reviewers should look at.
Keep PRs focused; several small PRs are easier to review than one big one.

## 5. Reviews

- Every PR needs **one approving review from another student** before merging.
- Reviewers check: does the code run and the CI pass; are the statistics
  sound (normalisation, leakage, baselines, uncertainty); does the text claim
  only what the evidence supports (see AGENTS.md).
- Use *Squash and merge* to keep `main` readable, then delete the branch.

## 6. Keeping up to date and resolving conflicts

```bash
git switch main && git pull
git switch feature/rq1-time
git merge main                 # bring your branch up to date
```

If Git reports a conflict, open each listed file, keep the correct parts
between `<<<<<<<`, `=======` and `>>>>>>>`, delete the markers, then:

```bash
git add <file>
git commit                     # completes the merge
pytest                         # make sure nothing broke
git push
```

Conflicts in `.ipynb` files are painful; avoid two people editing the same
notebook, and move reusable code into `src/names_project/` early. Each
report section lives in its own file under `report/sections/` for the same
reason.

## 7. Where code goes

| Kind of work | Location |
|---|---|
| Exploration, quick plots | `notebooks/0X_*.ipynb` |
| Anything the report depends on | `src/names_project/` with a test in `tests/` |
| Pipeline steps run from the command line | `scripts/` |
| Figures used in the report | saved with `visualisation.save_figure` into `report/figures/` |
