# External reference data

Small, hand-checked reference tables that are committed to the repository.

## `census_regions.csv`

State-to-region and state-to-division classification used by the US Census
Bureau (4 regions, 9 divisions; the District of Columbia is in the South
Atlantic division).

- Source: US Census Bureau, *Census Regions and Divisions of the United States*,
  <https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf>
- Columns: `state` (USPS code, matches the SSA state files), `state_name`,
  `region`, `division`.
- Transcribed by hand from the source map; `tests/test_data.py` checks that it
  covers exactly the 51 codes present in the SSA state file.
