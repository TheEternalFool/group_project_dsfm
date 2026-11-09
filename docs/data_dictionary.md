# SSA data dictionary — Phase 1

This dictionary describes the expected SSA schemas. It is not evidence that the group's files have passed validation. Source documentation: [publication limits](https://www.ssa.gov/oact/babynames/limits.html) and [data qualifications](https://www.ssa.gov/oact/babynames/background.html), consulted on 9 November 2026. Preserve the README supplied in each archive as the release-specific reference.

## Observation units and keys

- **National:** one published count for a `(year, sex, name)` combination. Each `yobYYYY.txt` file supplies `name, sex, count`; extract `year` from its filename.
- **State:** one published count for a `(state, year, sex, name)` combination. Each state text file supplies `state, sex, year, name, count`.

Rows are aggregate groups, not individual children. National and state data are two levels of aggregation; do not concatenate them as independent observations or add their counts together. The state coverage includes DC; national data exclude US territories.

| Field | Variable type | Intended representation after validation | Meaning and checks |
|---|---|---|---|
| `name` | Text | String | Published first-name spelling. Preserve strings and spelling variants; explicitly detect empty/whitespace values. Disable pandas' default missing-value string conversion when loading. |
| `sex` | Categorical | String/category | SSA's recorded `F` or `M` category. It is not a verified statement of a person's gender identity. Flag other values. |
| `year` | Temporal | Integer year | Birth cohort, not application or download year. National: filename-derived; state: explicit field. Check observed coverage against the intended period. Do not invent month/day values. |
| `count` | Numerical, discrete | Integer | Published count for the complete group key, drawn from Social Security applications. Investigate missing/noninteger values and values below the publication threshold of five. |
| `state` | Categorical | String/category | State of birth or DC; state data only. Validate allowed codes and consistency with the filename. |

There are **four analytical fields nationally** and **five by state**. Dictionary metadata, file paths and checksums are provenance, not extra substantive variables for the course column recommendation.

SSA removes hyphens and spaces before publication. Spelling and length features therefore describe the published name string, which may differ from the spelling on the original application. Keep distinct published spellings separate.

## Missingness and interpretation

An empty cell in a published row is different from an absent name–sex–year combination. An absent combination may be suppressed or unrecorded; do not automatically replace it with zero. Zero missing cells in the files does not establish complete population coverage. Early cohorts are incompletely represented, and spelling/recording limitations remain even when structural checks pass.

A state sum can be smaller than the national count because publication suppression operates at different geographical levels. Archive and per-file checksums identify the inspected snapshot; they do not prove it is the latest release.

## Candidate derived variables — not yet implemented

| Candidate | Purpose | Decision needed before calculation |
|---|---|---|
| Published popularity share | Compare name popularity across differently sized cohorts/places | Specify the year/sex/geography denominator and label it as a share of published counts, not all births. |
| Popularity rank | Compare relative positions | Define grouping and tie handling. |
| Female share | Track recorded-sex association for a name/cohort | Define how suppressed or absent components are handled; do not assume a missing component is zero. |
| Name length / character features | Investigate spelling and popularity period | Preserve the published spelling; learn any model vocabulary from training data only. |
| Decade | Group cohorts for later comparisons | Define decade boundaries and partial decades. |
| Census region and division | Regional comparisons | Source the lookup and validate a many-to-one join including DC. |

These enrich the analysis only when relevant. Derived columns are not independent new information, and the course's recommended number of variables does not justify arbitrary padding.
