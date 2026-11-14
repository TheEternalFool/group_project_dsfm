# Reusable Python code

Add Python modules here when a task produces functions that are useful across
notebooks, such as a shared file reader or a preparation function.

Use short, descriptive filenames and explain a function's inputs, outputs and
assumptions. Keep data files in `data/` and research explanations in notebooks.
`ssa_inventory.py` streams the original SSA files to produce checksums, record
counts and coverage metadata without changing source data. Run
`python src/ssa_inventory.py --datasets state` from the repository root with the
project environment activated. See the
[inventory guide](../docs/data_inventory/README.md) for results and limitations.

Data preparation and EDA are implemented in the notebooks; this directory
currently contains the inventory utility. Analytical modelling remains planned.
