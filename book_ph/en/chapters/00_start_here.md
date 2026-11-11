---
title: "00 Start here: you, Colab and an AI co-pilot"
description: "Open your first Colab notebook, learn the Ask → Run → Check loop, write prompts that get good code, and make the privacy pledge before chapter 01."
---

::::{div}
:class: ph-story
*Monday 27 July 2026 · CESU office, Santa Luz City*

:::{div}
:class: ph-say-nena
**Aling Nena:** Ate Maya, three more men from Purok 2 in Ilog. Fever, red eyes, masakit ang binti, their calves hurt. All of them cleared the canal after the flood.
:::

:::{div}
:class: ph-say-maya
**Maya:** That's eleven this week. Doc Mon wants a line list and a first analysis by Friday. I have never written a line of code.
:::

:::{div}
:class: ph-say-mon
**Doc Mon:** Then let an AI assistant write the first draft. Ask Tala. But check everything it gives you, and never give it a patient's name.
:::

> How do you work with an AI assistant you cannot fully trust?
::::

```{figure} images/scene_cesu_office.svg
:alt: Maya at her desk in the CESU office on a rainy afternoon, with a laptop showing a rising epidemic curve, a small star for Tala, and a stack of paper notification forms.
:width: 100%
Maya's desk. The forms are real work; the laptop is about to help.
```

This chapter has no code to write. It sets up three things you will use in every chapter
after it: **a notebook** to run code in, **a method** for working with an AI assistant,
and **a promise** about privacy.

## Your notebook: Google Colab

A **notebook** is a document that mixes text and code. You read a paragraph, then run
the code under it and see the result right there: a number, a table or a chart. Every
chapter from 01 on has one.

**Google Colab** runs notebooks in your web browser, on Google's computers. You install
nothing. You need a free Google account and an internet connection.

**Opening your first notebook, step by step.** Screens change over time, so these steps
describe what to look for rather than where to click.

1. Go to the notebook page of [chapter 01](notebooks/01_python_with_ai.ipynb). Near the
   page title there is an **Open in Colab** link. Click it. Colab opens in a new tab with
   its own copy of the notebook.
2. If Colab asks you to sign in, use your Google account.
3. Colab may warn that the notebook was not written by Google. That is normal for any
   notebook from outside Google; this one comes from the book's public repository.
   Choose to run it anyway.
4. Find the first **code cell**, titled *Google Colab setup*. Run it: press the round
   play button at its left edge, or click inside the cell and press **Shift + Enter**.
   It downloads the book's data and tools. Give it a minute.
5. Run the next cells one by one, from top to bottom. Each cell shows its result
   underneath when it finishes.
6. **Save your own copy.** In Colab's File menu, choose the option to save a copy in
   your Google Drive. Without it, your changes disappear when you close the tab.
7. If something gets stuck, use the Runtime menu to **restart**, then run the cells from
   the top again. Order matters: a cell can only use what earlier cells created.

If there is no Colab link, open Colab yourself, choose to open a notebook **from
GitHub**, type `ancientsky/python4epi`, and pick a notebook in the folder
`book_ph/en/chapters/notebooks/`.

:::{admonition} Privacy stop
:class: ph-privacy
Colab runs on Google's computers, not your office's. In this course that is fine: every
dataset is invented. **Do not upload a real line list to Colab or any other online tool
unless your office has approved that tool for patient data.**
:::

## What an AI assistant is, and what it is not

An AI coding assistant is a program that has read a huge amount of text and code. When
you type a request, it **predicts** what a helpful answer would look like, one word at a
time. That is why it is so fast, and also why it can be wrong.

| An AI assistant **is** | An AI assistant **is not** |
|---|---|
| a fast first-draft writer of code | a calculator that is always right |
| good at explaining a line you do not understand | aware of your data, unless you show it |
| patient: ask the same thing five times | responsible for the result. **You are.** |

The dangerous part is not obvious mistakes. It is code that runs without any error,
looks professional, and gives a **wrong number**. An assistant can be confidently wrong:
a wrong denominator, a function that does not exist, a date read the wrong way round. The
report goes out under your name, not the assistant's.

In this book the assistant is called **Tala**. Use whichever assistant your office allows;
the method is the same.

## The method: Ask → Run → Check

```{figure} images/ask_run_check_en.svg
:alt: A loop of three stations. Ask: name the columns and give fake example rows only. Run: run it in Colab and read the error. Check: test on a tiny case you can count by hand. An arrow from Check back to Ask says fix and ask again.
:width: 100%
Every piece of code in this book goes round this loop at least once.
```

1. **Ask.** Describe what you want, with the column names and a few made-up rows.
2. **Run.** Paste the code into a cell and run it. If there is an error, read the last
   line first. It usually says what is wrong.
3. **Check.** Test the code on a case so small you can count it by hand. Does the total
   match the number of rows? Is the denominator right? If anything is off, tell Tala what
   you saw and ask again.

**Check** is the step people skip, and the one this book trains most.

## Asking well: the five ingredients of a good prompt

A **prompt** is what you type to the assistant. Good prompts get good code. Put in:

1. **Context:** what the data is and what you are trying to do.
2. **Columns:** the exact column names, spelled as in the file.
3. **A tiny made-up example:** two or three invented rows, never real ones.
4. **Expected output:** what the answer should look like.
5. **Constraints:** what you need: beginner-friendly, comments on each line, only
   pandas, a way to check the result.

**Before:**

> count dengue per barangay

Tala has to guess everything: the file, the column names, whether you want a table or
a chart. You will get *some* code, probably with the wrong column names.

**After:**

:::{admonition} Ask Tala
:class: ph-ask-tala
I'm a surveillance officer learning Python. I have a pandas DataFrame `df`, one row per
case, with columns `case_id`, `disease` (`dengue` or `leptospirosis`), `barangay` and
`date_onset`. Three made-up rows:
`X-1, dengue, Barangay A, 2026-08-03` · `X-2, leptospirosis, Barangay A, 2026-07-27` ·
`X-3, dengue, Barangay B, 2026-08-04`.
Write beginner-friendly code that counts **dengue** cases per barangay, most to fewest,
with a comment on each line. For my three rows I expect A = 1, B = 1. Also show me a way
to check that the counts add up.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
dengue = df[df["disease"] == "dengue"]          # keep only dengue rows
counts = dengue["barangay"].value_counts()      # count rows per barangay
print(counts)
assert counts.sum() == len(dengue)              # check: every dengue row counted once
```
:::

:::{admonition} Check it
:class: ph-check
1. Run it on the three made-up rows first. You said you expect A = 1, B = 1. Do you get that?
2. The `assert` line checks the total. If it is silent, the counts add up.
3. Ask yourself: did it really drop the leptospirosis row? (It did: Barangay A shows 1, not 2.)
:::

Notice what is **not** in the good prompt: no names, no addresses, no real rows. You never
need real data to get good code. The made-up rows do the same job.

## Practise: pick the better prompt

:::{div}
:class: ph-game ph-game-prompt-pick
A good prompt names the columns, shows two or three made-up example rows,
says exactly what output you want, and asks for a way to check it.
:::

## The privacy pledge

You will handle data about real people's illnesses for the rest of your career.
[Chapter 02](02_privacy_first.md) explains the law and the techniques. Before you start,
make this promise.

:::{admonition} Privacy stop
:class: ph-privacy
**My pledge.** Before I use AI tools with health data, I promise that:

1. I will **never paste** names, phone numbers, addresses, ID numbers, exact birth dates
   or free-text remarks about a patient into an AI chat.
2. I will **describe the columns** and invent example rows instead.
3. I will **keep raw files inside the office**, on the computers and drives my office
   approves.
4. I will **check** every number before it leaves my desk, and remember that I am
   accountable for it, not the AI.
5. I will **ask my Data Protection Officer** when I am not sure.

Every row is a neighbour.
:::

## Quick check

:::{div}
:class: ph-game ph-game-quiz
**Quick check: start here**

1. Tala's code runs without any error. What does that tell you?
   - That the answer is right — no. Code can run perfectly and still give a wrong number.
   - ✓ Only that Python could run it — you still have to check the result on a case you can count by hand.
   - That Tala tested it — Tala cannot see your data or run your notebook.
2. Which of these belongs in a prompt?
   - Five real rows from the line list, to be precise — never: real rows identify real people.
   - ✓ The exact column names and two invented rows — that gives Tala everything it needs.
   - The patient's name, so Tala understands the case — names never go into an AI chat.
3. In Colab, a cell says a variable is not defined. What is the most likely cause?
   - ✓ An earlier cell was not run yet — run the cells from the top, in order.
   - Colab is broken — restarting helps sometimes, but the order of cells is the usual reason.
   - Your computer needs Python installed — no, Colab runs everything in the browser.
:::

:::{admonition} Baon
:class: ph-baon
- A notebook mixes text and code; Colab runs it in your browser. Run cells from the top,
  and save a copy in your Drive.
- Ask → Run → Check: an AI assistant predicts plausible code, so check every result on a
  case you can count by hand. You are accountable for the numbers.
- A good prompt has context, exact columns, made-up rows, the expected output and your
  constraints, and no real patient data.

Next stop: [01 Kumusta, Python?](01_python_with_ai.md)
:::
