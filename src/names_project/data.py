"""Acquisition, reading and validation of the SSA baby-name files.

Sources (public domain / CC0, documented at
https://www.ssa.gov/oact/babynames/limits.html):

* National file ``names.zip``: one ``yobYYYY.txt`` per year from 1880, each
  with rows ``name,sex,count`` and no header.
* State file ``namesbystate.zip``: one ``XX.TXT`` per state (50 states + DC)
  from 1910, each with rows ``state,sex,year,name,count`` and no header.

SSA only publishes a name when it has at least 5 occurrences in the given
year (and state, for the state file). Rows below that threshold are absent,
not zero, which matters for every diversity or "rare name" statistic.
"""

from __future__ import annotations

import os
import re
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

NATIONAL_URL = "https://www.ssa.gov/oact/babynames/names.zip"
STATE_URL = "https://www.ssa.gov/oact/babynames/state/namesbystate.zip"
DOCS_URL = "https://www.ssa.gov/oact/babynames/limits.html"

SSA_MIN_COUNT = 5
NATIONAL_FIRST_YEAR = 1880
STATE_FIRST_YEAR = 1910

NATIONAL_COLUMNS = ["name", "sex", "count"]
STATE_COLUMNS = ["state", "sex", "year", "name", "count"]
SEXES = ("F", "M")

USER_AGENT = "group_project_dsfm/0.1 (UNIL student research project)"


def project_root() -> Path:
    """Return the repository root (override with ``NAMES_PROJECT_ROOT``)."""
    env = os.environ.get("NAMES_PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Paths:
    """Standard locations of data files, relative to the project root."""

    root: Path = field(default_factory=project_root)

    @property
    def raw(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def national_raw(self) -> Path:
        return self.raw / "names"

    @property
    def state_raw(self) -> Path:
        return self.raw / "namesbystate"

    @property
    def external(self) -> Path:
        return self.root / "data" / "external"

    @property
    def processed(self) -> Path:
        return self.root / "data" / "processed"


class DownloadError(RuntimeError):
    """Raised when an SSA file cannot be downloaded automatically."""


def download_file(url: str, dest: Path, overwrite: bool = False, timeout: int = 120) -> Path:
    """Download ``url`` to ``dest`` and return the path.

    SSA's website sometimes refuses scripted requests (HTTP 403). In that
    case the error message explains how to download the file manually.
    """
    dest = Path(dest)
    if dest.exists() and not overwrite:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response, open(tmp, "wb") as fh:
            while chunk := response.read(1 << 20):
                fh.write(chunk)
    except (urllib.error.URLError, TimeoutError) as exc:
        tmp.unlink(missing_ok=True)
        raise DownloadError(
            f"Could not download {url} ({exc}). Open the URL in a web browser, "
            f"save the file as {dest}, and run the command again."
        ) from exc
    tmp.replace(dest)
    return dest


def extract_zip(archive: Path, dest_dir: Path) -> list[Path]:
    """Extract ``archive`` into ``dest_dir`` and return the extracted files."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(dest_dir)
        return [dest_dir / n for n in zf.namelist() if not n.endswith("/")]


_YOB_PATTERN = re.compile(r"yob(\d{4})\.txt$", re.IGNORECASE)


def read_national_year(path: Path) -> pd.DataFrame:
    """Read one ``yobYYYY.txt`` file, adding the year taken from its name."""
    match = _YOB_PATTERN.search(Path(path).name)
    if match is None:
        raise ValueError(f"Not a national year file: {path}")
    df = pd.read_csv(
        path,
        header=None,
        names=NATIONAL_COLUMNS,
        dtype={"name": "string", "sex": "string", "count": "int64"},
        keep_default_na=False,
    )
    df.insert(0, "year", int(match.group(1)))
    return df


def load_national_raw(directory: Path | None = None) -> pd.DataFrame:
    """Stack every national year file into one frame (year, name, sex, count)."""
    directory = Path(directory) if directory else Paths().national_raw
    files = sorted(p for p in directory.glob("*") if _YOB_PATTERN.search(p.name))
    if not files:
        raise FileNotFoundError(
            f"No yobYYYY.txt files in {directory}. Run scripts/download_data.py "
            f"or place the extracted contents of {NATIONAL_URL} there."
        )
    return pd.concat([read_national_year(p) for p in files], ignore_index=True)


def read_state_file(path: Path) -> pd.DataFrame:
    """Read one ``XX.TXT`` state file."""
    return pd.read_csv(
        path,
        header=None,
        names=STATE_COLUMNS,
        dtype={"state": "string", "sex": "string", "year": "int64", "name": "string", "count": "int64"},
        keep_default_na=False,
    )


def load_state_raw(directory: Path | None = None) -> pd.DataFrame:
    """Stack every state file into one frame (state, sex, year, name, count)."""
    directory = Path(directory) if directory else Paths().state_raw
    files = sorted(p for p in directory.glob("*") if re.fullmatch(r"[A-Z]{2}\.TXT", p.name, re.IGNORECASE))
    if not files:
        raise FileNotFoundError(
            f"No XX.TXT state files in {directory}. Run scripts/download_data.py "
            f"or place the extracted contents of {STATE_URL} there."
        )
    return pd.concat([read_state_file(p) for p in files], ignore_index=True)


def load_census_regions(path: Path | None = None) -> pd.DataFrame:
    """Read the US Census Bureau state -> region/division table."""
    path = Path(path) if path else Paths().external / "census_regions.csv"
    return pd.read_csv(path, dtype="string")


def validate_names_frame(df: pd.DataFrame, keys: list[str], first_year: int) -> list[str]:
    """Return a list of human-readable problems (empty if the frame is clean).

    Checks the assumptions the rest of the pipeline relies on: no missing
    values, binary sex codes, alphabetic names, counts at or above the SSA
    publication threshold, plausible years and unique keys.
    """
    problems: list[str] = []
    missing = df.isna().sum()
    for col, n in missing[missing > 0].items():
        problems.append(f"{n} missing values in '{col}'")
    bad_sex = ~df["sex"].isin(SEXES)
    if bad_sex.any():
        problems.append(f"{int(bad_sex.sum())} rows with sex not in {SEXES}")
    bad_name = ~df["name"].astype("string").str.fullmatch(r"[A-Za-z]+").fillna(False)
    if bad_name.any():
        problems.append(f"{int(bad_name.sum())} names with non-alphabetic characters")
    low = df["count"] < SSA_MIN_COUNT
    if low.any():
        problems.append(f"{int(low.sum())} rows with count below the SSA threshold of {SSA_MIN_COUNT}")
    bad_year = (df["year"] < first_year) | (df["year"] > pd.Timestamp.today().year)
    if bad_year.any():
        problems.append(f"{int(bad_year.sum())} rows with year outside {first_year}-present")
    dupes = df.duplicated(subset=keys)
    if dupes.any():
        problems.append(f"{int(dupes.sum())} duplicated rows on {keys}")
    return problems


def validate_national(df: pd.DataFrame) -> list[str]:
    return validate_names_frame(df, ["year", "name", "sex"], NATIONAL_FIRST_YEAR)


def validate_state(df: pd.DataFrame) -> list[str]:
    problems = validate_names_frame(df, ["state", "year", "name", "sex"], STATE_FIRST_YEAR)
    bad_state = ~df["state"].astype("string").str.fullmatch(r"[A-Z]{2}").fillna(False)
    if bad_state.any():
        problems.append(f"{int(bad_state.sum())} rows with malformed state codes")
    return problems
