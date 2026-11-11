---
title: "05 Hanapin ang pinagmulan"
description: "Sinusuri ni Maya ang isang case-control study ng leptospirosis pagkatapos ng Bagyong Amihan: 2×2 tables, odds ratio na may 95% confidence interval, bota at doxycycline bilang protective factor, at isang confounder na inaayos gamit ang Mantel–Haenszel."
---

:::{div}
:class: ph-story
*Lunes, 10 Agosto · Barangay Ilog Health Station*

**Aling Nena:** Tapos na po, Ate Maya. Bawat kaso sa tabing-ilog, tig-dalawang kapitbahay. Pare-pareho ang tanong sa lahat.

**Maya:** Lumusong ba sa baha? Nakabota? May sugat? Sumama sa clean-up? Uminom ng doxycycline?

**Doc Mon:** At kung may daga malapit sa bahay. Ngayon, iisang sagot ang gusto ng City Health Officer: ano ang sasabihin natin sa mga tao bago ang susunod na baha?

**Maya:** Paglusong sa baha, siyempre…

**Doc Mon:** Hindi odds ratio ang "siyempre".

> Aling mga exposure ang talagang nagpataas — o nagpababa — ng odds ng leptospirosis?
:::

```{figure} images/scene_health_station.svg
:alt: Barangay health station na may watawat, upuang hintayan sa ilalim ng puno ng mangga at si Aling Nena sa pinto, handa na sa mga interview.
:width: 100%
Mga interview sa health station. Kathang-isip ang study, ang 360 kalahok nito at bawat numero.
```

## Bakit case-control study?

Sa **cohort study**, sinusundan mo ang lahat ng na-expose at hindi na-expose at
binibilang kung sino ang nagkakasakit. Para sa Santa Luz, ibig sabihin niyan ay
interbyuhin ang sampu-sampung libong residente para makahanap ng ilang daang kaso. Sa
**case-control study**, nagsisimula ka sa mga taong may sakit (**cases**), pumipili ng
kahawig nilang walang sakit (**controls**), at ikinukumpara kung gaano kadalas
**na-expose** ang bawat grupo.

Kinuha ng team ni Doc Mon ang 120 probable o confirmed na kaso ng leptospirosis na edad
15 pataas sa walong barangay sa tabing-ilog. Para sa bawat kaso, pumili sila ng dalawang
control mula sa parehong barangay: 240 control, 360 tao lahat
(`lepto_case_control.csv`).

## Ang 2×2 table

Nagiging **2×2 table** ang bawat exposure: rows para sa exposed at hindi exposed, columns
para sa cases at controls.

|  | Cases | Controls |
|---|---|---|
| **Exposed** | a | b |
| **Hindi exposed** | c | d |

Ang **odds ratio** (OR) ay $\frac{a \times d}{b \times c}$. Ang OR na 1 ay walang
association. Kapag lampas sa 1, mas karaniwan ang exposure sa mga kaso (risk factor).
Kapag mas mababa sa 1, mas bihira ito sa mga kaso (protective factor).

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
Sa `cc`, 0/1 ang `waded_floodwater` at `case`/`control` ang `status`. Gawin ang 2×2
table at i-compute ang odds ratio ng paglusong sa baha.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
t = pd.crosstab(cc["waded_floodwater"], cc["status"])
a, b = t.iloc[0, 0], t.iloc[0, 1]
c, d = t.iloc[1, 0], t.iloc[1, 1]
print(t)
print("OR ni Tala =", round(a * d / (b * c), 2))
```
**0.18** ang odds ratio.
:::

:::{admonition} Nagkamali si Tala
:class: ph-oops
Ang OR na 0.18 ay nagsasabing *pinrotektahan* ng paglusong ang mga tao. Matatawa si
Aling Nena. Sa dalawang paraan ito nahuli ni Maya:

1. **Basahin ang mga label.** Inaayos ng `crosstab` ang rows na 0 bago 1, kaya ang unang
   row ay "**hindi** lumusong". Binasa ni Tala ang mga cell ayon sa posisyon, kaya ang
   *a* niya ay ang mga kasong hindi exposed. Nabaligtad ang isang axis, kaya baligtad din
   ang OR: 0.18 = 1 ÷ 5.57. (Hindi magbabago ang OR kung pagpapalitin ang rows *at*
   columns, kaya i-check ang bawat axis.)
2. **I-sanity-check muna ang direksiyon.** **75%** ng mga kaso ang lumusong, laban sa
   **35%** ng controls. Dapat malayong lampas sa 1 ang OR.
:::

Ang ligtas na paraan ay ayusin ang pagkakasunod at pangalanan ang rows at columns, para
mabasa ng kahit sino ang table:

```python
def two_by_two(data: pd.DataFrame, exposure: str) -> pd.DataFrame:
    """2x2 table: rows exposed / hindi exposed, columns cases / controls."""
    table = pd.crosstab(data[exposure], data["case"]).loc[[1, 0], [1, 0]]
    table.index = ["Exposed", "Hindi exposed"]
    table.columns = ["Cases", "Controls"]
    return table
```

Para sa paglusong, ito ang lumalabas: a = 90, b = 84, c = 30, d = 156, at **OR = 5.57**.

## Gaano tayo kasigurado? Ang 95% confidence interval

May sampling error ang OR mula sa 360 tao. Ibinibigay ng **95% confidence interval**
(CI) ang saklaw ng mga value na tugma sa ating datos. Kung buong nasa itaas ng 1 ang
interval (o buong nasa ibaba ng 1), malabong nagkataon lang ito. Sa log scale gumagana
ang simpleng *Woolf* method:

$$95\%\ CI = \exp\left(\ln OR \pm 1.96\sqrt{\tfrac1a+\tfrac1b+\tfrac1c+\tfrac1d}\right)$$

```python
se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
low, high = math.exp(math.log(or_wading) - 1.96 * se), math.exp(math.log(or_wading) + 1.96 * se)
```

:::{admonition} I-check natin
:class: ph-check
1. **Dapat magkasundo ang mano-mano, ang scipy at ang statsmodels.** **5.57 (3.41–9.10)**
   ang ibinibigay ng tatlo.
2. **Basahin ang default sa documentation.** Kailangang sabihan ang `odds_ratio` ng
   scipy ng `kind="sample"`. Ang default nito ay ang *conditional* OR (5.54), na ibang
   estimator, hindi bug.
3. **Direksiyon:** lampas sa 1 ang OR, at mas maraming kaso kaysa control ang lumusong.
   Magkatugma sila.
:::

## Risk ratio o odds ratio?

Hinahati ng **risk ratio** (RR) ang *risk* ng mga exposed sa risk ng mga hindi exposed,
$\frac{a/(a+b)}{c/(c+d)}$. Kailangan diyan ang lahat ng at risk, na siyang ibinibigay ng
cohort. Sa case-control study, *tayo ang pumili* kung ilang control ang kukunin, kaya ang
"risk" sa table natin ay nakadepende sa design natin. Ipinapakita ito ng notebook: kapag
dalawang control bawat kaso, 3.21 ang pekeng "RR"; kapag isang control bawat kaso,
nagiging 2.37 ito, habang halos hindi gumagalaw ang OR (5.57 laban sa 5.18).
**Cohort → RR. Case-control → OR.** Kapag bihira ang sakit, malapit ang OR sa RR.

:::{div}
:class: ph-game ph-game-two-by-two
Ang rows ay exposure, ang columns ay outcome. Ikinukumpara ng cohort study ang risk (RR);
ikinukumpara ng case-control study ang odds ng exposure (OR), hindi kailanman RR.
:::

## Bota at doxycycline

Mahalaga lang ang bota sa mga taong nasa tubig, kaya **sa mga lumusong lang** (174 na
tao) itinanong iyon. Sa kanila, may **OR na 0.35** (95% CI 0.16–0.80) ang
pagsusuot ng bota. Ang pag-inom ng **doxycycline prophylaxis**, na ipinamigay sa mga
evacuation center at sa mga clean-up volunteer, ay may **OR na 0.43** (0.21–0.86).
Parehong protective factor ang mga ito *sa kathang-isip na outbreak na ito*. Walang
naging pagkakaiba rito ang pagkakita ng daga malapit sa bahay (OR 1.03, 0.67–1.60).

Para sa totoong paggamit ng doxycycline prophylaxis (sino ang dapat bigyan, kailan at
anong dose), sundin ang kasalukuyang gabay ng Department of Health at ng inyong mga
doktor, hindi ang aklat na ito.

## Ang confounder: paglusong o clean-up?

Napansin ito ni Doc Mon: *"Mas madalas lumusong ang mga clean-up volunteer, di ba? At may
sariling panganib ang clean-up."* Ang **confounder** ay ikatlong factor na may kaugnayan
sa exposure **at** risk factor din ng sakit nang mag-isa, kaya nahahalo ang epekto nito
sa crude OR. Sa mga control, 69.1% ng mga clean-up worker ang lumusong, laban sa 21.5%
ng lahat ng iba, at may OR na 3.20 ang clean-up work mismo.

Kaya nag-**stratify** si Maya: kinuwenta niya nang hiwalay ang OR ng paglusong para sa
mga sumama at hindi sumama sa clean-up work. Pagkatapos, pinagsama niya ang dalawa gamit
ang **Mantel–Haenszel** (MH) odds ratio, isang weighted average ng mga stratum OR:

| Stratum | a | b | c | d | OR |
|---|---:|---:|---:|---:|---:|
| Hindi sumama sa clean-up | 32 | 37 | 21 | 135 | 5.56 |
| Sumama sa clean-up | 58 | 47 | 9 | 21 | 2.88 |
| **Crude (lahat)** | 90 | 84 | 30 | 156 | **5.57** |
| **Mantel–Haenszel** | | | | | **4.28** (2.53–7.27) |

**Ano ang nagbago, at bakit?** Kapag hindi na pinagagalaw ang clean-up work, bumababa
ang OR ng paglusong mula 5.57 hanggang 4.28. Bahagi ng crude na numero ay galing sa
clean-up work, dahil mas madalas lumusong ang mga clean-up worker. Malakas pa ring
kaugnay ng leptospirosis ang paglusong. Magkaiba ang itsura ng dalawang stratum OR, pero
sa mga numerong ito, hindi masabi ng test kung higit pa ito sa nagkataon (p ≈ 0.24),
kaya makatwiran ang iisang MH summary. Mukhang delikado ang pagiging lalaki sa crude table
(OR 2.82) sa parehong dahilan: mas madalas lumusong ang mga lalaki. Hinahayaan ka ng
notebook na i-check iyan.

:::{admonition} I-check natin
:class: ph-check
Dapat makuha ulit ng `StratifiedTable` ng statsmodels ang MH OR na kinuwenta nang
mano-mano: pumapasa ang `math.isclose(st.oddsratio_pooled, or_mh)`, at idinadagdag nito
ang 95% CI (2.53–7.27).
:::

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: hanapin ang pinagmulan**

1. 0.18 ang lumabas na OR mo, pero 75% ng kaso at 35% ng control ang na-expose. Ano ang nangyari?
   - ✓ Nabaligtad ang isang axis ng table — basahin ang mga label ng row at column; 1 ÷ 0.18 ang totoong OR.
   - Protective ang exposure — hindi, kung mas madalas na-expose ang mga kaso kaysa sa mga control.
2. Sa case-control study, dapat mong i-report ang…
   - Risk ratio — ang mga imbestigador ang pumipili ng bilang ng control, kaya hindi totoo ang mga risk.
   - ✓ Odds ratio na may 95% confidence interval.
3. Pagkatapos i-stratify ayon sa clean-up work, bumaba ang OR ng paglusong mula 5.57 hanggang 4.28. Ibig sabihin…
   - Hindi mahalaga ang paglusong — malakas pa rin ang association nito, na may OR na mga 4.
   - ✓ Confounder ang clean-up work sa crude OR — nahalo rito ang bahagi ng epekto nito.
:::

## Ang sinabi ni Maya sa City Health Officer

:::{div}
:class: ph-story
*Biyernes, 14 Agosto · Opisina ng City Health Officer*

**Maya:** Malakas na kaugnay ng leptospirosis ang paglusong sa baha pagkatapos ng Amihan, kahit isinaalang-alang na ang clean-up work (adjusted OR na mga 4), at mas mababa nang malaki ang odds sa mga nakabota sa mga lumusong. Bago ang susunod na baha, dapat magbigay ang lungsod ng bota at wound care sa mga clean-up crew at sa mga residenteng kailangang lumusong, at sabihan ang sinumang lagnatin pagkatapos madikit sa baha na magpakonsulta agad. Kaugnay ng mas mababang odds ng sakit ang doxycycline prophylaxis sa study na ito, kaya dapat ituloy ang pamamahagi nito sa mga high-exposure group, ayon sa kasalukuyang gabay ng DOH.
:::

:::{admonition} Baon
:class: ph-baon
- Ayusin at pangalanan ang rows at columns ng bawat 2×2 table; i-check muna ang direksiyon
  gamit ang simpleng porsiyento bago pagkatiwalaan ang formula.
- Case-control → odds ratio na may 95% CI; i-check ito gamit ang ikalawang paraan.
- Mag-stratify ayon sa pinaghihinalaang confounder at ikumpara ang crude at
  Mantel–Haenszel OR.

Buksan ang notebook: [](notebooks/05_find_the_source.ipynb)
:::
