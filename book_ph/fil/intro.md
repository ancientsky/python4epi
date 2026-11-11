---
title: "Mabuhay!"
description: "Ang Bantay Python ay libreng kurso para sa mga baguhan sa disease surveillance sa Pilipinas: matuto ng Python kasama ang AI co-pilot na natututo kang i-check, protektahan ang privacy ng pasyente, at bumuo ng outbreak dashboard."
---

:::{div}
:class: ph-hero
**Edisyong Pilipinas · Epi With Python**

## Bantay Python

Mula sa patong-patong na papel na notification form hanggang sa outbreak dashboard na
mababasa ng Mayor sa isang screen. Hindi kailangan ng karanasan sa coding. Ikaw ang may
alam sa epidemiology; ang AI co-pilot ang susulat ng unang draft ng code; **ikaw ang
matututong bumasa, magpatakbo at mag-check nito.**

{button}`Sakay na! Simulan ang biyahe → <chapters/00_start_here.md>`
:::

Ang *bantay* ay pagbabantay, pag-iingat. Iyan mismo ang surveillance: binabantayan ang
komunidad para maagang makita ang problema at mabilis itong matugunan. Isa pang
kasangkapan para sa trabahong iyan ang kursong ito.

:::{admonition} Tungkol sa edisyong Filipino
:class: tip
Isinalin ang edisyong ito sa tulong ng AI (machine-assisted), kaya baka may mga salitang
hindi pa natural o hindi tama. Kung Filipino ang wika mo at may napansin kang dapat
ayusin, malugod naming tatanggapin ang iyong pagtatama sa
[GitHub repository](https://github.com/ancientsky/python4epi). Maraming salamat po!
:::

## Ang mabubuo mo

Sa huling kabanata, magagawa mo ang **Bantay Santa Luz dashboard**: isang HTML file na
bumubukas sa kahit anong browser, kahit offline, at puwedeng i-email o ibahagi sa Local
Health Board. Bawat numero rito ay galing sa code na binasa at chineck mo mismo.

::::{grid} 1 2 3 3

:::{card} Headline tiles
Kaso, namatay at case fatality rate ng leptospirosis at dengue, sa isang tingin.
:::

:::{card} Epidemic curve
Mga kaso ayon sa araw o linggo ng onset, para ang hugis ng outbreak ang magkuwento.
:::

:::{card} Mapa ng barangay
Attack rate bawat 10,000 residente, hindi hilaw na bilang, sa mapa ng 24 na barangay.
:::

:::{card} Alert threshold
Lingguhang bilang ng dengue ngayong taon laban sa karaniwang antas sa panahong ito.
:::

:::{card} 7-1-7 scorecard
Gaano kabilis na-detect, na-notify at natugunan ang bawat event.
:::

:::{card} Privacy footer
Nakatago ang maliliit na bilang, walang pangalan o address, may source line at petsa.
:::
::::

Bubuuin mo ito sa [kabanata 09](chapters/09_dashboard.md). Bawat kabanata bago nito ay
nagdadagdag ng isang piraso.

:::{div}
:class: ph-banderitas
:::

## Kilalanin ang mga tauhan

:::::{div}
:class: ph-cast
::::{grid} 2 3 3 3

:::{card} Maya
![Si Maya Dela Cruz, ang Disease Surveillance Officer, may hawak na clipboard](chapters/images/cast_maya.svg)

*Disease Surveillance Officer, CESU*

"Ate Maya". Nurse, apat na buwan pa lang sa una niyang posisyon bilang DSO. Magaling sa tao at sa mga papel na form; hindi pa nakasusulat ng code kahit kailan. Kasabay mo siyang matututo.
:::

:::{card} Doc Mon
![Si Dr. Ramon Bautista, ang provincial epidemiologist, nakasalamin](chapters/images/cast_doc_mon.svg)

*Provincial epidemiologist, PESU*

Si Dr. Ramon Bautista, FETP graduate at mentor ni Maya. Laging nagtatanong: "Denominator? Case definition? Sino ang puwedeng makakita ng file na ito?"
:::

:::{card} Tala
![Si Tala, ang AI coding assistant, iginuhit bilang nakangiting bituin](chapters/images/cast_tala.svg)

*Ang AI coding assistant*

Ang *tala* ay maliwanag na bituin. Mabilis, palakaibigan at matulungin, pero minsan mali kahit siguradong-sigurado. Pareho itong ipinapakita ng aklat na ito.
:::

:::{card} Aling Nena
![Si Aling Nena Ramos, ang barangay health worker, may hawak na cellphone](chapters/images/cast_aling_nena.svg)

*Barangay Health Worker, Ilog*

Siya ang unang nakapansin na may mali. Ipinapaalala niya sa lahat na bawat row ay kapitbahay.
:::

:::{card} Jun
![Si Jun Villanueva, ang records clerk, may headphones at USB stick](chapters/images/cast_jun.svg)

*IT at records clerk, City Health Office*

Tagabantay ng shared drive at pinagmumulan ng napakagulong spreadsheet.
:::
::::
:::::

## Ang kuwento

```{figure} chapters/images/scene_flood_riverside.svg
:alt: Barangay sa tabing-ilog na lubog sa baha pagkatapos ng bagyo. Lumulusong ang mga lalaki sa tubig na may dalang kalat, dumaraan sa mga bahay na nakatayo sa poste; may maliit na bangka sa ulan.
:width: 100%
Ang Santa Luz pagkatapos ng Bagyong Amihan (kathang-isip na lungsod at kathang-isip na bagyo).
```

Noong **Sabado, 18 Hulyo 2026**, nag-landfall ang Bagyong Amihan sa Santa Luz City, sa
Lalawigan ng Kalinaw. Umapaw ang Ilog Marilag. Tatlong araw na lubog sa baha na
hanggang baywang ang walong barangay sa tabing-ilog. Lumusong sa baha ang mga lalaki
para maglinis ng kalat at ng mga kanal.

Makalipas ang isang linggo, nag-text si Aling Nena sa City Epidemiology and Surveillance
Unit (CESU): may ilang lalaki sa Barangay Ilog na may lagnat, mapupulang mata at masakit
na binti. Mukhang **leptospirosis** ito, isang bacterial infection na nakukuha kapag
nadikit sa tubig o lupang kontaminado ng ihi ng infected na hayop, lalo na ng daga.
Dumarami ang notification forms sa mesa ni Maya. Pagkatapos, habang nangingitlog ang
lamok sa naiipong tubig, tumataas din ang lingguhang kaso ng **dengue**.

May spreadsheet si Maya, may deadline, pero walang analyst. Payo ni Doc Mon: *"Tanungin
mo si Tala, pero i-check mo ang lahat ng ibibigay niya."*

## Ang Santa Luz sa mga numero

Ito ang mga pangunahing numero ng kathang-isip na datos ng kuwento. Makukuha mo ulit ang
bawat isa gamit ang sarili mong code.

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 186,000
na tao sa 24 na barangay
:::

:::{card} 449.1 mm
na ulan sa linggo ng Bagyong Amihan
:::

:::{card} 637
na row sa hilaw na line list export ni Jun
:::

:::{card} 618
na kaso matapos linisin
:::

:::{card} 230
na kaso ng leptospirosis
:::

:::{card} 388
na kaso ng dengue
:::

:::{card} 8.7%
case fatality rate ng leptospirosis (20 namatay)
:::

:::{card} 33
na kaso ng dengue sa unang linggong lampas sa epidemic threshold
:::
::::
:::::

Lahat ng kaso ay iyong mga naiulat sa CESU hanggang sa data freeze noong 30 Setyembre 2026.

## Ang ruta

Isang biyahe sa jeepney ang aklat na ito: labindalawang hintuan sa apat na yugto. Sumakay
sa simula; bawat hintuan ay nakapatong sa nauna.

:::{div}
:class: ph-wide
```{figure} chapters/images/route_map_fil.svg
:alt: Ruta ng jeepney na dumaraan sa labindalawang hintuan, mula Mabuhay hanggang kabanata 00 hanggang 10, may kulay ayon sa apat na yugto.
:width: 100%
Apat na yugto: tanggapin ang ulat, magbilang, magbantay, ipakita.
```
:::

:::{div}
:class: ph-route ph-act-1
**I · May ulat!**

- [00 Magsimula rito: ikaw, ang Colab at ang AI co-pilot](chapters/00_start_here.md)
- [01 Kumusta, Python?](chapters/01_python_with_ai.md)
- [02 Privacy muna: bawat row ay kapitbahay](chapters/02_privacy_first.md)
:::

:::{div}
:class: ph-route ph-act-2
**II · Bilangin natin**

- [03 Mula sa magulong line list tungo sa malinis na datos](chapters/03_clean_linelist.md)
- [04 Panahon, lugar, tao](chapters/04_time_place_person.md)
- [05 Hanapin ang pinagmulan](chapters/05_find_the_source.md)
:::

:::{div}
:class: ph-route ph-act-3
**III · Bantay**

- [06 Mga signal, threshold at 7-1-7](chapters/06_signals_and_thresholds.md)
- [07 Dengue sa susunod na buwan: forecasting gamit ang TimesFM](chapters/07_forecast_timesfm.md)
- [08 Nasaan ito? Mga mapa](chapters/08_maps.md)
:::

:::{div}
:class: ph-route ph-act-4
**IV · Ipakita**

- [09 Buuin ang Bantay Santa Luz dashboard](chapters/09_dashboard.md)
- [10 Sitrep, checklist at saan susunod](chapters/10_wrap_up.md)
:::

## Para kanino ito

Para sa mga gumagawa ng surveillance sa Pilipinas na **hindi pa nakasusulat ng code**
ang kursong ito: Disease Surveillance Officers, mga nurse sa Epidemiology and
Surveillance Unit (ESU), frontline FETP trainees, at mga supervisor ng Barangay Health
Workers. Kung marunong kang mag-fill out ng case investigation form at gumamit ng
spreadsheet, handa ka na.

Kailangan mo ng web browser, libreng Google account para sa Colab (ipinaliliwanag sa
kabanata 00), at AI assistant na pinapayagan ng opisina mo. Wala kang kailangang
i-install.

**Paano tumatakbo ang bawat kabanata.** Maikling eksena ng kuwento, isang ideya na may
larawan, ang prompt na tina-type ni Maya at ang code na ibinabalik, isang kahon kung
paano ito **i-check**, isang maliit na laro, at ang *baon* na iuuwi mo. Pagkatapos,
ikaw mismo ang magpapatakbo ng lahat sa isang notebook. Abangan ang pulang kahon na
**Nagkamali si Tala**: ipinapakita nito ang mga pagkakamaling talagang nagagawa ng AI
assistant, at kung paano ito nahuhuli ni Maya.

## Kathang-isip ang kuwento. Totoo ang sistema.

:::{admonition} Kathang-isip at totoo
:class: note
**Kathang-isip:** ang Santa Luz City, ang Lalawigan ng Kalinaw, ang Ilog Marilag, ang
Bagyong Amihan, bawat tao sa kuwento, at bawat pangalan, numero ng telepono, address at
bilang sa mga dataset ng Santa Luz. Peke ang mga pangalan sa hilaw na line list pero
ginawang *mukhang* totoo, para ligtas kang makapagpraktis ng privacy. Walang totoong
pasyente sa aklat na ito.

**Totoo:** ang surveillance system na nakapaligid sa kuwento. Iniuulat ang mga
notifiable disease sa pamamagitan ng PIDSR at ng information system nitong EDCS, ang
mga event sa pamamagitan ng Event-based Surveillance and Response (ESR), at umaakyat ang
mga ulat mula sa mga pasilidad papunta sa Epidemiology and Surveillance Units ng
lungsod, bayan, lalawigan at rehiyon hanggang sa DOH Epidemiology Bureau, sa ilalim ng
[Mandatory Reporting of Notifiable Diseases and Health Events of Public Health Concern
Act (RA 11332)](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html) at ng
[2020 Revised Implementing Rules and Regulations](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)
nito. May link sa pinagmulan ang bawat totoong batas, sistema at estadistika sa aklat na
ito.
:::

## Bahagi ng mas malaking aklat

Ang *Bantay Python* ay ang Edisyong Pilipinas ng
[**Epi With Python**](https://ancientsky.github.io/python4epi/en/), isang libre at bukas
na aklat na nagtuturo ng infectious disease epidemiology gamit ang Python, mula sa mga
batayan hanggang sa statistics, mapa at machine learning, sa pamamagitan ng imbestigasyon
ng outbreak sa isang nursing home. Pagkatapos mo rito, iyon ang susunod mong biyahe.

{button}`Sakay na! Magsimula rito → <chapters/00_start_here.md>`
