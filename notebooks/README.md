# Notebooks

Keep notebooks directly in this folder so relative paths stay consistent.

- `00_setup.ipynb` checks the Python environment and project directories.
- `01_data_acquisition_and_audit.ipynb` identifies SSA releases and audits published rows. Read its manual-download instructions if automated access fails. It does not choose cleaning rules or perform EDA.
- Name each later notebook `NN_short_description.ipynb`, in the order the work
  is performed; for example, `02_data_preparation.ipynb` when the group starts preparation after reviewing the audit.
- Begin with the question or objective, then explain the code and record what
  was actually observed. Keep one main task per notebook.
- Agree who edits a notebook before working on it. Restart its kernel and run
  all cells before sharing; remove accidental or oversized outputs.

Use `pathlib` and the project-root check from `00_setup.ipynb` rather than a
personal absolute path. Read original state data from `data/raw/state/`, national
data from `data/raw/national/`, and save future prepared data to
`data/processed/`.

Move functions into `src/` when multiple notebooks need the same code. Keep
interpretation and methodological explanations in the notebooks.
