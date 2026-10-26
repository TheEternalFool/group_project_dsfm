"""Small synthetic fixtures that mimic the SSA file formats."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

NATIONAL_FILES = {
    "yob1990.txt": "Ashley,F,300\nJessica,F,200\nJordan,F,20\nJordan,M,80\nMichael,M,400\n",
    "yob1991.txt": "Ashley,F,250\nJessica,F,150\nJordan,F,40\nJordan,M,60\nMichael,M,380\nKaitlyn,F,5\n",
}

STATE_FILES = {
    "AK.TXT": "AK,F,1990,Ashley,10\nAK,M,1990,Michael,12\nAK,F,1991,Ashley,8\nAK,M,1991,Michael,9\n",
    "DC.TXT": "DC,F,1990,Ashley,20\nDC,F,1990,Jordan,5\nDC,M,1990,Jordan,7\nDC,M,1990,Michael,30\n",
}


def _write(directory: Path, files: dict[str, str]) -> Path:
    directory.mkdir(parents=True)
    for name, text in files.items():
        (directory / name).write_text(text)
    return directory


@pytest.fixture
def national_dir(tmp_path: Path) -> Path:
    return _write(tmp_path / "names", NATIONAL_FILES)


@pytest.fixture
def state_dir(tmp_path: Path) -> Path:
    return _write(tmp_path / "namesbystate", STATE_FILES)


@pytest.fixture
def regions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "state": ["AK", "DC"],
            "state_name": ["Alaska", "District of Columbia"],
            "region": ["West", "South"],
            "division": ["Pacific", "South Atlantic"],
        }
    )
