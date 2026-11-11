---
title: "03 Mula sa magulong line list tungo sa malinis na datos"
description: "Ginagawa ni Maya na malinis at de-identified na line list ang magulong export ni Jun pagkatapos ng bagyo, gamit ang pandas at tulong ng AI, at chine-check ang bawat hakbang, kasama ang pagkakamali ni Tala sa petsa."
---

:::{div}
:class: ph-story
*Huwebes, 30 Hulyo · CESU office, Santa Luz City Health Office*

**Jun:** Ate Maya, heto ulit ang export, sa computer lang ng opisina ngayon. Lahat ng fever notification mula noong bagyo.

**Maya:** Salamat, Jun! Bakit anim na iba't ibang paraan nakasulat ang Ilog?

**Jun:** Anim? Ay, maraming kamay po ang nag-type. Ospital, health stations, kami. May nagsusulat ng `Brgy. Ilog`, may `ILOG`. Pati petsa… may kanya-kanyang style ang bawat encoder.

**Doc Mon:** Bago magbilang ang kahit sino: alisin ang mga pangalan sa table. Saka linisin. Saka patunayang malinis na.

> Paano natin gagawing line list na mapagkakatiwalaan — at maibabahagi — ang export ni Jun?
:::

```{figure} images/scene_cesu_office.svg
:alt: Si Maya sa mesa niya sa CESU office, may laptop na nagpapakita ng tumataas na epidemic curve, mga papel na form at mapa ng lungsod sa dingding.
:width: 100%
Ang mesa ni Maya, isang linggo pagkatapos ng Bagyong Amihan. Kathang-isip ang Santa Luz, ang mga tao at ang datos nito.
```

## Ano ang ibig sabihin ng "malinis"

Ang **line list** ay table na may isang row bawat kaso at isang column bawat
impormasyon: petsa ng onset, edad, sex, barangay at iba pa. *Malinis* ito kapag:

- ang bawat row ay **isang totoong kaso** (walang duplicate);
- **iisang style** ang gamit ng bawat column (`2026-07-24`, hindi apat na paraan ng
  pagsulat ng parehong araw);
- **posible** ang bawat value (walang 150 taong gulang o nagkasakit pagkatapos
  magpakonsulta);
- **walang makikilala** mula rito.

Sinasadyang nilalabag ng file ni Jun, `santa_luz_linelist_raw.csv`, ang lahat ng apat na
patakaran. Ang kopyang gagamitin mo ay ang export niya sa data freeze noong 30 Setyembre
(637 row), kaya nandito na ang mga kaso ng dengue na darating pa sa kuwento. Synthetic na
training data ito: imbento ang mga pangalan, numero ng telepono at address dito, pero
*mukhang* totoo para makapagpraktis kang protektahan ang mga ito.

Ang tool ay **pandas**, ang spreadsheet library ng Python. Tinatawag na **DataFrame** ang
isang pandas table; **Series** ang isang column nito. Binabasa muna natin ang bawat
column bilang text, para walang babaguhin ang pandas nang palihim:

```python
raw = pd.read_csv(RAW_PATH, skiprows=1, dtype=str, keep_default_na=False)
```

## Privacy ang unang hakbang

Itinakda ng kabanata 02 ang patakaran: aalis sa table ang mga identifier *bago* ang
analysis. Pero kailangan pa natin ang pangalan sa isang trabaho: hanapin ang parehong
pasyenteng dalawang beses na-notify. Kaya ginagawa muna ni Maya ang bawat pangalan na
**salted pseudonymous ID** mula sa [kabanata 02](02_privacy_first.md). Laging pareho ang
ID ng parehong inayos na pangalan, pero kung walang sikretong salt, walang makauulit
nito o makababasa ng pangalan pabalik.

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
SALT = secrets.token_hex(16)  # demo lang: sa totoong trabaho, gumawa nang isang beses at ikandado (kabanata 02)


def pseudo_id(name: str, salt: str) -> str:
    key = " ".join(name.upper().replace(".", " ").split())   # i-normalise ang pangalan
    digest = hmac.new(salt.encode(), key.encode(), hashlib.sha256).hexdigest()
    return "P-" + digest[:10]


df = raw.copy()
df.insert(0, "pseudo_id", df["Patient Name"].map(lambda n: pseudo_id(n, SALT)))
df = df.drop(columns=["Patient Name", "Contact No.", "Address", "Reporting Unit", "Remarks"])
```
:::

:::{admonition} Privacy muna
:class: ph-privacy
- Alisin din ang **remarks**: may pinapangalanang ibang tao ang free text gaya ng
  *"anak ni Dennis (kapitbahay)"*.
- Nakadugtong pa rin sa tao ang salted ID habang umiiral ang salt. Ikandado ang totoong
  salt sa opisina, hindi kailanman sa notebook o sa chat, at ituring na confidential ang
  file. Dito, working column lang ang ID: hindi ito umaabot sa malinis na file.
- Kapag hihingi ka ng tulong kay Tala, ilarawan ang mga column at mag-imbento ng dalawa o
  tatlong row. Huwag kailanman mag-paste ng totoong rows ni Jun sa AI chat.
:::

## Mga petsa: ang pagkakamaling walang error

Dumarating ang mga petsa ni Jun bilang `07/24/2026`, `7/24/2026`, `2026-07-24`,
`24-Jul-26`, `July 24, 2026` at mga numerong gaya ng `46227`, na siyang paraan ng Excel
sa pag-store ng petsa (bilang ng araw mula 30 Disyembre 1899).

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May mga petsa sa iba't ibang format ang column kong `date_of_onset`. I-convert ito sa
datetime.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
Gamitin ang `format="mixed"` na may `dayfirst=True`, dahil araw muna ang isinusulat ng
karamihan sa mundo:
```python
naive_onset = pd.to_datetime(df["date_of_onset"], format="mixed", dayfirst=True, errors="coerce")
```
:::

Tumatakbo ito, at walang pumupula. Dalawang tanong-nurse ang itinanong ni Maya: ilang
petsa ang **pumalya**, at may **nagkasakit ba pagkatapos magpakonsulta**?

:::{admonition} Nagkamali si Tala
:class: ph-oops
- **22 petsa ng onset ang naging `NaT`** ("not a time"). Iyon ang mga Excel serial
  number, na hindi itinuturing na petsa ng pandas.
- **56 na pasyente ang "nagkasakit pagkatapos nilang magpakonsulta".** Dahil sa
  `dayfirst=True`, naging 8 Enero ang `8/1/2026` (1 Agosto). Tama pa rin ang mga
  petsang gaya ng `7/29/2026`, dahil walang buwang 29, kaya nagtago ang mali sa gitna
  ng maayos na rows.

Sa Pilipinas, buwan/araw/taon ang style kapag may slash, at kinumpirma ni Jun na ganito
ang lahat ng slash date sa export niya. Ang ayos: **isang tahasang patakaran bawat
format**, at walang hulaan.
:::

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
Sumulat ng function na `parse_dates(s)` para sa pandas Series ng mga petsang text. Mga
format: `M/D/YYYY` (buwan muna, opsyonal ang leading zero), `YYYY-MM-DD`, `DD-Mon-YY`
(20YY ang mga taon), `Month D YYYY` may comma man o wala, at 5-digit na Excel serial
number (bilang ng araw mula 1899-12-30). Ang blangko ay missing. I-parse nang tahasan ang
bawat format; huwag hayaang manghula ang pandas.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
def parse_dates(s: pd.Series) -> pd.Series:
    """I-parse ang mga style ng petsa ni Jun, isang tahasang format sa bawat pagkakataon."""
    s = s.str.strip()
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    serial = s.str.fullmatch(r"\d{5}")  # binibilang ng Excel ang araw mula 30 Dis 1899
    out[serial] = pd.to_datetime(s[serial].astype(int), unit="D", origin="1899-12-30")
    for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%d-%b-%y", "%B %d %Y"]:
        attempt = pd.to_datetime(s.str.replace(",", "", regex=False), format=fmt, errors="coerce")
        out = out.fillna(attempt)  # pinupunan lang ang mga petsang kulang pa
    return out
```
:::

:::{admonition} Suriin
:class: ph-check
1. **Kasong kayang i-check sa tingin:** ang parehong araw na isinulat sa pitong paraan ay
   dapat maging `2026-07-24` nang pitong beses, at dapat manatiling missing ang blangko.
2. **Bilangin ang pumalya:** hindi dapat maging `NaT` ang petsang text na hindi blangko.
   Titigil ang notebook sa isang `assert` kapag may ganoon.
3. **Itanong ulit ang tanong-epidemiology:** bumababa mula 56 hanggang **2** ang rows na
   onset pagkatapos ng konsulta. Totoong typo ang dalawang iyon sa file ni Jun, at
   aayusin natin sa ibaba.
:::

Subukan mo mismo. Sinadyang malabo ang ilang petsa sa laro sa ibaba; kapag puwedeng
dalawa ang ibig sabihin ng isang petsa, ang tamang sagot ay magtanong, hindi manghula.

:::{div}
:class: ph-game ph-game-date-fixer
I-parse nang tahasan ang bawat kilalang format ng petsa, i-map ang mga buwan sa Filipino,
i-convert ang Excel serial number at i-flag ang malalabong petsa imbes na manghula.
:::

## Mga lugar, code at edad

Ganito rin ang ibang column: isulat ang patakaran, ilapat ito, saka i-check na walang
nakalusot.

| Column | Hilaw na value | Patakaran | Malinis |
|---|---|---|---|
| Barangay | `Brgy. Ilog`, `ILOG`, `Bgy Ilog `, `Sto. Nino` | alisin ang accent at prefix, gawing maliit na titik, `sto` → `santo`, ayusin ang 3 kilalang typo, hanapin sa opisyal na listahan | `Ilog`, `Santo Niño` + `barangay_id`, `band` |
| Sex | `male`, `lalaki`, `F`, `babae` | lookup table | `M` / `F` |
| Oo/hindi | `Y`, `oo`, `hindi`, `N/A` | lookup table | `1` / `0` / missing |
| Outcome | `buhay`, `Namatay`, `Expired` | lookup table | `alive` / `died` |
| Edad | `34 y/o`, `8 mos`, `150` | unang numero; buwan ÷ 12; lampas 110 → missing | `34`, `0`, missing |

Nagiging 23 barangay ang 137 spelling ng barangay ni Jun. Ang ika-24, ang Bukid sa
kabundukan, ay walang kahit isang notification, at kailangang tandaan iyan sa kabanata
04. Kasya sa ilang linya ang patakaran sa edad:

```python
def parse_age(s: pd.Series) -> pd.Series:
    """Buong taon mula sa text na gaya ng '34', '34 y/o', '34yo', '8 mos', '8 months'."""
    text = s.str.strip().str.lower()
    number = text.str.extract(r"^(\d+)")[0].astype("Int64")
    years = number.where(~text.str.contains("mo"), number // 12)  # buwan -> taon
    return years.where(years <= 110).astype("Int64")             # 150 -> missing
```

## Duplicates, imposibleng petsa at ang patunay

Nakakita ang `df.duplicated()` ng **6 na eksaktong kopya**. Pero nag-re-notify din ang
City Health Office ng ilang pasyente na muling na-type ang pangalan, iba ang style ng
petsa at iba ang spelling ng barangay. Matapos linisin, tugma na ang mga row na iyon sa
mahahalagang column, kaya nagde-de-duplicate tayo ayon sa *(pseudo ID, sakit, petsa ng
onset)*. **19 na duplicate** lahat ang nakita nito: ang 6 na eksaktong kopya at 13 na
halos-duplicate.

```python
duplicate = df.duplicated(subset=["pseudo_id", "disease", "date_onset"], keep="first")
```

Ginagawang missing ang dalawang onset na na-type nang lampas sa petsa ng konsulta (sa
totoong buhay, tatawagan ni Maya ang reporting unit). Bibigyan ng bagong ID ang
natitirang 618 kaso, `SLC-0001` hanggang `SLC-0618`. Saka ang mga **validation rule**:
mga pangungusap tungkol sa datos na dapat laging totoo, isinulat bilang `assert` para
malakas na huminto ang notebook kapag may maling export sa hinaharap.

```python
both = clean.dropna(subset=["date_onset", "date_consult"])
assert (both["date_onset"] <= both["date_consult"]).all()          # nagkasakit bago magpakonsulta
```

:::{admonition} Suriin
:class: ph-check
Tanong ni Doc Mon: *"Pareho ba ang sa iyo sa opisyal na malinis na file?"* Nagtatapos
ang notebook sa pagpapakumpara sa pandas ng dalawang table, cell por cell:

```python
pd.testing.assert_frame_equal(ours, official)
```

Kapag walang mensahe, magkapareho sila: 618 row × 18 column, ang file na ginagamit ng
bawat susunod na kabanata (`santa_luz_linelist.csv`).
:::

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: paglilinis ng line list**

1. Walang error ang date column mo pagkatapos ng `pd.to_datetime(..., dayfirst=True)`. Ligtas na ba?
   - ✓ Hindi pa: bilangin ang mga `NaT` at i-check na hindi kailanman lampas sa konsulta ang onset — walang error na lumalabas sa maling parse.
   - Oo: kung may problema, maglalabas ng error ang pandas — walang inilalabas ang tahimik na maling parse.
2. Bakit gagawing salted pseudonymous ID ang mga pangalan imbes na burahin na lang?
   - ✓ Kailangan pa nating hanapin ang dobleng notification ng parehong tao — nagtutugma ang mga ID nang hindi ipinapakita ang pangalan.
   - Dahil ligtas nang i-publish ang pseudonymised na file — confidential pa rin ito habang umiiral ang salt.
   - Para mabasa natin ulit ang pangalan mamaya — hindi nababasa pabalik ang magandang ID.
3. Nakakita ang `df.duplicated()` ng 6 na row. Iyan na ba ang lahat ng duplicate?
   - Oo — ang duplicate ay magkaparehong row. Iba ang pagkaka-type sa mga na-re-notify na pasyente, kaya hindi sila magkapareho.
   - ✓ Hindi — ang mga row lang na magkapareho sa bawat column ang nakikita nito. 13 pang halos-duplicate ang lumilitaw pagkatapos linisin, ayon sa pseudo ID, sakit at onset.
:::

:::{admonition} Baon
:class: ph-baon
- Protektahan muna ang pagkakakilanlan: salted pseudo ID, saka alisin ang pangalan,
  telepono, address at remarks.
- Huwag hayaang manghula ang computer ng petsa: isang tahasang patakaran bawat format,
  saka bilangin ang mga `NaT` at i-check na onset ≤ konsulta.
- Isulat ang mga patakaran mo bilang `assert` at patunayan ang resulta: `assert_frame_equal`
  laban sa pinagkakatiwalaang bersyon.

Buksan ang notebook: [](notebooks/03_clean_linelist.ipynb)
:::
