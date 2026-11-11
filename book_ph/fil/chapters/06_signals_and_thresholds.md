---
title: "06 Mga signal, threshold at 7-1-7"
description: "Inaalam ni Maya kung saan nanggagaling ang mga signal ng outbreak sa sistema ng Pilipinas, gumagawa siya ng epidemic threshold para sa dengue, nagbabasa ng endemic channel, inuunawa kung bakit laging mababa ang pinakabagong mga linggo, at sinusukat ang 7-1-7 timeliness."
---

:::{div}
:class: ph-story
*Miyerkoles, 12 Agosto · Opisina ng CESU, Santa Luz*

**Aling Nena:** Ate Maya, humuhupa na ang leptospirosis. Pero *lamok* naman ngayon — mataas ang lagnat ng mga bata sa Baybay, at puno ng kiti-kiti ang mga drum.

**Maya:** Dumarami na rin po ang mga form ng dengue. Outbreak na ba ito, o Agosto lang talaga?

**Doc Mon:** Magandang tanong. Ang "marami" ay pakiramdam. Ang alert threshold ay numero. At pag nag-alert ka na, tatakbo na ang orasan: pito, isa, pito.

> Kailan nagiging alert ang "maraming dengue" — at gaano kabilis tayong kumilos?
:::

## Dalawang uri ng signal

Ang **signal** ay anumang bagay na puwedeng mangahulugang may outbreak. Dalawang paraan
ang pagkuha nito sa sistema ng Pilipinas.

Ang **indicator-based surveillance** ay nagbibilang ng mga kasong pasok sa case definition,
gamit ang mga regular na ulat. Ito ang **PIDSR**, ang Philippine Integrated Disease
Surveillance and Response system, kasama ang web-based na information system nitong
**EDCS**. Ang mga disease reporting unit (ospital, RHU, klinika, laboratoryo) ay nag-uulat
ng Category I na sakit sa loob ng 24 oras, at ng Category II na sakit, gaya ng dengue,
linggo-linggo
([2020 Revised IRR ng RA 11332](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)).
Umaakyat ang mga ulat mula sa pasilidad papunta sa ESU ng lungsod o bayan, tapos sa PESU,
sa RESU at sa DOH Epidemiology Bureau
([WHO Joint External Evaluation, 2018](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf)).

Ang **event-based surveillance** naman ay sumasalo ng mga *di-pangkaraniwang pangyayari*
na walang form na nakalaan: kumpol ng maysakit na bata, tsismis, balita, isang text. Ito
ang **ESR** (Event-based Surveillance and Response) ng DOH, na umiiral na mula 2010
([WPSAR, 2015](https://ojs.wpro.who.int/ojs/index.php/wpsar/article/download/368/578?inline=1)).
Ang community reporting ng mga **barangay health worker** — ganito mismo ang ginagawa ni
Aling Nena — ay sinubukan (pilot) sa ilang bahagi ng Central Luzon noong 2024, at ayon sa
2024 Joint External Evaluation, prayoridad na gawin itong regular
([WHO JEE, 2024](https://www.who.int/publications/i/item/9789240116795)).

```{figure} images/reporting_ladder_fil.svg
:alt: Anim na antas ng pag-uulat, mula sa barangay health worker hanggang sa DOH Epidemiology Bureau, na may feedback na bumababa pabalik.
:width: 100%
Umaakyat ang mga ulat sa hagdan; dapat bumaba pabalik ang feedback. Bawat baitang ay umuubos ng oras.
```

Bawat baitang ay umuubos ng oras. Ayon sa Western Pacific office ng WHO, may **reporting
delay na 2–3 linggo** ang dengue data ng PIDSR
([WHO WPRO Dengue Situation Update 731, 2025](https://cdn.who.int/media/docs/default-source/wpro---documents/emergency/surveillance/dengue/dengue_202510021edf3700-e2a6-4e48-8e7c-acd86a16d530.pdf?sfvrsn=ba2e2c46_1)).
Tandaan ito; babalikan natin sa ibaba.

## Morbidity week

Binibilang ang dengue bawat **morbidity week**. ISO week ang gamit ng file natin: Lunes
hanggang Linggo, may label na gaya ng `2026-W32` (3–9 Agosto 2026). Hindi nito sinasabing
ito ang opisyal na kalendaryo ng PIDSR. Dahil sa mga column na `iso_year` at `iso_week`,
napagtatabi natin ang "parehong linggo" sa iba't ibang taon. Mula 2019-W01 hanggang
2026-W39 ang datos. **Synthetic** ito: kathang-isip ang Santa Luz, ang ulan nito at ang
mga kaso nito.

## Alert threshold

Sinasagot ng **epidemic threshold** ang tanong: *gaano kataas ang linggong ito sa isang
karaniwang taon?* Ito ang patakaran para sa series na ito:

1. Para sa ISO week *w*, kunin ang mga linggong *w*−1, *w* at *w*+1 ng **baseline years
   2022–2025**: 4 na taon × 3 linggo = 12 numero.
2. Threshold = ang **mean + 2 standard deviation** nila.
3. Huwag isama ang mga di-pangkaraniwang taon. Epidemic year ang 2019; ginulo ng COVID-19
   ang 2020–2021. Dapat *karaniwang* taon ang inilalarawan ng baseline.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May pandas DataFrame akong `weekly` na may mga column na `iso_year`, `iso_week` (1–53) at
`cases`. Mga gawa-gawang row: `(2022, 31, 9)`, `(2022, 32, 12)`, `(2023, 32, 7)`. Para sa
bawat ISO week w mula 1 hanggang 53, kuwentahin ang epidemic threshold = mean + 2 × sample
SD ng `cases` sa mga linggong w−1, w, w+1 ng mga taong 2022–2025 lang (ang window ng week 1
ay iikot pabalik sa week 52). Ibalik ito ayon sa linggo. Tapos sabihin mo kung aling linggo
ng 2026 ang unang lumampas sa threshold nito. Gawin mong madaling basahin para sa baguhan.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
BASELINE_YEARS = [2022, 2023, 2024, 2025]   # karaniwang taon lang: hindi 2019, 2020, 2021, at hinding-hindi 2026


def window_weeks(week):
    # Linggong w-1, w, w+1; ang week 1 ay iikot sa 52 at ang week 52 sa 1 (ang week 53 ay 52, 53, 1)
    if week == 53:
        return {52, 53, 1}
    return {(week - 2) % 52 + 1, week, week % 52 + 1}


def epidemic_threshold(weekly, years):
    base = weekly[weekly["iso_year"].isin(years)]
    rows = {}
    for week in range(1, 54):
        values = base.loc[base["iso_week"].isin(window_weeks(week)), "cases"]
        rows[week] = {"n_values": len(values), "baseline_mean": values.mean(),
                      "threshold": values.mean() + 2 * values.std(ddof=1)}
    return pd.DataFrame(rows).T
```
:::

Ang sagot: **unang lumampas sa threshold ang 2026 noong W32 (3–9 Agosto), 33 kaso laban sa
threshold na 17.5**. Nanatili itong lampas bawat linggo hanggang W39.

:::{admonition} Suriin
:class: ph-check
1. **Kuwentahin nang mano-mano ang isang linggo.** Inililista ng notebook ang 12 baseline
   value para sa W32 at kinukuwenta ulit ang mean + 2 SD gamit ang `statistics` module ng
   Python. Pareho silang 17.45.
2. **Ang laki ng window.** Dapat eksaktong 12 value ang bawat linggo 1–52.
3. **Ang kuwento.** Walang linggo ng 2026 bago ang W32 na lampas sa threshold, at lampas
   ang bawat linggo pagkatapos nito.
:::

## Ang endemic channel

Iginuguhit ng **endemic channel** ang karaniwang antas para sa bawat linggo ng taon. Sa
notebook, ang manipis na kulay-abong mga linya ay ang apat na baseline year, ang berdeng
linya ay ang mean nila (ang inaasahan natin), at ang orange na putol-putol na linya ay ang
threshold. Nasa ibabaw ang mga bar ng 2026; pula ang mga bar na lampas sa threshold. Bago
ang Bagyong Amihan (W29), mababa ang 2026 — mas tahimik kaysa karaniwan ang simula ng
taon. Tapos, mula W32, lumusot na ang mga bar sa channel.

:::{admonition} Nagkamali si Tala
:class: ph-oops
Sabi sa unang prompt ni Maya, "gamitin ang lahat ng taon sa file". Iyon nga mismo ang
ginawa ni Tala, kaya kasama sa baseline ang **2019** (isang epidemic year) at ang **2026
mismo**. Kapag nasa loob ng sarili nitong baseline ang isang epidemya, tumataas ang mean at
ang SD, kaya sumasabay sa pagtaas ng curve ang threshold. Tumalon ang threshold ng W32 mula
**17.5 papuntang 32.8**. Muntik nang hindi tumunog ang alarma (33 kaso), tapos **natahimik
ito noong W33 at W35** habang umaakyat ang epidemya.

Paano ito nahuli ni Maya: isang linya bago ang bawat pagkuwenta ng threshold,
`assert 2026 not in years`, at isang check na walang kilalang epidemic year sa listahan.
At binabasa niya nang malakas kay Doc Mon ang mga baseline year.
:::

## Bakit laging mukhang mababa ang pinakabagong mga linggo

Binibilang ng file ang mga kaso ayon sa **linggo ng onset**, pero nakakarating lang ang
kaso sa CESU kapag nakapagpakonsulta na ang pasyente at nakapag-notify na ang pasilidad.
Sa Santa Luz, 4 na araw ang median na delay mula onset hanggang ulat. Kaya laging kulang pa
ang pinakabagong mga linggo. Inuulit ito ng notebook gamit ang line list: parehong mga
linggo, binilang sa tatlong magkaibang araw.

| Linggo ng onset | W35 | W36 | W37 | W38 |
|---|---:|---:|---:|---:|
| alam noong 2 Set | 30 | 2 | 0 | 0 |
| alam noong 16 Set | 34 | 58 | 54 | 1 |
| alam noong 30 Set | 34 | 58 | 63 | 54 |

Noong 2 Setyembre, mukhang 2 kaso lang ang W36. Umabot ito sa 58. Kaya **kulang pa ang
huling linggo ng file natin, ang W39 (45 kaso)**, at kaya ito bumababa. Basahin ang
pinakabagong mga bar bilang "hindi bababa rito", hindi kailanman bilang "bumababa na".
Mas mahaba pa ang delay ng totoong PIDSR data, gaya ng nabanggit sa itaas.

:::{div}
:class: ph-game ph-game-threshold-watch
Sa lingguhang datos, kumilos sa araw mismong dumating ang bilang ng linggo: ma-detect sa
loob ng 7 araw mula emergence, mag-notify sa loob ng 1 araw, at tapusin ang early response
sa loob ng 7 araw.
:::

## 7-1-7: gaano kabilis tayong kumilos?

Ang paglampas sa threshold ay isang **detection**. Ang **7-1-7** ay target para sa mga
nangyayari bago at pagkatapos nito:

```{figure} images/timeline_717_fil.svg
:alt: Timeline mula emergence hanggang detection sa loob ng 7 araw, notification sa loob ng 1 araw, at natapos na early response sa loob ng 7 araw.
:width: 100%
7-1-7: ma-detect sa loob ng 7 araw mula emergence, mag-notify sa loob ng 1 araw mula detection, tapusin ang early response sa loob ng 7 araw mula notification.
```

Sa Pilipinas, nakita ng 2024 Joint External Evaluation na *ad hoc* lang ang paggamit ng
7-1-7; sa isang city ESU, 56% ng mga event ang na-detect sa loob ng 7 araw
([WHO JEE, 2024](https://www.who.int/publications/i/item/9789240116795)).

Nasa `signals_717.csv` ang 40 **synthetic** na event sa Santa Luz mula Enero 2025
hanggang Agosto 2026, bawat isa may apat na petsa at isang column na `bottleneck`.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May DataFrame akong `events` na may mga date column na `date_emergence`, `date_detection`,
`date_notification`, `date_response_complete` (gawa-gawang row: 2025-03-01, 2025-03-05,
2025-03-06, 2025-03-12). Idagdag ang tatlong delay sa buong araw, tatlong True/False na
column para sa mga 7-1-7 target (≤ 7, ≤ 1, ≤ 7) at isa para sa "pasado sa tatlo". I-print
kung ilang event ang pumasa sa bawat target, bilang count at porsiyento.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
events["days_to_detect"] = (events["date_detection"] - events["date_emergence"]).dt.days
events["days_to_notify"] = (events["date_notification"] - events["date_detection"]).dt.days
events["days_to_respond"] = (events["date_response_complete"] - events["date_notification"]).dt.days

events["detect_ok"] = events["days_to_detect"] <= 7
events["notify_ok"] = events["days_to_notify"] <= 1
events["respond_ok"] = events["days_to_respond"] <= 7
events["all_ok"] = events[["detect_ok", "notify_ok", "respond_ok"]].all(axis=1)
```
:::

| Target | Pasado | Hindi pasado |
|---|---:|---:|
| Detect ≤ 7 araw | 26 (65%) | 14 |
| Notify ≤ 1 araw | 31 (78%) | 9 |
| Respond ≤ 7 araw | 27 (68%) | 13 |
| **Pasado sa tatlo** | **15 (38%)** | 25 |

Median na delay: detection 6 na araw, notification 1 araw, response 6 na araw. Kung isa-isa,
mukhang "ayos naman" ang bawat target, pero 15 lang sa 40 event ang pumasa sa tatlo.

:::{admonition} Suriin
:class: ph-check
1. **Isang event, mano-mano.** Ang EV-040 ay ang dengue surge sa Baybay sa kuwento:
   emergence 3 Agosto (ang Lunes ng W32), detection 10 Agosto, notification 11 Agosto,
   tapos ang response 21 Agosto. Sa papel: 7, 1 at 10 araw. Detection ✓, notification ✓,
   response ✗. Dapat tugma rito ang mga column ni Tala.
2. **Lohika.** Hindi kailanman puwedeng mas marami ang "pasado sa tatlo" kaysa sa alinmang
   iisang target.
3. **Walang negatibong delay.** Kapag negatibo, may mali sa pagkaka-type ng petsa. Tawagan
   ang DRU.
:::

### Pagbasa sa column na bottleneck

Sinasabi ng porsiyento kung **gaano kadalas**; sinasabi ng column na `bottleneck` kung
**bakit**. Hatiin ito sa `"; "` at bilangin. Ang mga pangunahing dahilan sa Santa Luz:
*nagpatingin ang mga kaso sa pribadong klinikang hindi pa disease reporting unit ng PIDSR*
(5 event), *maraming sabay-sabay na trabaho* (5), *iisang DSO para sa 24 na barangay* (5),
at *napansin ng BHW ang cluster pero walang load para i-text ang CESU* (4). Wala sa mga ito
ang maaayos ng mas magandang code. Naaayos ang mga ito ng isang memo, isang back-up na DSO
at prepaid load. Dalhin ang listahang iyan sa Local Health Board.

:::{admonition} Privacy muna
:class: ph-privacy
Ang kailangan ng isang signal ay *ano, saan at kailan* — "limang batang may lagnat, Purok 3,
Baybay, mula Lunes". Hindi nito kailangan ng pangalan sa group chat. Isa sa mga bottleneck
sa Santa Luz ang *"na-notify sa personal na chat, hindi naitala"*: ipadala ang mga signal sa
opisyal na channel, para maitala ang mga ito at makita lang ng mga taong nangangailangan.
At gaya ng dati, huwag kailanman mag-paste ng line list sa AI chat. Ilarawan ang mga column
at gumamit ng gawa-gawang row.
:::

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: mga signal at threshold**

1. Bakit hindi isinama sa baseline ang 2019, 2020 at 2021?
   - ✓ Hindi sila karaniwang taon — magugulo ng isang epidemic year at dalawang taong ginulo ng COVID-19 ang "karaniwan".
   - Para bumilis ang code — walang kinalaman dito ang bilis.
2. Mas mababa nang malaki ang pinakahuling linggo ng series mo kaysa sa nakaraang linggo. Ano ang sasabihin mo?
   - Tapos na ang outbreak — hindi pa: kulang pa ang mga bagong linggo.
   - ✓ "Hindi bababa rito sa ngayon" — may mga huling ulat pang darating.
3. Na-detect ang isang event sa ika-6 na araw, na-notify sa ika-9 na araw, at natapos ang response sa ika-12 araw. Aling 7-1-7 target ang hindi naabot?
   - Detection — pasok sa 7 ang 6 na araw.
   - ✓ Notification — 3 araw matapos ang detection, 1 ang target.
   - Response — pasok sa 7 ang 3 araw matapos ang notification.
4. Nag-text ang isang BHW sa CESU tungkol sa ilang batang nilalagnat sa iisang purok. Ito ay…
   - ✓ Event-based surveillance — isang di-pangkaraniwang pangyayaring iniulat sa labas ng mga regular na form.
   - Indicator-based surveillance — iyon ay ang mga binibilang na case report mula sa mga pasilidad.
:::

:::{admonition} Baon
:class: ph-baon
- Kasinghusay lang ng baseline nito ang isang threshold: karaniwang taon lang, hindi
  kailanman ang season na sinusuri mo. I-assert ito.
- Laging kulang pa ang pinakabagong mga linggo. Basahin ang mga ito bilang "hindi bababa
  rito".
- Sukatin ang 7-1-7 sa bawat event, tapos basahin ang mga bottleneck. Karamihan ng solusyon
  ay hindi code.

Buksan ang notebook: [](notebooks/06_signals_and_thresholds.ipynb)
:::
