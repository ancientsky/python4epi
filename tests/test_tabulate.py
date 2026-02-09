import pandas as pd

from epi_learning.tabulate import summarize_by_group


def test_summarize_by_group_has_pct():
    df = pd.DataFrame({"case_id": [1, 2, 3], "location": ["N", "N", "S"]})
    summary = summarize_by_group(df, "location")
    assert list(summary.columns) == ["location", "n", "pct"]
    assert round(summary["pct"].sum(), 6) == 1.0
