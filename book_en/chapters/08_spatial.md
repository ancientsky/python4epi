# 08 Spatial Epidemiology: Which Floor and Wing Is Most Dangerous?

## What You Will Learn

- Compute attack rates by **floor × wing** to identify high-risk areas
- Use a seaborn **heatmap** to show how attack rates are distributed across floors and wings
- Compute the attack rate for each **room** and draw a **spot map**
- Understand the logic behind `groupby().agg()` / `pivot()` / scatter coordinate design
- Know when to choose a heatmap, a spot map, or a choropleth
- Once you spot a spatial difference, know how to dig deeper (CFR, comparing exposure factors)
- Draw a geographic choropleth with **GeoJSON + Plotly** (concept extension)
- Common pitfalls in spatial analysis and a debugging checklist

## The Scenario

Your supervisor asks: **"Where is it worst?"**

Songbai Nursing Home has **3 floors × 2 wings (A / B)** and 280 residents in total.
You need to map the spatial distribution and find out which floor-wing areas have the highest attack rates.
If one particular wing stands out, it may hint that the water system there (showerheads, hot-water piping) is the transmission route.

---

## Core Concepts

### The Three Levels of Spatial Analysis

Spatial questions at different scales call for different tools.

```{figure} images/spatial_analysis_levels.svg
:name: spatial-analysis-levels
:alt: Three levels of spatial analysis: inside a building, administrative districts, and the globe
:width: 100%

Spatial analysis spans three scales, from inside a building to the whole globe, each matched to a different visualization tool.
```

### When Do You Use Which Chart?

```{figure} images/spatial_chart_decision.svg
:name: spatial-chart-decision
:alt: Decision chart for spatial visualization
:width: 100%

Choose the most suitable spatial visualization based on your data structure. Part 1 of this chapter uses heatmaps and spot maps; Part 2 extends to choropleths.
```

---

## Part 1: Floor-Wing Attack Rates (`08_spatial_rates.ipynb`)

### Step 1 — Prepare the Data

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
df["died"]     = (df["outcome"] == "dead").astype(int)
```

> **Line-by-line breakdown**
>
> - `df["clinical_severity"] != "not_ill"` finds all residents who are "symptomatic or lab-confirmed"; the result is a True/False series
> - `.astype(int)` turns True → 1 and False → 0, creating an **infection flag** (indicator variable)
> - `df["outcome"] == "dead"` builds a **death flag** in the same way
> - The advantage of flag columns: you can later apply `.sum()` directly (summing 1s = counting people) or `.mean()` (the average = the proportion)

### Step 2 — Floor × Wing Attack Rates

```python
spatial = df.groupby(["floor", "wing"]).agg(
    total    = ("case_id",   "count"),
    infected = ("infected",  "sum"),
    died     = ("died",      "sum"),
).reset_index()
spatial["attack_rate"] = (spatial["infected"] / spatial["total"] * 100).round(1)
spatial["cfr"]         = (spatial["died"] / spatial["infected"] * 100).round(1)
```

> **Line-by-line breakdown: `groupby().agg()`**
>
> | Code snippet | In plain words |
> |---|---|
> | `groupby(["floor", "wing"])` | "Split the data into groups by the floor and wing columns" |
> | `agg(total=("case_id","count"))` | "Within each group, count the number of case_id rows → store it in the total column" |
> | `agg(infected=("infected","sum"))` | "Within each group, sum the infected flag → store it in the infected column" (summing flags = number infected) |
> | `agg(died=("died","sum"))` | Likewise, count the number of deaths in each group |
> | `.reset_index()` | Turn the grouping keys (floor, wing) from the DataFrame's "index" back into ordinary columns, which makes later steps easier |
>
> **Why use `agg()` instead of three separate `groupby()` calls?**
> `agg()` computes all the metrics at once, making the code more concise and faster.
>
> The `agg()` syntax formula: `new_column_name = ("source_column", "aggregation_function")`. Common aggregation functions are `"count"`, `"sum"`, `"mean"`, `"max"`, and `"min"`.

**Reading the output**

After running it, you'll see a 6 × 5 table (3 floors × 2 wings = 6 groups).
How to read it: `attack_rate` is the attack rate (higher means that wing was hit harder), and `cfr` is the case fatality rate (the proportion of infected people who died).

### Step 3 — Attack Rate Heatmap

```python
heatmap_ar = spatial.pivot(index="floor", columns="wing", values="attack_rate")
sns.heatmap(heatmap_ar, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={"label": "%"})
plt.title("Attack Rate (%) by Floor × Wing")
```

> **Line-by-line breakdown**
>
> - `pivot(index="floor", columns="wing", values="attack_rate")`
>   turns the "long table" (each row is one floor-wing combination) into a "matrix" (rows = floor, columns = wing, cells = attack rate).
>   A heatmap needs matrix format to draw the color cells, so this line is the key preprocessing step.
> - `annot=True`: display the value on each cell (otherwise you only get color, no numbers)
> - `fmt=".1f"`: format the values to one decimal place
> - `cmap="YlOrRd"`: a palette running from yellow (low) to orange (medium) to red (high), intuitively matching the level of danger
>
> **When do you use a heatmap?**
> When the grouping variables happen to be **two categories** (here, floor × wing), they naturally form a matrix → a heatmap is the most intuitive choice.
> If you only have one categorical variable, a bar chart is more appropriate.

### Step 4 — Attack Rate per Room

```python
room_stats = df.groupby("room").agg(
    total    = ("case_id",  "count"),
    infected = ("infected", "sum"),
).reset_index()
room_stats["attack_rate"] = (room_stats["infected"] / room_stats["total"] * 100).round(1)

# Parse the room name "2A-03" → floor_num=2, wing_code="A", room_num=3
room_stats["floor_num"] = room_stats["room"].str[0].astype(int)
room_stats["wing_code"] = room_stats["room"].str[1]
room_stats["room_num"]  = room_stats["room"].str.split("-").str[1].astype(int)
```

> **Line-by-line breakdown: string parsing**
>
> The room code format is `"2A-03"` (floor + wing + hyphen + room number).
>
> | Operation | Result (using "2A-03") |
> |---|---|
> | `room.str[0]` | `"2"` → the 0th character = floor |
> | `room.str[1]` | `"A"` → the 1st character = wing |
> | `room.str.split("-").str[1]` | `"03"` → split on `-` and take the second part = room number |
> | `.astype(int)` | `2`, `3` → convert to integers so they can be used as coordinates |
>
> **Why parse it instead of using the `room` string directly?**
> Drawing a spot map requires numeric x/y coordinates. The string "2A-03" can't be placed on an axis directly; it has to be broken down into numbers first.

### Step 5 — Floor-Wing Spot Map (bubble chart)

```python
max_room_a = room_stats[room_stats["wing_code"] == "A"]["room_num"].max()
gap = 5  # Leave a 5-unit gap between wing A and wing B

room_stats["x"] = room_stats.apply(
    lambda r: r["room_num"] if r["wing_code"] == "A"
              else r["room_num"] + max_room_a + gap,
    axis=1,
)

fig, ax = plt.subplots(figsize=(14, 5))
sc = ax.scatter(
    room_stats["x"],
    room_stats["floor_num"],
    s = room_stats["total"] * 50,       # dot size = number of residents × scaling factor
    c = room_stats["attack_rate"],      # color = attack rate
    cmap="YlOrRd",
    edgecolors="black", linewidth=0.5, alpha=0.8,
)
plt.colorbar(sc, label="Attack Rate (%)")
```

> **Line-by-line breakdown**
>
> **Why do we need an x offset?**
> The nursing home has a wing A and a wing B. If both wings number their rooms starting from 01 and you use `room_num` directly as the x coordinate, the points from wing A and wing B will overlap.
> The fix: wing B's x = wing B room number + wing A's maximum room number + gap. This lays the two wings out side by side, mimicking the left-right layout of the real floor plan.
>
> | Parameter | What it represents |
> |---|---|
> | `x = room_stats["x"]` | The room's horizontal position (wing A on the left, wing B on the right) |
> | `y = room_stats["floor_num"]` | The floor the room is on (y-axis = floor) |
> | `s = total × 50` | Dot area ∝ number of residents (rooms with more residents get bigger dots) |
> | `c = attack_rate` | Dot color corresponds to the attack rate (redder = more dangerous) |
>
> **When do you use a spot map?**
> A spot map works best when each observational unit (here, a "room") maps to an **x/y position** (or one that can be derived).
> It directly shows "where high-risk points cluster," offering finer detail than a heatmap.

```{figure} images/spatial_spot_map_guide.svg
:name: spatial-spot-map-guide
:alt: Guide to reading a spot map
:width: 100%

Four steps to reading a spot map: use color to find clusters, size to judge reliability, left-right to compare wings, and up-down to compare floors.
```

### Step 6 — Sorted Bar Chart of Wing Attack Rates

```python
spatial["label"] = spatial["floor"].astype(str) + "F-" + spatial["wing"]
spatial_sorted = spatial.sort_values("attack_rate", ascending=True)
ax.barh(spatial_sorted["label"], spatial_sorted["attack_rate"],
        color=["#e34a33" if ar > 50 else "#2c7fb8" for ar in spatial_sorted["attack_rate"]])
```

> A sorted horizontal bar chart makes the high-risk wings obvious at a glance. Conditional coloring (>50% shown in red) highlights the areas that need to be dealt with first.
> The wing furthest to the right = the most dangerous, and environmental sampling and investigation resources should be directed there first.

---

### Going Further: Once You Find a Difference Between Wings, What's Next?

Finding a high-attack-rate wing is only the first step. The investigator then has to answer: **"Why is that wing worse?"**

**Direction 1: Compare the spatial distribution of case fatality rates (CFR)**

Do wings with high attack rates also carry a higher risk of death? Or is the infection rate simply higher while the illness is similar in severity?

```python
# cfr was already computed in the spatial table in Step 2 of the notebook
# Use sns.heatmap to draw the CFR heatmap (demonstrated in Step 3 of the notebook)
heatmap_cfr = spatial.pivot(index="floor", columns="wing", values="cfr")
sns.heatmap(heatmap_cfr, annot=True, fmt=".1f", cmap="Reds")
```

**Direction 2: Compare the spatial distribution of a specific exposure factor**

The main transmission route for Legionnaires' disease is aerosolized contaminated hot water (showerheads, whirlpool tubs).
If a wing has a high attack rate, is shower usage in that wing also especially high?

```python
# Shower usage rate by wing
shower_by_wing = df.groupby("wing").agg(
    total        = ("case_id",     "count"),
    shower_users = ("shower_use",  "sum"),
).reset_index()
shower_by_wing["shower_pct"] = (shower_by_wing["shower_users"] / shower_by_wing["total"] * 100).round(1)
print(shower_by_wing)
```

**Direction 3: Prioritizing environmental sampling**

One of the ultimate goals of spatial analysis is to guide environmental sampling:
- The wing with the highest attack rate → prioritize collecting water samples from showerheads and hot-water pipes
- A wing with a low attack rate but adjacent to a high one → check whether they share the same piping
- An isolated room with a high attack rate → there may be an individual exposure source (such as a personal humidifier)

---

## Part 2: Choropleth Maps (`08_spatial_choropleth.ipynb`)

A choropleth (a shaded/graduated-color map) is a core skill for community-level outbreak investigation. This notebook uses **real government open data**:
- **Map boundaries**: [National Land Surveying and Mapping Center county/city boundaries SHP (TWD97 EPSG:3824)](https://maps.nlsc.gov.tw)
- **Case data**: [Taiwan CDC Legionnaires' disease statistics by area, age, and sex (2003–)](https://od.cdc.gov.tw)

### Normalizing 台/臺

One of the easiest traps when making a choropleth: **inconsistent glyphs for 台/臺**.

| County/City | 台 (common variant) | 臺 (orthodox form, used in government documents) |
|---|---|---|
| North | 台北市 | **臺北市** |
| Central | 台中市 | **臺中市** |
| South | 台南市 | **臺南市** |
| East | 台東縣 | **臺東縣** |

Other counties/cities (New Taipei, Taoyuan, Kaohsiung, Chiayi, etc.) **have no 台/臺 difference**.

```python
TAI_NORMALIZE = {
    "台北市": "臺北市",  "台中市": "臺中市",
    "台南市": "臺南市",  "台東縣": "臺東縣",
    # 2010 reorganization: Taipei County → New Taipei City, Taichung County/City → Taichung City …
    "臺北縣": "新北市",  "台北縣": "新北市",
    "臺中縣": "臺中市",  "高雄縣": "高雄市",
    "桃園縣": "桃園市",
}
def normalize_county(name):
    return TAI_NORMALIZE.get(str(name).strip(), str(name).strip())
```

Before the JOIN you must apply this function to **both sides** — the SHP and the CDC CSV — otherwise the map will have large blank areas.

### Workflow

```python
# 1. Download the SHP (ZIP) → unzip → geopandas.read_file()
gdf = gpd.read_file(shp_path).to_crs(epsg=4326)

# 2. Auto-detect the county-name column (NLSC SHP column names vary by version)
# 3. Download the CDC CSV → detect columns → normalize 台/臺

# 4. ID matching (the most important debugging step)
shp_counties  = set(gdf[county_col].apply(normalize_county))
data_counties = set(df["county"].unique())
print("Only in SHP:", sorted(shp_counties - data_counties))  # blank on the map
print("Only in data:", sorted(data_counties - shp_counties))   # not displayed

# 5. Aggregate by year + standardize by population → incidence rate per 100,000
annual = df.groupby(["year","county"])["cases"].sum().reset_index()
annual["rate_per_100k"] = annual["cases"] / annual["county"].map(COUNTY_POP) * 100_000

# 6. Static choropleth (latest year)
gdf_merged = gdf.merge(latest, left_on="county_norm", right_on="county", how="left")
gdf_merged.plot(column="rate_per_100k", cmap="Reds", legend=True, ax=ax)

# 7. Animated choropleth (year-by-year animation → GIF)
anim = FuncAnimation(fig, update_func, frames=years, interval=800)
anim.save("animation.gif", writer="pillow", fps=1, dpi=80)
```

> **Why use GeoPandas + matplotlib instead of Plotly?**
> The SHP format needs `geopandas.read_file()` to be read, and GeoPandas itself can draw a choropleth directly with `.plot()`.
> The animation (`FuncAnimation`) also requires matplotlib. Plotly is a good fit for GeoJSON + interactive maps; GeoPandas is a good fit for SHP + static/animated maps.

### Incidence Rate per 100,000 vs. Absolute Case Counts

A populous county (like Taipei City with 2.53 million people) naturally has more absolute cases, but that doesn't mean its risk is higher than a less populous county's.
When comparing counties, you **must always use the incidence rate per 100,000**:

```
Incidence rate (per 100k) = confirmed cases / county population × 100,000
```

---

## Exercises

- Exercise version: [`08_spatial_exercise.ipynb`](exercises/08_spatial_exercise.ipynb)
- Solution version (instructor): [`08_spatial_solution.ipynb`](solutions/08_spatial_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/08_spatial_solution.ipynb>)

## Common Mistakes

| Mistake | The right way |
|------|---------|
| Looking only at case counts, ignoring the denominator | Always compute "attack rate = cases / residents" |
| Using equal-sized dots despite different room sizes | Spot map dot size should reflect the number of residents |
| Treating dot size as meaningless and looking only at color | A room with few residents (e.g. 1/1 = 100%) has an unreliable attack rate and can't be compared directly with a large room |
| GeoJSON IDs not matching the data | Do a string comparison first (`set.difference()`) to confirm the IDs line up |
| Mixing different time windows in one chart | Standardize the analysis time period |
| Treating a spatial cluster as causation | Ecological fallacy: a high attack rate in a wing is only a hypothesis; exposure-factor analysis is needed to confirm the cause |

## Next Step

Spatial analysis tells us "where" it is worst.
In the next chapter (Ch09), we ask a harder question: **after onset, who survives longer? Which factors affect prognosis?** → survival analysis.
