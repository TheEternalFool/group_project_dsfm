# Methodology

How data become evidence, and the safeguards that keep conclusions honest.

## 1. Acquisition

`scripts/download_data.py` downloads `names.zip` and `namesbystate.zip` from
SSA and extracts them into `data/raw/names/` and `data/raw/namesbystate/`.
Files already present are kept unless `--force` is given. If SSA refuses the
request (HTTP 403, observed on 26 Oct 2026 for scripted requests), save the
zip manually under `data/raw/` and rerun the script. Record the download date
in the report, because SSA revises recent years.

## 2. Validation

`data.validate_national` / `data.validate_state` check, before anything is
written: no missing cells; `sex` ∈ {F, M}; names alphabetic only; `count` ≥ 5;
years within the documented range; no duplicate keys; valid state codes.
Files are read with `keep_default_na=False` because "Nan" and "Na" are real
names (the state file contains 649 rows for "Nan").

## 3. Preprocessing

`scripts/build_dataset.py` writes Parquet tables to `data/processed/`:

1. Compact dtypes and stable sort (`tidy_types`).
2. Popularity normalised by published births of the same year and sex (and
   state): `share`, `per_million`, `rank` (`add_popularity`).
3. `decade` (`add_decade`).
4. Female share per name and year (`female_share`, national table).
5. Census region and division merged on `state` (`add_regions`), with a check
   that every state is matched.

Trajectory analyses add a documented minimum total count (`apply_min_count`)
and report results for several thresholds.

## 4. Methods by research question

| RQ | Question | Variables | Methods | Evaluation |
|---|---|---|---|---|
| RQ1 | Popularity patterns; spelling → period | `year`, `per_million`, `name` n-grams, `mean_year` | Time series, trajectory features, clustering of shape-normalised trajectories, ridge regression on character n-grams | Split by name; MAE in years vs. predicting the training mean; bootstrap CI |
| RQ2 | State distinctiveness; convergence | `state`, `region`, `decade`, `count` | Diversity indices, TF-IDF over state-decade documents, Jensen–Shannon distance to national profile | Trends over decades with uncertainty; sensitivity to suppression (compare large vs. small states) |
| RQ3 | Sex association change; predictability | `female_share`, `year`, n-grams, trajectory features | Female-share trajectories, clustering, classifier for future shifts | Temporal hold-out; balanced accuracy / F1 / calibration vs. "no change" baseline; bootstrap CI |

## 5. Leakage rules

- **Unseen names:** `modelling.split_by_name` puts every row of a name on one
  side. Vectorisers and scalers are fitted on the training names only.
- **Future information:** `modelling.temporal_split` trains on years ≤ cut-off.
  Features for the classifier are computed from data up to the cut-off only;
  the label uses data after it.
- **Seeds:** `names_project.RANDOM_STATE = 42` for splits, models and bootstraps.

## 6. Reporting standards

- Compare every model with a simple baseline; report test metrics only.
- Give uncertainty (bootstrap intervals) and effect sizes in interpretable
  units (years, percentage points), and comment on practical significance.
- Class imbalance (most names are almost entirely one sex; few names shift)
  must be reported, with metrics robust to it.

## 7. Known limitations

| Limitation | Consequence | Mitigation |
|---|---|---|
| Suppression below 5 occurrences | Diversity understated, especially small states and recent years; 0 counts in female share mean "< 5" | State threshold; sensitivity checks; caution with small states (WY has the fewest rows) |
| Early-cohort coverage | Births before the late 1930s represented by later applicants | Flag pre-1940 results; optional later start year |
| Binary recorded sex | Cannot represent gender identity or non-binary people | Wording "SSA-recorded sex"; population-level claims only |
| Spelling variants | Same "name" split across spellings | Keep distinct by default; robustness check on grouped variants |
| Aggregate data | No information on parents or individuals | Descriptive and predictive claims only; no causal or individual-level inference |
| Data revisions | SSA revises recent years | Record download date; re-run the pipeline before final numbers |
