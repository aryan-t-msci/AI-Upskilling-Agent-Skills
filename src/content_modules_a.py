"""Agent Skills course content - modules A (0-6).

Each module dict:
  id, num, title, lesson, duration_min, objective
  key_points: list[str]             - retainable bullets
  deep_dive: list[str]              - prose paragraphs (senior-practitioner depth)
  spec_box: list[(label, value)]    - hard facts / limits
  artifacts: list[dict]             - real code/file artifacts {title, lang, code, caption}
  gotchas: list[str]
  visual: str | None                - diagram id rendered in the HTML app
"""

MODULES_A = [
{
 "id": "m0", "num": "00", "title": "Course Map and the One-Sentence Mental Model",
 "lesson": "Introduction", "duration_min": 8,
 "objective": "Hold the whole course in one frame before any code: what a skill is, what it is not, and the order in which the eight lessons build on each other.",
 "key_points": [
   "A skill is a **folder of instructions** that gives an agent procedural knowledge it did not have — nothing more exotic than that.",
   "Minimum viable skill = one file: `SKILL.md`, with YAML frontmatter carrying `name` and `description`, plus a markdown body.",
   "Optional companions: other markdown files, executable scripts, and assets (templates, logos, schemas).",
   "The runtime requirement is small and fixed: **filesystem access + a bash-style execution tool**. No special model, no special API.",
   "Progressive disclosure is the whole trick: only `name` + `description` sit in context permanently; the body loads on match; bundled files load only if the body asks for them.",
   "Skills are an **open standard**, so one folder runs across Claude Code, Claude.ai/Desktop, the API, the Agent SDK, Codex, Gemini CLI, Copilot, Cursor, OpenCode and ~40 other products.",
   "Course arc: Claude.ai (L1–L4) → Claude API (L5) → Claude Code (L6) → Agent SDK (L7). Same folder, four harnesses.",
 ],
 "deep_dive": [
   "The trigger for building a skill is behavioural, not technical: **if you are retyping the same prompt across conversations, that prompt has become a workflow, and workflows belong in version control rather than in your clipboard.** Everything else in the course is downstream of that observation.",
   "It helps to separate three things people conflate. *Capability* is whether the agent can do the thing at all (tools give this). *Knowledge* is whether the agent knows your particular way of doing the thing (skills give this). *Context economy* is whether knowing it costs you tokens on every unrelated turn (progressive disclosure gives this). A skill is the second and third of those, and it leans on the first.",
   "The course deliberately teaches the same skill folder in four increasingly bare harnesses. Claude.ai hands you a container, a filesystem and built-in document skills for free. The Messages API hands you nothing — you must switch on the code execution tool and the Files API yourself. Claude Code hands you a real filesystem and adds subagents. The Agent SDK hands you the Claude Code harness programmatically and makes you wire every tool by name. By L7 you can see exactly which conveniences were doing which job.",
 ],
 "spec_box": [
   ("Required files", "SKILL.md (1)"),
   ("Required frontmatter", "name, description"),
   ("Runtime floor", "filesystem + bash/exec tool"),
   ("Course lessons", "8 (intro + 7)"),
   ("Harnesses covered", "Claude.ai/Desktop, Messages API, Claude Code, Agent SDK"),
 ],
 "artifacts": [
   {"title": "The smallest legal skill", "lang": "markdown", "code": """---
name: analyzing-marketing-campaign
description: Analyze weekly marketing campaign performance from CSV or BigQuery data. Use when the user asks about campaign metrics, funnel analysis, ROAS, or budget reallocation.
---

# Analyzing Marketing Campaign Performance

## Input requirements
...

## Budget reallocation
When the user asks about budget reallocation, read
references/budget_reallocation_rules.md and apply it in full.""",
    "caption": "The course's first skill, reduced to its load-bearing parts. Two frontmatter keys and a body that defers its bulkiest section to a reference file."},
 ],
 "gotchas": [
   "A skill is not a tool. It cannot grant an agent an ability the harness does not already have; it can only direct abilities the harness already has.",
   "A skill is not a prompt template you paste. If it is not on disk in a discoverable folder, the agent cannot find it, and none of the loading mechanics apply.",
 ],
 "visual": "skill-anatomy",
},

{
 "id": "m1", "num": "01", "title": "Why Skills: From Repeated Prompt to Packaged Asset",
 "lesson": "Why Use Skills, Part I", "duration_min": 14,
 "objective": "Reconstruct the marketing-campaign walkthrough and be able to name the four specific costs of the prompt-based version that the skill removes.",
 "key_points": [
   "The demo case: weekly marketing campaign analysis from a CSV of date, campaign, impressions, clicks, conversions.",
   "Prompt-based flow needed three escalating turns: quality check + funnel analysis, then efficiency metrics (ROAS, CPA, net profit), then budget reallocation rules pasted in as a third document.",
   "Cost 1 — **repetition**: the operator retypes or re-pastes the spec every week.",
   "Cost 2 — **tacit knowledge**: the operator must already know the benchmarks and the reallocation framework, or go find the person who does.",
   "Cost 3 — **context pollution**: every pasted document stays in the window for the rest of the conversation even when the topic moves on.",
   "Cost 4 — **no distribution**: the workflow lives in one person's chat history, not in a shareable, editable asset.",
   "The fix is structural, not clever: move the instructions into `SKILL.md`, move the bulky conditional rules into `references/`, zip the folder, upload once.",
   "Composition is the payoff: the custom analysis skill hands its output to Claude's **built-in Excel skill**, which writes a colour-coded workbook with executive summary, funnel and efficiency tabs.",
 ],
 "deep_dive": [
   "The walkthrough is worth reading as a cost curve rather than a demo. Turn one is cheap. Turn two needs the operator to remember which efficiency metrics matter and in what output shape. Turn three needs an external document describing budget reallocation rules — a document the operator did not write and may not fully understand. By turn three the conversation contains three specifications and one dataset, and none of the specifications will survive into next week's chat.",
   "Notice which part becomes a reference file rather than body text. Budget reallocation is **conditional** — most weeks nobody asks for it — and **long**, because it encodes thresholds, guardrails and a decision framework. That combination (rarely needed + bulky) is the exact signature of a `references/` file. The SKILL.md keeps one line pointing at it: read this file only when the user asks about reallocation.",
   "Folder naming conventions appear here for a reason. Lowercase, hyphenated, gerund-style (`analyzing-marketing-campaign`), no reserved vendor words. The folder name is not cosmetic: under the open standard the folder name and the frontmatter `name` must match, and the API rejects names containing `anthropic` or `claude`.",
   "The Claude.ai install path is deliberately mundane: zip the folder, Settings → Capabilities → Skills → Add, drag the zip. After upload the UI shows the skill's name and description — the same two fields the model will use to decide whether to fire it. If the description reads badly in the settings list, it will trigger badly in conversation.",
   "The final step of the lesson is the first composition: a custom skill produced the analysis, a built-in document skill produced the artefact. Nobody wrote spreadsheet code. That division — *my domain logic, vendor's file-format mechanics* — is the single most reliable way to get value out of skills in week one.",
 ],
 "spec_box": [
   ("Naming", "lowercase, hyphens, gerund form"),
   ("Forbidden in name", "'anthropic', 'claude'"),
   ("Folder vs name", "must match under the open spec"),
   ("Install in Claude.ai", "zip folder → Settings → Capabilities → Skills → Add"),
   ("Reference path in body", "references/<file>.md, relative, one level deep"),
 ],
 "artifacts": [
   {"title": "Folder layout produced in Lesson 1", "lang": "text", "code": """analyzing-marketing-campaign/
├── SKILL.md
└── references/
    └── budget_reallocation_rules.md""",
    "caption": "Two files. The conditional, bulky rule system is pulled out of SKILL.md so it costs nothing on the weeks nobody asks about reallocation."},
   {"title": "The 'load only if asked' pattern", "lang": "markdown", "code": """## Budget reallocation

Only when the user asks about reallocating budget, read
`references/budget_reallocation_rules.md` and apply every rule in it.
Do not summarise the rules — apply them as written.""",
    "caption": "The instruction that makes progressive disclosure happen. Without an explicit read directive, a bundled file is just a file the agent never opens."},
 ],
 "gotchas": [
   "Uploading a skill to Claude.ai does not make it available in the API or in Claude Code. Those are separate stores; the same folder must be installed separately in each.",
   "The zip must contain the skill folder with SKILL.md at its top level. Zipping the contents without the parent folder, or nesting an extra directory, breaks the upload.",
   "Anything you paste into the chat still pollutes context. Moving it to a reference file only helps if the skill reads it conditionally rather than unconditionally.",
 ],
 "visual": "prompt-to-skill",
},

{
 "id": "m2", "num": "02", "title": "Anatomy of a Skill and the Open Standard",
 "lesson": "Why Use Skills, Part II", "duration_min": 16,
 "objective": "Write frontmatter that validates against the published specification, and place every kind of payload — markdown, script, asset — in the directory the standard expects.",
 "key_points": [
   "`name`: required, ≤ **64 characters**, lowercase alphanumeric plus hyphens, no leading/trailing hyphen, no consecutive hyphens, must match the parent directory name.",
   "`description`: required, ≤ **1024 characters**, non-empty. Must describe *what it does* **and** *when to use it*.",
   "Optional fields in the spec: `license`, `compatibility` (≤ 500 chars), `metadata` (arbitrary string→string map), and the experimental `allowed-tools`.",
   "Unknown top-level fields are ignored for forward compatibility — but wrong casing, duplicate keys or invalid YAML stop the skill loading entirely.",
   "Three conventional directories: `scripts/` (code to execute), `references/` (docs to read on demand), `assets/` (templates, logos, schemas, images used in output).",
   "Body: no format restrictions, but keep it under ~**500 lines** / ~5,000 tokens and defer the rest to reference files.",
   "Skills are where the agent lacks *your* way of working — brand guides, newsletter formats, review conventions — not where it lacks general competence.",
   "The standard was published openly in **December 2025** and aligned with the Agentic AI Foundation; long-term stewardship is still an open question.",
 ],
 "deep_dive": [
   "Frontmatter deserves more care than its size suggests, because it is the only part of the skill the model sees before deciding to load anything. Everything else in the folder is invisible until the description wins. Treat the description as a routing key written for a reader who will see it alongside fifty others, not as marketing copy.",
   "The three-directory convention is not arbitrary; each maps to a different loading mechanic. `references/` files are **read into context** when the body tells the agent to read them — so their size is a context cost you pay at read time. `scripts/` files are **executed**, and only their stdout enters context — so a 600-line Python file can cost you thirty tokens of output. `assets/` are consumed by code or embedded in output — a `.pptx` template, a logo PNG, a JSON schema — and often never enter context at all. Choosing the right directory is therefore a token-budgeting decision disguised as a filing decision.",
   "The lesson's PDF example makes the script case concrete: converting PDFs to images, extracting form fields, filling forms with annotations. None of that is describable in prose the model can execute; it needs real code. So the SKILL.md's job shrinks to *which script, which arguments, when* — the deterministic steps stay in Python where they cannot drift.",
   "The 'where skills shine' framing is the part practitioners under-use. Claude can design a newsletter, review a contract, build a deck. What it cannot know is that your firm puts the disclaimer on page two, uses one specific blue, never uses serial commas, and files everything under a naming convention with a ticket ID in it. That gap — general competence minus house convention — is the highest-yield skill surface in any organisation.",
   "Also from this lesson: the **agent-design argument**. The industry moved from many single-purpose agents (each with bespoke tools and context) towards one simple harness — bash plus a filesystem — that is easier to evaluate and scale. That simpler harness is more capable but less knowledgeable. Skills are the mechanism that re-injects domain expertise into a deliberately generic agent, on demand, without inflating it.",
   "Three distinct things skills deliver, worth naming separately because they justify different skills: **domain expertise** (do it our way), **repeatable workflow** (do it in this order, every time, in a non-deterministic system), and **new capability** (do something the agent genuinely could not do, usually via bundled scripts).",
 ],
 "spec_box": [
   ("name max", "64 chars"),
   ("description max", "1024 chars"),
   ("compatibility max", "500 chars"),
   ("Body target", "< 500 lines / < 5,000 tokens"),
   ("Metadata tier cost", "~100 tokens per skill"),
   ("Conventional dirs", "scripts/ · references/ · assets/"),
   ("Spec published", "18 Dec 2025, agentskills.io"),
   ("Validator", "skills-ref validate ./my-skill"),
 ],
 "artifacts": [
   {"title": "Full frontmatter with every spec field", "lang": "yaml", "code": """---
name: reviewing-cli-command
description: Review a newly added CLI command for structure, type annotations, registration and error handling. Use when the user asks to review a command, check a CLI implementation, or validate that a command follows project conventions.
license: Apache-2.0
compatibility: Requires Python 3.11+, pytest and a POSIX shell. Needs no network access.
metadata:
  author: platform-tooling
  version: "1.4"
allowed-tools: Bash(pytest:*) Bash(git:*) Read Grep
---""",
    "caption": "Only the first two keys are required. `allowed-tools` is experimental and honoured in some products (notably Claude Code) and silently ignored in others."},
   {"title": "Directory layout with all three payload types", "lang": "text", "code": """analyzing-time-series/
├── SKILL.md                  # orchestration: which script, which order, what to report
├── scripts/
│   ├── diagnose.py           # executed - only stdout enters context
│   └── visualize.py          # executed - writes plots to results/plots/
├── references/
│   └── interpretation.md     # read on demand - costs tokens when read
└── assets/
    └── report_template.md    # consumed by code / embedded in output""",
    "caption": "The course's time-series skill. Statistics stay in Python where they are deterministic; the SKILL.md only sequences them."},
 ],
 "gotchas": [
   "Angle-bracket / XML-like tags in `name` or `description` are an injection risk and are rejected by both the spec guidance and the API.",
   "Casing matters: `Name:` or `Description:` in frontmatter is not the same field as `name:` / `description:` and will fail to load.",
   "Filename should be `SKILL.md` in uppercase. Some implementations accept `skill.md` as a fallback; do not rely on it if portability matters.",
   "You will encounter real skills — including some from vendors — that predate or ignore the directory conventions. The standard is young and still moving; read before you copy.",
 ],
 "visual": "skill-anatomy",
},

{
 "id": "m3", "num": "03", "title": "Progressive Disclosure and Context as a Public Good",
 "lesson": "Why Use Skills, Part II", "duration_min": 12,
 "objective": "Explain the three loading tiers precisely enough to predict, for any given skill, what it costs when idle and what it costs when fired.",
 "key_points": [
   "Tier 1 — **metadata**: `name` + `description` for *every* installed skill, loaded at session start. ~100 tokens each. This is the only permanent cost.",
   "Tier 2 — **instructions**: the full SKILL.md body, loaded when the description matches the request.",
   "Tier 3 — **resources**: reference files, assets, scripts — loaded or executed only if the body directs it.",
   "Executed scripts are the cheapest tier of all: the source never enters context, only the output does.",
   "Reported effect: roughly **70–90% token savings** versus loading the same material as static context; a skill bundling 50k tokens of reference material can cost ~100 tokens on a turn where it never fires.",
   "Treat the context window as a **public good**: every token you add raises cost, fills the window faster and increases the odds of degradation or a wrong answer.",
   "This is why a system can carry 100+ skills without collapsing — the fixed cost is metadata only.",
 ],
 "deep_dive": [
   "The arithmetic is worth doing once, because it changes how you design. Fifty installed skills at ~100 tokens of metadata is ~5,000 tokens of standing overhead — real, but bounded and predictable. The same fifty skills loaded in full might be 250,000 tokens, which is not a budgeting problem but an architectural impossibility. Progressive disclosure is what converts 'a library of expertise' from impossible to routine.",
   "The script tier is the one people forget to exploit. If a procedure is deterministic — statistical tests, XML surgery on an Office file, a validation pass — putting it in `scripts/` means the agent pays for the *call and the result*, not the method. It also means the method cannot drift between runs, which is the second, quieter argument for scripts: determinism, not just economy.",
   "There is a corollary that constrains skill design: **the description must be self-sufficient.** The model decides whether to open the body using nothing but ~100 tokens of metadata. Anything essential to the routing decision that lives only in the body is, for routing purposes, invisible. This is the root cause of most 'my skill never fires' reports.",
   "Context degradation is the reason the framing is 'public good' rather than 'cost'. A window that is 80% full of stale specifications is not merely expensive — it demonstrably produces worse answers, because relevant material competes with irrelevant material for the model's attention. Skills are as much an accuracy mechanism as an economy one.",
 ],
 "spec_box": [
   ("Tier 1 cost", "~100 tokens / skill, always loaded"),
   ("Tier 2 target", "< 5,000 tokens (body)"),
   ("Tier 3 cost", "only when read / executed"),
   ("Script cost", "stdout only; source never tokenised"),
   ("Reported saving", "~70-90% vs static context"),
   ("Practical skill count", "100+ supported"),
 ],
 "artifacts": [
   {"title": "What actually loaded, from the Lesson 5 API trace", "lang": "text", "code": """1. bash: cat /skills/generating-practice-questions/SKILL.md     <- tier 2
2. bash: cat /mnt/user-data/uploads/notes04.tex                 <- input
3. bash: cat /skills/generating-practice-questions/assets/markdown_template.md
                                                                <- tier 3, only
                                                                   because markdown
                                                                   output was asked for
4. python: write questions to notes04.md
5. cp to output dir -> file_id returned""",
    "caption": "The LaTeX template in the same assets/ folder was never opened, because the request asked for markdown. That is progressive disclosure visible in a trace."},
 ],
 "gotchas": [
   "Progressive disclosure does **not** apply inside a dispatched subagent in Claude Code: a skill attached to a subagent has its full SKILL.md injected at startup. Budget accordingly.",
   "A reference file the body reads unconditionally is not progressively disclosed — it is just a slower way of writing a long SKILL.md.",
   "Metadata cost is per *installed* skill, not per used skill. A bloated skill library still has a standing tax; prune it.",
 ],
 "visual": "progressive-disclosure",
},

{
 "id": "m4", "num": "04", "title": "Skills vs Tools vs MCP vs Subagents vs Prompts",
 "lesson": "Skills vs Tools, MCP and Subagents", "duration_min": 15,
 "objective": "Given a requirement, pick the right primitive and justify the choice on context, permissions and persistence grounds rather than taste.",
 "key_points": [
   "**Prompt** — most atomic unit of communication. Reactive, ephemeral, does not scale across people or sessions.",
   "**Tool** — low-level capability. Tool *definitions live in the context window permanently*; skills load progressively.",
   "**MCP** — connectivity to external systems and data (databases, Drive, BigQuery, Notion). Brings the tooling; says nothing about how to use it well.",
   "**Skill** — procedural knowledge: which tools, in what order, to what standard, producing what output.",
   "**Subagent** — isolated context window, restricted tool permissions, parallel execution. Reports back to the parent.",
   "The carpentry analogy: tools are the hammer, saw and nails; the skill is *how to build the bookshelf*.",
   "MCP + skill is the canonical pairing: MCP supplies secure connectivity, the skill supplies the procedural knowledge for using it effectively.",
   "Decision rule: **skills for procedural, predictable workflows; subagents for full agentic logic, only when a task genuinely needs its own context.**",
   "If multiple agents or conversations need the same expertise, that is a skill — not a subagent.",
 ],
 "deep_dive": [
   "The cleanest way to keep these straight is to ask what each one costs you when it is *not* being used. An MCP server's tool definitions sit in context whether or not you call them — which is why a dozen chatty MCP servers can eat a window before you type anything. A skill costs ~100 tokens. A subagent costs nothing until dispatched, then costs a whole separate window that the parent never sees. Those three cost profiles, not the vocabulary, are what should drive the choice.",
   "The composition pattern in the lesson is the one to internalise: **MCP brings the data in, subagents parallelise the work, skills make the output predictable.** The worked example is a customer-insight analyser — MCP servers supply the survey and interview data, subagents analyse interviews and surveys in isolation and in parallel, and skills define how feedback is categorised, how findings are summarised, and what the report must look like every time.",
   "Skills can also act as *deferred tools*. If a capability is only needed in a small fraction of conversations, bundling the script inside a skill means its cost is paid only when the skill fires, instead of a permanent tool definition in the window. That is a genuine architectural use of progressive disclosure, not a trick.",
   "On persistence: subagents persist across sessions between parent and child; skills persist across conversations between user and application. Neither is memory in the long-term sense, but for teams the practical difference is that a skill is a reviewable artefact in a repository, and a conversation is not.",
   "Subagents in Claude Code carry an important asymmetry: they do **not** inherit skills from the parent, and cannot spawn further subagents. Both constraints exist to keep the context topology a shallow tree rather than a graph, and both catch people out the first time.",
 ],
 "spec_box": [
   ("Tool definitions", "always in context"),
   ("Skill metadata", "~100 tokens, in context"),
   ("Skill body", "on match only"),
   ("Subagent context", "isolated window; not shared with parent"),
   ("Subagent nesting", "not allowed (no Task tool inside)"),
   ("Skill inheritance", "subagents do not inherit parent skills"),
 ],
 "artifacts": [
   {"title": "Choosing the primitive - a working decision table", "lang": "text", "code": """Need                                        -> Primitive
------------------------------------------------------------------
Reach an external system or dataset          -> MCP server
Give the agent a raw capability it lacks     -> Tool
Encode our house method for a recurring job  -> Skill
Make a non-deterministic output predictable  -> Skill (explicit steps)
Ship the same expertise to many agents       -> Skill (not a subagent)
Isolate a noisy task from the main window    -> Subagent
Run N independent investigations at once     -> Subagents in parallel
Restrict what a step is allowed to touch     -> Subagent with tool allow-list
One-off instruction for this turn only       -> Prompt""",
    "caption": "The test that matters is context cost, permission scope and reuse across agents — not which word sounds most advanced."},
 ],
 "gotchas": [
   "Reaching for a subagent when you needed a skill is the commonest architectural error: it buys isolation you did not need and loses reusability you did.",
   "MCP tool definitions are a standing context cost. Auditing which servers are connected is part of context hygiene.",
   "A skill cannot enforce permissions. If a step must be prevented from writing files, that is a subagent tool allow-list or a permission hook, not a sentence in SKILL.md.",
 ],
 "visual": "ecosystem-map",
},

{
 "id": "m5", "num": "05", "title": "Pre-Built Skills, the Marketplace and skill-creator",
 "lesson": "Exploring Pre-Built Skills", "duration_min": 14,
 "objective": "Know what ships in the box, how to install vendor skill collections into Claude Code, and how to use skill-creator to author, modify and grade skills instead of hand-rolling folders.",
 "key_points": [
   "Two families in `github.com/anthropics/skills`: **document skills** (docx, pdf, pptx, xlsx) and **example skills** (skill-creator, mcp-builder, webapp-testing, brand-guidelines, canvas-design, frontend-design, artifacts-builder, algorithmic-art and more).",
   "Document skills are **built into Claude.ai and Claude Desktop** and cannot be toggled off — they are what makes 'give me an Excel file' work.",
   "Example skills are toggleable in Claude settings and are **off by default**, with skill-creator the exception (on).",
   "Claude Code ships with **none** of them: install via marketplace — `/plugin marketplace add anthropics/skills`, then install the `document-skills` and/or `example-skills` collections.",
   "Installed collections are recorded in `.claude/settings.json` under `enabledPlugins`; Claude Code must be **restarted** before `/skills` shows them.",
   "Document skills work by treating Office files as ZIP+XML: unpack, edit XML or run helper scripts, repack; several shell out to headless LibreOffice.",
   "`skill-creator` is the meta-skill: it scaffolds, packages, validates, and — in current versions — **benchmarks and optimises** skills.",
   "Its scripts include `package_skill.py`, `quick_validate.py`, `run_eval.py`, `run_loop.py`, `aggregate_benchmark.py` and an eval viewer (`generate_review.py`).",
 ],
 "deep_dive": [
   "The lesson's PowerPoint walkthrough is the best available example of a long SKILL.md that is still well-built. It carries an overview, read/edit paths, design principles, typography and colour-palette selection for when the user does not specify, and pointers to scripts for the mechanical work. It is long because presentations genuinely have that much convention — and it still defers the heavy mechanics to code.",
   "`skill-creator` matters for a reason beyond convenience: it encodes the best-practice list in a form that can *grade* your work. Running your own skills through it is the cheapest quality gate you will find, and in the course both custom skills score well (practice-questions 9/10, weaker on conciseness; time-series scoring higher, with praise for frontmatter quality and avoiding duplication).",
   "Current versions of skill-creator go further than the course shows, and this is the single biggest gap worth patching in your own practice. It ships a real evaluation harness: save test cases to `evals/evals.json`, dispatch *with-skill* and *baseline* subagents in the same turn, capture token counts and durations, grade against a rubric, and aggregate into `benchmark.json` / `benchmark.md` with means and standard deviations. `run_loop.py` goes one step further and optimises the description itself — 60/40 train/test split, each query run three times for a stable trigger rate, up to five iterations, best description chosen on the held-out set to avoid overfitting.",
   "One piece of hard-won guidance from skill-creator's own text deserves quoting in spirit: descriptions should be a little **pushy**, because models systematically *under*-trigger skills. Adding explicit 'make sure to use this skill whenever the user mentions X, Y or Z' language measurably improves firing. And even a perfect description will not fire on a trivial one-step request — the model just does it directly.",
   "The lesson's MCP integration is the other thing to take away. Modifying the marketing skill from 'CSV upload' to 'query BigQuery' is a skill edit, not a rewrite: the analysis, benchmarks and output format are unchanged; only the input section changes, and it now names the MCP server and the specific tool. skill-creator applied a best practice unprompted here — refusing ambiguous or unbounded date ranges and asking the user to clarify.",
 ],
 "spec_box": [
   ("Repo", "github.com/anthropics/skills"),
   ("Document skills", "docx · pdf · pptx · xlsx"),
   ("Built-in where", "Claude.ai + Desktop (not toggleable)"),
   ("Example skills default", "off, except skill-creator"),
   ("Claude Code install", "/plugin marketplace add anthropics/skills"),
   ("Collections", "document-skills · example-skills"),
   ("Recorded in", ".claude/settings.json → enabledPlugins"),
   ("After install", "restart Claude Code, then /skills"),
 ],
 "artifacts": [
   {"title": "Installing vendor skills into Claude Code", "lang": "bash", "code": """# inside Claude Code
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills

# then quit and relaunch Claude Code
/skills          # lists available skills + their token cost""",
    "caption": "Marketplace install writes to .claude/settings.json. The restart is not optional — new skills are discovered at startup."},
   {"title": "skill-creator's evaluation loop", "lang": "bash", "code": """# package a finished skill
python -m scripts.package_skill ./my-skill

# quantitative benchmark of one iteration
python -m scripts.aggregate_benchmark workspace/iteration-1 --skill-name my-skill
# -> benchmark.json / benchmark.md: pass_rate, duration, tokens (mean +/- sd)

# optimise the description against a held-out set
python -m scripts.run_loop --eval-set evals/evals.json \\
  --skill-path ./my-skill --max-iterations 5 --verbose

# human review UI over the results
python eval-viewer/generate_review.py            # or --static <path> for headless""",
    "caption": "The part of skill-creator the course does not reach. This is the answer to 'how do I know my skill is good?'"},
 ],
 "gotchas": [
   "Document skills are famously hard to discover — there is an open issue where Claude itself sometimes claims the PDF skill does not exist. Knowing they are built-in in Claude.ai and absent in Claude Code prevents a lot of confusion.",
   "Document skills are source-available, not open source; example skills are mostly Apache-2.0. Check `THIRD_PARTY_NOTICES.md` before redistributing.",
   "skill-creator is efficient but not clairvoyant. Everything the course says about giving it proper context — the schema, the constraints, which sections not to touch — is load-bearing.",
 ],
 "visual": "marketplace-flow",
},

{
 "id": "m6", "num": "06", "title": "Authoring Practice: Descriptions, Degrees of Freedom, Structure",
 "lesson": "Creating Custom Skills", "duration_min": 18,
 "objective": "Author a skill that triggers reliably, stays under the size budget, and gives the agent exactly as much latitude as the task deserves.",
 "key_points": [
   "Name: lowercase, numbers and hyphens only; gerund (`verb+ing`) form reads best and sorts sensibly; ≤ 64 chars.",
   "Description: state **what it does and when to use it**, in the third person, with the trigger keywords a user would actually type.",
   "Be slightly **pushy** in the description — models under-trigger skills far more often than they over-trigger them.",
   "Body: step-by-step instructions, named edge cases, and — where a step may be skipped — an explicit reason why.",
   "Keep the body under ~500 lines. Anything longer goes to `references/`, and instruct the agent to read the *whole* file when it is long.",
   "**Degrees of freedom** is a design dial: low freedom for compliance and house style (exact sequence), high freedom for creative output (multiple colours, styles, fonts).",
   "Decompose. Several small, well-named, sequential skills beat one omnibus skill that tries to do everything.",
   "Use forward slashes in every path, even on Windows — portability across harnesses depends on it.",
 ],
 "deep_dive": [
   "The two worked examples are chosen to sit at opposite ends of the freedom dial, and that is the lesson. **generating-practice-questions** prescribes a fixed question progression — true/false, then explanatory, then coding, then realistic application — with sub-guidelines per type, and pushes every output format into `assets/` templates (one for markdown, one for LaTeX) so only the requested format is ever loaded. **analyzing-time-series** goes further towards determinism: the statistical work lives in `scripts/diagnose.py` and `scripts/visualize.py`, and the SKILL.md exists mainly to fix the order — run diagnostics, optionally generate plots, read `summary.txt`, report findings, consult `references/interpretation.md` for guidance on what the numbers mean.",
   "That second pattern — *scripts for determinism, SKILL.md for sequence, references for interpretation* — is the most reusable architecture in the course, and it is exactly what you want for any analytical workflow where the same input must produce the same numbers every time.",
   "Output formats belong in `assets/`, not in the body. Writing out a full LaTeX skeleton inside SKILL.md costs those tokens on every invocation, including the ones that wanted markdown. Two template files cost you only the one you use. The same logic applies to schemas, letterheads and deck templates.",
   "Dependencies need declaring. If your scripts import statsmodels and matplotlib, say so in the skill and make sure they are installed — in a sandboxed container with no internet, an undeclared dependency is a hard failure with a confusing traceback.",
   "On evaluation, the course proposes something more disciplined than eyeballing: treat a skill like software and write a test harness around it. For the practice-questions skill that means enumerating queries (generate to markdown / to LaTeX / to PDF), the input files each query uses, and the expected behaviours — correct library for PDF input, learning objectives extracted, each question type generated to its guideline, the right output template used, LaTeX actually compiling, files written to the right paths. For the time-series skill, the Python scripts are assumed unit-tested in the ordinary way, so the skill-level test asserts the *workflow*: correct scripts invoked, correct order, optional plot step honoured when requested, summary interpreted, output tree exactly as specified. Both harnesses end the same way — gather human feedback, and test across every model you intend to run on.",
   "One practical note on running these evaluations: in the course they are run by dispatching two subagents in parallel from Claude Code, one per skill, each grading against skill-creator's best-practice list. That is a cheap pattern to copy for any skill review, and it keeps the grading out of your main context window.",
 ],
 "spec_box": [
   ("Name form", "gerund, lowercase-hyphenated"),
   ("Description content", "what + when + trigger keywords"),
   ("Body ceiling", "~500 lines"),
   ("Long reference files", "instruct: read the entire file"),
   ("Freedom dial", "low = compliance · high = creative"),
   ("Paths", "always forward slashes"),
   ("Declare", "script dependencies, explicitly"),
 ],
 "artifacts": [
   {"title": "A deterministic workflow section (time-series skill)", "lang": "markdown", "code": """## Workflow

1. Run diagnostics. This step is mandatory and always first:
   `python scripts/diagnose.py <input.csv> --output-dir results/`
2. If the user asked for plots, run:
   `python scripts/visualize.py <input.csv> --output-dir results/plots/`
   Skip this step ONLY if the user explicitly declined plots.
3. Read `results/summary.txt` and report the findings to the user.
4. For interpreting stationarity, seasonality or autocorrelation results,
   read `references/interpretation.md` in full before answering.

## Output tree
results/
├── diagnostics.json
├── summary.txt
└── plots/*.png""",
    "caption": "Low degrees of freedom: fixed order, an explicit reason a step may be skipped, and a named output tree so the result is inspectable."},
   {"title": "A skill-level test harness (concept)", "lang": "yaml", "code": """queries:
  - "Generate practice questions from notes04.tex and save as markdown"
  - "Generate practice questions from lecture.pdf and save as LaTeX"
files: [notes04.tex, lecture.pdf]
expected_behavior:
  - uses the correct library for PDF input
  - extracts stated learning objectives
  - generates all four question types in the prescribed order
  - follows the per-type guidelines
  - uses the template from assets/ matching the requested format
  - LaTeX output compiles without errors
  - writes output to the specified path and filename
review:
  - human feedback captured
  - repeated across every model we deploy on""",
    "caption": "Skills are non-deterministic software. The harness asserts behaviour and workflow order, not exact strings."},
 ],
 "gotchas": [
   "Vague descriptions are the number-one cause of skills that never fire. 'Helps with data' routes nothing.",
   "A skill will not trigger on a trivial one-step request no matter how well the description matches — the model simply answers directly.",
   "Name collisions and near-identical descriptions across a large library actively degrade routing. Distinct scopes, distinct trigger words.",
   "Do not encode secrets, credentials or customer data in a skill. Skills get zipped, shared and installed by other people.",
 ],
 "visual": "freedom-dial",
},
]
