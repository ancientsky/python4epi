# 14 Case Study: A Legionnaires' Disease Outbreak Investigation Report

## What You'll Learn

- How to walk through a complete outbreak investigation, from receiving the notification to finishing the final report
- How to integrate every skill from the previous 13 chapters
- How to produce "actionable" analytic conclusions

## The Scenario

It all started with that phone call.

> In mid-January 2026, you receive a notification from Songbai Nursing Home: several residents have recently developed pneumonia symptoms.
> You grab your laptop, rush to the site, and begin an epidemiological investigation.
> Now the investigation is over — it's time to pull all of your analyses together into a formal **outbreak investigation report**.

This chapter is the final challenge: use Python to produce a complete, end-to-end outbreak investigation report.

## Report Structure

A standard outbreak investigation report contains the following sections:

| Section | Related Chapter | Core Skills |
|------|---------|---------|
| 1. Background & Notification | Ch00, Ch04 | Case definition, notification workflow |
| 2. Methods | Ch02 | Data collection, line list cleaning |
| 3. Descriptive Epidemiology | Ch02, Ch03, Ch04 | Person/time/place distribution, epidemic curve, attack rate |
| 4. Analytic Epidemiology | Ch03, Ch05, Ch06 | 2×2 tables, stratified analysis, logistic regression |
| 5. Time & Space Analysis | Ch07, Ch08 | Time series, spatial distribution |
| 6. Advanced Analysis | Ch09, Ch10 | Survival analysis, prediction models |
| 7. Discussion & Recommendations | — | Source identification, intervention measures |
| 8. Conclusion | — | Action recommendations |

## Summary of Key Findings

In the notebook, you'll produce the following key numbers:

- **280** residents, **121** infected (attack rate **43.2%**)
- **19** deaths (case fatality rate **15.7%**)
- Peak of onset: **2026-01-19 to 01-22**
- High-risk zones: **2F-A** (54.5%), **3F-B** (57.4%)
- Main risk factor: **shower use** (adjusted OR > 1)
- Conclusion: the shower system is the most likely source of infection

## Exercises

- Exercise version: [`14_case_study_exercise.ipynb`](exercises/14_case_study_exercise.ipynb)
- Solution version (instructor): [`14_case_study_solution.ipynb`](solutions/14_case_study_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/14_case_study_solution.ipynb>)

## Common Pitfalls

| Mistake | Correct Approach |
|------|----------|
| Listing numbers with no context | Give every number a comparison baseline (e.g., national CFR) |
| Too many charts, no focus | Pick 3–5 key charts, each with a clear conclusion |
| Stopping once the analysis is done | Always include an "action recommendations" section |
| Inconsistent report formatting | Use a standard outbreak investigation report format |

## Next Step

Congratulations! Finishing this chapter means you now have the full ability to conduct an outbreak investigation with Python.
The appendix (Ch15) collects advanced terminology and reference resources.
