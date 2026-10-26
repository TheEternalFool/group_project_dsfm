# Research plan

## Main research question

**How have American first-name patterns evolved across time, geography and
recorded sex categories, and what demographic information can names reliably
convey?**

The project treats a first name as a small signal about a population: when
people with that name were born, where, and with which recorded sex. Each
sub-question measures one of those signals and, just as importantly, how
reliable it is. The final section combines them to answer what names can and
cannot tell us, at population level, and why individual-level inferences are
unsafe.

## Sub-questions and their contribution

### RQ1 Time

**What historical popularity patterns do American first names follow, and how
informative is a name's spelling about the period in which it was popular?**

- *Contribution:* measures the temporal signal in names: whether a name
  "dates" its bearers, and whether that information is carried by the letters
  themselves (so it generalises to names never seen before).
- *Data:* national file, 1880–2025 (temporal, numerical, text, categorical).
- *Methods:* time series of `per_million`; trajectory features (peak year,
  years in use, birth-weighted mean year); clustering of normalised
  trajectories (e.g. k-means on shape-normalised curves) to separate fads from
  classics; ridge regression of `mean_year` on character n-grams, evaluated on
  names held out entirely (split by name), against a mean-year baseline.

### RQ2 Place

**How distinctive are first-name distributions across US states, and have
regional naming preferences become more similar over time?**

- *Contribution:* measures the geographic signal in names and whether it is
  weakening, which bounds how much a name can say about where someone was born.
- *Data:* state file, 1910–2025, with Census region and division.
- *Methods:* diversity indices per state-year-sex (entropy, effective number of
  names, HHI, top-10 share); TF-IDF with each state-decade as a document to
  find characteristic names; Jensen–Shannon distance between each state and
  the national distribution, tracked over decades; maps by state and region.

### RQ3 Recorded sex

**How have associations between first names and SSA-recorded sex changed over
time, and how reliably can these changes be anticipated from historical naming
patterns?**

- *Contribution:* measures the sex signal in names, how stable it is, and
  whether shifts are predictable, which directly informs the reliability of
  name-based sex inference used in surveys and databases.
- *Data:* national file (female share by name and year); state file for
  regional differences.
- *Methods:* female-share trajectories; classification of whether a name's
  female share shifts by more than a threshold after a cut-off year, trained
  only on information up to the cut-off (temporal hold-out), compared with a
  "no change" baseline; calibration and bootstrap intervals; discussion of
  asymmetry (Lieberson et al., 2000) versus stability (Seguin et al., 2021).

### Synthesis: what can names reliably reveal?

Compare the strength of the three signals on a common footing (e.g. how much a
name reduces uncertainty about birth decade, state/region and recorded sex),
and state the limits: suppression, coverage of early cohorts, binary recorded
sex, spelling variants, and the gap between population association and
individual identity.

## Response to teaching-assistant feedback (proposal, 8.5/10)

| Feedback | Where it is addressed |
|---|---|
| Show numerical, categorical, temporal and text data | `docs/data-dictionary.md` (type of every variable); report Data section |
| Link methods to each objective | Sub-question sections above; `docs/methodology.md` |
| Explicit research questions with question marks, linked to the main question | This document; report introduction |
| Too few variables vs. the 8–12 recommended | `docs/data-dictionary.md`, section *Number of variables*; open decision below |
| Document acquisition and extraction | README *Reproducing the data*; `scripts/download_data.py`; `docs/data-audit.md` |

## Open decisions for the team

1. **External data.** The original data have 4 (national) or 5 (state)
   variables. Census region/division are groupings of `state` and add no
   independent information. Options that add genuinely external information:
   annual US births from CDC/NCHS (to estimate SSA coverage by year), or state
   population/urbanisation from the Census. Decide whether one of these
   answers a research question; do not add data only to reach a variable count.
2. **Minimum-count thresholds** for trajectory analyses (e.g. total ≥ 1,000
   births) and the sensitivity grid to report.
3. **Cut-off year and shift definition** for the RQ3 classifier (e.g. train to
   2000, predict change in female share of more than 0.2 by 2025).
4. **Spelling variants:** keep as distinct names (default) or group a small,
   documented set for a robustness check.
5. **Time window:** whether to start some analyses after the late 1930s to avoid
   early-cohort coverage issues.

## Timeline

| Period | Work |
|---|---|
| 20 Oct – 2 Nov | Data pipeline, audit, derived variables |
| 3 – 15 Nov | EDA and visualisation for RQ1–RQ3 |
| **16 Nov** | **Project update (Quarto HTML)** |
| 17 Nov – 5 Dec | Clustering, TF-IDF, convergence, models, robustness |
| 6 – 14 Dec | Interpretation, final figures, limitations |
| 15 – 20 Dec | Review, slides, video |
| **21 Dec** | **Final report, slides and video** |
