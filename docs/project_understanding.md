# Project understanding

Notes taken on **9 November 2026** from the [project README](../README.md),
the folder guides and a read-only inspection of the local files. The README
remains the main project reference. This is an onboarding snapshot, not an
analysis result or a new set of agreed decisions.

Preparation and EDA notebooks and a report were added after this snapshot.
See the [current project status](../README.md#current-status-and-phase-1-completion)
and [report guide](../reports/README.md) for the subsequent work.

**Follow-up on 9 November:** the [state-data inventory](data_inventory/README.md)
now verifies 51 files, 6,696,687 records and observed coverage of 1910–2025.
The snapshot below describes the state before that inventory; use its linked
record for current coverage and the remaining provenance and audit gaps.

**Course-description notes added on 9 November:**
[course_requirements.md](course_requirements.md) records the supplied assignment
instructions: the project is 70% of the course grade (proposal 10%, update 10%,
video 25%, final report 25%); submission formats and filenames; the slides and
public video-link requirements; and the recommended dataset size and types.
Our five raw state-data fields fall below the recommended 8–12-variable range,
so useful enrichment and a clear suitability rationale remain part of the plan.
The November update must contain initial analysis and preliminary findings,
not just the completed inventory. Stages 1–5 are our internal proposal plan;
the course deadlines and deliverable requirements are recorded separately.

## What the project is trying to explain

**What's in a Name?** is Group AJ's Data Science Methods for Management project
at the University of Lausanne. It uses public US Social Security Administration
(SSA) first-name counts to study how naming patterns vary with **time, place
and recorded sex**, in that narrative order.

The intended coverage is 1880–2025 nationally and 1910–2025 by state. These
are target periods; the downloaded releases and actual coverage still need
verification. The broader motivation is to understand demographic associations
and the limits of using names as demographic proxies.

| Question | What I understand the planned work to be |
|---|---|
| RQ1: Time | Describe and later cluster name-popularity life cycles. Test whether spelling features predict a name's count-weighted mean birth year, evaluating on names unseen during training. |
| RQ2: Place | Compare state naming profiles, diversity and convergence towards the national profile. Later use state–decade TF-IDF to identify distinctive names, with matching periods and recorded-sex categories. |
| RQ3: Recorded sex | Describe female-share trajectories and assess stability or asymmetric shifts. Later cluster trajectories and test whether earlier spelling information helps predict subsequent shifts. |

These are research questions and proposed methods, not established findings.
The project needs justified definitions, meaningful baselines and sensitivity
checks. Predictive preprocessing must be fitted on training data only.

## Data and interpretation rules

- National observations are **name × recorded sex × year** counts; year comes
  from the filename. State observations additionally include **state**.
- Raw files stay unchanged and local. Prepared outputs belong in
  `data/processed/`; notebooks explain the work, and `src/` holds reusable code.
- Missing published records are not automatically zero. In particular, an
  absent opposite-sex record does not justify a female share of 0 or 1.
- Shares must identify their denominator. Published SSA counts are not a
  complete census of births, and state totals need not equal national totals.
- Spelling variants are treated as separate names. Early coverage, suppression,
  recording errors and binary recorded-sex categories constrain interpretation.
- Conclusions concern aggregate associations, not causes of parental choices
  or an individual's identity.

The [data guide](../data/README.md) contains source links and acquisition rules.
Regional comparisons additionally require a sourced Census lookup and a
validated many-to-one state join, including DC.

## What exists locally today

| Component | Observed state |
|---|---|
| Project foundation | README, proposal PDF, folder guides and pinned direct dependencies are present. Python 3.12 is the documented reference; `requirements.txt` pins pandas 2.3.3 and JupyterLab 4.6.4. The installed environment was not tested for these notes. |
| State data | 51 local `.TXT` files, including DC, are present. No SSA source README is present; provenance and actual coverage remain unverified. |
| National and prepared data | Both directories contain only `.gitkeep`; no datasets are present there. |
| Notebook | `00_setup.ipynb` checks the environment and paths only. It has no saved outputs and was not executed for these notes. It does not validate data. |
| Analysis and reporting | No preparation or EDA notebook, reusable analysis module, report source, figure or analytical result is present in the inspected project folders. |

The repository is therefore a documented foundation with local state inputs;
completion of data preparation is not yet evidenced. Dates in the timetable
do not establish that a stage has been completed.

## Next work implied by the README

1. Establish provenance and coverage for the relevant national/state releases:
   source URLs, access dates, checksums, inventory, years and row counts.
2. Write the data dictionary and audit keys, missing values, duplicates, codes,
   years, counts and unusual entries. Explain any treatment decisions.
3. Agree and document suppression handling, denominators, rank ties and
   minimum-count rules. Prepare outputs reproducibly with before/after checks.
4. Begin focused EDA once the relevant inputs meet those criteria. Validate
   the Census lookup before regional comparisons; national exploration does
   not depend on that lookup.
5. Assemble the **16 November 2026 Quarto HTML update** from preparation and
   EDA actually completed. The report template has not yet been introduced.

The proposal timetable places analysis/modelling on 17 November–5 December,
interpretation/writing on 6–14 December, and review/presentation on
15–20 December. Final submission is **21 December 2026**, comprising the
Quarto/HTML report and a presentation video of at most ten minutes.

## Open decisions and housekeeping

- Individual assignments remain to be agreed by the group.
- Release selection, coverage, analytical thresholds and the definition of a
  name–sex shift still require documented decisions.
- The root README links to `notebooks/README.md`, which is missing locally
  because of a pre-existing staged deletion. This note records that state;
  the deletion was left untouched.
- No data were downloaded, changed or analysed when taking these notes, and
  no remote repository state was verified.
