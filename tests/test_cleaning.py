import pandas as pd
import pytest

from epi_learning.cleaning import standardize_line_list


def test_standardize_line_list_columns_and_values():
    raw = pd.DataFrame(
        {
            "Case_ID": ["A1"],
            "Date_Onset": ["2025-01-01"],
            "Date_Report": ["2025-01-02"],
            "Location": [" North "],
            "Age": [33],
            "Sex": ["female"],
            "Outcome": [" Recovered "],
        }
    )

    out = standardize_line_list(raw)
    assert out.loc[0, "sex"] == "F"
    assert out.loc[0, "location"] == "North"
    assert out.loc[0, "outcome"] == "recovered"


def test_standardize_line_list_missing_required_columns():
    raw = pd.DataFrame({"case_id": [1]})
    with pytest.raises(ValueError):
        standardize_line_list(raw)
