---
title: "08 Where is it? Maps"
description: "Maya maps dengue across the 24 barangays of Santa Luz — counts versus attack rates, class breaks and colour-blind-safe palettes, unstable small numbers, a join that silently loses two barangays — then draws the real 18-region map of the Philippines and makes a map that is safe to publish."
---

:::{div}
:class: ph-story
*Wednesday 30 September · Office of the City Mayor*

**Mayor:** Ate Maya, I don't need tables. Just tell me: *where* is the dengue?

**Maya:** Ilog has the most cases, Mayor…

**Doc Mon:** Ilog also has the most people. Where is a resident most *likely* to get dengue? That's a different map.

**Aling Nena:** And please — no dots on our houses. People will know whose child is sick.

> Where is the dengue — and how do we draw a map that tells the truth without pointing at anyone?
:::

```{figure} images/santa_luz_map_en.svg
:alt: The fictional Santa Luz City in three bands, upland in the north, the riverside along the Marilag River, and the coast in the south, with the CESU and health stations marked.
:width: 100%
Santa Luz City and its three bands. The city, its 24 barangays and all their numbers are fictional.
```

## Counts or rates?

A **choropleth** is a map that colours each area by a number. The first decision is
*which* number.

- A **count** answers "where is the workload?": how many patients, how many houses for
  the 4S teams to visit.
- An **attack rate** answers "where is the risk?": cases ÷ population × 10,000, the
  chance that a resident became a case (per 10,000 people).

In Santa Luz, **Ilog** (riverside) has the most dengue cases: 31. But it is also one of
the biggest barangays, so its rate is 23.1 per 10,000. **Talaba** (coastal) has 29
cases among only 6,688 residents: **43.4 per 10,000**, the highest. Next is Buhangin,
35.5. On a count map the riverside glows; on a rate map the coast does. Mapping raw
counts as if they were risk is one of the most common map mistakes.

:::{admonition} Ask Tala
:class: ph-ask-tala
I have a GeoDataFrame `brgy` (24 rows; columns `barangay_id`, `barangay`, `band`,
`population`, `geometry`) and a line list `ll` (one row per case; columns `barangay_id`,
`disease`). Made-up example: `ll` rows `("SL01", "dengue")`, `("SL01", "dengue")`,
`("SL02", "leptospirosis")`. Count dengue cases per `barangay_id`, join the counts to
`brgy` **on `barangay_id`**, put 0 where a barangay has no case, and add `attack_rate` =
cases / population × 10,000. The result must still have 24 rows.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
dengue_counts = ll[ll["disease"] == "dengue"].groupby("barangay_id").size().rename("cases")
brgy = brgy.merge(pop, on="barangay_id", how="left")
brgy = brgy.merge(dengue_counts, left_on="barangay_id", right_index=True, how="left")
brgy["cases"] = brgy["cases"].fillna(0).astype(int)        # a barangay with no case is 0, not missing
brgy["attack_rate"] = brgy["cases"] / brgy["population"] * 10_000
```
:::

:::{admonition} Check it
:class: ph-check
1. **24 rows** after the join: `assert len(brgy) == 24`.
2. **The total**: the barangay counts add up to all 388 dengue cases.
3. **One rate by hand**: Talaba, 29 ÷ 6,688 × 10,000 = 43.4.
4. **The zero**: upland Bukid had no dengue case, so `groupby` gave only 23 rows.
   Without `fillna(0)` Bukid would be blank ("no data") instead of 0.
:::

## Class breaks and colours

A choropleth usually groups values into a few **classes**. The breaks change the
message:

- **Equal interval:** classes of equal width (here about 11 per 10,000 each). With
  4 classes, only 2 barangays land in the top class.
- **Quantile:** the same number of barangays in each class (24 ÷ 4 = 6). Every colour
  is used, but two neighbouring classes can be close in value.

Neither is "right". Choose on purpose, and write the breaks in the legend.

Colours matter just as much. Use a **sequential** palette, light for low and dark for
high, such as `YlOrRd` or `viridis`. People read it in order without a legend, and it
survives colour-blindness and black-and-white printing. Avoid **rainbow** palettes
(`jet`): they have no natural order, and their bright yellow middle pulls the eye to
*medium* values.

:::{div}
:class: ph-game ph-game-map-paint
Map rates, not counts; choose class breaks on purpose; use a light-to-dark palette.
:::

## Small numbers jump around

The upland barangays have 3,000–5,000 residents and a handful of cases. Maligaya has
**1 case: 3.0 per 10,000**. One more case would double it to 6.1. The notebook computes
an exact 95% confidence interval for each rate: for Maligaya it runs from 0.1 to 16.9,
for Talaba from 29.0 to 62.3. A wide interval means **don't rank that barangay on its
colour alone**. Add the counts to the hover text or the table next to the map.

## An interactive map

For a screen, plotly draws the same map with hover labels showing barangay, band,
cases, population and rate. It needs the polygons as GeoJSON and the key that links each
row to a polygon, `featureidkey="properties.barangay_id"`. We draw no background map
tiles: Santa Luz is fictional, and its coordinates deliberately sit in the open sea, so
it can never be mistaken for a real place.

:::{admonition} Tala got it wrong
:class: ph-oops
Jun sent a quick table of dengue counts by barangay **name**, typed by hand. Tala joined
it to the map **on the name**. The map looked fine. But Jun had typed `Santo Nino` (no ñ)
and `Tabing Ilog` (no hyphen). With an inner join, those two rows simply disappeared:
no error, no warning. Two riverside barangays with 41 cases between them would have
been blank on the Mayor's map.

How Maya catches it:

```python
merged = brgy[["barangay_id", "barangay", "geometry"]].merge(jun, on="barangay", how="inner")   # Tala's join
assert len(merged) == 24, f"join kept {len(merged)} of 24 barangays"
```

The assert fails with *"join kept 22 of 24 barangays"*, and an outer join with
`indicator=True` shows the two mismatched names. The fix: **join on the code**
(`barangay_id`), never on a typed name. [Chapter 03](03_clean_linelist.md) shows how to turn messy names into codes.
:::

## Zooming out: the 18 regions

For a briefing it helps to show the whole country. `ph_regions.topo.json` holds the
**real** boundaries of the 18 regions as TopoJSON, a compact cousin of GeoJSON.
`geopandas.read_file` reads it directly. We join the real statistics in
`ph_regions_stats.csv` on the PSGC code **`adm1_psgc`** and assert 18 rows.

The notebook maps **population density in 2024**. NCR has **22,015 people per km²**,
about 22 times more than the next region, CALABARZON (1,004). With equal-width classes
every other region would get the same colour, so we use quantile classes. The density is
derived from the 2024 population and the land area, both taken from
[Regions of the Philippines (Wikipedia)](https://en.wikipedia.org/wiki/Regions_of_the_Philippines)
through this book's research file. Every value in the CSV carries its own source URL;
quote it with the number.

Every map drawn from this file carries the credit line: *Boundaries: NAMRIA, PSA via
OCHA COD-AB (CC BY-IGO); TopoJSON: faeldon/philippines-json-maps (MIT).*

This is a **context** map of the real country. Never draw fictional Santa Luz on it.

:::{admonition} Privacy stop
:class: ph-privacy
A **dot map** of households with cases is a list of addresses drawn as dots. Anyone who
knows the street can point at a house. Inside the CESU it may guide the 4S teams. On a
public page it identifies neighbours, which is the concern of
[chapter 02](02_privacy_first.md). Public maps show **aggregated areas** (barangays),
and even then a barangay with very few cases can point to a person. This book's rule:
**suppress counts of 1–4** (show "<5"), and suppress their **rates** too, because
rate × population gives the count back. In Santa Luz that hides 5 of the 24 barangays on
the public map. The notebook draws them hatched, labelled "1–4 cases: not shown".
:::

## Back to the lamok

A map tells the 4S teams *where* to go. What they do there is search and destroy breeding
sites: any container that holds clean, still water.

```{figure} images/mosquito_4s_en.svg
:alt: The 4S against dengue around an Aedes mosquito: search and destroy breeding sites, secure self-protection, seek early consultation, support fogging in outbreak hotspots.
:width: 100%
The 4S against dengue.
```

:::{div}
:class: ph-game ph-game-lamok-patrol
4S: Search and destroy breeding sites, Secure self-protection, Seek early
consultation, Support fogging only in outbreak hotspots.
:::

:::{div}
:class: ph-game ph-game-quiz
**Quick check: maps**

1. Ilog has the most dengue cases, Talaba the highest attack rate. Where is a resident's risk highest?
   - Ilog — it has the most cases, but also many more residents.
   - ✓ Talaba — the rate divides by the population at risk.
2. Your merged map table has 22 rows instead of 24. What do you do?
   - Nothing, the map still draws — two barangays are now blank or missing.
   - ✓ Find the names that did not match and join on `barangay_id` instead.
3. Which palette should a dengue rate map use?
   - ✓ A sequential palette, light to dark — it reads in order and is colour-blind safe.
   - A rainbow palette — it has no natural order and highlights the middle values.
4. A barangay has 3 cases. On the public map you show…
   - The count and the rate — a small cell can point to a person.
   - ✓ "<5", and no rate — the rate times the population gives the count back.
:::

:::{admonition} Baon
:class: ph-baon
- Map **rates** for risk and counts for workload. Say which one you are showing.
- Join on a **code**, keep zero-case areas, and `assert` the number of rows.
- Sequential palette, deliberate breaks, credit line, and no small cells or dots on
  public maps.

Open the notebook: [](notebooks/08_maps.ipynb)
:::
