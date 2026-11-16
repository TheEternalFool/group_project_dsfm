# Course project requirements

Source: course instructions and the detailed project-update rubric supplied by
the group. Dates use the project's **2026** calendar. Submission times and links
are provided on Moodle; they are not specified in the supplied text.

## Scope and grading

The project covers data acquisition, visualisation, statistical analysis and
communication of results on a topic chosen by the group. A group of **four
students is recommended**.

The assessed submissions contribute **70% of the total course grade**. The
weights below are percentages of the total course grade.

| Deadline | Submission | Format and destination | Weight |
|---|---|---|---:|
| 19 October | Group self-enrolment | Course enrolment link | — |
| 19 October | Project proposal | Google Form; optional supporting files | 10% |
| **16 November** | **Project update** | Moodle: `update_<group_name>.html`, or `update_<group_name>.pdf` with code attached separately | **10%** |
| **21 December** | **Video presentation** | Moodle: slides and a public Google Drive video link | **25%** |
| **21 December** | **Final report** | Moodle: `final_<group_name>.qmd` and `final_<group_name>.html` | **25%** |

For Group AJ, use `update_AJ.html` (or `update_AJ.pdf`), `final_AJ.qmd` and
`final_AJ.html`. Confirm that AJ matches the enrolled Moodle group.
Extensions are permitted only for medical reasons. Projects submitted after
the final deadline will not be graded.

## Proposal

Include background, objectives, research questions, data source and timeline.
Supporting uploads are optional, with no prescribed format.

## Project update

Present significant progress covering **approximately half of the final
report's content**, including preprocessing, EDA and preliminary findings.
Figures and tables may be preliminary. Finalise the project title and use it
consistently in the final report and presentation.

Follow the [course template](https://github.com/Elwin-Freudiger/project-template)
with **Introduction → Data → EDA → Analysis → Conclusion**. HTML generated
from Quarto is preferred; the PDF alternative requires code attached separately.

| Required section | Points / 10 | Required content |
|---|---:|---|
| Introduction and Research Questions | 2 | Goals, research questions and refinements to the proposal |
| Data Sources and Preprocessing | 2 | Sources, completed preprocessing, data challenges and their treatment |
| Exploratory Data Analysis (EDA) | 3 | Initial visualisations, summary statistics and interpretation of the main patterns |
| Preliminary Analysis | 2.5 | Methods or models being explored, reasons for selecting them and what they aim to establish |
| Conclusion and Next Steps | 0.5 | Achievements and specific work remaining for the final report |

Within Analysis, include methods and findings/discussion. The update requires
preliminary analysis even though the generic template describes Methods as
optional. Distinguish proposed methods from fitted models and observed results.

## Final report

Cover the complete process from data collection through analysis to conclusions.
Submit **both the Quarto source and compiled HTML**; the update's PDF alternative
does not apply to the final report. Code must be **hidden in the report but
available for reproducibility**.

## Video presentation

Present the key insights and contributions in **at most ten minutes**. Submit
both:

- Slides in **PDF, HTML or PowerPoint** format through Moodle.
- A **publicly accessible Google Drive link** to the video through Moodle.

No particular slide or video filename is specified in the supplied instructions.
Detailed rubrics for the proposal, final report and presentation are on their
Moodle submission pages and are not reproduced here.

## Report template

The [template source](https://github.com/Elwin-Freudiger/project-template/blob/main/report/report.qmd)
provides title, author, institution and date metadata; an abstract of **at most
250 words**; numbered sections; a table of contents; folded code in HTML;
references; and optional appendices. Preserve the report structure and remove
the template's instructional guide and example content. Keep central figures
and their interpretation in the main report; use appendices for supporting detail.

## Dataset recommendations

These are **recommendations**, not mandatory submission-format rules.

| Dimension | Recommendation |
|---|---|
| Observations | At least 1,000 rows |
| Variables | 8–12 variables |
| Numerical | 3–5 integer/double variables |
| Categorical | 2–3 variables |
| Date/time | At least one, if applicable |
| Text | At least one character/text variable |

The dataset should support meaningful cleaning, univariate and multivariate
exploration, and modelling while remaining manageable. Justify useful derived
variables and any departure from these recommendations. Derived columns do not
add independent information, and row count alone does not establish statistical
validity; observation units, dependence, coverage, assumptions and validation
still matter.

The project's internal stages and schedule are planning choices, not additional
course submission requirements.
