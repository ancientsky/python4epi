---
title: "10 Sitrep, checklist at saan susunod"
description: "Ang isang-pahinang situation report ni Maya para sa 30 Setyembre 2026, isang checklist sa paggamit ng AI assistant sa health office, simpleng mapa ng totoong surveillance system ng Pilipinas, glossary sa tatlong wika at kung saan susunod na pupunta."
---

:::::{div}
:class: ph-story
*Miyerkoles, 30 Setyembre, 6:40 ng gabi · Opisina ng CESU, Santa Luz*

::::{div}
:class: ph-say-mon
**Doc Mon:** Pasado ang dashboard. Ngayon ang sitrep — isang pahina, ang mahahalagang numero, ang ginagawa natin. Ang dashboard ang binabasa ng Board; ang sitrep ang ifa-file ng Probinsiya.
::::

::::{div}
:class: ph-say-maya
**Maya:** Kaya po itong i-draft ni Tala mula sa mga table ko…
::::

::::{div}
:class: ph-say-mon
**Doc Mon:** Kaya nga. At susuriin mo ang bawat numero laban sa notebook, at isusulat mong tumulong ito. Pangalan mo ang nasa ibaba, hindi kay Tala.
::::

> Ano ang itsura ng tapos na trabaho — at paano tayo patuloy na gagamit ng AI nang ligtas pagkatapos ng kursong ito?
:::::

## Ang sitrep ni Maya, 30 Setyembre 2026

Ang **situation report (sitrep)** ay maikli at may petsang buod ng isang pangyayari para
sa mga taong kailangang kumilos: ano ang nangyari, gaano kalaki, saan, ano ang ginagawa,
ano ang kailangan. Bawat numero sa ibaba ay mula sa synthetic na datos ng Santa Luz at
inilabas ng mga notebook ng kabanata 04–09.

:::{admonition} SITREP · Santa Luz City CESU · hanggang 30 Setyembre 2026 (data freeze)
:class: note
**Pangyayari.** Leptospirosis cluster at dengue outbreak pagkatapos ng Bagyong Amihan
(landfall 18 Hulyo; binaha ang mga barangay sa tabing-ilog 18–20 Hulyo). *Kathang-isip na
lungsod, synthetic na datos — para sa pagsasanay lamang.*

**Leptospirosis — patapos na ang cluster.** 230 kaso (119 confirmed, 52 probable,
59 suspect), 143 na-ospital (62.2%), **20 namatay (CFR 8.7%)**. Onset mula 22 Hulyo
hanggang 23 Agosto, rurok noong week 31 (108 kaso). Attack rate na 19.7 bawat 10,000 sa
tabing-ilog; pinakamataas sa Tabing-Ilog (29.8) at Ilog (29.1). Case-control study
(120 kaso, 240 matched control): paglusong sa baha OR 5.57 (95% CI 3.41–9.10), 4.28
matapos i-adjust sa clean-up work; bota sa mga lumusong OR 0.35 (0.16–0.80); doxycycline
prophylaxis OR 0.43 (0.21–0.86). Walang bagong onset mula 23 Agosto.

**Dengue — tuloy pa ang outbreak.** 388 kaso (49 confirmed, 172 probable, 167 suspect),
206 na-ospital (53.1%), 132 may warning signs, 15 severe, **1 namatay (CFR 0.3%)**. Lampas
sa epidemic threshold bawat linggo mula week 32 (33 kaso laban sa 17.5); rurok noong week
37 (63); week 38: 54. Kulang pa ang week 39 (reporting delay). Attack rate na 29.6 bawat
10,000 sa baybayin; pinakamataas sa Talaba (43.4) at Buhangin (35.5).

**Timeliness (7-1-7).** 15 sa 40 event mula Enero 2025 (38%) ang pumasa sa tatlong target.
Sa cluster na ito: 2 araw ang notification (target 1). 10 araw ang dengue response
(target 7). Median mula konsulta hanggang lab confirmation ng leptospirosis: 18 araw.

**Mga aksiyon.** 4S search-and-destroy kasama ang mga BHW sa mga barangay sa baybayin;
handa ang mga ospital sa severe dengue; close-out report ng leptospirosis; i-enrol ang
pribadong klinika bilang disease reporting unit; i-follow up ang mga specimen sa reference
laboratory.

**Inihanda ni** M. Dela Cruz, DSO. **Sinuri ni** R. Bautista, PESU. *Tinulungan ng isang
AI assistant sa pag-draft; bawat numero ay sinuri laban sa mga analysis notebook.*
:::

Ang buong screen ay ang [Bantay Santa Luz dashboard](/dashboard/).

## Ang AI-use checklist para sa health office

I-print ito at idikit sa tabi ng computer. Ito ang paraan ng buong kurso sa iisang
listahan: **Magtanong → Patakbuhin → Suriin**, na nakapaligid ang privacy.

![Ang ikot ng Magtanong, Patakbuhin, Suriin na nasa gitna si Tala](images/ask_run_check_fil.svg)

**Bago ka magtanong**

1. Gamitin ang assistant na aprubado ng opisina mo, ayon sa mga patakaran nito.
2. **Huwag kailanman mag-paste ng datos na nakakakilala ng tao**: pangalan, numero ng
   telepono, address, PhilHealth number, petsa ng kapanganakan, free-text na remarks,
   litrato ng mga form. Sundin ang Data Privacy Act of 2012 (RA 10173) ayon sa
   pagpapatupad ng Data Protection Officer ng opisina mo.
3. Sa halip, ilarawan ang mga **column** at magbigay ng dalawa o tatlong **gawa-gawang**
   row (kabanata 02).
4. Sabihin nang eksakto ang output na gusto mo at kung paano mo ito susuriin.

**Habang nagtatrabaho**

5. Patakbuhin ang code sa maliit na kasong kaya mong bilangin nang mano-mano.
6. Basahin ang bawat linyang hindi mo naiintindihan; hilingin sa assistant na ipaliwanag ito,
   tapos suriin ang paliwanag.
7. Suriin ang **denominator**, ang mga petsa at ang mga missing value.
8. Bantayan ang mga kumpiyansang pagkakamali: inimbentong function, maling column,
   tahimik na maling pagbasa ng petsa, kabuuang hindi nagtutugma.

**Pagkatapos, bago lumabas ng opisina ang anuman**

9. Patakbuhin ulit ang notebook mula itaas hanggang ibaba; dapat tugma ang mga numero sa
   teksto mo sa output.
10. Patakbuhin ang **publish check** (kabanata 09): aggregate lang, naka-suppress ang
    maliliit na cell, may petsang "as of", may mga tala sa datos.
11. May **taong** mananagot: ikaw ang pipirma, at may pangalawang taong magsusuri.
12. **Itala kung ano ang tinulungan ng AI** — aling bahagi, anong araw — sa report o sa
    mga tala ng file.

## Paano gumagana ang surveillance sa totoong Pilipinas

Kathang-isip ang Santa Luz; totoo ang sistemang nakapaligid dito. Heto ito sa simpleng
salita, mula sa research na tinipon para sa aklat na ito. (Nagbabago ang mga detalye;
sundin ang kasalukuyang issuance ng DOH at ng LGU mo.)

```{figure} images/reporting_ladder_fil.svg
:alt: Anim na antas ng pag-uulat, mula sa barangay health worker hanggang sa DOH Epidemiology Bureau, na may feedback na bumababa pabalik.
:width: 100%
Umaakyat ang mga ulat sa hagdan; dapat bumaba pabalik ang feedback.
```

**Sino ang nag-uulat kanino.** Ang disease reporting unit (rural health unit, ospital,
klinika, laboratoryo, pantalan) ay nag-uulat sa Epidemiology and Surveillance Unit ng
lungsod o bayan (**CESU/MESU**), na nag-uulat sa provincial unit (**PESU**), tapos sa
regional unit (**RESU**, sa regional office ng DOH), tapos sa **Epidemiology Bureau** ng
DOH
([2018 Joint External Evaluation](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf);
[2020 Revised IRR ng RA 11332](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)).
Sa ilalim ng IRR, iniuulat ang Category I na sakit sa loob ng 24 oras at ang Category II
na sakit linggo-linggo, tuwing Biyernes. Ang RA 11332 (2019), ang batas sa mandatory
reporting ng mga notifiable disease, at ang mga patakaran nito ay nag-aatas ng mga unit na
ito sa bawat antas
([RA 11332](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html)).

| Sistema | Para saan ito |
|---|---|
| **PIDSR**, ine-encode sa **EDCS** | case-based reporting ng mga notifiable disease gaya ng dengue, leptospirosis at tigdas — dito pumapasok ang line list ni Maya |
| **ESR** (event-based surveillance and response) | mga signal na hindi case report: tsismis, balita, text, di-pangkaraniwang pangyayari, iniuulat sa loob ng 24 oras ([JEE 2018](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf)) |
| **FHSIS** | regular na buwanan at quarterly na service statistics ng mga health facility ([Murai et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8880878/)) |
| **SPEED** | syndromic surveillance na binubuksan pagkatapos ng sakuna, dapat ma-activate sa loob ng 48 oras ([WPSAR 2015](https://ojs.wpro.who.int/ojs/index.php/wpsar/article/download/368/578?inline=1)) |
| **RITM at ang laboratory network** | kumpirmasyon ng mga kaso sa reference at subnational na laboratoryo ([2024 Joint External Evaluation](https://www.who.int/publications/i/item/9789240116795)) |
| **FETP** | ang Field Epidemiology Training Program ng DOH, mula frontline hanggang advanced na antas ([TEPHINET](https://www.tephinet.org/training-programs/philippines-field-epidemiology-training-program)) |

**Tatlong tapat na kakulangan** na binabanggit ng mga evaluation:

- **Reporting delay.** Ayon sa Western Pacific office ng WHO, may reporting delay na 2–3
  linggo ang dengue data ng PIDSR ([Dengue Situation Update 731](https://cdn.who.int/media/docs/default-source/wpro---documents/emergency/surveillance/dengue/dengue_202510021edf3700-e2a6-4e48-8e7c-acd86a16d530.pdf?sfvrsn=ba2e2c46_1)).
  Kaya laging masyadong mababa ang huling linggo sa chart ni Maya.
- **Walang iisang unique person ID sa lahat ng sistema**, kaya mano-mano pa rin ang
  de-duplication at ang pag-link ng lab result — ang problemang ipinakita ng mga duplicate
  ni Jun sa kabanata 03
  ([JEE 2018](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf)).
- **Kulang ang mga epidemiologist.** 128 advanced FETP graduate ang binilang ng 2024 Joint
  External Evaluation ([report](https://www.who.int/publications/i/item/9789240116795));
  ayon sa isang review noong 2023, 49 advanced graduate lang ang nagtatrabaho sa
  epidemiology ng gobyerno noong 2022
  ([Creating "boots on the ground"](https://pmc.ncbi.nlm.nih.gov/articles/PMC10632096/)).
  Natutulungan ng mga kasangkapang gaya ng nasa kursong ito ang isang maliit na team na
  makagawa ng mas marami — pero hindi nila ito napapalitan.

## Glossary sa tatlong wika

Pinapanatili ng column na Filipino ang terminong Ingles kung saan ito karaniwang ginagamit
sa mga health office. Sa mga katutubong nagsasalita ng Filipino: malugod naming
tinatanggap ang inyong mga pagwawasto. Taiwan terms ang gamit ng column na 中文.

| English | Filipino | 中文 |
|---|---|---|
| case | kaso | 病例 |
| case definition | case definition (pamantayan ng kaso) | 病例定義 |
| suspect / probable / confirmed case | suspect / probable / confirmed na kaso | 疑似 / 可能 / 確診病例 |
| line list | line list (talaan ng mga kaso) | 造冊（line list） |
| surveillance | surveillance, pagbabantay | 監測 |
| notification (reporting) | pag-uulat, notification | 通報 |
| cluster | cluster (kumpol ng mga kaso) | 群聚 |
| outbreak | outbreak, paglaganap | 群突發 |
| epidemic curve | epidemic curve | 流行曲線 |
| incubation period | incubation period | 潛伏期 |
| attack rate | attack rate | 侵襲率 |
| denominator | denominator (populasyong pinaghahatian) | 分母 |
| case fatality rate (CFR) | case fatality rate (CFR) | 致死率 |
| exposure | exposure (pagkalantad) | 暴露 |
| case-control study | case-control study | 病例對照研究 |
| odds ratio (OR) | odds ratio | 勝算比 |
| risk ratio (RR) | risk ratio | 風險比 |
| confidence interval (CI) | confidence interval | 信賴區間 |
| confounding | confounding | 干擾作用 |
| prophylaxis | prophylaxis (pang-iwas na gamot) | 預防性投藥 |
| epidemic threshold | epidemic threshold | 流行閾值 |
| reporting delay | reporting delay (pagkaantala ng ulat) | 通報延遲 |
| forecast | forecast, pagtataya | 預測 |
| de-identification | de-identification (pag-alis ng pagkakakilanlan) | 去識別化 |
| sensitive personal information | sensitive personal information | 敏感性個人資料 |
| small-cell suppression | small-cell suppression (pagtatago ng maliliit na bilang) | 小格數值隱藏 |
| dashboard | dashboard | 儀表板 |

## Saan susunod

- **Ang buong aklat.** Mas malalim ang *Epi With Python*, na ang kuwento ay isang
  Legionella outbreak sa isang nursing home: ang [outbreak workflow](https://ancientsky.github.io/python4epi/en/chapters/outbreak-workflow/),
  [stratified analysis at confounding](https://ancientsky.github.io/python4epi/en/chapters/stratified/),
  [logistic regression](https://ancientsky.github.io/python4epi/en/chapters/logistic-regression/),
  [time series](https://ancientsky.github.io/python4epi/en/chapters/time-series/),
  [spatial epidemiology](https://ancientsky.github.io/python4epi/en/chapters/spatial/),
  [deep learning at TimesFM](https://ancientsky.github.io/python4epi/en/chapters/deep-learning/)
  at [reproducible workflows](https://ancientsky.github.io/python4epi/en/chapters/reproducibility/)
  (sa Ingles).
- **FETP.** Kung field epidemiology ang landas mo, nagsasanay ang Field Epidemiology
  Training Program ng DOH sa frontline, intermediate at advanced na antas
  ([program page sa TEPHINET](https://www.tephinet.org/training-programs/philippines-field-epidemiology-training-program)).
- **Sarili mong datos, nang ligtas.** Ulitin ang kabanata 03–09 gamit ang de-identified na
  extract mula sa opisina mo, sa loob ng opisina mo, nang may pahintulot ng supervisor mo.
  Panatilihin ang publish check.

:::::{div}
:class: ph-story
*Biyernes, 2 Oktubre · Session hall, Santa Luz City Hall*

::::{div}
:class: ph-say-maya
**Maya:** …kaya lampas pa rin po sa threshold ang dengue, pero mas mababa na sa rurok ang huling kumpletong linggo. Humihingi po kami ng mga volunteer para sa 4S sa mga barangay sa baybayin.
::::

::::{div}
:class: ph-say-nena
**Aling Nena:** *(mula sa likurang hanay, mahinahon)* Isasama ko ang mga BHW ng Ilog. Malinis na ang mga kanal — nakabota na ang mga lalaki.
::::

::::{div}
:class: ph-say-mon
**Doc Mon:** *(nagte-text kay Maya sa ilalim ng mesa)* Magaling ang sitrep. Sa susunod na linggo, ituturo natin kay Jun ang notebook.
::::

::::{div}
:class: ph-say-tala
**Tala:** Nagkamali ako nang isa o dalawang beses sa daan. Salamat sa pagsusuri.
::::

> Bawat row ay kapitbahay. Bawat numero ay sinuri. *Salamat, Bantay!*
:::::

```{figure} images/cast_all.svg
:alt: Ang limang tauhan ng kuwento na magkakatabi: Maya, Doc Mon, Tala, Aling Nena at Jun.
:width: 80%
Sina Maya, Doc Mon, Tala, Aling Nena at Jun. Kathang-isip silang lahat, pati ang Santa Luz.
```

:::{div}
:class: ph-game ph-game-quiz
**Huling check: ang buong ruta**

1. Ano ang puwede mong i-paste sa AI chat para matulungan ka sa line list mo?
   - ✓ Mga pangalan ng column at dalawa o tatlong gawa-gawang row — hindi kailanman totoong datos.
   - Ang unang sampung row ng totoong file — totoong tao ang mga iyon.
   - Litrato ng notification form — may mga pangalan at address ito.
2. Tumakbo nang walang error ang code ni Tala. Ano ang susunod?
   - Kopyahin ang resulta sa report.
   - ✓ Suriin ito sa kasong kaya mong bilangin nang mano-mano at suriin ang denominator — hindi porke tumakbo ay tama na.
3. Sino ang mananagot sa sitrep na dinraft sa tulong ng AI assistant?
   - Ang assistant.
   - ✓ Ang opisyal na pumirma rito — at sinasabi ng report kung aling bahagi ang tinulungan ng AI.
4. Bakit mas mababa ang huling linggo sa chart ng dengue?
   - Natapos ang outbreak noong linggong iyon.
   - ✓ Reporting delay — dumarating pa ang mga kasong nag-onset noong linggong iyon.
5. Sa totoong sistema ng Pilipinas, ang surveillance unit ng lungsod ay sunod na nag-uulat sa…
   - Direkta sa DOH Epidemiology Bureau.
   - ✓ Sa provincial unit (PESU), tapos sa regional unit (RESU), tapos sa Bureau.
:::

:::{admonition} Baon
:class: ph-baon
- Maikli, may petsa at nasuri ang sitrep; sinasabi nito kung ano ang ginagawa at kung
  sino ang pumirma.
- Magtanong gamit ang pekeng row, patakbuhin, suriin, itala na tumulong ang AI — at isang
  tao ang pipirma.
- Kaya mo na ngayong umabot mula sa magulong line list hanggang sa dashboard. Ituloy mo:
  ang buong aklat at ang FETP.

Balik sa simula: [](00_start_here.md) · [Buksan ang dashboard](/dashboard/)
:::
