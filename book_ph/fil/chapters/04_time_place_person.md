---
title: "04 Panahon, lugar, tao"
description: "Gamit ang malinis na line list, nagde-define si Maya ng kaso, gumuguhit ng epidemic curve na may marka ng bagyo, kumukuwenta ng attack rate bawat 10,000 gamit ang totoong denominator, at inilalarawan kung sino ang nagkasakit at sino ang namatay."
---

:::{div}
:class: ph-story
*Lunes, 3 Agosto · video call sa Provincial Health Office*

**Doc Mon:** Malinis na ang listahan, mabuti. Ngayon, sabihin mo sa akin ang tatlong bagay: kailan, saan, sino.

**Maya:** Karamihan ng kaso ay taga-tabing-ilog, Doc. Walumpu't dalawang porsiyento!

**Doc Mon:** Walumpu't dalawang porsiyento ng *kaso*. Karamihan din ng tao sa Santa Luz ay nakatira sa tabi ng ilog. Denominator?

**Aling Nena:** *(nasa linya mula sa Ilog)* Doc, ang mga lalaking naglinis ng kanal po. Kilala ko silang lahat.

> Kailan nagkasakit ang mga tao, saan pinakamataas ang panganib, at sino ang tinatamaan?
:::

```{figure} images/scene_flood_riverside.svg
:alt: Mga bahay na nakatayo sa poste sa tabing-ilog pagkatapos ng bagyo, mga lalaking lumulusong sa kulay-tsokolateng baha na hanggang baywang na may dalang kalat, maliit na bangka, umuulan.
:width: 100%
Pagkatapos ng Bagyong Amihan, ilang araw na lumusong sa baha ang mga residente sa tabing-ilog. Kathang-isip ang Santa Luz at ang outbreak.
```

## Sino ang bibilangin bilang kaso?

Bago magbilang, nagkakasundo muna tayo sa **case definition**: maikling listahan ng
pamantayan na nagpapasya kung sino ang bibilangin, para pare-pareho ang pagbibilang ng
bawat health facility. Kadalasang hinahati ng surveillance ang mga kaso ayon sa
katiyakan. Ang mga definition sa ibaba ay **pinasimpleng bersiyon para sa pagtuturo** na
ginagamit sa kuwento ng aklat na ito. Nasa PIDSR Manual of Procedures at mga update nito
ang opisyal na pananalita
([catalogue entry](https://www.medbox.org/document/manual-of-procedures-for-the-philippine-integrated-disease-surveillance-and-response)).

| Antas | Leptospirosis (sa kuwentong ito) | Dengue (sa kuwentong ito) |
|---|---|---|
| **Suspect** | biglaang lagnat na may sintomas gaya ng sakit ng ulo, pananakit ng kalamnan (madalas sa binti) o mapupulang mata, matapos madikit sa baha, putik o hayop | lagnat na may sintomas gaya ng sakit ng ulo, sakit sa likod ng mata, pananakit ng katawan o kasu-kasuan o rashes, sa taong nakatira o bumisita sa lugar na may dengue |
| **Probable** | suspect + positibong rapid test | suspect + positibong NS1 rapid test o karaniwang findings sa blood count |
| **Confirmed** | suspect + positibong laboratory test sa reference lab | suspect + positibong laboratory test (RT-PCR) |

Sa freeze noong 30 Setyembre, sa 230 kaso ng leptospirosis, 119 ang confirmed, 52 ang
probable at 59 ang suspect. Sa 388 kaso ng dengue, 49 ang confirmed, 172 ang probable at
167 ang suspect. Matagal lumabas ang lab results, kaya madalas na ang "suspect" ay
"naghihintay pa ng lab" lang.

## Panahon: ang epidemic curve

Ang **epidemic curve** (epi curve) ay bar chart ng mga kaso ayon sa **petsa ng onset**:
isang bar bawat araw o linggo, walang puwang sa pagitan ng mga bar, at kasama ang mga
araw na walang kaso.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May datetime column na `date_onset` ang DataFrame kong `lepto` (gawa-gawang rows:
`2026-07-24`, `2026-07-24`, `2026-07-27`). Gumuhit ng epidemic curve: isang bar bawat
araw mula 15 Hulyo hanggang 31 Agosto 2026, **kasama ang mga araw na zero ang kaso**,
walang puwang sa pagitan ng mga bar. Markahan ang 18 Hulyo ng pulang putol-putol na
linya na may label na 'Landfall ng Bagyong Amihan', lagyan ng shading ang mga araw ng baha
18–20 Hulyo at ang clean-up 21 Hulyo – 2 Agosto.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
Ang susi ay ilatag ang daily counts sa buong kalendaryo:
```python
lepto = ll[ll["disease"] == "leptospirosis"]
days = pd.date_range("2026-07-15", "2026-08-31", freq="D")
daily = lepto["date_onset"].value_counts().reindex(days, fill_value=0)
```
Pagkatapos, iguhit ang mga bar gamit ang `ax.bar`, ang landfall gamit ang `ax.axvline` at
ang mga may shading na panahon gamit ang `ax.axvspan`.
:::

:::{admonition} I-check natin
:class: ph-check
1. Dapat tumugma ang kabuuan ng mga bar sa mga kasong **may** petsa ng onset: 228 + 2 na
   wala = 230.
2. Dapat tumugma ang lingguhang total sa outbreak report: ang ISO week 30–34 ay 35,
   **108**, 68, 15 at 2 kaso.
3. Ang peak day ay **27 Hulyo, na may 19 na kaso**, ang araw na nag-text si Aling Nena sa
   CESU.
:::

**Basahin ang hugis.** Tatlong klasikong hugis ang nakatutulong:

- **Point source**: sabay-sabay na na-expose ang lahat, gaya ng iisang kainan. Isang
  matulis na peak ang lalabas, mga isang incubation period ang lapad. Ang **incubation
  period** ay ang panahon mula impeksiyon hanggang sa unang sintomas.
- **Continuing common source**: parehong pinagmulan sa loob ng ilang araw o linggo.
  Tumataas ang curve, nananatiling mataas habang may exposure, saka bumababa.
- **Propagated**: hawaan ng tao sa tao, sunod-sunod na alon na mga isang henerasyon ang
  pagitan.

Iisang alon ang leptospirosis curve. Ang unang onset ay 22 Hulyo, apat na araw pagkatapos
ng landfall; ang median na onset ay **14 na araw** pagkatapos ng landfall. Mataas ang
kaso mula mga 24 Hulyo hanggang 6 Agosto, saka humuhupa pagdating ng kalagitnaan ng
Agosto. Tugma ito sa **continuing common source**: ilang araw ng paglusong noong baha at
clean-up, saka ang paghihintay dahil sa incubation. Ayon sa WHO, karaniwang 7–10 araw ang
incubation period ng leptospirosis, mula 2 hanggang 30 araw, at napakadalang itong
maipasa mula tao sa tao
([WHO Disease Outbreak News, 2022](https://www.who.int/emergencies/disease-outbreak-news/item/2022-DON403)),
kaya nakagugulat kung propagated ang pattern. Ganito rin ang delay sa totoong baha.
Pagkatapos ng mga baha noong huling bahagi ng Hulyo 2025, nagbabala ang DOH noong unang
bahagi ng Agosto na puwede pang tumaas ang kaso ng leptospirosis
([Philstar, 9 Ago 2025](https://www.philstar.com/headlines/2025/08/09/2464294/doh-warns-leptospirosis-cases-may-still-rise-coming-days)).

Iba ang itsura ng dengue. Karaniwang nagsisimula ang sintomas nito 4–10 araw pagkatapos
makagat ng lamok
([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue)),
pero kinailangan munang mangitlog ng lamok na *Aedes* sa naiipong tubig. Ilang linggong
tumataas ang lingguhang kaso ng dengue at umaabot sa peak sa ISO week 37 (63 kaso).

:::{div}
:class: ph-game ph-game-epicurve-builder
Ang iisang matulis na alon sa loob ng mga isang incubation period ay nagpapahiwatig ng
point source; ang alon na nananatiling mataas habang tuloy ang exposure ay nagpapahiwatig
ng continuing source; ang sunod-sunod na alon ay nagpapahiwatig ng hawaan ng tao sa tao.
:::

## Lugar: kailangan ng denominator ang attack rate

:::{admonition} Nagkamali si Tala
:class: ph-oops
Tanong ni Maya: *"I-compute ang dengue attack rate ayon sa bahagi ng lungsod (band)."* Sumagot si Tala ng
`dengue["band"].value_counts(normalize=True) * 100`: tabing-ilog 50.3%, baybayin 44.8%,
kabundukan 4.9%.

100% ang kabuuan ng mga numerong iyan. Iyan ang palatandaan. Ipinapakita nito **kung
nasaan ang mga kaso**, hindi **gaano kadelikadong tumira roon**. Bilang ng *kaso* ang
naging denominator. Isang dahilan kung bakit pinakamarami ang kaso sa tabing-ilog: ito
rin ang may pinakamaraming tao, 96,064 sa 186,000.
:::

Ang **attack rate** ay ang bilang ng bagong kaso sa isang grupo na hinati sa **mga taong
at risk** sa grupong iyon. Para sa isang lungsod, ibinibigay natin ito **bawat 10,000
residente**. Galing sa `santa_luz_barangays.csv` ang populasyon, hindi sa line list:

```python
population = barangays.groupby("band")["population"].sum()
cases = pd.crosstab(ll["band"], ll["disease"])

attack = cases.div(population, axis=0) * 10_000
attack.loc["city"] = cases.sum() / population.sum() * 10_000
```

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 19.7
leptospirosis bawat 10,000, tabing-ilog
:::

:::{card} 29.6
dengue bawat 10,000, baybayin
:::

:::{card} 12.4
leptospirosis bawat 10,000, buong lungsod
:::

:::{card} 20.9
dengue bawat 10,000, buong lungsod
:::
::::
:::::

| Bawat 10,000 | tabing-ilog | baybayin | kabundukan | lungsod |
|---|---:|---:|---:|---:|
| Leptospirosis | **19.7** | 5.6 | 2.6 | 12.4 |
| Dengue | 20.3 | **29.6** | 6.1 | 20.9 |

Kapag totoong denominator ang gamit, bumabaligtad ang kuwento ng dengue: ang
**baybayin** ang may pinakamataas na panganib, hindi ang tabing-ilog. **I-check** nang
mano-mano ang isang cell: 189 na kaso ng leptospirosis sa tabing-ilog ÷ 96,064 na
residente × 10,000 = 19.7.

Ayon sa barangay, pinakamataas ang leptospirosis rate sa Tabing-Ilog (29.8) at Ilog
(29.1), parehong nasa tabi ng ilog. Pinakamataas ang dengue rate sa mga barangay sa
baybayin na Talaba (43.4) at Buhangin (35.5). Magsimula sa barangay table, hindi sa
listahan ng kaso, para lumabas pa rin ang Bukid sa kabundukan, na walang kaso, na may
rate na 0. Gagawing mapa ng kabanata 08 ang mga numerong ito.

```{figure} images/santa_luz_map_fil.svg
:alt: Iginuhit na mapa ng kathang-isip na Santa Luz City: kabundukan sa hilaga, mga barangay sa tabing-ilog sa tabi ng Ilog Marilag sa gitna, at mga barangay sa baybayin sa timog.
:width: 100%
Ang tatlong bahagi ng Santa Luz City: kabundukan, tabing-ilog at baybayin. Kathang-isip na lungsod.
```

## Tao: sino ang nagkasakit, at sino ang namatay

Tinamaan ng leptospirosis ang **mga lalaking nasa edad ng paghahanapbuhay**: 155 sa 230
kaso ay lalaki (67%), at 32 ang median na edad. Tugma ito sa sinabi ni Aling Nena na
"ang mga lalaking naglinis ng kanal". Pantay ang dengue ayon sa sex (50% lalaki) at mas
bata, na may median na edad na 18. Iginuguhit ng notebook ang dalawa bilang
magkatabing age–sex chart.

Ang **case fatality rate** (CFR) ay ang namatay na hinati sa **kaso**. Sa pagkakataong
ito, ang mga kaso *mismo* ang tamang denominator, dahil ang tanong ay "sa mga
nagkasakit, ilan ang namatay?"

| | Kaso | Namatay | CFR | Na-ospital |
|---|---:|---:|---:|---:|
| Leptospirosis | 230 | 20 | **8.7%** | 143 (62.2%) |
| Dengue | 388 | 1 | **0.3%** | 206 (53.1%) |

:::{admonition} Privacy muna
:class: ph-privacy
Mabilis lumiit ang bilang kapag hinati ayon sa barangay, age group at sex. Ang cell na
gaya ng "isang namatay, babae, 65+, sa isang barangay" ay puwedeng tumuro sa iisang
pamilya. Sa loob ng CESU, ayos lang ang buong table. Bago mag-publish ng kahit ano,
sinu-suppress ang maliliit na bilang (ipinapakita ng kabanata 09 kung paano).
:::

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: panahon, lugar, tao**

1. Aling numero ang attack rate?
   - 50.3% ng kaso ng dengue ay nakatira sa tabing-ilog — bahagi iyan ng mga kaso; 100% ang kabuuan nito sa lahat ng bahagi ng lungsod.
   - ✓ 29.6 na kaso ng dengue bawat 10,000 residente ng baybayin — kaso na hinati sa mga taong at risk.
   - 8.7% ng kaso ng leptospirosis ang namatay — iyan ang case fatality rate.
2. Tumaas ang leptospirosis curve 4 na araw pagkatapos ng baha, nanatiling mataas nang mga dalawang linggo at humupa. Ang pinakatugma ay…
   - Point source — iyon ay iisang matulis na peak mula sa iisang sandali ng exposure.
   - ✓ Continuing common source — tumagal ang exposure hanggang sa baha at clean-up.
   - Hawaan ng tao sa tao — sunod-sunod na alon ang lalabas doon, at bihirang kumalat nang ganoon ang leptospirosis.
3. Bakit dapat isama sa epidemic curve ang mga araw na zero ang kaso?
   - ✓ Kapag inalis, napipiga ang panahon at nababago ang hugis na binabasa mo.
   - Mali ang mga araw na zero at dapat alisin — totoong impormasyon ang mga iyon.
:::

:::{admonition} Baon
:class: ph-baon
- Mag-define ng kaso bago magbilang: suspect, probable, confirmed.
- Basahin ang hugis ng epi curve laban sa incubation period at sa panahon ng exposure.
- Kailangan ng attack rate ang population at risk bilang denominator; kaso naman ang sa
  CFR. Hindi panganib ang bahagi ng mga kaso.

Buksan ang notebook: [](notebooks/04_time_place_person.ipynb)
:::
