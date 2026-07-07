# 13 Reproducible Research and Reporting

## What You'll Learn

- How to lock your environment and versions with `uv`
- How to design a reproducible analysis workflow
- How to build a minimal verifiable report (data + code + result)

## The Scenario

The analysis of the Legionnaires' disease cluster at Songbai Nursing Home is finally complete.
A week from now you'll need to regenerate the same outbreak report, and you have to guarantee that a colleague on a different machine gets identical results.

> "Last time it came out as 121 infected and 19 deaths, but when I rerun it I get something different?"

This is exactly the problem that **reproducible research** is meant to solve.

## Core Concepts

- **Environment lock**: pin your dependency versions with `uv.lock`
- **Single command workflow**: rerun the whole analysis with one command
- **Traceability**: every result can be traced back to its data source and code version

## Minimal Runnable Code

```bash
uv sync
uv run pytest
uv run python notebooks/run_sitrep.py
```

```python
from pathlib import Path
import pandas as pd

path = Path("data/synthetic/legionella_outbreak.csv")
df = pd.read_csv(path)

summary = {
    "n_residents": len(df),
    "n_zones": df.groupby(["floor", "wing"]).ngroups,
    "n_infected": int((df["clinical_severity"] != "not_ill").sum()),
    "n_deaths": int((df["outcome"] == "dead").sum()),
}
print(summary)
```

## Reproducibility Checklist

1. Is there a `uv.lock`?
2. Can you run `uv sync && uv run pytest` from a clean environment?
3. Is there a fixed data column contract (line list schema)?
4. Is there a minimal rerunnable script (e.g., `run_sitrep.py`)?

## Exercises

- Exercise version: [`13_reproducibility_exercise.ipynb`](exercises/13_reproducibility_exercise.ipynb)
- Solution version (instructor): [`13_reproducibility_solution.ipynb`](solutions/13_reproducibility_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/13_reproducibility_solution.ipynb>)

## Common Pitfalls

| Mistake | The Right Way |
|------|----------|
| Manually editing data in a notebook without recording it | Write all transformations in code |
| Sharing only result figures, not the code | Include rerunnable code and version info |
| Not pinning package versions | Lock the environment with `uv.lock` |
| Not fixing the random seed | Set `random_state` or `torch.manual_seed` |

## Next Step

Once your analysis is reproducible, in the next chapter (Ch14) we'll integrate all these skills into one **complete real-world case study** → an outbreak investigation SitRep.
