# Course project requirements

Recorded on **9 November 2026**, with the detailed **project-update instructions
and marking rubric added on 11 November** from the user's pasted course text.
The linked course template was checked again on 11 November. Moodle itself,
the other milestones' detailed rubrics and the previous-project example have
not been inspected.

The dates below use **2026**, consistent with the project README and proposal
timetable; the pasted description itself gives month/day only. Exact submission
times and time zone are not specified in that text.

## Purpose and grading

The assignment covers the full data science process on a topic chosen by the
group: acquire data, design visualisations, run statistical analysis, and
communicate results. A group of **four students is recommended**, not stated as
mandatory.

The project accounts for **70% of the total course grade**. These weights are
percentages of the **total course grade**, not percentages within the project:

| Milestone | Due date | Course-grade weight | Submission |
|---|---|---|---|
| Group self-enrolment | 19 October | No separate weight stated | Course enrolment link |
| Project proposal | 19 October | 10% | Google Form; optional supporting files |
| Project update | 16 November | 10% | File upload through Moodle |
| Video presentation | 21 December | 25% | Slides upload and Google Drive video link through Moodle |
| Final report | 21 December | 25% | `.qmd` source and compiled HTML through Moodle |

The course description permits deadline extensions only for medical reasons
and states that projects submitted after the final deadline will not be graded.
The update rubric is transcribed below; the other detailed grading criteria
remain on the corresponding Moodle submission pages.
The pasted “Submit here” placeholders contain no usable submission URLs.

## Deliverables

### Proposal

Include background, objectives, research questions, data source and timeline.
Submit through the Google Form. Optional supporting uploads have no particular
format constraint in the supplied description. The repository retains the
proposal at [project_proposal.pdf](project_proposal.pdf); a local PDF alone is
not independent evidence of a successful form submission.

### Project update

- Demonstrate significant progress covering **approximately half of the final
  report's content**. Include preprocessing, EDA and preliminary findings;
  an inventory alone does not satisfy the scope. Figures and tables need not
  be final or polished, but must reflect work actually completed.
- Follow the [course template](https://github.com/Elwin-Freudiger/project-template)
  and preserve its structure in the `.qmd` source before rendering.
- Submit an **HTML report**, preferably generated from Quarto `.qmd`; a **PDF
  report with code attached separately** is also allowed for this milestone.
- Required filename: `update_<group_name>.html` or `update_<group_name>.pdf`.
- Submit the file through Moodle by **16 November**.
- Finalise the project title now and use it consistently in the final report
  and presentation. The existing project title is **What's in a Name?**.

| Required section | Points / 10 | Content to include |
|---|---:|---|
| Introduction and Research Questions | 2 | Restate the goals and research questions; explain any refinements to the proposal. |
| Data Sources and Preprocessing | 2 | Describe sources and completed preprocessing; explain data challenges and their treatment. |
| Exploratory Data Analysis (EDA) | 3 | Present initial visualisations and summary statistics, and interpret the main patterns. |
| Preliminary Analysis | 2.5 | Outline the statistical methods or models being explored, why they were selected and what they aim to establish. |
| Conclusion and Next Steps | 0.5 | State what has been achieved and the specific work remaining for the final report. |

The five report sections are **Introduction, Data, EDA, Analysis and
Conclusion**. The template's analysis file contains Methods and Findings and
Discussion; preserve those roles within Analysis. Its general note that
Methods can be optional does not remove the update's explicit preliminary
analysis requirement. Distinguish planned methods from fitted models and
verified findings.

Our planned route remains Quarto HTML. With the repository's current group
label **AJ**, the expected name is `update_AJ.html`; verify that label against
the enrolled Moodle group before submission. The permitted PDF alternative
would be `update_AJ.pdf`, with code supplied separately.

The [template source](https://github.com/Elwin-Freudiger/project-template/blob/main/report/report.qmd)
provides title/author/institution/date metadata, a short abstract (at most
250 words), numbered sections, a table of contents, folded code in HTML,
references and appendices. Its main file includes five section sources from
`sections/`; remove the instructional `_quarto_guide.qmd` include and example
content when adapting it. Keep central figures and their interpretations in
the main report; use appendices only for supporting detail.

### Video presentation

- Present the key insights and contributions in **at most ten minutes**.
- Upload the presentation slides as **PDF, HTML or PowerPoint** to Moodle.
- Submit a **Google Drive link** to the video through Moodle, with the video
  **publicly accessible**. Verify access without relying on the owner's session
  before submission.
- Both components are due **21 December**.

### Final report

- Cover data collection, analysis and conclusions across the complete process.
- Submit **both** the Quarto source and its compiled HTML through Moodle by
  **21 December**. The update's PDF alternative is not stated for the final.
- Required names: `final_<group_name>.qmd` and `final_<group_name>.html`;
  expected names for AJ are `final_AJ.qmd` and `final_AJ.html`, subject to the
  group-label check above.
- Code must be **hidden in the report but available for reproducibility**.
  Rendering should hide or collapse code without deleting the source.

The template contains a main `report.qmd`, section sources and a bibliography.
We will adapt these under our existing `reports/` directory. When assembling
the submission, check that source dependencies are supplied or incorporated so
the submitted `.qmd` can actually reproduce the HTML. This is an implementation
check, not an additional file-format rule from the pasted course description.

## Dataset recommendations

The description frames these as **recommended guidelines**, not an explicit
hard rejection rule:

| Dimension | Recommendation |
|---|---|
| Observations | At least 1,000 rows |
| Variables | At least 8–12 variables |
| Numeric | 3–5 integer/double variables |
| Categorical | 2–3 variables |
| Date/time | At least one, if applicable |
| Text | At least one character/text variable |

The stated motivation is to provide meaningful cleaning/wrangling, univariate
and multivariate exploration, and modelling opportunities while keeping the
work manageable. Statistical validity still depends on the study design,
dependence, sampling, assumptions and validation; a row-count threshold alone
does not ensure significance or validity.

## Implications for What's in a Name?

The verified local state dataset has **6,696,687 aggregate records**, comfortably
exceeding the recommended row count. A record is a state × name × recorded sex
× year combination, not one individual birth or necessarily an independent
observation. See the [inventory evidence](data_inventory/README.md).

It has **five raw fields**, below the recommended variable range:

| Field | Analytical role |
|---|---|
| `count` | Numeric frequency |
| `state`, `sex` | Two categorical variables |
| `year` | Temporal variable stored as an integer; not a full date |
| `name` | Text |

The raw table has all four broad variable types, but only one non-temporal
numeric measure. The prepared table meets the recommended range through four
documented, useful features. Implemented or planned features, consistent with
the research questions, include:

- **Popularity shares and ranks:** describe prominence within an explicitly
  defined geography/year/sex group, with documented denominators and tie rules.
- **Name length:** a numeric spelling characteristic for the time and
  recorded-sex questions.
- **Decade:** a temporal grouping for trajectories and state profiles.
- **Census region/division:** categorical enrichment through a sourced,
  validated state lookup for geographical comparisons.
- **Female share:** useful at a name/year/geography grain after appropriate
  aggregation, with missing/suppressed opposite-sex records handled explicitly.

The preparation notebook executed successfully on **11 November 2026** and
verified a nine-column table containing the five original fields plus decade,
name length, published share and rank. The state audit passed, the raw files
were unchanged, and the exported table was reloaded and compared with the
prepared data. Initial EDA also executed, including selected name–sex
trajectories in a separate analytical table. The Census region/division lookup
remains planned. Tables at different grains must not be joined blindly.
The prepared table has four numeric measures (including ordinal rank), two
categorical fields, two temporal integer fields and one text field. This
meets the recommended mix; derived columns are not independent new
information. Every addition needs a research purpose. Adding national data
would extend coverage rather than increase the variable count.

## How this affects our plan

The course specifies submission milestones. Our **Stages 1–5** and their
internal dates come from the group's proposal; they are not separate course
submission requirements in the pasted description.

1. State dictionary, audit and preparation are complete for the local snapshot.
   Resolve its original acquisition provenance, acquire national data and
   validate a Census lookup before extending the scope.
2. Initial state EDA, figures, tables and the **16 November update source** are
   available. Review the interpretations and render/inspect the HTML before
   submission; distinguish the completed work from planned modelling.
3. Keep modelling, substantive conclusions, slides and the final reproducible
   report aligned with the later project stages and December deadlines.
4. Check the update against the rubric above. Confirm exact submission times,
   group label and upload links before packaging; obtain the other milestones'
   detailed rubrics before those submissions. These remaining checks do not
   prevent current preparation work.

The previous-project example, **Sentiment analysis of political news across
different media outlets**, is referenced by title only. No file or link was
provided, so its structure, analysis depth and quality have not been assessed.

## Submission checks to complete at each milestone

- [ ] Compare the deliverable with its detailed Moodle rubric.
- [ ] Confirm group label, deadline time/time zone and submission destination.
- [ ] Include the milestone's required content and use the required filenames.
- [ ] Render and inspect the HTML (or permitted update PDF) and confirm figures
      and required assets are available when opened outside the working copy.
- [ ] For the final: include reproducible `.qmd` source and keep code hidden
      but available.
- [ ] For the presentation: include slides, verify the ten-minute limit, and
      check public access to the Google Drive video link.
- [ ] Verify the actual submission receipt; local files are not proof of upload.
