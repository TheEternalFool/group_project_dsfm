# Data dictionary

The study uses the [SSA national](https://www.ssa.gov/oact/babynames/names.zip)
and [state](https://www.ssa.gov/oact/babynames/state/namesbystate.zip) datasets.
Rows are published aggregate counts from Social Security applications, not
individual children or a complete census of births.

## Source fields and observation units

National files contain `name, sex, count`, with `year` derived from
`yobYYYY.txt`. State files contain `state, sex, year, name, count`.
The unique keys are `(year, sex, name)` nationally and
`(state, year, sex, name)` by state.

| Field | Type | Meaning |
|---|---|---|
| `name` | Text | Published spelling; variants remain distinct. |
| `sex` | Category | Recorded `F` or `M`; not an inferred gender identity. |
| `year` | Integer / temporal | Birth year: 1880–2025 nationally, 1910–2025 by state. |
| `count` | Integer | Published frequency for the complete key; at least five. |
| `state` | Category | State of birth, including DC; state table only. |

## Prepared fields

The [preparation notebook](../notebooks/01_state_preparation.ipynb) retains all
source rows and values and adds four fields. National groups are `sex–year`;
state groups are `state–sex–year`.

| Field | Definition |
|---|---|
| `decade` | Birth year rounded down to the decade; the 2020s are incomplete. |
| `name_length` | Number of characters in the published spelling. |
| `published_share` | Count divided by the sum of published counts in the group. |
| `rank` | Descending count within the group, with alphabetical tie-breaking. |

The national table has eight columns and the state table nine. These derived
fields serve the analysis; they are not independent source information.

## Analysis measures

The [EDA notebook](../notebooks/02_state_eda.ipynb) uses both prepared tables.

| Measure | Definition |
|---|---|
| Top-ten concentration | Sum of the ten largest counts divided by the state–sex–year published total. |
| Relative popularity | National published share divided by the name–sex series' observed peak share. |
| Years near peak | Number of observed years at or above half the peak share; periods need not be consecutive. |
| Final-letter share | Published counts for a selected final letter divided by the national sex–year total. |
| State divergence | Jensen–Shannon divergence from pooled other states, conditional on names published in both; compared with a simulated publication-threshold benchmark. |
| Name over-representation | A name's state share divided by its pooled other-state share, within sex, over 2016–2025. |
| Female share | `F / (F + M)`; absent annual counts carry 0–4 bounds under the publication-threshold assumption. |

Name–sex shifts compare a name's first complete decade with at least 1,000
published counts, no later than the 1990s, with 2016–2025 (also at least
1,000). Classification requires the full female-share interval to move
from below 30% to above 70%, or the reverse. This is a selected common-name
cohort, not all names. The report and notebook specify each analysis filter.

## Preparation and outputs

The preparation notebook displays missing values, duplicate keys, recorded-sex
categories, count ranges and observed coverage. The data contain 292 national
sex–year groups and 11,832 state–sex–year groups. The 655 national and 1,811
state placeholder-like records are retained because their labels alone do
not establish errors.

Prepared tables are saved as `data/processed/national_names.csv.gz` and
`data/processed/state_names.csv.gz`.
The report's `tables/national_state_coverage.csv` compares published totals
for the 232 shared sex–year groups. Its ratio is not population coverage.

## Interpretation and source limits

- An absent name record may be suppressed or unrecorded. A 0–4 interval models
  the publication threshold; it does not recover records missing for other reasons.
- Shares use published counts, not all births. National and state tables overlap,
  so their counts must not be added together.
- Early coverage is incomplete. Published spellings may contain recording errors;
  SSA removes spaces and hyphens. Preserve the source spelling.
- The supplied national README describes records as of 1 March 2026. Original
  archive provenance and alignment of the national/state releases remain
  unconfirmed.

See the [SSA publication limits](https://www.ssa.gov/oact/babynames/limits.html)
and [data qualifications](https://www.ssa.gov/oact/babynames/background.html).
