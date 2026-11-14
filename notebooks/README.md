# Notebooks

Keep notebooks directly in this folder so relative paths stay consistent.

- `00_setup.ipynb` checks the Python environment and project directories.
- `01_data_acquisition_and_audit.ipynb` identifies SSA releases and audits published rows. Read its manual-download instructions if automated access fails. It does not choose cleaning rules or perform EDA.
- `01_state_preparation.ipynb` audits the existing state snapshot and exports the prepared data.
- `02_state_eda.ipynb` uses those prepared data to produce the report figures and tables.

For the existing state data, run `00_setup.ipynb`, `01_state_preparation.ipynb`, then `02_state_eda.ipynb`. All three passed in the project `.venv` on 14 November 2026. The acquisition notebook is a separate workflow for the remaining release-provenance and national-data work; its real-data execution has not been verified.

- Name each later notebook `NN_short_description.ipynb`, in the order the work is performed.
- Begin with the question or objective, then explain the code and record what
  was actually observed. Keep one main task per notebook.
- Agree who edits a notebook before working on it. Restart its kernel and run
  all cells before sharing; remove accidental or oversized outputs.

Use `pathlib` and the project-root check from `00_setup.ipynb` rather than a
personal absolute path. Read original state data from `data/raw/state/`, national
data from `data/raw/national/`, and save prepared data to
`data/processed/`.

Move functions into `src/` when multiple notebooks need the same code. Keep
interpretation and methodological explanations in the notebooks.
