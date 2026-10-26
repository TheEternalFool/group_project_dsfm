# AGENTS.md

Durable conventions for anyone, human or AI assistant, working in this
repository. Read this before changing code, data handling or report text.

## Project scope

- **Title:** What's in a Name? Time, Place and Sex in American First Names, 1880–2025.
- **Main question:** How have American first-name patterns evolved across time,
  geography and recorded sex categories, and what demographic information can
  names reliably convey?
- **RQ1 Time**, **RQ2 Place**, **RQ3 Recorded sex**: see README. Every analysis
  must say how it contributes to the main question.
- The scope is the **United States** only. Do not add Switzerland,
  immigration or ethnicity analyses unless the team changes the scope in
  `docs/research-plan.md`.
- Narrative order: Time → Place → Recorded sex → What can names reliably reveal?

## Data rules

- Sources: SSA national (1880–) and state (1910–) files, plus the committed
  Census region table. Never invent data, observations, results or conclusions.
  If something cannot be verified, say so explicitly.
- Never commit raw or processed data (`data/raw/`, `data/processed/` are
  git-ignored). Only small, documented reference tables go in `data/external/`.
- SSA suppresses any name with fewer than **5** occurrences in a year (or
  state-year). Missing rows mean "fewer than 5", not zero. Diversity, rare-name
  and female-share statistics are biased by this; state with the threshold and
  test sensitivity.
- Normalise popularity by the published births of the same year and sex (and
  state): use `share` / `per_million`, not raw counts, for comparisons over time.
- Early cohorts (born before the late 1930s) are under-covered because Social Security
  numbers were assigned later in life. Treat comparisons involving those cohorts with care.
- Spelling variants (Caitlin, Kaitlyn) are distinct names in the data. Any
  grouping of variants must be documented and justified.
- Distinguish **original** variables (name, sex, year, state, count) from
  **engineered** ones; derived columns do not add independent information.
- Read files with `keep_default_na=False` so that names like "Na" or "Nan" are
  not parsed as missing.

## Recorded sex

- `sex` is the binary category recorded on SSA applications. It is **not**
  gender identity. Write "recorded female/male" or "SSA-recorded sex".
- Results are population-level associations. Never present a name as
  evidence of an individual's sex, gender, age, location or background.

## Modelling rules

- Use `names_project.RANDOM_STATE` (42) for every stochastic step.
- Unseen-name generalisation: split by complete name
  (`modelling.split_by_name`). Fit vectorisers and scalers on training data only.
- Temporal prediction: train on years ≤ cut-off only (`modelling.temporal_split`);
  features must not use information after the cut-off.
- Always compare against a meaningful baseline (mean / majority / previous-value)
  and report test-set metrics with uncertainty (`modelling.bootstrap_ci`), effect
  sizes and practical significance. Training accuracy alone is never evidence.
- Prefer simple, interpretable models. Do not add complexity to impress.

## Code conventions

- Python 3.11+, pandas, NumPy, SciPy, scikit-learn, matplotlib (seaborn optional).
- Reusable logic goes in `src/names_project/` with type hints, a docstring
  and a test on a small synthetic fixture in `tests/`. Notebooks are for
  exploration and must not be the only place a reported number is computed.
- Pipeline entry points live in `scripts/`.
- Figures: call `visualisation.set_style()`; use `SEX_COLOURS` for sex;
  label axes with units; save report figures with `visualisation.save_figure`.
- Before pushing: `pytest` and `ruff check .` must pass.

## Collaboration

- Work on a feature branch and open a pull request into `main`
  (see CONTRIBUTING.md). Never push directly to `main`.
- Never delete or overwrite a teammate's work without examining it first.
- Do not change repository visibility, permissions, branch protection or
  collaborators without the team's explicit approval.

## Report writing

Each analytical section answers: What question? Why interesting? Which
variables and methods, and why? What does the evidence show? What can and
cannot be concluded? How does it contribute to the main question?
Interpretation matters more than the number of plots.
