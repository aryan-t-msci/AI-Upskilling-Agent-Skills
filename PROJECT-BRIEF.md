# Project brief — Agent Skills course bundle

Standalone record of the ask, constraints and decisions, so the project survives a new session or
a move to a different tool. Last updated 22 September 2026.

## The ask

Turn the DeepLearning.AI course **"Agent Skills with Anthropic"** (Elie Schoppik, 8 lessons, full
transcripts supplied) into a complete course-content bundle: notes, presentation, quiz, memory
flashcards, concept visuals and real artifacts, with gaps filled and confusing parts clarified
through research. Role taken: expert course curator working through an existing course.

Later additions: a separate timed quiz app driven by an Excel bank, this repo packaging, and a
**Short notes** section in the study app built from the user's own condensed PDF write-up of the
course — with its twelve figures extracted and inlined, and twelve further questions derived from
it added to the timed-paper bank plus ten to the practice set.

## Constraints and decisions

| Decision | Choice | Source |
|---|---|---|
| Deliverable formats | Branded files **and** an interactive HTML study app | user choice |
| Audience | Deep notes for the user **and** a trainable deck and quiz for the team | user choice |
| Enrichment level | Moderate-to-heavy: fill gaps, plus gotchas and adoption landscape | user choice |
| Notes format | Branding dropped — plain, retention-optimised layout instead | user override |
| Author byline | None | user choice |
| Deck | "Best possible for training" → MSCI Creative Mode, training theme | user choice |
| Screenshots | Course video frames not extractable; substituted real artifacts — SKILL.md excerpts, folder trees, API traces, CLI commands | constraint |
| Quiz scope | 20 questions per attempt, 10 minutes, +1 / −1, one at a time, no revisit, auto-submit, review, PDF | user spec |
| Quiz bank | 75 questions across five domains, 15 each; Excel is the editing surface, `quiz_bank.py` the source of truth | design |
| Fifth domain | `SKL` — Agent Skills and Claude Code workflow — contributed via the workbook, completed to 15 | user |
| Quiz content | 80/20 applied to recall, enforced per paper; framed in geospatial, ESG, climate and quality-process work | user spec |
| Quiz balance | 12 per domain, 16 per difficulty level; asserted at build time | user spec |

## Structure choice

The 8 lessons were restructured into **14 modules**. Three subjects are buried inside lessons
about something else and carry more weight than their screen time: progressive disclosure,
evaluation and security. Modules 00–09 track the lessons; 10–13 are the enrichment layer
(evaluation including the skill-creator harness the course does not reach, security and
governance, portability and ecosystem, and applied batch-verification work).

## Research inputs beyond the transcripts

- agentskills.io specification and client showcase (open standard, published December 2025)
- github.com/anthropics/skills — document skills, example skills, skill-creator scripts
- github.com/https-deeplearning-ai/sc-agent-skills-files — the course's own artifacts
- Anthropic platform documentation: Skills API, code execution tool, Files API, Claude Code skills
  and subagents, Agent SDK
- Third-party audits of public skill registries, for security and quality context (indicative only)

## Known version drift — re-verify before teaching

1. **API surface.** The Skills API has gone GA, so its beta header is now optional, and the
   code-execution tool has versions newer than `code_execution_20250825`. Exact strings are kept
   for reproducibility but are dated examples.
2. **Subagent skill injection.** Documentation describes the `skills:` frontmatter field preloading
   full skill content. There are open reports of it not behaving that way, while filesystem-capable
   subagents can often discover skills anyway. Present the documented behaviour, flag the caveat.
3. **Standard governance.** Published openly and aligned with an industry foundation; long-term
   stewardship still undecided.

## Deliverables

| File | What it is |
|---|---|
| `agent-skills-study-app.html` | 14 modules, a Short notes section with 12 inlined course figures, 98 flashcards, 60 practice items, 13 SVG diagrams, reference tables, glossary, gotcha index. Session-only progress. Links to the timed paper. |
| `agent-skills-quiz.html` | Timed assessment: 20 of 75 questions, 10 minutes, +1/−1/0, one at a time, no revisit, auto-submit, per-question review, PDF export with a sandbox fallback. |
| `Agent-Skills-Study-Notes.docx` | 59 pages. Per module: objective, key points, reference facts, in-depth prose, artifacts, gotchas, check-yourself prompts. Appendices: spec cheat sheet, glossary, answer key. |
| `Agent-Skills-Training-Deck.pptx` | 40 slides, 8 sections, ~20 diagram types, MSCI Creative styling. QA: 0 errors. |
| `Agent-Skills-Assessment-Bundle.xlsx` | 6 sheets, 312 formulas. Practice bank, flashcards, spec cheat sheet, glossary, score tracker with per-module and per-type breakdowns. |
| `Agent-Skills-Quiz-Bank.xlsx` | The 75-question timed-paper bank plus its config. Regenerated from `quiz_bank.py`. |
| `src/` | Content spine and all builders, with `BUNDLE_OUT` so the repo rebuilds itself in place. |

## Validation performed

- Study app and quiz app: every view rendered headlessly without error; 400 simulated papers
  checked for length, duplicates, domain balance, the 4-applied + 1-recall split and
  option-to-answer mapping integrity. All 60 bank questions confirmed reachable across those
  papers, and every inlined figure confirmed to decode as a valid image.
- Quiz bank: build-time asserts on domain, difficulty and applied share; every row checked for a
  single-letter correct answer, a valid kind and a non-empty distractor note.
- Workbooks: recalculated with zero formula errors.
- Deck: skill QA check, 0 errors; slides visually inspected and four reworked after review.
- Notes: rendered to PDF and inspected; cover and heading defects fixed.
- Full pipeline re-run into a clean output directory to confirm the repo reproduces every artifact.

## Sources of question content

- `quiz_bank.py` — 60 timed-paper questions: 48 written from the transcripts and research, 12 from
  the condensed write-up (allowed-tools as a capability limiter, deferred tools, the persistence
  row of the summary table, the container_upload mailbox pattern, pre-installed libraries, the
  skill-creator pipeline order, tools as the floor under skills, and per-subagent skill scoping).
- `content_quiz.py` — 65 practice items; ten from the write-up and five covering the Claude Code
  workflow material, so the practice set stays thematically in step with the timed paper.
- `SKL` domain — ten questions contributed through the workbook (progressive disclosure, hooks,
  project skill location, enterprise settings, description quality, script output, subagents for
  context isolation, name-conflict precedence, slash commands, subagent skill inheritance) plus
  five written to complete the grid (plugin namespacing, `disable-model-invocation`, plugin
  distribution, the commands-to-skills merge, and why a project skill cannot enforce a mandate).

## Open items

- Re-verify the three version-drift points above before any external delivery.
- The L6 skill inventory in the course files repo lists `adding-cli-command` and
  `reviewing-cli-command`; the transcript also names `generating-cli-tests`. Confirm against the
  live repository if quoting file names exactly.
- `build_deck.py` only re-runs where the `msci-pptx-skill` is installed. The generated .pptx is
  fully editable without it.
- The uploaded workbook was based on a pre-fix copy of the bank: it reinstated the option-letter
  references in the rationales and reset every answer to A. No existing question had been edited,
  so the corrected versions were kept and only the ten new rows were taken. Anyone editing the
  workbook should re-download it after a rebuild to avoid reintroducing fixed issues.
- Difficulty is balanced within the quiz bank, not within an individual paper. The draw balances
  domain and question kind instead. Changing that is a small edit to the draw rule.
