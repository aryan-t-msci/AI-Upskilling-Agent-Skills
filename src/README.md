# src — content spine and builders

One spine feeds every deliverable. Edit the spine, re-run a builder, and the outputs stay
consistent with each other.

## Content spine

| File | Feeds |
|---|---|
| `content_modules_a.py` | Modules 00–06 |
| `content_modules_b.py` | Modules 07–13 |
| `content_cards.py` | 98 flashcards and 24 glossary terms |
| `content_quiz.py` | 65 practice items used by the study app, the workbook and the notes appendix |
| `diagrams.js` | 13 SVG concept diagrams for the study app |
| `quiz_bank.py` | The 75-question timed-paper bank across five domains (separate from `content_quiz.py`) |
| `content_shortnotes.py` | The Short notes section — condensed course write-up, sectioned into blocks |
| `figures/` | The 12 figures from the source write-up, inlined into the study app as base64 at build time |

Two separate question sets, on purpose. `content_quiz.py` is open-ended practice, including
short-answer and applied items you grade yourself. `quiz_bank.py` is the timed paper: exactly one
correct option, a deliberate near-miss, and a balance the build enforces.

### Figures

`build_app.py` reads every `fig` block in `content_shortnotes.py`, loads the named file from
`figures/`, and inlines it as a base64 data URI so the app stays one file. A missing figure fails
the build rather than shipping a broken image. The originals were extracted from the source PDF
with `pdfimages -j` and resized to 1200 px wide at quality 80, which is what keeps the app around
1.1 MB rather than several.

## Builders

Every builder writes to `$BUNDLE_OUT`, defaulting to `/mnt/user-data/outputs`. To regenerate in
place, point it at the repo root:

```bash
cd src
export BUNDLE_OUT=..

python3 build_app.py          # -> agent-skills-study-app.html
python3 build_xlsx.py         # -> Agent-Skills-Assessment-Bundle.xlsx
python3 build_deck.py         # -> Agent-Skills-Training-Deck.pptx     (see requirements)
python3 make_doc_data.py      # -> doc_data.json (intermediate)
node     build_docx.js        # -> Agent-Skills-Study-Notes.docx
python3 build_quiz_app.py     # -> agent-skills-quiz.html              (reads the bank workbook)
```

### The quiz bank is authoritative

`build_quiz_app.py` **reads** `Agent-Skills-Quiz-Bank.xlsx` and never writes to it. So the normal
loop is: edit the workbook — questions, options, the correct letter, rationales, or any value on
the Config sheet — then run `build_quiz_app.py`. The app follows.

`build_quiz_bank.py` goes the other way: it regenerates the workbook from `quiz_bank.py` and
**overwrites it**. Use it to create the workbook or to reset it after editing the Python source.
Do not run it once your edits live in the workbook.

It also **spreads the correct answer across A, B, C and D** before writing. Authoring puts the right
answer first, which is convenient to write and useless to sit. The spread is round-robin over list
order — deterministic, so rebuilds are byte-identical, and even by construction. The app shuffles
option order again at run time on top of this.

It enforces the bank's design and fails rather than shipping an unbalanced set:

- equal questions per domain, and per difficulty level within each domain
- enough of each kind per domain to satisfy the draw. With 20 questions over five domains that is
  4 per domain, split 3 applied + 1 recall, so each domain needs at least 3 applied and 1 recall.
  Adding or removing a domain changes this arithmetic — `questions_per_attempt` should stay
  divisible by the number of domains on the Domains sheet
- an applied share between 75% and 85%
- an even spread of the correct letter, overall and within each domain

### Adding questions by hand

Append rows to the **Question Bank** sheet in the same column order and run
`build_quiz_app.py`. Three things to get right:

1. **Rebuild after editing.** The app embeds the questions at build time — a browser cannot read a
   local .xlsx — so the existing HTML does not change until the builder runs again.
2. **Use a domain code that exists on the Domains sheet.** With `stratify_by_domain=1` the draw
   picks per domain from that sheet, so a question in an unlisted domain is silently never drawn.
   Add the code and label to the Domains sheet first, or reuse an existing one.
3. **Fill the Kind column.** A blank defaults to `applied`. Each domain needs enough of both kinds
   to satisfy the per-paper split, or the draw quietly tops up from whatever the domain has.
4. **Never name an option by letter** in the Rationale or Distractor note. Option order is shuffled
   on every attempt, so "B is tempting" points at nothing by the time the learner reads the review.
   Quote the option's wording instead. Put the correct answer in whichever slot you like — the
   builder redistributes it anyway.

`build_quiz_app.py` now validates the workbook on every run: it skips and reports rows missing a
question, options or a valid Correct letter, and warns about unlisted domains, bad or missing Kind,
duplicate IDs, empty Distractor notes and domains too thin for the draw. It prints the resulting
per-domain counts and applied share so you can see what the app actually received.

Note that the balance asserts in `build_quiz_bank.py` do **not** run on a hand-edited workbook —
those only fire when the bank is regenerated from `quiz_bank.py`. Keeping the counts even is on you
in that case, and the validation summary is how you check.

### Config you can change without touching code

On the workbook's Config sheet: questions per attempt, time limit, marks for correct, incorrect
and skipped, whether to stratify by domain, and whether to show a Skip button. Edit a value, run
`build_quiz_app.py`, and the app reflects it.

## Requirements

| Builder | Needs |
|---|---|
| `build_app.py`, `build_quiz_*.py`, `make_doc_data.py` | Python 3.11+, `openpyxl` |
| `build_xlsx.py` | Python 3.11+, `openpyxl`. Run the xlsx recalc helper afterwards so cached formula values are current |
| `build_docx.js` | Node with the `docx` package |
| `build_deck.py` | **The `msci-pptx-skill` on the Python path** — it imports `creative_builders` and opens `MSCI_Creative_Template.pptx`. This one only rebuilds in an environment where that skill is installed. The generated .pptx in the repo root is fully editable without it. |

## Conventions worth keeping

- Claims that could date carry the date and a verify-first note. Do not quietly drop those.
- Every timed-paper question needs a `Distractor note` explaining why the closest wrong option
  fails — it is shown to the learner in the review, and it is most of the teaching value.
- The apps hold no state between sessions by design. Cohort tracking belongs in the score tracker
  sheet of `Agent-Skills-Assessment-Bundle.xlsx`.
