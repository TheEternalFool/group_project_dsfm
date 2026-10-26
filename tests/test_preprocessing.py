import numpy as np
import pytest

from names_project import data, preprocessing


def test_shares_sum_to_one_within_year_and_sex(national_dir):
    df = preprocessing.build_national(data.load_national_raw(national_dir))
    sums = df.groupby(["year", "sex"], observed=True)["share"].sum()
    np.testing.assert_allclose(sums.to_numpy(), 1.0)
    assert {"per_million", "rank", "decade"} <= set(df.columns)


def test_rank_one_is_most_common(national_dir):
    df = preprocessing.build_national(data.load_national_raw(national_dir))
    top = df[(df["year"] == 1990) & (df["sex"] == "F") & (df["rank"] == 1)]
    assert top["name"].tolist() == ["Ashley"]


def test_female_share(national_dir):
    df = data.load_national_raw(national_dir)
    fs = preprocessing.female_share(df, by=["year"])
    jordan = fs[(fs["name"] == "Jordan") & (fs["year"] == 1990)].iloc[0]
    assert jordan["total"] == 100
    assert jordan["female_share"] == pytest.approx(0.2)
    michael = fs[(fs["name"] == "Michael") & (fs["year"] == 1990)].iloc[0]
    assert michael["female_share"] == 0


def test_state_build_adds_regions(state_dir, regions):
    df = preprocessing.build_state(data.load_state_raw(state_dir), regions)
    assert set(df["region"].astype(str)) == {"West", "South"}
    sums = df.groupby(["state", "year", "sex"], observed=True)["share"].sum()
    np.testing.assert_allclose(sums.to_numpy(), 1.0)


def test_missing_region_raises(state_dir, regions):
    with pytest.raises(ValueError, match="DC"):
        preprocessing.add_regions(data.load_state_raw(state_dir), regions[regions["state"] == "AK"])


def test_apply_min_count(national_dir):
    df = data.load_national_raw(national_dir)
    kept = preprocessing.apply_min_count(df, min_total=100)
    assert "Kaitlyn" not in set(kept["name"])
    assert "Jordan" in set(kept["name"])
