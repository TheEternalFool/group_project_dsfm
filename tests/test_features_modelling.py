import numpy as np
import pandas as pd
import pytest

from names_project import audit, data, features, modelling, preprocessing


def test_name_text_features():
    out = features.name_text_features(pd.Series(["Anna", "Mark"]))
    assert out["length"].tolist() == [4, 4]
    assert out["ends_in_vowel"].tolist() == [True, False]
    assert out["first_letter"].tolist() == ["a", "m"]


def test_char_ngrams_use_boundaries():
    vec = features.char_ngram_vectorizer(ngram_range=(2, 2), min_df=1).fit(["Ann", "Anna"])
    vocab = set(vec.get_feature_names_out())
    assert "^a" in vocab and "a$" in vocab and "n$" in vocab


def test_trajectory_features(national_dir):
    df = preprocessing.build_national(data.load_national_raw(national_dir))
    traj = features.trajectory_features(df)
    ashley = traj[(traj["name"] == "Ashley") & (traj["sex"] == "F")].iloc[0]
    assert ashley["first_year"] == 1990 and ashley["last_year"] == 1991
    assert ashley["years_in_use"] == 2
    assert ashley["mean_year"] == pytest.approx((1990 * 300 + 1991 * 250) / 550)


def test_diversity_known_values():
    uniform = features.diversity([10, 10, 10, 10], top_k=2)
    assert uniform["effective_names"] == pytest.approx(4)
    assert uniform["hhi"] == pytest.approx(0.25)
    assert uniform["top2_share"] == pytest.approx(0.5)
    assert features.diversity([7])["entropy"] == 0


def test_jensen_shannon_bounds():
    p = pd.Series({"Ann": 10, "Bob": 10})
    assert features.jensen_shannon(p, p) == pytest.approx(0)
    assert features.jensen_shannon(pd.Series({"Ann": 1}), pd.Series({"Bob": 1})) == pytest.approx(1)


def test_split_by_name_has_no_leakage():
    df = pd.DataFrame({"name": np.repeat([f"n{i}" for i in range(50)], 3), "year": np.tile([1, 2, 3], 50)})
    train, test = modelling.split_by_name(df, test_size=0.2)
    assert set(train["name"]).isdisjoint(set(test["name"]))
    assert len(train) + len(test) == len(df)


def test_split_by_name_is_reproducible():
    df = pd.DataFrame({"name": [f"n{i}" for i in range(30)]})
    a, _ = modelling.split_by_name(df)
    b, _ = modelling.split_by_name(df)
    assert a["name"].tolist() == b["name"].tolist()


def test_temporal_split_excludes_future():
    df = pd.DataFrame({"year": range(2000, 2010)})
    train, test = modelling.temporal_split(df, cutoff_year=2004)
    assert train["year"].max() <= 2004 < test["year"].min()


def test_bootstrap_ci_contains_point_estimate():
    y = np.arange(100.0)
    est, lo, hi = modelling.bootstrap_ci(y, y + 1, lambda a, b: float(np.mean(np.abs(a - b))), n_boot=200)
    assert lo <= est <= hi and est == pytest.approx(1)


def test_audit_frame(state_dir):
    df = data.load_state_raw(state_dir)
    result = audit.audit_frame(df, "state")
    assert result["n_rows"] == 8 and result["n_states"] == 2
    assert result["validation_problems"] == []
    assert result["share_rows_at_threshold"] == pytest.approx(1 / 8)
    md = audit.audit_to_markdown(result, audit.threshold_by_year(df))
    assert "| Rows | 8 |" in md
