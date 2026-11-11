---
title: "08 Nasaan ito? Mga mapa"
description: "Iminamapa ni Maya ang dengue sa 24 na barangay ng Santa Luz — bilang ng kaso laban sa attack rate, class break at mga palette na ligtas sa color-blind, ang pabago-bagong maliliit na numero, isang join na tahimik na nawalan ng dalawang barangay — tapos iginuguhit ang totoong mapa ng 18 rehiyon ng Pilipinas at gumagawa ng mapang ligtas i-publish."
---

:::{div}
:class: ph-story
*Miyerkoles, 30 Setyembre · Tanggapan ng City Mayor*

**Mayor:** Ate Maya, hindi ko kailangan ng mga table. Sabihin mo lang: *saan* ang dengue?

**Maya:** Ang Ilog po ang may pinakamaraming kaso, Mayor…

**Doc Mon:** Ang Ilog din ang may pinakamaraming tao. Saan pinakamalamang na *magka*-dengue ang isang residente? Ibang mapa iyon.

**Aling Nena:** At pakiusap po — walang tuldok sa mga bahay namin. Malalaman ng mga tao kung kaninong anak ang may sakit.

> Saan ang dengue — at paano tayo guguhit ng mapang nagsasabi ng totoo nang walang itinuturong tao?
:::

```{figure} images/santa_luz_map_fil.svg
:alt: Ang kathang-isip na Santa Luz City sa tatlong bahagi: kabundukan sa hilaga, tabing-ilog sa kahabaan ng Ilog Marilag, at baybayin sa timog, na may marka ng CESU at mga health station.
:width: 100%
Ang Santa Luz City at ang tatlong bahagi nito. Kathang-isip ang lungsod, ang 24 na barangay nito at lahat ng numero nila.
```

## Bilang o rate?

Ang **choropleth** ay mapang kinukulayan ang bawat lugar ayon sa isang numero. Ang unang
desisyon ay *kung aling* numero.

- Sinasagot ng **bilang** (count) ang "saan ang trabaho?": ilang pasyente, ilang bahay ang
  pupuntahan ng mga 4S team.
- Sinasagot ng **attack rate** ang "saan ang panganib?": kaso ÷ populasyon × 10,000, ang
  tsansang naging kaso ang isang residente (bawat 10,000 tao).

Sa Santa Luz, ang **Ilog** (tabing-ilog) ang may pinakamaraming kaso ng dengue: 31. Pero
isa rin ito sa pinakamalalaking barangay, kaya 23.1 bawat 10,000 ang rate nito. Ang
**Talaba** (baybayin) ay may 29 na kaso sa 6,688 residente lang: **43.4 bawat 10,000**,
ang pinakamataas. Sunod ang Buhangin, 35.5. Sa mapa ng bilang, nagliliwanag ang
tabing-ilog; sa mapa ng rate, ang baybayin. Isa sa pinakakaraniwang pagkakamali sa mapa
ang pagmamapa ng hilaw na bilang na para bang ito ang panganib.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May GeoDataFrame akong `brgy` (24 na row; mga column na `barangay_id`, `barangay`, `band`,
`population`, `geometry`) at isang line list na `ll` (isang row bawat kaso; mga column na
`barangay_id`, `disease`). Gawa-gawang halimbawa: mga row ng `ll` na `("SL01", "dengue")`,
`("SL01", "dengue")`, `("SL02", "leptospirosis")`. Bilangin ang mga kaso ng dengue bawat
`barangay_id`, i-join ang mga bilang sa `brgy` **gamit ang `barangay_id`**, lagyan ng 0
ang barangay na walang kaso, at idagdag ang `attack_rate` = cases / population × 10,000.
Dapat 24 na row pa rin ang resulta.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
dengue_counts = ll[ll["disease"] == "dengue"].groupby("barangay_id").size().rename("cases")
brgy = brgy.merge(pop, on="barangay_id", how="left")
brgy = brgy.merge(dengue_counts, left_on="barangay_id", right_index=True, how="left")
brgy["cases"] = brgy["cases"].fillna(0).astype(int)        # 0 ang barangay na walang kaso, hindi missing
brgy["attack_rate"] = brgy["cases"] / brgy["population"] * 10_000
```
:::

:::{admonition} Suriin
:class: ph-check
1. **24 na row** pagkatapos ng join: `assert len(brgy) == 24`.
2. **Ang kabuuan**: dapat umabot sa lahat ng 388 kaso ng dengue ang suma ng mga bilang
   bawat barangay.
3. **Isang rate, mano-mano**: Talaba, 29 ÷ 6,688 × 10,000 = 43.4.
4. **Ang zero**: walang kaso ng dengue ang Bukid sa kabundukan, kaya 23 row lang ang
   ibinigay ng `groupby`. Kung walang `fillna(0)`, blangko ("walang datos") ang Bukid sa
   halip na 0.
:::

## Class break at kulay

Karaniwang pinapangkat ng choropleth ang mga value sa ilang **class**. Binabago ng mga
break ang mensahe:

- **Equal interval:** pare-pareho ang lapad ng mga class (dito, mga 11 bawat 10,000 ang
  bawat isa). Kapag 4 na class, 2 barangay lang ang napupunta sa pinakamataas.
- **Quantile:** pare-pareho ang bilang ng barangay sa bawat class (24 ÷ 4 = 6). Nagagamit
  ang bawat kulay, pero puwedeng magkalapit ang value ng dalawang magkatabing class.

Walang "tama" sa dalawa. Pumili nang sadya, at isulat ang mga break sa legend.

Kasinghalaga ang mga kulay. Gumamit ng **sequential** na palette, mapusyaw para sa mababa
at madilim para sa mataas, gaya ng `YlOrRd` o `viridis`. Nababasa ito nang sunod-sunod
kahit walang legend, at kaya nito ang color-blindness at ang black-and-white na pag-print.
Iwasan ang mga **rainbow** na palette (`jet`): wala silang natural na pagkakasunod, at
hinihila ng matingkad na dilaw sa gitna ang mata papunta sa mga *katamtamang* value.

:::{div}
:class: ph-game ph-game-map-paint
Rate ang imapa, hindi bilang; pumili ng class break nang sadya; gumamit ng palette na
mula mapusyaw hanggang madilim.
:::

## Palundag-lundag ang maliliit na numero

May 3,000–5,000 residente ang mga barangay sa kabundukan at iilang kaso lang. Ang Maligaya
ay may **1 kaso: 3.0 bawat 10,000**. Kapag nadagdagan ng isa pang kaso, dodoble ito sa
6.1. Kinukuwenta ng notebook ang exact 95% confidence interval ng bawat rate: sa Maligaya,
mula 0.1 hanggang 16.9; sa Talaba, mula 29.0 hanggang 62.3. Ang ibig sabihin ng malapad na
interval: **huwag i-ranggo ang barangay na iyon batay lang sa kulay nito**. Idagdag ang
mga bilang sa hover text o sa table sa tabi ng mapa.

## Isang interactive na mapa

Para sa screen, iginuguhit ng plotly ang parehong mapa na may hover label: barangay, band,
kaso, populasyon at rate. Kailangan nito ang mga polygon bilang GeoJSON at ang key na
nag-uugnay sa bawat row sa isang polygon, `featureidkey="properties.barangay_id"`. Hindi
tayo naglalagay ng background map tile: kathang-isip ang Santa Luz, at sadyang nasa gitna
ng dagat ang mga coordinate nito, para hindi ito kailanman mapagkamalang totoong lugar.

:::{admonition} Nagkamali si Tala
:class: ph-oops
Nagpadala si Jun ng mabilisang table ng bilang ng dengue ayon sa **pangalan** ng barangay,
mano-manong tinype. Ini-join ito ni Tala sa mapa **gamit ang pangalan**. Mukhang ayos ang
mapa. Pero ang tinype ni Jun ay `Santo Nino` (walang ñ) at `Tabing Ilog` (walang gitling).
Sa isang inner join, basta na lang nawala ang dalawang row na iyon: walang error, walang
babala. Blangko sana sa mapa ng Mayor ang dalawang barangay sa tabing-ilog na may 41 kaso
sa kabuuan.

Paano ito nahuli ni Maya:

```python
merged = brgy[["barangay_id", "barangay", "geometry"]].merge(jun, on="barangay", how="inner")   # ang join ni Tala
assert len(merged) == 24, f"join kept {len(merged)} of 24 barangays"
```

Pumapalya ang assert na may *"join kept 22 of 24 barangays"*, at ipinapakita ng outer join
na may `indicator=True` ang dalawang pangalang hindi nagtugma. Ang solusyon: **mag-join
gamit ang code** (`barangay_id`), hindi kailanman gamit ang tinype na pangalan. Ipinapakita
ng [kabanata 03](03_clean_linelist.md) kung paano gawing code ang magugulong pangalan.
:::

## Pag-zoom out: ang 18 rehiyon

Sa isang briefing, nakakatulong na ipakita ang buong bansa. Nasa `ph_regions.topo.json`
ang **totoong** hangganan ng 18 rehiyon bilang TopoJSON, isang siksik na pinsan ng
GeoJSON. Direktang nababasa ito ng `geopandas.read_file`. Ini-join natin ang totoong
statistics sa `ph_regions_stats.csv` gamit ang PSGC code na **`adm1_psgc`** at ina-assert
na 18 row ito.

Iminamapa ng notebook ang **population density noong 2024**. May **22,015 tao bawat km²**
ang NCR, mga 22 beses kaysa sa sumunod na rehiyon, ang CALABARZON (1,004). Kung equal-width
na class, iisa ang kulay ng lahat ng iba pang rehiyon, kaya quantile class ang gamit natin.
Kinuwenta ang density mula sa populasyon noong 2024 at sa sukat ng lupa, na parehong kinuha
mula sa
[Regions of the Philippines (Wikipedia)](https://en.wikipedia.org/wiki/Regions_of_the_Philippines)
sa pamamagitan ng research file ng aklat na ito. May sariling source URL ang bawat value sa
CSV; banggitin ito kasama ng numero.

Bawat mapang iginuhit mula sa file na ito ay may credit line: *Boundaries: NAMRIA, PSA via
OCHA COD-AB (CC BY-IGO); TopoJSON: faeldon/philippines-json-maps (MIT).*

Isa itong **context** map ng totoong bansa. Huwag kailanman iguhit dito ang kathang-isip na
Santa Luz.

:::{admonition} Privacy muna
:class: ph-privacy
Ang **dot map** ng mga bahay na may kaso ay listahan ng mga address na iginuhit bilang
tuldok. Kayang ituro ng sinumang nakakakilala sa kalye ang isang bahay. Sa loob ng CESU,
puwede itong gabay ng mga 4S team. Sa isang pampublikong pahina, kinikilala nito ang mga
kapitbahay, na siyang paksa ng [kabanata 02](02_privacy_first.md). Ang ipinapakita ng
pampublikong mapa ay **pinagsama-samang lugar** (mga barangay), at kahit ganoon, puwedeng
magturo sa isang tao ang barangay na kakaunti ang kaso. Ang patakaran ng aklat na ito:
**itago ang bilang na 1–4** (ipakita bilang "<5"), at itago rin ang **rate** nila, dahil
ibinabalik ng rate × populasyon ang bilang. Sa Santa Luz, 5 sa 24 na barangay ang
naitatago nito sa pampublikong mapa. Iginuguhit ito ng notebook na may guhit-guhit
(hatched), may label na "1–4 kaso: hindi ipinapakita".
:::

## Balik sa lamok

Sinasabi ng mapa sa mga 4S team *kung saan* pupunta. Ang gagawin nila roon ay hanapin at
sirain ang mga pinamumugaran ng lamok: anumang lalagyang may malinis at di-gumagalaw na
tubig.

```{figure} images/mosquito_4s_fil.svg
:alt: Ang 4S laban sa dengue sa paligid ng isang lamok na Aedes: search and destroy sa mga pinamumugaran, secure self-protection, seek early consultation, support fogging sa mga outbreak hotspot.
:width: 100%
Ang 4S laban sa dengue.
```

:::{div}
:class: ph-game ph-game-lamok-patrol
4S: Search and destroy ang mga pinamumugaran ng lamok, Secure self-protection, Seek early
consultation, Support fogging sa mga outbreak hotspot lang.
:::

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: mga mapa**

1. Ang Ilog ang may pinakamaraming kaso ng dengue, ang Talaba ang may pinakamataas na attack rate. Saan pinakamataas ang panganib ng isang residente?
   - Ilog — ito ang may pinakamaraming kaso, pero mas marami rin ang residente nito.
   - ✓ Talaba — hinahati ng rate ang bilang sa population at risk.
2. 22 row ang merged na table ng mapa mo sa halip na 24. Ano ang gagawin mo?
   - Wala, naiguguhit pa rin naman ang mapa — blangko o nawawala na ngayon ang dalawang barangay.
   - ✓ Hanapin ang mga pangalang hindi nagtugma at mag-join gamit ang `barangay_id`.
3. Anong palette ang dapat gamitin ng mapa ng dengue rate?
   - ✓ Sequential na palette, mapusyaw hanggang madilim — nababasa nang sunod-sunod at ligtas sa color-blind.
   - Rainbow na palette — walang natural na pagkakasunod at itinatampok ang mga value sa gitna.
4. May 3 kaso ang isang barangay. Sa pampublikong mapa, ipapakita mo ang…
   - Ang bilang at ang rate — puwedeng magturo sa isang tao ang maliit na cell.
   - ✓ "<5", at walang rate — ibinabalik ng rate na pinarami sa populasyon ang bilang.
:::

:::{admonition} Baon
:class: ph-baon
- **Rate** ang imapa para sa panganib, at bilang para sa trabaho. Sabihin kung alin ang
  ipinapakita mo.
- Mag-join gamit ang **code**, panatilihin ang mga lugar na zero ang kaso, at i-`assert`
  ang bilang ng row.
- Sequential na palette, sadyang mga break, credit line, at walang maliliit na cell o
  tuldok sa pampublikong mapa.

Buksan ang notebook: [](notebooks/08_maps.ipynb)
:::
