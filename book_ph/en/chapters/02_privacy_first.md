---
title: "02 Privacy first: every row is a neighbour"
description: "Why privacy matters in surveillance, which columns identify a person, the three rules for AI tools, and hands-on de-identification: pseudonymous IDs, generalisation, small-cell suppression and a re-identification check."
---

::::{div}
:class: ph-story
*Wednesday 29 July 2026 · CESU office*

:::{div}
:class: ph-say-jun
**Jun:** Here's the export from the shared drive, Ma'am Maya. All the notifications since the flood. Names, contact numbers, everything.
:::

:::{div}
:class: ph-say-maya
**Maya:** Perfect. I'll paste the first twenty rows into Tala so it can see the format.
:::

:::{div}
:class: ph-say-nena
**Aling Nena:** Ate, wait. I know every person on that list. Mang Lito, the Aguilar boy, the twins on Rizal Street. If their names go somewhere they shouldn't, they will never tell me when they're sick again.
:::

:::{div}
:class: ph-say-mon
**Doc Mon:** She's right. Before anything leaves this office, ask yourself: who can see this file?
:::

> How do we share the line list without sharing our neighbours?
::::

```{figure} images/scene_health_station.svg
:alt: A barangay health station with a flag, a waiting bench under a mango tree, and Aling Nena standing at the door.
:width: 100%
Surveillance works only while people trust the health station.
```

## Why privacy comes first

**Trust.** Surveillance depends on people coming forward. If a family learns that their
illness was talked about, or their name turned up in a group chat, they stop coming,
and the next outbreak is found later.

**Stigma.** A diagnosis can cost someone work, a place at school or their standing in the
barangay. Some diseases carry more stigma than others, but none should be gossip.

**The law.** Two laws sit side by side in your job:

| You **must** report | You **must** protect |
|---|---|
| [RA 11332](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html), the mandatory reporting law of 2019, makes reporting notifiable diseases a duty. Under its [2020 Revised IRR](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf), Category I diseases are reported within 24 hours and Category II weekly. | The same law lists the unauthorised disclosure of confidential information about a patient's medical condition among its prohibited acts. The **Data Privacy Act of 2012 (RA 10173)** treats information about a person's health as *sensitive personal information*, which needs the strictest care. |

Reporting and confidentiality do not fight each other. The law sends the data **up the
reporting chain to the people who need it**, and nowhere else. DOH and the National
Privacy Commission have issued joint guidance on exactly this balance, for example
[JMC 2020-0002](https://law.upd.edu.ph/wp-content/uploads/2020/05/DOH-NPC-JMC-No-2020-0002.pdf)
on COVID-19 surveillance data.

:::{admonition} Not legal advice
:class: warning
This chapter teaches good practice for training. It is not legal advice and does not
cover every rule that applies to your office. When in doubt, follow your office's **Data
Protection Officer** (DPO) and the DOH guidance that applies to you.
:::

## What identifies a person?

A **line list** is a table with one row per case. Its columns fall into four groups:

| Group | What it is | In Jun's export |
|---|---|---|
| **Direct identifier** | points to one person on its own | `Patient Name`, `Contact No.`, `Address` (also PhilHealth or other ID numbers) |
| **Indirect identifier** (quasi-identifier) | harmless alone, identifying in combination | `Barangay`, `Age`, `Sex`, the four dates, `Reporting Unit` |
| **Sensitive health information** | what the row is *about* | `Disease`, `Classification`, `Admitted`, `Outcome`, exposures |
| **Free text** | anything at all | `Remarks`: treat it as a direct identifier until you have read it |

Indirect identifiers are the ones people forget. *A 34-year-old man in Barangay Ilog
whose fever began on 24 July* may fit exactly one person, and his neighbours know who.

:::{admonition} Privacy stop
:class: ph-privacy
**Three rules for AI tools**

1. **Never paste identifiable rows** into an AI chat: no names, phone numbers,
   addresses, ID numbers, exact birth dates or remarks.
2. **Describe the schema instead:** the column names, the kind of values, and two or
   three obviously made-up rows.
3. **Keep raw files inside the office,** on the computers and drives your office
   approves. The code travels; the data stays.
:::

## Tap what must not leave the office

:::{div}
:class: ph-game ph-game-spot-pii
Names, phone numbers, street addresses, PhilHealth numbers, exact birth dates
and free-text remarks never leave the office or go into an AI chat.
:::

## Hands-on: de-identify Jun's export

In the notebook you work on `santa_luz_linelist_raw.csv`, 637 rows and 19 columns.

:::{admonition} The names in this file are fake
:class: warning
Every name, phone number and address in `santa_luz_linelist_raw.csv` was invented by a
computer and made to **look** real for practice. The phone numbers are all in a
fictional `0900 555` block. No real person is in the file.
:::

Maya follows rule 2. She shows Tala the column names only.

:::{admonition} Ask Tala
:class: ph-ask-tala
I have a pandas DataFrame `raw` with 19 text columns: Date Reported, Reporting Unit,
Patient Name, Sex, Age, Contact No., Address, Barangay, Disease, Date of Onset,
Date Consulted, Classification, Date Lab Confirmed, Admitted, Outcome,
Waded in Floodwater, Did Cleanup Work, Dengue Severity, Remarks.
I cannot share any rows: they are confidential patient data.
Write pandas code that removes the direct identifiers so I can share the table
with our provincial epidemiologist.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
direct_identifiers = ["Patient Name", "Contact No.", "Address"]
shared = raw.drop(columns=direct_identifiers)
```
:::

It runs, and the three columns are gone. But "no error" is not "no names".

:::{admonition} Check it
:class: ph-check
1. Take every first name from the column you just removed.
2. Search **every remaining cell** for those names, as whole words.
3. The answer must be zero. If it is not, look at where the names are hiding.
:::

```python
first_names = sorted(set(raw["Patient Name"].str.split().str[0]))
pattern = r"\b(?:" + "|".join(first_names) + r")\b"

hits = shared.apply(lambda column: column.str.contains(pattern)).sum()
```

:::{admonition} Tala got it wrong
:class: ph-oops
The search finds names in **40 remarks**, such as *"anak/kapatid ni Dennis
(kapitbahay)"*, "child or sibling of Dennis, a neighbour". The remark names **someone
else**, and with the barangay it points straight at a household. Other remarks are risky
too: *"estudyante, Grade 5"* narrows a child down to one class.

Tala removed the columns *called* name, phone and address. It could not see inside
`Remarks`, because Maya, rightly, never showed it any rows. **An AI only knows what you
tell it. Checking the result is your job.**
:::

The fix: drop `Remarks` (code anything useful in it into a yes/no column inside the
office first), and drop `Reporting Unit`, because some units sent only one or two
reports, so the unit's name can point to a person. Then run the same search again until it
finds zero.

## A pseudonymous ID, with a secret

Doc Mon still needs to say *"check case 17 again"*. That needs an ID that means nothing
outside the office: a **pseudonymous ID**.

A tempting shortcut is to **hash** the name: turn it into a jumble of characters with a
fixed recipe. But the same name always gives the same jumble, so anyone with a list of
likely names (a voters' list, a class list, social media) can hash every name and look
for a match. In the notebook, a five-name guess list finds "Juan P. Santos" at once.
**An unsalted hash of a name is not anonymous.**

The fix is a **salt**: a long random secret mixed into the hash. Without the salt, nobody
can redo the hashing. The office keeps the salt locked away, never in the notebook, never
in an AI chat, never sent with the data.

```python
def pseudo_id(name: str, salt: str) -> str:
    key = " ".join(name.upper().replace(".", " ").split())   # normalise the name
    digest = hmac.new(salt.encode(), key.encode(), hashlib.sha256).hexdigest()
    return "P-" + digest[:10]
```

The simplest pseudonym of all is a running number, `SLC-0001`, `SLC-0002` and so on,
with the key that links numbers to names kept locked in the office. That is what the
clean Santa Luz file uses.

## Generalise: coarser is safer

- **Age → age group** (`0-4`, `5-14`, `15-24`, `25-44`, `45-64`, `65+`).
- **Address → barangay.** Keep the barangay (you need it for maps); drop the street and
  purok.
- **Exact dates → weeks** in anything you publish. Keep exact dates inside the office for
  the epidemic curve and delays.

## Small-cell suppression

A published **1** can be a person. *"One dengue death in Buhangin"* is news the whole
barangay can put a name to. The common rule is to show counts from **1 to 4** as `<5`
(zero stays zero).

```python
def suppress(table: pd.DataFrame, threshold: int = 5) -> pd.DataFrame:
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    small = (table > 0) & (table < threshold)
    return table.astype(object).mask(small, f"<{threshold}")
```

There is one more trap. If a column has **only one** hidden cell and its total is
public, anyone can subtract to recover it. In the notebook, deaths by barangay have a
dengue column with exactly one hidden cell, so the dengue deaths go out as a city total
only. Even that total (1) is a decision for Doc Mon and the DPO, not for the code.

## Re-identification check: who is unique?

How do you know you have done enough? Count how many people are **unique** on their
indirect identifiers, meaning nobody else in the file shares their combination. The idea
behind **k-anonymity** is that every combination should be shared by at least *k* people,
say five.

On the clean line list (rows with missing values left out):

| Indirect identifiers kept | Unique people |
|---|---:|
| barangay + age + sex + disease + onset date | 99.0% |
| barangay + age + sex + disease | 80.9% |
| barangay + age group + sex + disease | 17.5% |
| band + age group + sex + disease | 1.3% |

With exact age and onset date, almost **everyone** is unique, even without a name.
Coarsening is what protects them.

## Quick check

:::{div}
:class: ph-game ph-game-quiz
**Quick check: privacy first**

1. Which of these is an indirect identifier?
   - `Patient Name` — that identifies a person on its own: a direct identifier.
   - ✓ `Age` — harmless alone, identifying together with barangay, sex and dates.
   - `Disease` — that is sensitive health information, what the row is about.
2. You need Tala's help with a cleaning step. What do you paste?
   - The first 20 rows, so Tala sees the format — never: rows identify people.
   - ✓ The column names and two obviously made-up rows — enough for good code.
   - The rows with names blurred out — remarks and dates can still identify people.
3. Why is a plain hash of a name not anonymous?
   - It is anonymous: nobody can read a hash — they don't need to: they hash a guess list and compare.
   - ✓ Anyone with a list of likely names can hash them and find the match — a secret salt stops that.
   - Hashes are too short — length is not the problem; the missing secret is.
4. A table you will publish shows `2` deaths in one barangay. What do you do?
   - ✓ Show it as `<5`, and check that no column has only one hidden cell — a small count can be a person.
   - Publish it: it is just a number — a 2 in one barangay can point to a family.
   - Delete the barangay from the table — suppression keeps the table useful.
:::

:::{admonition} Baon
:class: ph-baon
- Every row is a neighbour. Report up the chain as RA 11332 requires; share nowhere else.
- For AI tools: never paste identifiable rows, describe the schema instead, and keep raw
  files inside the office. Then **check** the result: Tala's code left 40 names in the
  remarks.
- Pseudonymise with a secret, generalise age and dates, suppress counts of 1 to 4, and
  measure who is still unique before anything is published.

Run it yourself: [Open the notebook](notebooks/02_privacy_first.ipynb)
:::
