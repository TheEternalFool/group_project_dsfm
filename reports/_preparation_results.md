The preparation retained **6,696,687 records** across **51 states/DC** and **1910–2025**. The rows contain **33,757 distinct spellings** and sum to **330,978,761 published counts** across the period. These aggregate records are not individual people or independent observations.

| Audit check | Result |
|---|---:|
| Missing field values | 0 |
| Blank text fields | 0 |
| Invalid state codes | 0 |
| Invalid recorded-sex codes | 0 |
| Years outside 1910–2025 | 0 |
| Counts below 5 | 0 |
| Excess duplicate-key rows | 0 |
| Missing state–sex–year groups | 0 |
| Unexpected state–sex–year groups | 0 |
| Observed state–sex–year groups | 11,832 |
| Raw-file SHA-256 checks unchanged | 51 / 51 |
| Rows dropped or original field values changed | 0 |
| Export/reload comparison | Passed |

Review flags were kept separate from structural failures: surrounding whitespace: 0; fewer than two characters: 0; nonalphabetic spelling: 0; placeholder-like label: 1,811. These labels do not by themselves establish an error; no flagged record was removed.

Four derived variables were added: decade, name length, share of published counts within state–sex–year, and descending count rank with alphabetical tie-breaking. Each group’s shares sum to one. Missing name records were not filled with zeros, spellings were preserved, and the CSV export was reloaded and checked against the prepared table.

The original acquisition date and exact release remain undocumented. SHA-256 checks identify the local input snapshot; they do not authenticate its original download or resolve SSA coverage limitations.
