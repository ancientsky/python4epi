---
title: "09 Buuin ang Bantay Santa Luz dashboard"
description: "Ginagawa ni Maya na isang self-contained na HTML screen para sa Local Health Board ang sampung linggo ng surveillance: mga headline number, epidemic curve, mapa ng mga rate at ang dengue threshold, at isang publish check na humaharang sa maliliit na cell at sa line-level data."
---

:::::{div}
:class: ph-story
*Miyerkoles, 30 Setyembre · City Health Office, Santa Luz*

::::{div}
:class: ph-say-jun
**Jun:** Ate Maya, tumawag ang opisina ng Mayor. Sa Biyernes ang pulong ng Local Health Board. Ang gusto ng Mayor: "isang screen, hindi apatnapung slide".
::::

::::{div}
:class: ph-say-maya
**Maya:** Isang screen? May epi curve ako, mapa, threshold chart, 7-1-7 table, mga resulta ng case-control…
::::

::::{div}
:class: ph-say-mon
**Doc Mon:** E di pumili ka. Dalawang minuto lang mayroon ang isang board member. Ilan, saan, pataas o pababa, at ano ang gagawin natin. At Maya — walang lalabas sa opisinang ito hangga't hindi ko nasusuri.
::::

::::{div}
:class: ph-say-tala
**Tala:** Kaya kong ilagay lahat sa iisang HTML file! Isasama ko ba ang buong line list, para ma-download ng mga tao ang datos?
::::

> Paano tayo bubuo ng isang screen na sumasagot sa mga tanong ng Board at nagpoprotekta sa bawat kapitbahay na nasa loob nito?
:::::

**[Buksan ang Bantay Santa Luz dashboard](/dashboard/)** — ang tapos na screen na
binubuo ng kabanatang ito. Gumagana ito kahit offline, sa phone at sa papel (isang
landscape na pahina). Kathang-isip ang Santa Luz at bawat numero rito, para sa kursong ito.

## Ano ang sinasagot ng mahusay na dashboard

Ang **dashboard** ay iisang pahina ng pinakamahahalagang numero at chart, ina-update ayon
sa iskedyul, para sa mga taong kailangang magdesisyon. Hindi ito report: walang mahabang
teksto, walang kabanata ng methods. Apat na tanong ang sinasagot nito, sa ganitong
pagkakasunod:

| Tanong | Ano ang sumasagot dito sa screen ng Santa Luz |
|---|---|
| **Ilan?** | mga headline tile: kaso, namatay, case fatality rate, mga linggong lampas sa threshold |
| **Saan?** | mapa ng **attack rate** bawat barangay (kaso bawat 10,000 residente), hindi hilaw na bilang |
| **Pataas o pababa?** | ang epidemic curve at ang lingguhang bilang ng dengue laban sa **epidemic threshold** nito |
| **Ano ang gagawin natin?** | maikli at may numerong listahan ng aksiyon para sa linggong ito |

Kasunod, mas maliit: sino ang tinamaan (edad at kasarian), gaano kabilis kumilos ang
sistema (7-1-7) at ano ang nagpasimula ng leptospirosis cluster (ang mga odds ratio mula
sa kabanata 05).

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 618
kasong naiulat hanggang 30 Set (230 leptospirosis, 388 dengue)
:::

:::{card} 21
namatay (20 leptospirosis, 1 dengue)
:::

:::{card} 8
sunod-sunod na linggong lampas sa threshold ang dengue, mula W32
:::

:::{card} 38%
ng 40 event ang pumasa sa tatlong 7-1-7 target
:::
::::
:::::

```{figure} images/scene_cesu_office.svg
:alt: Si Maya sa mesa niya sa opisina ng CESU, may laptop na nagpapakita ng tumataas na epidemic curve at si Tala na bituin sa screen, mga papel na form sa tabi niya, mapa sa dingding at electric fan.
:width: 100%
Ang sampung linggo ng mga form, paglilinis at pagsusuri ay nagiging iisang screen. Kathang-isip ang Santa Luz at ang CESU nito.
```

## Hakbang 1: ang mga headline number

Nagsisimula si Maya sa mga tile. Inilalarawan niya ang mga column at nagbibigay ng tatlong
gawa-gawang row.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May pandas DataFrame akong `ll`, isang row bawat kaso, na may mga column na `case_id`,
`disease` (`leptospirosis` o `dengue`), `outcome` (`alive` o `died`) at `hospitalised`
(0/1). Mga gawa-gawang row: `X-1, dengue, alive, 0` · `X-2, leptospirosis, died, 1` ·
`X-3, dengue, alive, 1`. Sumulat ng function na `compute_kpis(ll)` na nagbabalik ng
bilang ng kaso, namatay, na-ospital at ng case fatality rate sa % (isang decimal) para sa
bawat sakit at para sa buong lungsod.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
def compute_kpis(ll: pd.DataFrame) -> pd.DataFrame:
    """Kaso, namatay, na-ospital at CFR (%) bawat sakit, at isang row ng kabuuan ng lungsod."""
    kpis = ll.groupby("disease").agg(
        cases=("case_id", "size"),
        deaths=("outcome", lambda s: (s == "died").sum()),
        hospitalised=("hospitalised", "sum"),
    )
    kpis.loc["total"] = kpis.sum()
    kpis["cfr_pct"] = (100 * kpis["deaths"] / kpis["cases"]).round(1)
    return kpis
```
:::

:::{admonition} I-check natin
:class: ph-check
1. Patakbuhin ito sa tatlong gawa-gawang row ni Tala: dapat 2 kaso ang dengue, at 100% ang
   CFR ng leptospirosis.
2. Bilangin ang namatay sa ibang paraan, `(ll["outcome"] == "died").sum()`, at ikumpara sa
   row ng kabuuan.
3. Basahin ang **denominator** ng case fatality rate (CFR): namatay ÷ *kaso*, hindi ÷
   populasyon. Sa Santa Luz: leptospirosis 20 ÷ 230 = **8.7%**, dengue 1 ÷ 388 = **0.3%**.
:::

## Hakbang 2: tatlong chart, iisang patakaran

Sa notebook, gumagawa si Maya ng tatlong Plotly chart: ang **epidemic curve** ayon sa
linggo ng onset na may marka ng Bagyong Amihan, isang **mapa** ng dengue attack rate (ang
Talaba, 43.4, at Buhangin, 35.5 bawat 10,000, ang pinakamataas), at ang lingguhang bilang
ng dengue laban sa **epidemic threshold** (mean + 2 standard deviation ng parehong mga
linggo noong 2022–2025, kabanata 06). Linggo, hindi araw: ang daily count na 1 ay
magbubunyag ng petsa ng onset ng isang tao.

Iisang patakaran ang sinusunod ng bawat chart, isinulat nang minsan bilang function:

```python
def suppress(counts: pd.Series | pd.DataFrame, threshold: int = 5) -> pd.Series | pd.DataFrame:
    """Palitan ng '<5' ang bilang mula 1 hanggang threshold - 1 (nananatiling 0 ang zero)."""
    small = (counts > 0) & (counts < threshold)
    return counts.astype(object).mask(small, f"<{threshold}")
```

:::{admonition} Privacy muna
:class: ph-privacy
Lumalabas ng opisina ang dashboard, kaya ituring itong pampubliko. Ang **small-cell
suppression** ay ang pagtatago ng anumang bilang mula 1 hanggang 4 sa isang maliit na
grupo (isang barangay, isang linggo, isang age group) at ang hindi paglalabas ng rate
nito, dahil ang "isang kasong 65 pataas sa barangay na may 3,000 tao" ay taong kayang
pangalanan ng mga kapitbahay. Nananatiling zero ang zero: wala itong inilalarawang tao.
Puwedeng ipakita ang kabuuan ng buong lungsod para sa buong panahon, gaya ng sa mga
karaniwang bulletin. Mauuna ang mga patakaran sa pag-publish ng sarili mong opisina at
ang Data Privacy Act of 2012 (RA 10173); ang patakarang ito ang pinakamababang ginagamit
ng kurso.
:::

## Hakbang 3: iisang self-contained na HTML file

Dala ng isang **self-contained** na HTML file sa loob nito ang lahat ng kailangan nito:
teksto, style, datos at ang charting code. Nabubuksan ito kahit walang internet, mula sa
e-mail o sa USB stick. Pinupunan ng `string.Template` ng Python ang isang maliit na pahina
na may mga `$placeholder`; nagiging HTML fragment ang bawat Plotly figure sa pamamagitan ng
`fig.to_html(full_html=False, ...)`, at ang una lang ang may dalang Plotly library:

```python
figures = [fig.to_html(full_html=False, include_plotlyjs=(i == 0), config={"responsive": True})
           for i, fig in enumerate([fig_curve, fig_map, fig_thr])]
page_html = PAGE.substitute(
    title="Bantay Santa Luz",
    as_of=AS_OF,
    kpis="".join(f'<div class="kpi">{label}<b>{value}</b></div>' for label, value in tiles),
    figures="\n".join(figures),
    notes="".join(f"<li>{note}</li>" for note in notes),
)
```

Isinusulat ng notebook ang resulta sa **temporary folder** ng computer mo (mga 4.9 MB,
karamihan ay ang Plotly library) at ipinapakita kung nasaan ito. Buksan ito sa browser,
tapos sa phone mo. Isang eksepsiyon sa "kahit walang internet": nagda-download ang mapa ng
Plotly ng maliit na file ng outline ng mundo sa unang beses na gumuguhit ito, kaya sa
simpleng bersiyong ito, walang laman ang map panel kapag offline. Sariling mapa ang
iginuguhit ng buong dashboard sa ibaba at hindi nito kailangan ng internet.

## Hakbang 4: ang publish check ni Doc Mon

May ilang item sa checklist ni Doc Mon na kayang i-test ng code, bawat pagkakataon, sa
loob ng isang segundo:

```python
def publish_check(page: str) -> list[str]:
    """Ibalik ang mga problemang haharangin ni Doc Mon (walang laman na listahan = OK i-publish)."""
    problems = []
    if re.search(r"SLC-\d{4}", page):
        problems.append("may nakitang case ID: bawal i-publish ang line-level data")
    for column in ["case_id", "date_onset", "date_report"]:
        if column in page:
            problems.append(f"may nakitang column ng line list: {column!r}")
    small = re.findall(r"<td>\s*[1-4]\s*</td>", page)
    if small:
        problems.append(f"{len(small)} table cell na may 1-4 kaso: i-suppress ang mga ito")
    for must in ["Datos hanggang", "Mga tala sa datos", "synthetic"]:
        if must not in page:
            problems.append(f"kulang: {must!r}")
    return problems
```

Pasado ang pahina ni Maya. Tapos humingi ang staff ng Mayor ng "mas detalyado".

:::{admonition} Nagkamali si Tala
:class: ph-oops
Pinakiusapan ni Maya si Tala na *magdagdag ng table ng kaso ayon sa barangay at age
group, at ng button para i-download ang datos*. Idinagdag ni Tala ang
`pd.crosstab(ll["barangay"], ll["age_group"])` — hilaw na bilang na may dose-dosenang 1 at
2 — at inilagay ang `ll.to_json()` sa loob ng isang `<script>`: **ang buong line list**,
kasama ang case ID, edad at eksaktong petsa ng onset, na mababasa ng kahit sino gamit ang
*View source*. Mukhang pareho pa rin ang pahina. Pero hindi lumusot sa publish check:
hinarang nito ang mga case ID, tatlong column ng line list at 55 maliliit na cell. Ang
solusyon ay i-publish lang ang aggregate: mas malawak na table (bahagi ng lungsod × age group),
naka-suppress, at walang download ng case-level data kahit kailan.
:::

Hindi lahat ay kayang suriin ng code. Tao pa rin ang gagawa ng natitira sa checklist:

1. **Aggregate lang.** Walang pangalan, address, numero ng telepono, case ID o eksaktong petsa ng isang kaso — sa pahina *o* nakatago sa code nito.
2. **I-suppress ang maliliit na cell** (1–4 → "<5", walang rate) at huwag mag-publish ng kabuuang magagamit para ibawas at makuha ulit ang isang nakatagong cell.
3. **Rate, hindi bilang, sa mga mapa**, at nakasaad ang denominator.
4. **Tapat na axis**: nagsisimula sa zero ang bar chart; may label ang kulang pang huling linggo.
5. **Mga tala sa datos**: synthetic o totoo, source, mga depinisyon, ano ang itinago.
6. **Petsang "as of"** sa screen at sa printout.
7. **Na-test sa phone**, at binasa nang malakas nang minsan ng ibang tao.

:::{div}
:class: ph-game ph-game-publish-check
Bago mag-publish: walang pangalan o eksaktong address, i-suppress ang bilang na 1–4,
walang download ng case-level data, axis na nagsisimula sa zero, at may source line.
:::

## Ang buong dashboard: parehong ideya, mas pinalawak

Ang [Bantay Santa Luz dashboard](/dashboard/) sa site na ito ay binuo ng script na
`scripts/build_ph_dashboard.py` sa repository ng aklat, sa parehong mga hakbang ng notebook
mo: `load_data()`, `compute_kpis()`, `suppress_small_cells()`, `render_html()`. Lumalampas
pa ito sa apat na paraan:

- **Mga chart na iginuhit mismo.** Iginuguhit ang mga ito ng isang maikling script mula sa
  maliit na bloke ng mga nakapaloob na numero, kaya wala pang 0.1 MB ang buong pahina,
  gumagana offline at naipi-print sa iisang landscape na pahina.
- **Mas mahigpit na suppression.** Kapag naka-publish ang isang kabuuan at iisang maliit na
  cell lang ang nakatago sa isang column, may itinatagong pangalawang cell (may markang
  `x`), para walang makakuha ulit sa maliit na cell sa pamamagitan ng pagbabawas.
- **Mas maraming panel.** Edad at kasarian, 7-1-7 timeliness kasama ang pinakamadalas na
  bottleneck, ang mga odds ratio ng case-control, at ang forecast fan ng TimesFM mula sa
  [kabanata 07](07_forecast_timesfm.md) kapag naroon ang naka-cache na forecast nito.
- **Tatlong wika, light at dark, keyboard at touch.**

Ini-import ng notebook ang dalawa sa mga function nito at sinusuri kung pareho ang
headline number na ibinibigay nila at ng sa iyo.

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: mga dashboard**

1. Tanong ng Board: "saan pinakamalala ang dengue?". Ano ang ilalagay sa mapa?
   - Bilang ng kaso bawat barangay — laging mukhang pinakamalala ang malalaking barangay.
   - ✓ Kaso bawat 10,000 residente (attack rate) — patas nitong naikukumpara ang panganib.
   - Ang address ng bawat kaso — hindi kailanman sa pampublikong screen.
2. May 3 kaso ng dengue ang isang barangay. Ano ang ipinapakita ng pampublikong table?
   - 3 at ang rate nito — puwede iyang magturo sa isang pamilya.
   - ✓ "<5" at walang rate — sina-suppress ang bilang na 1–4, at ibabalik ito ng rate.
   - 0 — hindi iyon totoo.
3. Mas mababa ang bar ng huling linggo. Bumababa na ba ang dengue?
   - Oo, mas mababa ang bar.
   - ✓ Hindi pa alam — kulang pa ang huling linggo dahil sa reporting delay.
4. Nag-alok si Tala ng "download the data" na button na nasa loob ng pahina ang line list. Sabi ni Doc Mon…
   - Ayos lang kung maliit ang file.
   - ✓ Hindi — hindi kailanman puwedeng ilagay ang case-level data sa pampublikong pahina, kahit nakatago sa code.
:::

:::{admonition} Baon
:class: ph-baon
- Apat na tanong ang sinasagot ng dashboard: ilan, saan, pataas o pababa, ano ang
  gagawin.
- I-suppress ang bilang na 1–4 sa bawat maliit na grupo, rate ang imapa, at tatakan ng
  petsang "as of".
- Patakbuhin ang publish check bawat pagkakataon; tapos susuriin ito ng isang tao sa phone.

Buksan ang notebook: [](notebooks/09_dashboard.ipynb) · [Buksan ang dashboard](/dashboard/)
:::
