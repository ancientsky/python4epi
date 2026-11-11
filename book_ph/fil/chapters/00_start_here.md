---
title: "00 Magsimula rito: ikaw, ang Colab at ang AI co-pilot"
description: "Buksan ang una mong Colab notebook, alamin ang ikot ng Ask → Run → Check, sumulat ng prompt na nagbibigay ng magandang code, at gawin ang privacy pledge bago ang kabanata 01."
---

::::{div}
:class: ph-story
*Lunes, 27 Hulyo 2026 · CESU office, Santa Luz City*

:::{div}
:class: ph-say-nena
**Aling Nena:** Ate Maya, tatlo pang lalaki mula sa Purok 2 sa Ilog. Lagnat, mapupulang mata, masakit ang binti. Lahat sila naglinis ng kanal pagkatapos ng baha.
:::

:::{div}
:class: ph-say-maya
**Maya:** Labing-isang form na iyan mula noong Biyernes. Gusto ni Doc Mon ng line list at unang analysis bago mag-Biyernes. Hindi pa ako nakasusulat kahit isang linya ng code.
:::

:::{div}
:class: ph-say-mon
**Doc Mon:** Kung ganoon, hayaan mong AI assistant ang sumulat ng unang draft. Tanungin mo si Tala. Pero i-check mo ang lahat ng ibibigay niya, at huwag na huwag mong ibibigay sa kanya ang pangalan ng pasyente.
:::

> Paano ka makikipagtrabaho sa AI assistant na hindi mo lubos na mapagkakatiwalaan?
::::

```{figure} images/scene_cesu_office.svg
:alt: Si Maya sa mesa niya sa CESU office sa maulang hapon, may laptop na nagpapakita ng tumataas na epidemic curve, maliit na bituin para kay Tala, at patong-patong na papel na notification form.
:width: 100%
Ang mesa ni Maya. Totoong trabaho ang mga form; tutulong na ang laptop.
```

Walang code na isusulat sa kabanatang ito. Inihahanda nito ang tatlong bagay na gagamitin
mo sa bawat kabanata pagkatapos nito: **isang notebook** na pagpapatakbuhan ng code,
**isang paraan** ng pakikipagtrabaho sa AI assistant, at **isang pangako** tungkol sa
privacy.

## Ang notebook mo: Google Colab

Ang **notebook** ay dokumentong pinaghahalo ang text at code. Magbabasa ka ng isang
talata, tapos patatakbuhin mo ang code sa ilalim nito at makikita mo agad ang resulta:
isang numero, table o chart. May isa nito ang bawat kabanata mula 01.

Pinapatakbo ng **Google Colab** ang mga notebook sa web browser mo, sa mga computer ng
Google. Wala kang i-i-install. Kailangan mo lang ng libreng Google account at internet.

**Pagbukas ng una mong notebook, hakbang-hakbang.** Nagbabago ang itsura ng screen
paglipas ng panahon, kaya sinasabi ng mga hakbang na ito kung ano ang hahanapin, hindi
kung saan eksaktong pipindot.

1. Pumunta sa notebook page ng [kabanata 01](notebooks/01_python_with_ai.ipynb). Malapit
   sa pamagat ng page, may link na **Open in Colab**. I-click ito. Bubukas ang Colab sa
   bagong tab na may sarili nitong kopya ng notebook.
2. Kung pinapa-sign in ka ng Colab, gamitin ang Google account mo.
3. Puwedeng magbabala ang Colab na hindi Google ang sumulat ng notebook. Normal iyan sa
   kahit anong notebook na galing sa labas ng Google; galing ito sa public repository ng
   aklat. Piliing patakbuhin pa rin.
4. Hanapin ang unang **code cell**, na may pamagat na *Google Colab setup*. Patakbuhin
   ito: pindutin ang bilog na play button sa kaliwang gilid nito, o mag-click sa loob ng
   cell at pindutin ang **Shift + Enter**. Dina-download nito ang datos at mga tool ng
   aklat. Bigyan ito ng isang minuto.
5. Patakbuhin ang mga susunod na cell isa-isa, mula itaas pababa. Lumalabas ang resulta
   ng bawat cell sa ilalim nito kapag tapos na.
6. **Mag-save ng sarili mong kopya.** Sa File menu ng Colab, piliin ang option na
   mag-save ng kopya sa Google Drive mo. Kung hindi, mawawala ang mga binago mo kapag
   isinara mo ang tab.
7. Kapag may na-stuck, gamitin ang Runtime menu para mag-**restart**, tapos patakbuhin
   ulit ang mga cell mula sa itaas. Mahalaga ang pagkakasunod: magagamit lang ng isang
   cell ang ginawa ng mga naunang cell.

Kung walang Colab link, buksan mo mismo ang Colab, piliing magbukas ng notebook **mula sa
GitHub**, i-type ang `ancientsky/python4epi`, at pumili ng notebook sa folder na
`book_ph/fil/chapters/notebooks/`.

:::{admonition} Privacy muna
:class: ph-privacy
Tumatakbo ang Colab sa mga computer ng Google, hindi sa opisina mo. Sa kursong ito,
ayos lang iyan: kathang-isip ang lahat ng dataset. **Huwag mag-upload ng totoong line
list sa Colab o sa kahit anong online tool maliban kung aprubado ng opisina mo ang tool
na iyon para sa datos ng pasyente.**
:::

## Ano ang AI assistant, at ano ang hindi

Ang AI coding assistant ay programang nakabasa na ng napakaraming text at code. Kapag
nag-type ka ng request, **hinuhulaan** nito kung ano ang itsura ng isang matulunging
sagot, isang salita sa bawat pagkakataon. Kaya ito napakabilis, at kaya rin ito puwedeng
magkamali.

| Ang AI assistant **ay** | Ang AI assistant ay **hindi** |
|---|---|
| mabilis na tagasulat ng unang draft ng code | calculator na laging tama |
| magaling magpaliwanag ng linyang hindi mo maintindihan | may alam sa datos mo, maliban kung ipakita mo |
| matiyaga: puwede mong itanong ang parehong bagay nang limang beses | responsable sa resulta. **Ikaw iyon.** |

Ang delikado ay hindi ang halatang mali. Ito ay ang code na tumatakbo nang walang error,
mukhang propesyonal, at nagbibigay ng **maling numero**. Puwedeng mali ang AI assistant
kahit siguradong-sigurado ito: maling denominator, function na hindi naman umiiral,
petsang binasa nang baligtad. Pangalan mo ang nakalagay sa report, hindi ang sa AI
assistant.

Sa aklat na ito, **Tala** ang pangalan ng AI assistant. Gamitin kung anong assistant ang
pinapayagan ng opisina mo; pareho ang paraan.

## Ang paraan: Ask → Run → Check

```{figure} images/ask_run_check_fil.svg
:alt: Ikot ng tatlong istasyon. Magtanong: pangalanan ang mga column at gawa-gawang rows lang ang ibigay. Patakbuhin: patakbuhin sa Colab at basahin ang error. I-check: subukan sa maliit na kasong kayang bilangin nang mano-mano. May palaso mula I-check pabalik sa Magtanong: ayusin at magtanong ulit.
:width: 100%
Dadaan sa ikot na ito kahit isang beses ang bawat piraso ng code sa aklat na ito.
```

1. **Ask (magtanong).** Ilarawan ang gusto mo, kasama ang pangalan ng mga column at ilang
   gawa-gawang row.
2. **Run (patakbuhin).** I-paste ang code sa isang cell at patakbuhin. Kung may error,
   basahin muna ang huling linya. Kadalasan, sinasabi nito kung ano ang mali.
3. **Check (i-check).** Subukan ang code sa kasong napakaliit na kaya mong bilangin nang
   mano-mano. Tugma ba ang total sa bilang ng rows? Tama ba ang denominator? Kung may
   mali, sabihin kay Tala ang nakita mo at magtanong ulit.

Ang **Check** ang hakbang na madalas nilalaktawan, at ito ang pinakasinasanay ng aklat na
ito.

## Magtanong nang tama: ang limang sangkap ng magandang prompt

Ang **prompt** ay ang tina-type mo sa AI assistant. Magandang prompt, magandang code.
Ilagay ang:

1. **Context:** ano ang datos at ano ang gusto mong gawin.
2. **Columns:** ang eksaktong pangalan ng mga column, kung paano nakasulat sa file.
3. **Maliit na gawa-gawang halimbawa:** dalawa o tatlong imbentong row, hindi kailanman
   totoo.
4. **Inaasahang output:** ano ang dapat na itsura ng sagot.
5. **Constraints:** ano ang kailangan mo: madaling intindihin ng baguhan, may comment sa
   bawat linya, pandas lang, may paraan para i-check ang resulta.

**Dati:**

> bilangin ang dengue bawat barangay

Kailangang hulaan ni Tala ang lahat: ang file, ang pangalan ng mga column, kung table o
chart ang gusto mo. May makukuha kang *kung anong* code, malamang mali pa ang pangalan
ng mga column.

**Ngayon:**

:::{admonition} Tanungin si Tala
:class: ph-ask-tala
Surveillance officer ako na nag-aaral ng Python. May pandas DataFrame akong `df`, isang
row bawat kaso, na may columns na `case_id`, `disease` (`dengue` o `leptospirosis`),
`barangay` at `date_onset`. Tatlong gawa-gawang row:
`X-1, dengue, Barangay A, 2026-08-03` · `X-2, leptospirosis, Barangay A, 2026-07-27` ·
`X-3, dengue, Barangay B, 2026-08-04`.
Sumulat ng code na madaling intindihin ng baguhan na bibilang ng kaso ng **dengue** bawat
barangay, mula pinakamarami hanggang pinakakaunti, may comment sa bawat linya. Sa tatlong
row ko, inaasahan kong A = 1, B = 1. Ipakita mo rin kung paano i-check na tama ang
kabuuan.
:::

:::{admonition} Sagot ni Tala
:class: ph-tala-says
```python
dengue = df[df["disease"] == "dengue"]          # dengue rows lang ang itira
counts = dengue["barangay"].value_counts()      # bilangin ang rows bawat barangay
print(counts)
assert counts.sum() == len(dengue)              # check: isang beses nabilang ang bawat dengue row
```
:::

:::{admonition} I-check natin
:class: ph-check
1. Patakbuhin muna ito sa tatlong gawa-gawang row. Sinabi mong inaasahan mo ang A = 1,
   B = 1. Iyan ba ang lumabas?
2. Chine-check ng linyang `assert` ang total. Kung tahimik ito, tama ang kabuuan.
3. Tanungin ang sarili: talaga bang inalis nito ang leptospirosis row? (Oo: 1 ang
   Barangay A, hindi 2.)
:::

Pansinin kung ano ang **wala** sa magandang prompt: walang pangalan, walang address,
walang totoong row. Hindi mo kailanman kailangan ng totoong datos para makakuha ng
magandang code. Pareho ang nagagawa ng gawa-gawang rows.

## Magpraktis: piliin ang mas magandang prompt

:::{div}
:class: ph-game ph-game-prompt-pick
Ang magandang prompt ay may pangalan ng mga column, nagpapakita ng dalawa o tatlong
gawa-gawang halimbawang row, sinasabi kung ano mismo ang output na gusto mo, at humihingi
ng paraan para i-check ito.
:::

## Ang privacy pledge

Hahawak ka ng datos tungkol sa sakit ng totoong tao sa buong karera mo.
Ipinaliliwanag ng [kabanata 02](02_privacy_first.md) ang batas at ang mga teknik. Bago ka
magsimula, gawin ang pangakong ito.

:::{admonition} Privacy muna
:class: ph-privacy
**Ang pangako ko.** Bago ako gumamit ng AI tools sa health data, ipinapangako ko na:

1. **Hindi ako kailanman magpe-paste** ng pangalan, numero ng telepono, address, ID
   number, eksaktong birth date o free-text remarks tungkol sa pasyente sa AI chat.
2. **Ilalarawan ko ang mga column** at mag-iimbento ako ng halimbawang rows.
3. **Itatago ko ang mga hilaw na file sa loob ng opisina**, sa mga computer at drive na
   aprubado ng opisina ko.
4. **Iche-check ko** ang bawat numero bago ito umalis sa mesa ko, at tatandaan kong ako
   ang mananagot dito, hindi ang AI.
5. **Magtatanong ako sa Data Protection Officer** namin kapag hindi ako sigurado.

Bawat row ay kapitbahay.
:::

## Mabilisang check

:::{div}
:class: ph-game ph-game-quiz
**Mabilisang check: magsimula rito**

1. Tumakbo ang code ni Tala nang walang kahit anong error. Ano ang sinasabi nito sa iyo?
   - Na tama ang sagot — hindi. Puwedeng tumakbo nang perpekto ang code pero mali pa rin ang numero.
   - ✓ Na kaya lang itong patakbuhin ng Python — kailangan mo pa ring i-check ang resulta sa kasong kayang bilangin nang mano-mano.
   - Na tinest na ito ni Tala — hindi nakikita ni Tala ang datos mo at hindi niya mapapatakbo ang notebook mo.
2. Alin dito ang dapat nasa prompt?
   - Limang totoong row mula sa line list, para eksakto — hindi kailanman: nakikilala ang totoong tao sa totoong rows.
   - ✓ Ang eksaktong pangalan ng mga column at dalawang imbentong row — iyan na ang lahat ng kailangan ni Tala.
   - Ang pangalan ng pasyente, para maintindihan ni Tala ang kaso — hindi kailanman pumapasok sa AI chat ang pangalan.
3. Sa Colab, sinasabi ng isang cell na hindi naka-define ang isang variable. Ano ang malamang na dahilan?
   - ✓ May naunang cell na hindi pa napapatakbo — patakbuhin ang mga cell mula sa itaas, nang sunod-sunod.
   - Sira ang Colab — minsan nakatutulong ang pag-restart, pero kadalasang ang pagkakasunod ng mga cell ang dahilan.
   - Kailangang may naka-install na Python sa computer mo — hindi: pinapatakbo ng Colab ang Python sa mga computer ng Google; browser lang ang kailangan mo.
:::

:::{admonition} Baon
:class: ph-baon
- Pinaghahalo ng notebook ang text at code; pinapatakbo ito ng Colab sa browser mo.
  Patakbuhin ang mga cell mula sa itaas, at mag-save ng kopya sa Drive mo.
- Ask → Run → Check: hinuhulaan lang ng AI assistant ang code na mukhang tama, kaya
  i-check ang bawat resulta sa kasong kayang bilangin nang mano-mano. Ikaw ang mananagot
  sa mga numero.
- Ang magandang prompt ay may context, eksaktong columns, gawa-gawang rows, inaasahang
  output at mga constraint mo, at walang totoong datos ng pasyente.

Susunod na hintuan: [01 Kumusta, Python?](01_python_with_ai.md)
:::
