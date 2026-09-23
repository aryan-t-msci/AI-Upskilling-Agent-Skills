# Agent Skills — course bundle

Everything from the DeepLearning.AI course **"Agent Skills with Anthropic"** (Elie Schoppik,
8 lessons), restructured into 14 modules and enriched with the published open specification,
the `anthropics/skills` repository, the course's own artifact repository and Anthropic's
platform documentation.

Compiled September 2026.

---

## What is here

| File | What it is | Open it with |
|---|---|---|
| `agent-skills-study-app.html` | Interactive study app — 14 modules, **short notes with the 12 course figures inlined**, 98 flashcards, 65 practice items, 13 concept diagrams, reference tables, glossary, gotcha index | Any browser, double-click |
| `agent-skills-quiz.html` | Timed assessment — 20 questions drawn from a bank of 75, 10 minutes, +1 / −1 marking, full review and PDF export | Any browser, double-click |
| `Agent-Skills-Study-Notes.docx` | 59-page study document with objectives, artifacts, gotchas and per-module self-check prompts | Word, or anything that reads .docx |
| `Agent-Skills-Training-Deck.pptx` | 40-slide training deck, 8 sections, MSCI Creative styling | PowerPoint |
| `Agent-Skills-Assessment-Bundle.xlsx` | Quiz bank, flashcards, spec cheat sheet, glossary and a live score tracker | Excel |
| `Agent-Skills-Quiz-Bank.xlsx` | The 75-question bank that drives the quiz app — five domains, 15 each — plus its config | Excel |
| `PROJECT-BRIEF.md` | The ask, constraints, decisions and open items | Any text editor |
| `src/` | Content spine and build scripts, so all of the above can be regenerated | — |

**Keep the two HTML files in the same folder.** They link to each other with relative paths —
the study app has a *Timed paper* button, and the quiz links back. No server is needed.

---

## Two sets of notes, on purpose

The study app carries **Short notes** and **Study** as separate sections, and they are not the same
material at different lengths.

- **Short notes** is the condensed write-up of the course, in the original lesson order, with the
  twelve figures from it inlined — the folder-structure diagram, the progressive-disclosure
  flowchart, the Skills vs MCP and Skills vs Tools slides, the Customer Insight Analyzer, the
  five-primitive summary table, the skill-creator pipeline and the Agent SDK example. Use it to
  revise quickly or to get someone oriented in twenty minutes.
- **Study** is the 14-module treatment: objectives, spec limits, worked artifacts, gotchas, and the
  enrichment modules on evaluation, security, portability and applied work. Use it when you need
  the depth or you are preparing to teach.

## Suggested path through it

1. **Skim the short notes** in the study app to get the shape of the whole thing.
2. **Read the notes** (`Agent-Skills-Study-Notes.docx`), module by module. Answer the
   *check yourself* prompts from memory before looking at Appendix C. Retrieval beats re-reading.
3. **Drill the flashcards** in the study app until the answer arrives before you finish reading
   the prompt. Filter by module to work on a weak area.
4. **Use the practice section** in the study app for open-ended work — no clock, no penalty,
   and short-answer items you grade yourself against a model answer.
5. **Sit the timed paper** when you want a score. 20 questions — four from each of the five
   domains — in 10 minutes, negative marking, no going back. Export the result as a PDF if you want a record.
6. **Teach it** from the deck. Each section stands alone, so a 30-minute session can take two
   or three sections rather than the whole thing.

---

## Module map

| # | Module | Source |
|---|---|---|
| 00 | Course map and the one-sentence mental model | Introduction |
| 01 | Why skills: from repeated prompt to packaged asset | Lesson 1 |
| 02 | Anatomy of a skill and the open standard | Lesson 2 |
| 03 | Progressive disclosure and context as a public good | Lesson 2 |
| 04 | Skills vs tools vs MCP vs subagents vs prompts | Lesson 3 |
| 05 | Pre-built skills, the marketplace and skill-creator | Lesson 4 |
| 06 | Authoring practice: descriptions, degrees of freedom, structure | Lesson 5 |
| 07 | Skills with the Claude Messages API | Lesson 6 |
| 08 | Skills in Claude Code, and wiring them to subagents | Lesson 7 |
| 09 | Skills with the Claude Agent SDK | Lesson 8 |
| 10 | Evaluating skills like software | enrichment |
| 11 | Security, trust and governance | enrichment |
| 12 | Portability, ecosystem and what is still moving | enrichment |
| 13 | Applying this to data-operations work | enrichment |

Modules 10 to 13 are additions. Progressive disclosure, evaluation and security are each buried
inside a lesson about something else, and each carries more weight than its screen time suggests.

---

## Verify before you teach this

Three claims sit on a fast-moving surface and were accurate as of September 2026:

1. **API beta headers and the code-execution tool version string.** The Skills API has gone GA,
   so its header is now optional, and newer code-execution tool versions exist. Exact strings
   appear throughout as dated examples.
2. **Subagent skill injection.** The `skills:` frontmatter field is documented to preload the full
   skill body at dispatch. There are open reports of it not behaving that way, while
   filesystem-capable subagents can often discover skills themselves.
3. **Stewardship of the standard.** Published openly in December 2025 and aligned with an industry
   foundation; long-term governance is still undecided.

Everything else — the specification limits, the directory conventions, the loading tiers, the
sandbox constraints — has been stable since the standard was published.

---

## Regenerating any of it

See `src/README.md`. In short: one content spine feeds every deliverable, so edit the spine and
re-run the relevant builder rather than editing four files by hand and watching them drift apart.
