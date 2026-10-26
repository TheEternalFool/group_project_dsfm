import io
import zipfile

import pandas as pd
import pytest

from names_project import data


def test_load_national_adds_year(national_dir):
    df = data.load_national_raw(national_dir)
    assert list(df.columns) == ["year", "name", "sex", "count"]
    assert set(df["year"]) == {1990, 1991}
    assert len(df) == 11
    assert data.validate_national(df) == []


def test_load_state(state_dir):
    df = data.load_state_raw(state_dir)
    assert list(df.columns) == data.STATE_COLUMNS
    assert set(df["state"]) == {"AK", "DC"}
    assert data.validate_state(df) == []


def test_missing_directory_gives_helpful_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="download_data"):
        data.load_national_raw(tmp_path)


def test_name_na_is_not_parsed_as_missing(tmp_path):
    # "Na" and "Nan" are real first names and must not become NaN.
    (tmp_path / "yob2000.txt").write_text("Na,F,6\nNan,F,7\n")
    df = data.load_national_raw(tmp_path)
    assert df["name"].tolist() == ["Na", "Nan"]
    assert data.validate_national(df) == []


def test_validation_flags_problems():
    df = pd.DataFrame(
        {
            "year": [1990, 1990, 1850],
            "name": ["Ann", "Ann", "Jo-Jo"],
            "sex": ["F", "F", "X"],
            "count": [10, 10, 3],
        }
    )
    problems = " | ".join(data.validate_national(df))
    for expected in ["sex not in", "non-alphabetic", "below the SSA threshold", "year outside", "duplicated"]:
        assert expected in problems


def test_extract_zip(tmp_path):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("yob1990.txt", "Ann,F,10\n")
    archive = tmp_path / "names.zip"
    archive.write_bytes(buf.getvalue())
    files = data.extract_zip(archive, tmp_path / "out")
    assert [f.name for f in files] == ["yob1990.txt"]


def test_census_regions_cover_ssa_states():
    regions = data.load_census_regions()
    assert len(regions) == 51
    assert regions["state"].is_unique
    assert set(regions["region"]) == {"Northeast", "Midwest", "South", "West"}
    assert regions["division"].nunique() == 9
