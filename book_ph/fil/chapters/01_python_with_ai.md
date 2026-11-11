---
title: "01 Kumusta, Python?"
description: "Ang pinakakaunting Python na kailangan mo para mabasa ang code na isinulat ng AI: variables, lists, dictionaries, loops, if, functions at f-strings, unang silip sa line list gamit ang pandas, at kung paano basahin nang kalmado ang error."
---

::::{div}
:class: ph-story
*Martes, 28 Hulyo 2026 · 7:40 n.u. · CESU office*

:::{div}
:class: ph-say-maya
**Maya:** Anim na bagong form sa mesa ko, at isang tally sheet. *Isa, dalawa, tatlo...* Tatlong leptospirosis. Gagawin ko ba ito tuwing umaga?
:::

:::{div}
:class: ph-say-tala
**Tala:** Kaya kong bilangin iyan para sa iyo sa apat na linya ng Python.
:::

:::{div}
:class: ph-say-mon
**Doc Mon:** Mabuti. Pero Maya, kung hindi mo mabasa ang apat na linyang iyon, hindi mo mapipirmahan ang report. Matuto ka ng sapat na Python para *mabasa* ang isinusulat ni Tala.
:::

> Gaano karaming Python ang kailangan mo para mabasa, at ma-check, ang code na iba ang sumulat?
::::

Mas kaunti kaysa inaakala mo. Hindi mo kailangang *sumulat* ng programa mula sa memorya.
Kailangan mo lang makilala ang mga pitong building block, gaya ng pagkilala mo sa mga
bahagi ng case investigation form. Itinuturo ng kabanatang ito ang pitong iyon, gamit ang
anim na form ni Maya.

## Pitong building block

| Block | Ganito ang itsura | Isipin mo na parang |
|---|---|---|
| **Variable** | `barangay = "Ilog"` | label sa isang folder; ang `=` ay *ilagay ito rito* |
| **Text at numero** | `"Ilog"`, `34`, `True` | nasa loob ng quotes ang text; oo/hindi ang `True`/`False` |
| **List** | `ages = [34, 9, 41]` | isang column ng mga value, nakaayos |
| **Dictionary** | `{"disease": "dengue", "age": 9}` | isang form: mga label (keys) at mga sagot (values) |
| **Loop** | `for f in forms:` | isa-isang pagdaan sa patong ng form |
| **`if`** | `if f["disease"] == "dengue":` | tanong na oo/hindi; ang `==` ay nagtatanong ng *"pareho ba?"* |
| **Function** | `def percent(part, whole):` | recipe na may pangalan at puwedeng gamitin ulit; ibinabalik ng `return` ang resulta |

Dalawa pang bagay na makikita mo kahit saan. Ang **f-string**, `f"{n} cases"`, ay
naglalagay ng value sa loob ng pangungusap. Nagsisimula sa `#` ang **comment**; hindi
ito pinapansin ng Python, kaya tala ito para sa tao. Maraming comment ang magandang code
na isinulat ng AI.

Isang bitag: nagsisimula sa **0** ang bilang ng Python sa mga posisyon sa list. Ang unang
item ng `ages` ay `ages[0]`, hindi `ages[1]`. Karaniwan din sa AI code ang ganitong
"off-by-one" na pagkakamali.

## Ang mga form ni Maya, sa Python

Tina-type ni Maya ang anim niyang form bilang **list ng dictionaries**, isang dictionary
bawat form. Letra ang ginagamit niya, hindi pangalan, para sa bawat form. Imbento ang
lahat ng anim.

```python
forms = [
    {"form": "A", "barangay": "Ilog",   "disease": "leptospirosis", "age": 34, "waded": True},
    {"form": "B", "barangay": "Ilog",   "disease": "dengue",        "age": 9,  "waded": False},
    {"form": "C", "barangay": "Wawa",   "disease": "leptospirosis", "age": 41, "waded": True},
    {"form": "D", "barangay": "Sapa",   "disease": "dengue",        "age": 15, "waded": False},
    {"form": "E", "barangay": "Ilog",   "disease": "leptospirosis", "age": 52, "waded": False},
    {"form": "F", "barangay": "Talaba", "disease": "dengue",        "age": 23, "waded": True},
]
```

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May Python list akong `forms`. Bawat item ay dictionary na may keys na `form`,
`barangay`, `disease`, `age`, `waded` (True/False). Dalawang gawa-gawang item:
`{"form": "A", "barangay": "Ilog", "disease": "leptospirosis", "age": 34, "waded": True}` at
`{"form": "B", "barangay": "Ilog", "disease": "dengue", "age": 9, "waded": False}`.
Sumulat ng code na madaling intindihin ng baguhan na bibilang ng mga leptospirosis
form. Ipaliwanag ang bawat linya.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
lepto_count = 0                      # simulan ang tally sa zero
for f in forms:                      # tingnan ang bawat form, isa-isa
    if f["disease"] == "leptospirosis":   # nagtatanong ang == ng "pareho ba?"
        lepto_count = lepto_count + 1     # magdagdag ng isang tally mark

print(f"Mga leptospirosis form: {lepto_count}")
```
:::

Basahin ito na parang tally sheet ni Maya: magsimula sa zero, tingnan ang bawat form, at
**kung** leptospirosis ito, magdagdag ng isang marka. Ang mga linyang naka-indent (apat
na space papasok) ay bahagi ng loop at ng `if`; sa indentation nalalaman ng Python kung
ano ang nasa loob ng ano.

:::{admonition} Suriin
:class: ph-check
1. **Bilangin muna nang mano-mano**, bago ka magpatakbo ng kahit ano: leptospirosis ang
   form A, C at E. **3** iyon.
2. Patakbuhin ang code. Ipi-print nito ang `Mga leptospirosis form: 3`.
3. Gawing awtomatiko ang check: titigil nang may error ang `assert lepto_count == 3`
   kapag hindi magkatugma ang mga numero, at tahimik lang kapag tugma.
:::

## Nagkamali si Tala: "porsiyento ng ano?"

Sunod na tanong ni Maya: *ilang porsiyento ng mga leptospirosis form ang lumusong sa
baha?* Tumakbo ang code ni Tala nang walang kahit anong error at nag-print ng **33.3%**.

```python
waded_lepto = 0
for f in forms:
    if f["disease"] == "leptospirosis" and f["waded"]:
        waded_lepto = waded_lepto + 1
percent_waded = waded_lepto / len(forms) * 100
```

:::{admonition} Nagkamali si Tala
:class: ph-oops
Bilangin nang mano-mano. Mga leptospirosis form: A, C, E, kaya **3**. Sa mga iyon, ang
lumusong: A at C, kaya **2**. Dalawa sa tatlo ay **66.7%**, hindi 33.3%.

Tama ang numerator. Mali ang **denominator**: binibilang ng `len(forms)` ang **lahat ng
anim** na form, kasama ang dengue. Malinis tingnan ang code, tumatakbo nang maayos, pero
mali ang sagot. Ito ang pinakadelikadong uri ng pagkakamali, at bilang nang mano-mano
lang ang makahuhuli nito.
:::

Ang ayos ay maliit na **function** na tahasang input ang denominator, kaya kailangan mo
itong pagpasyahan tuwing gagamitin mo ito. Tumatanggi rin itong mag-divide sa zero.

```python
def percent(part: int, whole: int) -> float:
    # Ibalik ang part bilang porsiyento ng whole.
    if whole == 0:
        raise ValueError("Ang denominator ay 0: walang puwedeng kunan ng porsiyento.")
    return part / whole * 100


lepto_forms = [f for f in forms if f["disease"] == "leptospirosis"]   # lepto forms lang
waded_lepto = len([f for f in lepto_forms if f["waded"]])

answer = percent(waded_lepto, len(lepto_forms))
print(f"{waded_lepto} sa {len(lepto_forms)} leptospirosis form ang lumusong: {answer:.1f}%")
```

Ipi-print nito ang `2 sa 3 leptospirosis form ang lumusong: 66.7%`. Ang linyang
`[f for f in forms if ...]` ay isang-linyang loop: itinitira lang nito ang mga form na
pumasa sa test. Ang mga label na `: int` at `-> float` ay opsyonal na tala kung ano ang
pumapasok at ano ang lumalabas.

## Hanapin ang bug

Limang piraso ng code na isinulat ng AI, may isang mali ang bawat isa. I-tap ang linyang
mali.

:::{div}
:class: ph-game ph-game-bug-hunt
Kahit mukhang tama ang AI code, puwedeng mali pa rin: basahin linya-linya, patakbuhin sa
kasong kayang bilangin nang mano-mano, at basahin ang error message.
:::

## Mula anim na form hanggang 618 kaso: pandas

Para sa daan-daang row, may **pandas** ang Python: isang spreadsheet na kinokontrol mo sa
code. Sa notebook, bubuksan mo ang **malinis at de-identified** na line list ng Santa Luz.
Wala itong pangalan, telepono o address; ipinapakita ng [kabanata 02](02_privacy_first.md)
kung paano ito naging ganoon.

```python
import pandas as pd

df = pd.read_csv("data/synthetic/ph/santa_luz_linelist.csv")
print(df.shape)
print(list(df.columns))
df.head()
```

Ipi-print ng `df.shape` ang `(618, 18)`: 618 kaso at 18 column. Kopyahin nang
**eksakto** ang pangalan ng mga column kapag humihingi ka ng code kay Tala: `date_onset`,
hindi "onset date". Pagkatapos, ginagawa ng `df["disease"].value_counts()` ang ginawa ng
loop ni Maya, para sa buong file: **388** kaso ng dengue at **230** ng leptospirosis. Ang
check: `388 + 230 = 618`, ang bilang ng rows.

## Basahin nang kalmado ang error

Mensahe ang error, hindi insulto. Nang i-type ni Maya ang `df["Disease"]`, huminto ang
Python na may mahabang pulang text. Ang mahalagang bahagi ay ang **huling linya**:

```text
KeyError: 'Disease'
```

Sinasabi ng **error type** kung anong klaseng problema ito. Ang ibig sabihin ng
`KeyError` ay *"Hinanap ko ang key na ito, dito ay pangalan ng column, at wala ito."*
`disease` ang column, maliit na *d*: magkaibang letra para sa Python ang malaki at
maliit. Tatlong error na madalas mong makikita:

| Error | Kadalasang ibig sabihin |
|---|---|
| `KeyError` | mali ang spelling ng pangalan ng column o key |
| `NameError` | ginamit ang variable bago napatakbo ang cell na gumagawa nito |
| `SyntaxError` | kulang na bracket, quote o colon |

Kapag nalilito ka sa isang linya, ipaliwanag kay Tala ang **linyang iyon lang**: code,
hindi kailanman datos.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
Ipaliwanag mo ang linyang ito ng pandas sa isang baguhan, salita por salita, at sabihin
kung ano ang ipi-print nito para sa maliit na gawa-gawang table na may 3 row:
`df["disease"].value_counts()`.
:::

Pagkatapos, patakbuhin ang linya at ikumpara: ginagawa ba talaga nito ang sinabi ni Tala?

:::{admonition} Privacy muna
:class: ph-privacy
Kapag magpe-paste ka ng error message sa AI chat, tingnan muna ito. Puwedeng ipakita ng
error message ang mga value ng cell na pumalya, at sa totoong line list, puwedeng
pangalan ang mga value na iyon. I-paste ang **code at ang error type**, at palitan ng
gawa-gawang value ang anumang datos sa mensahe.
:::

## Mabilisang check

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: pagbasa ng Python**

1. `ages = [34, 9, 41]`. Ano ang `ages[1]`?
   - `34` — iyan ang `ages[0]`: nagsisimula sa 0 ang bilang ng Python.
   - ✓ `9` — ang posisyon 1 ay ang ikalawang item, dahil nagsisimula sa 0 ang bilang.
   - `41` — iyan ang `ages[2]`, o `ages[-1]`.
2. Tumakbo nang walang error ang code na kumukuwenta ng porsiyento. Ano ang una mong iche-check?
   - Wala: kapag walang error, tama na — hindi, tumakbo nang perpekto ang 33.3% ni Tala pero mali.
   - ✓ Ang denominator, sa maliit na halimbawang binilang nang mano-mano — "porsiyento ng ano?"
   - Ang kulay ng chart — may silbi mamaya, pero numero muna.
3. Sinasabi ng Python ang `KeyError: 'Barangay'`. Ano ang malamang na ayos?
   - ✓ I-check ang spelling at malalaking titik ng pangalan ng column — `barangay` ang nasa file, maliit na b.
   - I-install ulit ang pandas — maayos ang library; mali ang pangalan.
   - Burahin ang row na may error — tungkol sa pangalan ang `KeyError`, hindi sa row.
:::

:::{admonition} Baon
:class: ph-baon
- Sapat na ang pitong building block (variables, text at numero, lists, dictionaries,
  loops, `if`, functions) para *mabasa* ang karamihan ng analysis code na isinulat ng AI.
- Bilangin nang mano-mano ang maliit na halimbawa bago pagkatiwalaan ang isang numero.
  Laging itanong ang *"porsiyento ng ano?"*: hinati ng code ni Tala sa lahat ng form
  imbes na sa mga leptospirosis form lang.
- Basahin muna ang huling linya ng error. Kadalasan, maling spelling ng column ang ibig
  sabihin ng `KeyError`.

Patakbuhin mo mismo: [Buksan ang notebook](notebooks/01_python_with_ai.ipynb)
:::
