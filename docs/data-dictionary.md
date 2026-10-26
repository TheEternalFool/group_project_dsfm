# Data dictionary

Variables are grouped by origin. **Original** variables come straight from
the SSA files. **External** variables are merged from another source.
**Engineered** variables are computed from the original ones: they make the
research questions answerable but do not add independent information.

## Original variables (SSA)

| Variable | Table | Type | Description |
|---|---|---|---|
| `name` | national, state | text | First name as recorded: letters A–Z only, capitalised, 2–15 characters (verified in the state file). Spelling variants are distinct names. |
| `sex` | national, state | categorical (F, M) | Sex recorded on the Social Security card application. Binary; not gender identity. |
| `year` | national, state | temporal (integer year) | Year of birth. In the national file it comes from the file name `yobYYYY.txt`. |
| `state` | state | categorical (51 levels) | USPS code of the state of birth (50 states + DC). |
| `count` | national, state | numerical (integer ≥ 5) | Number of births with that name, sex and year (and state). Names with fewer than 5 occurrences are suppressed. |

Unit of observation: one name × sex × year (national) or name × sex × year ×
state (state). Verified dimensions of the state table are in
[data-audit.md](data-audit.md). The national table has not yet been audited
(see the audit for the reason).

## External variables (US Census Bureau)

| Variable | Type | Description |
|---|---|---|
| `region` | categorical (4) | Census region of `state`: Northeast, Midwest, South, West. |
| `division` | categorical (9) | Census division of `state`. |
| `state_name` | text | Full state name (for labels). |

Source and transcription notes: [../data/external/README.md](../data/external/README.md).
These are deterministic groupings of `state`.

## Engineered variables

| Variable | Level | Type | Definition | Code |
|---|---|---|---|---|
| `share` | row | numerical | `count` / published births of the same year and sex (and state) | `preprocessing.add_popularity` |
| `per_million` | row | numerical | `share` × 10⁶ | `preprocessing.add_popularity` |
| `rank` | row | ordinal | Popularity rank within year and sex (and state); 1 = most common, ties share the lowest rank | `preprocessing.add_popularity` |
| `decade` | row | temporal | `year` rounded down to the decade | `preprocessing.add_decade` |
| `count_f`, `count_m`, `total` | name × year (× state) | numerical | Female, male and combined counts; 0 means "fewer than 5 recorded" | `preprocessing.female_share` |
| `female_share` | name × year (× state) | numerical in [0, 1] | `count_f` / `total` | `preprocessing.female_share` |
| `length`, `n_vowels` | name | numerical | Letters and vowels (a, e, i, o, u, y) in the name | `features.name_text_features` |
| `first_letter`, `last_letter`, `ends_in_vowel` | name | categorical / boolean | Orthographic features | `features.name_text_features` |
| character n-grams | name | text → sparse numerical | TF-IDF of 1–3 letter sequences with boundary markers `^`, `$` | `features.char_ngram_vectorizer` |
| `first_year`, `last_year`, `years_in_use` | name × sex | temporal / numerical | Span of the trajectory | `features.trajectory_features` |
| `peak_year`, `peak_share` | name × sex | temporal / numerical | Year and value of maximum `share` | `features.trajectory_features` |
| `mean_year` | name × sex | numerical | Birth-weighted mean year of birth | `features.trajectory_features` |
| `entropy`, `effective_names`, `hhi`, `top10_share` | group (e.g. state × year × sex) | numerical | Diversity of the name distribution | `features.diversity_by` |
| JS distance | state × decade | numerical in [0, 1] | Jensen–Shannon distance to the national distribution | `features.jensen_shannon` |
| cluster label | name × sex | categorical | Trajectory cluster (RQ1, RQ3), to be added | — |

## Data types covered

| Type | Variables |
|---|---|
| Numerical | `count`, `share`, `per_million`, `female_share`, `length`, diversity indices, distances |
| Categorical | `sex`, `state`, `region`, `division`, `first_letter`, cluster labels |
| Temporal | `year`, `decade`, `peak_year`, `mean_year` |
| Text | `name` and its character n-grams |

## Number of variables

The SSA files have **4 (national) or 5 (state) original variables**, below the
8–12 suggested on Moodle. We do not think adding derived columns fixes this:
`share`, `rank` or `female_share` are functions of the original variables, and
Census region/division are functions of `state`. Our position for the report:

- The dataset is *long* rather than *wide*: millions of rows spanning 146 years
  and 51 states, and the `name` variable is rich text that supports n-gram
  features. The analytical richness comes from these dimensions.
- The engineered variables are listed separately and described as derived.
- Genuinely external variables are added only if they serve a research
  question (see *Open decisions* in [research-plan.md](research-plan.md)). The
  most defensible candidate is CDC/NCHS annual births, which would let us
  estimate SSA coverage by year; this is not yet implemented.

## Missing values and coverage

- No missing cells in the state table (verified, see the audit). Missing
  *rows* arise from suppression below 5 occurrences.
- National file starts in 1880, state file in 1910 (state verified 1910–2025
  with no missing years).
- Early birth cohorts are under-represented because Social Security numbers
  were assigned from the late 1930s, often in adulthood.
