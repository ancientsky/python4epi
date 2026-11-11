---
title: "07 Dengue sa susunod na buwan: forecasting gamit ang TimesFM"
description: "Gumagawa si Maya ng forecast ng dengue para sa susunod na walong linggo: mga simpleng baseline muna, tapos ang zero-shot na time-series foundation model na TimesFM 3.0 sa isang tapat na rolling-origin backtest, ang pagsablay nito sa pag-arangkada ng outbreak, at kung ano ang pinapayagan ng lisensiya nito."
---

:::{div}
:class: ph-story
*Miyerkoles, 30 Setyembre · Opisina ng CESU, pagkatapos ng data freeze*

**Doc Mon:** Sa Biyernes ang pulong ng Local Health Board. Tatlong bagay ang itatanong nila: ilang kama, ilang fogging team, ilang NS1 kit para sa Oktubre at Nobyembre.

**Maya:** Ibig sabihin po… gusto nilang hulaan ko ang hinaharap?

**Doc Mon:** Hindi. Gusto nila ng range na mapagpaplanuhan, at tapat na sagot kung gaano ito kahusay.

**Tala:** Kaya kong patakbuhin ang isang forecasting model na natuto mula sa napakaraming time series!

**Doc Mon:** Ayos. Pero ipakita mo muna sa akin na mas magaling ito kaysa sa basta pagkopya ng nakaraang taon.

> Ilang kaso ng dengue ang dapat paghandaan ng Santa Luz sa susunod na walong linggo — at gaano natin mapagkakatiwalaan ang numerong iyan?
:::

## Para saan ang forecast

Sa isang health office, ang forecast ay **kasangkapan sa pagpaplano**, hindi hula ng
manghuhula. Ginagawa nitong "maghanda para sa mga 20 hanggang 60 kaso kada linggo sa
unang bahagi ng Oktubre, at bababa pagkatapos" ang "mataas ang dengue", para makapagbukas
ng kama ang ospital, makapag-iskedyul ang lungsod ng 4S at fogging team, at makapag-order
ng test kit ang botika. May **tatlong bagay** ang mahusay na forecast: isang numero, isang
range, at isang track record.

## Baseline muna

Ang **baseline** ay ang pinakasimpleng forecast na kayang gawin sa papel ng isang pagod na
DSO. Dapat itong talunin ng anumang model, kung hindi ay hindi ito sulit.

- **Last value:** ang susunod na linggo = ang linggong ito, inulit.
- **Seasonal naive:** ang susunod na mga linggo = ang parehong mga linggo noong nakaraang
  taon.

Para patas ang paghusga, gumagamit tayo ng **rolling-origin backtest**: nagkukunwari tayong
nakatayo sa isang lumipas na linggo (ang **origin**), gumagawa ng forecast para sa
susunod na 8 linggo gamit lang ang alam noon, at saka lang ikinukumpara sa totoong
nangyari. Ginagawa natin ito tuwing ikalawang linggo mula 2023-W01 hanggang 2026-W31:
**94 na forecast**. Ang score ay ang **mean absolute error** (MAE): ang karaniwang laki ng
sablay, sa kaso kada linggo.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May NumPy array akong `y` ng lingguhang bilang ng dengue, sunod-sunod ayon sa oras
(gawa-gawang halimbawa: `[5, 9, 11, 4, ...]`, mahigit 52 linggo). Para sa forecast na
ginawa sa row `o` (`y[:o]` lang ang alam natin), gusto ko ang susunod na `H = 8` linggo
mula sa dalawang baseline: "last value" (ulitin ang `y[o-1]`) at "seasonal naive" (kopyahin
ang `y[o-52 : o-52+8]`). Gawin ito para sa isang listahan ng origin at ibigay ang MAE
laban sa totoong value. Magdagdag ng check na kaya kong gawin nang mano-mano.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
H = 8                                             # forecast horizon: 8 linggo
first, last = row_of["2023-W01"], row_of["2026-W39"] + 1
origins = list(range(first, last - H + 1, 2))     # tuwing ika-2 linggo; hindi lalampas sa 2026-W39 ang dulo ng bawat forecast
actual = np.stack([y[o:o + H] for o in origins])  # shape (94, 8): ang totoong nangyari

last_value = np.stack([np.repeat(y[o - 1], H) for o in origins])
seasonal_naive = np.stack([y[o - 52:o - 52 + H] for o in origins])  # walang ISO week 53 pagkatapos ng 2020
```
:::

:::{admonition} I-check natin
:class: ph-check
1. Pumili ng isang origin at tingnan: inuulit ba talaga ng "last value" ang linggo *bago*
   ang origin? Kinokopya ba ng "seasonal naive" ang parehong ISO week isang taon bago?
2. Dapat huminto ang bawat history sa origin nito: `len(context) == o`. Kung nakikita ng
   forecast ang mismong mga linggong hinuhulaan nito, walang saysay ang score nito.
:::

## Isang zero-shot na foundation model: TimesFM 3.0

Ang **TimesFM** ay isang **time-series foundation model** mula sa Google. Minsan itong
sinanay sa napakalaking koleksiyon ng time series. Ginagamit natin ito nang
**zero-shot**: walang training sa datos natin, "heto ang history, ibigay mo ang susunod
na 8 linggo" lang. Nagbabalik ito ng median na forecast at siyam na **quantile**; ang 0.1
at 0.9 na quantile ang hangganan ng **80% prediction interval**, ang range na dapat
maglaman ng totoong value mga 8 beses sa 10.

Ipinapakita ng notebook ang totoong mga tawag, na tumatakbo sa Google Colab pagkatapos ng
`pip install "timesfm[torch]"` (minsan lang nada-download ang weights, mga 1.3 GB):

```python
from timesfm3 import ModelConfig, TimesFM3Evaluator

config = ModelConfig(
    checkpoint_path="google/timesfm-3.0-pytorch",  # weights sa Hugging Face (~1.3 GB, sa unang run lang)
    per_core_batch_size=32,                        # ilang series bawat forward pass
    device=tsfm.default_device(),                  # "cuda" kung GPU runtime, kung hindi ay "cpu"
)
model = TimesFM3Evaluator(config)
```

```python
contexts = tsfm.rolling_origin_contexts(y, origins)
bt = tsfm.forecast_batch(model, contexts, H, cache_key="backtest_cases", cache_file=CACHE)
```

Tinatawag ng `tsfm.forecast_batch` (mula sa `epi_learning` package ng aklat na ito) ang
`model.predict_batch(...)` kapag naka-load ang model. Kapag binubuo ang website na ito,
hindi dina-download ang model; inuulit ng helper ang mga forecast na na-save mula sa isang
totoong run ng TimesFM 3.0 sa parehong notebook, at ipinapakita ng bawat cell kung aling
daan ang tinahak nito.

## Ang scoreboard

| Panahon | Last value | Seasonal naive | TimesFM 3.0 | Saklaw ng 80% band |
|---|---:|---:|---:|---:|
| Karaniwang taon 2023–2025 (75 forecast) | 4.76 | 4.31 | **3.50** | 79% |
| 2026, ang taon ng bagyo (19 forecast) | 6.22 | **5.21** | 5.32 | 72% |

*MAE sa kaso kada linggo, average sa 8 linggong susunod.*

Sa karaniwang mga taon, malinaw na TimesFM ang pinakamahusay, at tapat ang 80% band nito.
Noong 2026, **hindi ito mas magaling kaysa sa pagkopya ng nakaraang taon**. Ito ang
pinakamahusay para sa susunod na linggo (MAE 1.97) pero napag-iiwanan pagdating ng ika-8
linggo (10.08 laban sa 8.68 ng seasonal naive). Natakpan sana ito ng iisang kabuuang
average. **Laging i-score nang hiwalay ang di-pangkaraniwang panahon.**

:::{admonition} Nagkamali si Tala
:class: ph-oops
Humingi si Maya ng "mas magandang baseline: ang average ng parehong linggo sa lahat ng
taon". Nakakuha ang bersiyon ni Tala ng MAE na **3.27** sa lahat ng 94 na forecast, mas
mahusay pa kaysa sa 3.86 ng TimesFM sa parehong mga forecast. Isang tanong lang ang
ibinato ni Doc Mon: *"Aling mga taon ang pumasok sa average na iyan?"* Lahat, **kasama ang
mismong mga linggong hinuhulaan**. Iyan ang **leakage**: nakita na ng forecast ang sagot.
Kapag ang tatlong taon lang *bago* ang bawat origin ang ina-average, **3.95** ang lumalabas,
medyo mas masama kaysa sa 3.86 ng TimesFM.

Mas tahimik na daya ang iulat lang ang **pinakamagandang** linggo. Ang pinakamahusay na
origin ng TimesFM ay may MAE na 0.54; ang pinakamasama (2026-W31), 31.50. Ang tapat na
numero ay ang average ng lahat, 3.86.

Paano mahuhuli ang dalawa: itanong *"magagawa ba ang forecast na ito noong araw na iyon?"*
at iulat ang average ng bawat origin, kasama ang pinakamasama.
:::

## Kapag umarangkada ang outbreak

Ang pinakamahalagang mga linggo ay iyong lumiliko ang curve. Sa history hanggang
2026-W31, mga **10 kaso kada linggo** ang forecast ng TimesFM. Ang dumating sa sumunod na
apat na linggo: **33, 28, 48 at 34**. Wala ni isa sa sumunod na walong linggo ang pumasok
sa 80% band nito. Mula W32, 29% ng mga linggo ang nasaklaw ng band; mula W34 lang, nang
nasa history na ang surge, nito nasaklaw ang lahat.

Hindi sira ang model. Ang alam lang nito ay ang *karaniwang* susunod na gagawin ng mga
dengue curve. Hindi nito malalaman na binaha ng bagyo ang lungsod tatlong linggo bago
nito.

**Makakatulong ba ang ulan?** Sa synthetic na series na ito, nauuna ang ulan sa mga kaso
nang mga 7 linggo, at tumatanggap ang TimesFM 3.0 ng rainfall bilang **covariate**. Kasama
ang rainfall, halos hindi gumalaw ang MAE ng backtest (3.50 → 3.47 noong 2023–2025,
5.32 → 5.27 noong 2026), at mula W31, nanatili ang forecast sa mga 9–12 kaso kada linggo,
kahit nasa history na ang ulan ng Amihan, ang pinakamaulang linggo sa buong series.
May silbi lang ang covariate kung napatunayan mo ito sa parehong backtest.

:::{div}
:class: ph-game ph-game-forecast-guess
Husgahan ang forecast laban sa mga simpleng baseline, iulat ang error at uncertainty
nito, at sabihin kapag may nagbagong hindi nakikita ng model.
:::

## Ang forecast para sa Oktubre at Nobyembre

Mula sa lahat ng datos hanggang 2026-W39, bumababa ang median ng TimesFM mula **42 kaso sa
W40 (80% interval 24–63)** papuntang **16 sa W47 (6–44)**. 215 kaso ang kabuuan ng mga
lingguhang median para sa walong linggo; 75 ang parehong walong linggo noong 2025.

:::{admonition} I-check natin
:class: ph-check
1. **Kumpleto na ba ang huling linggo?** Hindi pa: inuulat pa ang W39 (45 kaso) (tingnan
   ang [kabanata 06](06_signals_and_thresholds.md)). Mula sa datos hanggang W38, 53 kaso
   ang inaasahan ng model para sa W39. Kapag hindi isinama ang W39, tumataas ang forecast
   ng W40 mula 42 papuntang 46. Kapag ginagalaw ng pinakahuling linggo ang forecast,
   sabihin ito.
2. **Malapad ba ang band?** Oo, at dapat lang: ang 6 hanggang 44 kaso sa W47 ay isang
   tapat na "hindi namin alam nang eksakto".
3. **Ikumpara sa baseline.** 75 kaso sa 8 linggo ang sabi ng seasonal naive. Ganyan ang
   itsura ng karaniwang Oktubre–Nobyembre, hindi ng taong ito.
:::

Ang isinulat ni Maya para sa Board: *"Maghanda para sa mga 20 hanggang 60 kaso ng dengue
kada linggo sa unang bahagi ng Oktubre, na malamang bababa hanggang Nobyembre. Ia-update
namin ito linggo-linggo; mababago ito ng bagong bagyo o ng pagdami ng severe na kaso."*

:::{admonition} Ang lisensiya, sa simpleng salita
:class: warning
Apache-2.0 ang **code** ng TimesFM. Ang **weights ng TimesFM 3.0** ay nasa ilalim ng
**TimesFM Non-Commercial License v1.0**: para sa research, evaluation at pagtuturo,
**bawal sa commercial at production na gamit**
([lisensiya sa Hugging Face](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE)).
Apache-2.0 ang mas lumang weights ng **TimesFM 2.5**
([model card](https://huggingface.co/google/timesfm-2.5-200m-pytorch)), at itinuturo ng
Google ang TimesFM sa BigQuery (Google Cloud) para sa opisyal na suporta
([TimesFM sa GitHub](https://github.com/google-research/timesfm)).

Para sa isang health office ng gobyerno, ibig sabihin nito: pasok ang pag-aaral,
pag-explore at pag-backtest sa lumang datos — gaya ng kabanatang ito. Hindi pasok ang
paggamit ng mga forecast ng 3.0 sa isang regular na early-warning system o sa isang
pampublikong bulletin. **Suriin ang lisensiya, at ang mga patakaran ng opisina mo, bago
ang anumang operational na gamit.** Hindi ito legal advice.
:::

:::{admonition} Privacy muna
:class: ph-privacy
**Lingguhang bilang** lang ang kailangan ng forecast, hindi kailanman ang line list.
Aggregate data ang lingguhang kabuuan ng isang buong lungsod. Gayunman, patakbuhin ang
model sa notebook mo, at huwag i-paste sa AI chat ang mga surveillance table ng opisina
mo. Tanungin si Tala gamit ang gawa-gawang numero, gaya sa itaas.
:::

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: forecasting**

1. May MAE na 5.3 noong 2026 ang isang bagong model. Mahusay ba ito?
   - Oo, maliit ang 5.3 — maliit kumpara saan?
   - ✓ Kung tatalunin lang nito ang mga baseline sa parehong mga linggo — 5.2 ang score ng seasonal naive dito.
2. Nakakuha ng 3.27 ang same-week average ni Tala, mas mahusay pa kaysa sa TimesFM. Ano ang mali?
   - ✓ Leakage — kasama sa average ang mismong mga linggong hinuhulaan.
   - Wala — madalas mahusay ang simpleng paraan, pero nakita na nito ang sagot.
3. Bakit hindi nahuli ng TimesFM ang pag-arangkada pagkatapos ng W31?
   - Kailangan pa nito ng training — zero-shot ito; hindi training ang problema.
   - ✓ Ang alam lang nito ay kung paano karaniwang nagpapatuloy ang mga curve; hindi nito nakitang paparating ang epekto ng bagyo.
4. Puwede bang gamitin ng isang city health office ang weights ng TimesFM 3.0 sa regular nitong early-warning system?
   - Oo, open source ang code — Apache-2.0 ang code, pero hindi ang weights ng 3.0.
   - ✓ Hindi, sa ilalim ng non-commercial at non-production na lisensiya ng weights ng 3.0 — suriin muna ang lisensiya.
:::

:::{admonition} Baon
:class: ph-baon
- Baseline muna: dapat talunin ng model ang "last value" at ang "parehong mga linggo
  noong nakaraang taon" sa isang patas na rolling-origin backtest, na may hiwalay na score
  para sa di-pangkaraniwang panahon.
- Huwag hayaang makita ng forecast ang sagot, at iulat ang average ng lahat ng origin,
  hindi ang pinakamagandang linggo.
- Ang forecast ay range para sa pagpaplano. Hindi nito nakikita ang bagyo o ang mga kasong
  hindi pa naiuulat — at suriin ang lisensiya bago ang operational na gamit.

Buksan ang notebook: [](notebooks/07_forecast_timesfm.ipynb)
:::
