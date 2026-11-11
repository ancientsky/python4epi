---
title: "02 Privacy muna: bawat row ay kapitbahay"
description: "Bakit mahalaga ang privacy sa surveillance, aling mga column ang nakapagpapakilala sa tao, ang tatlong patakaran sa AI tools, at aktuwal na de-identification: pseudonymous ID, generalisation, small-cell suppression at re-identification check."
---

::::{div}
:class: ph-story
*Miyerkoles, 29 Hulyo 2026 · CESU office*

:::{div}
:class: ph-say-jun
**Jun:** Heto po ang export mula sa shared drive, Ma'am Maya. Lahat ng notification mula noong baha. Pangalan, contact number, lahat.
:::

:::{div}
:class: ph-say-maya
**Maya:** Ayos. Ipe-paste ko kay Tala ang unang dalawampung row para makita niya ang format.
:::

:::{div}
:class: ph-say-nena
**Aling Nena:** Ate, sandali. Kilala ko ang bawat tao sa listahang iyan. Si Mang Lito, ang batang Aguilar, ang kambal sa Rizal Street. Kapag napunta ang pangalan nila kung saan hindi dapat, hindi na nila ako sasabihan kapag may sakit sila.
:::

:::{div}
:class: ph-say-mon
**Doc Mon:** Tama siya. Bago lumabas ang kahit ano sa opisinang ito, tanungin mo ang sarili mo: sino ang puwedeng makakita ng file na ito?
:::

> Paano natin ibabahagi ang line list nang hindi ibinabahagi ang ating mga kapitbahay?
::::

```{figure} images/scene_health_station.svg
:alt: Barangay health station na may watawat, upuang hintayan sa ilalim ng puno ng mangga, at si Aling Nena na nakatayo sa pinto.
:width: 100%
Gumagana lang ang surveillance habang may tiwala ang tao sa health station.
```

## Bakit privacy muna

**Tiwala.** Nakasalalay ang surveillance sa paglapit ng tao. Kapag nalaman ng isang
pamilya na pinag-usapan ang sakit nila, o lumabas ang pangalan nila sa group chat,
hindi na sila lalapit, at mas huli nang makikita ang susunod na outbreak.

**Stigma.** Puwedeng mawalan ng trabaho, ng puwesto sa paaralan o ng dangal sa barangay
ang isang tao dahil sa diagnosis. Mas may stigma ang ilang sakit kaysa sa iba, pero
walang sakit na dapat gawing tsismis.

**Ang batas.** Dalawang batas ang magkatabi sa trabaho mo:

| **Obligado** kang mag-report | **Obligado** kang magprotekta |
|---|---|
| Ginagawang tungkulin ng [RA 11332](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html), ang mandatory reporting law ng 2019, ang pag-report ng notifiable diseases. Sa ilalim ng [2020 Revised IRR](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf) nito, nire-report sa loob ng 24 oras ang Category I diseases at lingguhan ang Category II. | Pinamamahalaan ng **Data Privacy Act of 2012 (RA 10173)** kung paano kinokolekta, ginagamit at ibinabahagi ang personal information, at ang kalusugan ng tao ay kabilang sa pinakasensitibong laman ng isang file. Masasabi sa iyo ng Data Protection Officer ng opisina mo kung ano ang hinihingi sa iyo ng batas. |

Hindi nagbabanggaan ang pag-report at ang confidentiality. Umaakyat ang mga report **sa
reporting chain papunta sa mga taong nangangailangan nito**, at wala nang iba pa.
Naglabas ang DOH at National Privacy Commission ng pinagsamang gabay tungkol mismo sa
balanseng ito, halimbawa ang
[JMC 2020-0002](https://law.upd.edu.ph/wp-content/uploads/2020/05/DOH-NPC-JMC-No-2020-0002.pdf)
tungkol sa COVID-19 surveillance data.

:::{admonition} Hindi ito legal advice
:class: warning
Itinuturo ng kabanatang ito ang magandang gawi para sa training. Hindi ito legal advice
at hindi nito saklaw ang lahat ng patakarang nalalapat sa opisina mo. Kapag may duda,
sundin ang **Data Protection Officer** (DPO) ng opisina mo at ang gabay ng DOH na
nalalapat sa iyo.
:::

## Ano ang nakapagpapakilala sa isang tao?

Ang **line list** ay table na may isang row bawat kaso. Nahahati sa apat na grupo ang
mga column nito:

| Grupo | Ano ito | Sa export ni Jun |
|---|---|---|
| **Direct identifier** | tumuturo sa iisang tao nang mag-isa | `Patient Name`, `Contact No.`, `Address` (pati PhilHealth o ibang ID number) |
| **Indirect identifier** (quasi-identifier) | walang panganib nang mag-isa, nakapagpapakilala kapag pinagsama | `Barangay`, `Age`, `Sex`, ang apat na petsa, `Reporting Unit` |
| **Sensitive health information** | kung *tungkol saan* ang row | `Disease`, `Classification`, `Admitted`, `Outcome`, mga exposure |
| **Free text** | kahit ano | `Remarks`: ituring itong direct identifier hangga't hindi mo pa nababasa |

Ang mga indirect identifier ang madalas makalimutan. *Isang 34 taong gulang na lalaki sa
Barangay Ilog na nagsimulang lagnatin noong 24 Hulyo* — puwedeng iisang tao lang iyan, at
alam ng mga kapitbahay niya kung sino.

:::{admonition} Privacy muna
:class: ph-privacy
**Tatlong patakaran sa AI tools**

1. **Huwag kailanman mag-paste ng nakikilalang rows** sa AI chat: walang pangalan,
   numero ng telepono, address, ID number, eksaktong birth date o remarks.
2. **Ilarawan na lang ang schema:** ang pangalan ng mga column, ang klase ng mga value,
   at dalawa o tatlong halatang gawa-gawang row.
3. **Itago ang mga hilaw na file sa loob ng opisina,** sa mga computer at drive na
   aprubado ng opisina mo. Ang code ang bumibiyahe; ang datos ay naiiwan.
:::

## I-tap ang hindi dapat lumabas ng opisina

:::{div}
:class: ph-game ph-game-spot-pii
Hindi kailanman lumalabas ng opisina o pumapasok sa AI chat ang mga pangalan, numero ng
telepono, street address, PhilHealth number, eksaktong birth date at free-text remarks.
:::

## Hands-on: i-de-identify ang export ni Jun

Sa notebook, gagamitin mo ang `santa_luz_linelist_raw.csv`, 637 row at 19 column.

:::{admonition} Peke ang mga pangalan sa file na ito
:class: warning
Bawat pangalan, numero ng telepono at address sa `santa_luz_linelist_raw.csv` ay inimbento
ng computer at ginawang **mukhang** totoo para sa praktis. Nasa kathang-isip na
`0900 555` block ang lahat ng numero ng telepono. Walang totoong tao sa file.
:::

Sinusunod ni Maya ang patakaran 2. Pangalan lang ng mga column ang ipinapakita niya kay
Tala.

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
May pandas DataFrame akong `raw` na may 19 na text column: Date Reported, Reporting Unit,
Patient Name, Sex, Age, Contact No., Address, Barangay, Disease, Date of Onset,
Date Consulted, Classification, Date Lab Confirmed, Admitted, Outcome,
Waded in Floodwater, Did Cleanup Work, Dengue Severity, Remarks.
Hindi ako puwedeng magbahagi ng kahit anong row: confidential na datos ito ng pasyente.
Sumulat ng pandas code na mag-aalis ng direct identifiers para maibahagi ko ang table sa
aming provincial epidemiologist.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
direct_identifiers = ["Patient Name", "Contact No.", "Address"]
shared = raw.drop(columns=direct_identifiers)
```
:::

Tumatakbo ito, at wala na ang tatlong column. Pero ang "walang error" ay hindi "walang
pangalan".

:::{admonition} Suriin
:class: ph-check
1. Kunin ang bawat first name mula sa column na kaaalis mo lang.
2. Hanapin ang mga pangalang iyon sa **bawat natitirang cell**, bilang buong salita.
3. Dapat zero ang sagot. Kung hindi, tingnan kung saan nagtatago ang mga pangalan.
:::

```python
first_names = sorted(set(raw["Patient Name"].str.split().str[0]))
pattern = r"\b(?:" + "|".join(first_names) + r")\b"

hits = shared.apply(lambda column: column.str.contains(pattern)).sum()
```

:::{admonition} Nagkamali si Tala
:class: ph-oops
May nakitang pangalan ang search sa **40 remarks**, gaya ng *"anak/kapatid ni Dennis
(kapitbahay)"*. **Ibang tao** ang pinapangalanan ng remark, at kasama ang barangay,
diretso itong tumuturo sa isang sambahayan. Delikado rin ang ibang remarks: pinapakitid
ng *"estudyante, Grade 5"* ang isang bata sa iisang klase.

Inalis ni Tala ang mga column na *tinatawag na* name, phone at address. Hindi niya
nakita ang laman ng `Remarks`, dahil tama si Maya na hindi kailanman nagpakita sa kanya
ng kahit anong row. **Ang alam lang ng AI ay ang sinasabi mo. Trabaho mo ang mag-check
ng resulta.**
:::

Ang ayos: alisin ang `Remarks` (i-code muna sa loob ng opisina ang anumang may silbi
rito bilang oo/hindi na column), at alisin ang `Reporting Unit`, dahil isa o dalawang
report lang ang ipinadala ng ilang unit, kaya puwedeng tumuro sa isang tao ang pangalan
ng unit. Pagkatapos, patakbuhin ulit ang parehong search hanggang zero ang makita nito.

## Pseudonymous ID, na may sikreto

Kailangan pa ring masabi ni Doc Mon ang *"pakitingnan ulit ang case 17"*. Kailangan
diyan ng ID na walang kahulugan sa labas ng opisina: isang **pseudonymous ID**.

Nakatutuksong shortcut ang i-**hash** ang pangalan: gawin itong halo-halong character
gamit ang nakapirming recipe. Pero laging pareho ang lumalabas sa parehong pangalan, kaya
ang sinumang may listahan ng posibleng pangalan (listahan ng botante, class list, social
media) ay puwedeng mag-hash ng bawat pangalan at maghanap ng tugma. Sa notebook,
nahahanap agad ng limang-pangalang guess list si "Juan P. Santos".
**Hindi anonymous ang unsalted hash ng pangalan.**

Ang ayos ay **salt**: mahabang random na sikretong inihahalo sa hash. Kung walang salt,
walang makauulit ng hashing. Nakakandado ang salt sa opisina, hindi kailanman sa
notebook, hindi kailanman sa AI chat, hindi kailanman ipinapadala kasama ng datos.

```python
def pseudo_id(name: str, salt: str) -> str:
    key = " ".join(name.upper().replace(".", " ").split())   # i-normalise ang pangalan
    digest = hmac.new(salt.encode(), key.encode(), hashlib.sha256).hexdigest()
    return "P-" + digest[:10]
```

Ang pinakasimpleng pseudonym sa lahat ay running number, `SLC-0001`, `SLC-0002` at iba
pa, at nakakandado sa opisina ang susing nagdudugtong sa numero at pangalan. Iyan ang
gamit ng malinis na file ng Santa Luz.

## Generalise: mas ligtas kapag mas malawak

- **Edad → age group** (`0-4`, `5-14`, `15-24`, `25-44`, `45-64`, `65+`).
- **Address → barangay.** Itira ang barangay (kailangan mo ito sa mapa); alisin ang
  kalye at purok.
- **Eksaktong petsa → linggo** sa anumang ipa-publish mo. Itira ang eksaktong petsa sa
  loob ng opisina para sa epidemic curve at sa mga delay.

## Small-cell suppression

Ang na-publish na **1** ay puwedeng isang tao. *"Isang namatay sa dengue sa Buhangin"*
— balitang kayang lagyan ng pangalan ng buong barangay. Ang karaniwang patakaran ay
ipakita ang bilang na **1 hanggang 4** bilang `<5` (nananatiling zero ang zero).

```python
def suppress(table: pd.DataFrame, threshold: int = 5) -> pd.DataFrame:
    if threshold < 1:
        raise ValueError("dapat hindi bababa sa 1 ang threshold")
    small = (table > 0) & (table < threshold)
    return table.astype(object).mask(small, f"<{threshold}")
```

May isa pang bitag. Kung **iisa lang** ang nakatagong cell sa isang column at public ang
total nito, kayang ibawas ng kahit sino para makuha ito. Sa notebook, may dengue column
ang mga namatay ayon sa barangay na may eksaktong isang nakatagong cell, kaya city total
lang ang ilalabas para sa mga namatay sa dengue. Kahit ang total na iyon (1) ay
desisyon nina Doc Mon at ng DPO, hindi ng code.

## Re-identification check: sino ang unique?

Paano mo malalaman kung sapat na ang ginawa mo? Bilangin kung ilang tao ang **unique**
sa kanilang indirect identifiers, ibig sabihin walang ibang tao sa file na kapareho ng
kombinasyon nila. Ang ideya sa likod ng **k-anonymity** ay dapat may kahati ang bawat
kombinasyon na hindi bababa sa *k* na tao, halimbawa lima.

Sa malinis na line list (hindi kasama ang rows na may kulang na value):

| Indirect identifiers na itinira | Unique na tao |
|---|---:|
| barangay + edad + sex + sakit + petsa ng onset | 99.0% |
| barangay + edad + sex + sakit | 80.9% |
| barangay + age group + sex + sakit | 17.5% |
| band + age group + sex + sakit | 1.3% |

Kapag eksaktong edad at petsa ng onset, halos **lahat** ay unique, kahit walang
pangalan. Ang pagpapalawak ng kategorya ang nagpoprotekta sa kanila.

## Mabilisang check

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: privacy muna**

1. Alin dito ang indirect identifier?
   - `Patient Name` — nakikilala nito ang tao nang mag-isa: direct identifier iyan.
   - ✓ `Age` — walang panganib nang mag-isa, nakapagpapakilala kasama ng barangay, sex at mga petsa.
   - `Disease` — sensitive health information iyan, kung tungkol saan ang row.
2. Kailangan mo ng tulong ni Tala sa isang cleaning step. Ano ang ipe-paste mo?
   - Ang unang 20 row, para makita ni Tala ang format — hindi kailanman: nakikilala ang tao sa rows.
   - ✓ Ang pangalan ng mga column at dalawang halatang gawa-gawang row — sapat na iyan para sa magandang code.
   - Ang rows na binura ang pangalan — puwede pa ring makapagpakilala ang remarks at mga petsa.
3. Bakit hindi anonymous ang simpleng hash ng pangalan?
   - Anonymous iyan: walang makababasa ng hash — hindi na nila kailangang basahin: iha-hash nila ang guess list at ikukumpara.
   - ✓ Ang sinumang may listahan ng posibleng pangalan ay kayang i-hash ang mga ito at hanapin ang tugma — napipigilan iyan ng sikretong salt.
   - Masyadong maikli ang hash — hindi haba ang problema; ang kulang ay ang sikreto.
4. Nagpapakita ng `2` namatay sa isang barangay ang table na ipa-publish mo. Ano ang gagawin mo?
   - ✓ Ipakita ito bilang `<5`, at i-check na walang column na iisa lang ang nakatagong cell — puwedeng isang tao ang maliit na bilang.
   - I-publish: numero lang naman iyan — puwedeng tumuro sa isang pamilya ang 2 sa isang barangay.
   - Alisin ang barangay sa table — pinananatiling may silbi ng suppression ang table.
:::

:::{admonition} Baon
:class: ph-baon
- Bawat row ay kapitbahay. Mag-report pataas sa chain ayon sa hinihingi ng RA 11332; huwag
  ibahagi kahit saan pa.
- Sa AI tools: huwag kailanman mag-paste ng nakikilalang rows, ilarawan na lang ang
  schema, at itago ang mga hilaw na file sa loob ng opisina. Pagkatapos, **i-check** ang
  resulta: nag-iwan ng 40 pangalan sa remarks ang code ni Tala.
- Mag-pseudonymise gamit ang sikreto, i-generalise ang edad at petsa, i-suppress ang
  bilang na 1 hanggang 4, at sukatin kung sino pa ang unique bago mag-publish ng kahit
  ano.

Patakbuhin mo mismo: [Buksan ang notebook](notebooks/02_privacy_first.ipynb)
:::
