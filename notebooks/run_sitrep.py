"""Generate a minimal situation report table from synthetic line list data."""

from __future__ import annotations

import pandas as pd

from epi_learning.cleaning import standardize_line_list
from epi_learning.metrics import attack_rate, case_fatality_rate
from epi_learning.tabulate import summarize_by_group


def main() -> None:
    df = pd.read_csv("data/synthetic/line_list.csv")
    clean = standardize_line_list(df)

    total_cases = len(clean)
    deaths = int((clean["outcome"] == "dead").sum())

    print("=== SitRep Snapshot ===")
    print(f"Total cases: {total_cases}")
    print(f"Deaths: {deaths}")
    print(f"CFR: {case_fatality_rate(deaths=deaths, cases=total_cases):.2%}")
    print(f"Attack rate (pop=5000): {attack_rate(total_cases, 5000):.2%}")
    print()
    print("Cases by location")
    print(summarize_by_group(clean, group_col="location").to_string(index=False))


if __name__ == "__main__":
    main()
