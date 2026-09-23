"""Short notes — condensed from the user's own PDF write-up of the course.

Kept close to the source wording and ordering, lightly tidied for reading on
screen. Figures are the images embedded in that PDF, extracted and inlined by
build_app.py, so the app stays a single file.

Block types:
  bullets  {items:[...]}                 top-level bullets
  sub      {title, items:[...]}          a labelled sub-list
  code     {lang, code, caption}         monospace block
  fig      {file, caption}               inlined figure from the PDF
  table    {headers, rows, caption}
  note     {text}                        pulled-out remark
"""

SHORT_NOTES = [
{
 "id": "sn-intro", "title": "Introduction", "num": "01",
 "blurb": "What a skill is, what it contains, and the loading behaviour that makes it cheap.",
 "blocks": [
  {"type": "bullets", "items": [
    "Skills give Claude Code and other agents new abilities to carry out tasks.",
    "Skills are **folders of instructions** that extend an agent's capabilities with specialised knowledge.",
    "Any skill should include a **SKILL.md** markdown file containing the skill's name, description and main instructions. The main instructions can also refer to other files — scripts, additional markdown, and assets such as templates and images.",
    "Skills are **progressively disclosed**: the name and description always live in the context window, but the agent does not load the rest of the instructions until a user request matches the description.",
    "To use a skill, the agent needs a basic set of tools — **filesystem access** to read and write files, and a **bash tool** to execute code.",
    "Skills combine with **MCP and subagents** to create agentic workflows. MCP gets data from external sources; a skill knows what to do with that data, or how to retrieve it efficiently. A task can also be delegated to a subagent with isolated context, which can itself use skills.",
    "**When to use a skill:** a workflow you repeatedly need the agent to implement. Instead of explaining the same workflow every time, package it once so the agent already knows what to do.",
  ]},
  {"type": "code", "lang": "text", "code": """my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories""",
   "caption": "At its core a skill is a folder containing SKILL.md. That file holds metadata — name and description at minimum — and the instructions telling an agent how to perform a task."},
  {"type": "sub", "title": "Why Agent Skills", "items": [
    "Agents are increasingly capable but often lack the context to do real work reliably. Skills package procedural knowledge and company-, team- and user-specific context into portable, version-controlled folders that agents load on demand.",
    "**Domain expertise** — capture specialised knowledge, from legal review processes to data analysis pipelines to presentation formatting, as reusable instructions and resources.",
    "**Repeatable workflows** — turn multi-step tasks into consistent, auditable procedures.",
    "**Cross-product reuse** — build a skill once and use it across any skills-compatible agent.",
  ]},
  {"type": "fig", "file": "f-001.jpg",
   "caption": "The three stages: discovery loads name and description for every available skill; activation reads the full SKILL.md into context once a task matches; execution follows the loaded instructions and runs bundled code or loads referenced files as needed."},
 ]},

{
 "id": "sn-why", "title": "Why Use Skills", "num": "02",
 "blurb": "Packaging a recurring prompt set, and the structure and naming rules that follow.",
 "blocks": [
  {"type": "bullets", "items": [
    "Skills package a prompt, or a set of prompts, that gets used regularly — so instead of working through the whole set every time and filling session context with things that may not be needed, you reference the skill. Its SKILL.md holds the prompts, rules and references, some of which are read only conditionally. Optimum use of the context window.",
    "In the marketing example, the analysis is carried out through SKILL.md, and **only when the user asks about budget reallocation** is the budget reallocation rules markdown referred to.",
  ]},
  {"type": "fig", "file": "f-002.jpg",
   "caption": "The marketing campaign SKILL.md: efficiency targets, output format with status indicators, and the final section deferring reallocation to references/budget_reallocation_rules.md."},
  {"type": "bullets", "items": [
    "Every skill needs a **name** (to link or refer to the skill) and a **description** (to know when the skill is to be used). Both go at the very start of SKILL.md in YAML format. This becomes the skill metadata, which is always loaded into the context window when a skill is added or loaded from the filesystem.",
    "**Structure:** a folder named after the skill, containing SKILL.md (prompt, tasks, rules) and a references folder for external references. Anything SKILL.md refers to should live in that folder. The zipped folder is uploaded to Claude as a skill for future use.",
    "SKILL.md is loaded only when the skill is triggered, and additional resources — reference markdown, scripts — load only as needed. That is progressive disclosure.",
    "**Naming conventions** for the folder: lowercase letters, dashes between words, and no reserved keywords like Claude or Anthropic.",
    "Because skills are an open standard, the same folder is supported in other coding environments such as Codex and Gemini CLI.",
  ]},
  {"type": "fig", "file": "f-003.jpg",
   "caption": "The finished folder: SKILL.md and budget_reallocation_rules.md inside analyzing-marketing-campaign, with the name and description visible as YAML at the top of the file."},
  {"type": "fig", "file": "f-004.jpg",
   "caption": "Agent Skills as a lightweight open format: a folder of organised files — instructions, scripts, assets, resources — that agents discover on the filesystem to perform a task accurately."},
  {"type": "fig", "file": "f-005.jpg",
   "caption": "The same shape for a non-coding skill: designing-newsletters, with a style guide in references/ and a header image, icons and templates in assets/."},
  {"type": "sub", "title": "Old way vs new way of building agents", "items": [
    "Teams used to build separate, single-purpose agents for coding, research, finance and so on, each with its own hardcoded tools and context. It turns out most agents need the same simple scaffolding underneath — basic tools like bash and a filesystem to find, edit and run things. The domain-specific part was knowledge, not architecture.",
    "**Skills fill the gap that generic agents lack.** A bare-bones agent is easy to build and scale, but it does not know how to do finance analysis \"the right way\" or follow a specific research process. Skills load that expertise — procedural knowledge plus company, team and user context — on demand, giving the agent **repeatable workflows** (clear steps, so output is predictable rather than random each time) and **new capabilities** (things Claude could not do at all before, such as handling a new data format), all without bloating the core setup.",
  ]},
  {"type": "fig", "file": "f-006.jpg",
   "caption": "Use cases by category, and what you are stuck doing without skills: describing instructions and requirements every time, bundling all references and supporting files every time, and trying to ensure workflows or outputs stay consistent."},
  {"type": "note", "text": "Skills are not just standalone add-ons — you can **stack multiple skills together** in one workflow. By referencing which skills apply and the order of steps needed, you turn an otherwise non-deterministic system into one that produces consistent, predictable results for complex, multi-part tasks."},
 ]},

{
 "id": "sn-vs", "title": "Skills vs Tools, MCP and Subagents", "num": "03",
 "blurb": "What each primitive provides, what it costs in context, and how they compose.",
 "blocks": [
  {"type": "fig", "file": "f-007.jpg",
   "caption": "Skills teach the agent what to do with the data; MCP connects the agent to external systems and data."},
  {"type": "sub", "title": "Skills vs MCP", "items": [
    "**MCP (Model Context Protocol) is the connection to outside tools and data.** It lets the agent reach external systems it would not otherwise know about — a database, Google Drive, any other data source — essentially plugging in the raw tools and information.",
    "**Skills are the instructions for what to do with those tools.** MCP brings the ingredients; skills provide the recipe — the repeatable steps that tell the agent how to combine and use external data to reliably produce the output you actually want, whether a calculation, a report or a specific metric.",
    "In short: MCP gets the agent *access* to outside systems; skills tell it *how* to use that access in a consistent, repeatable way.",
  ]},
  {"type": "fig", "file": "f-008.jpg",
   "caption": "Skills extend capability with specialised knowledge and can include scripts as tools used on demand. Tools provide the essential capabilities — and tool definitions (name, description, parameters) always live in the context window."},
  {"type": "sub", "title": "Skills vs Tools", "items": [
    "**Tools are the low-level building blocks; skills are the know-how for using them.** Hammer, saw and nails versus knowing how to build a bookshelf. Tools are the underlying capabilities that let an agent access systems, execute code or read and write files — and in fact tools are what power the ability to generate, read and load skills in the first place.",
    "**Skills sit on top of tools and add specialised knowledge.** A skill can pull in extra files and scripts that need to run, but the actual execution of those scripts and the loading of those files is still handled by tools underneath. Tools themselves come from three places: built into the agentic ecosystem, custom-written, or loaded via MCP.",
    "**The key structural difference is context cost and when each loads.** Tool definitions live in the context window at all times, while skills are progressively loaded only when needed. That is what makes them work well together: a skill can create a predictable workflow and pull in a script \"like a tool\" on demand — so a tool not needed in every conversation can be tucked inside a skill and loaded only when the task calls for it.",
  ]},
  {"type": "sub", "title": "Can skills restrict tool usage?", "items": [
    "Yes. A SKILL.md frontmatter can declare an **allowed-tools** list, scoping what the agent is permitted to use while that skill is active.",
    "This matters for the predictability theme: if a skill is meant to, say, only read and reformat a spreadsheet, restricting it to file read and write tools — and denying network or shell access — makes its behaviour more constrained and auditable.",
    "So skills act as both a **capability unlock** (bringing in scripts and knowledge) and, optionally, a **capability limiter** (restricting which tools apply while following that skill's instructions).",
  ]},
  {"type": "note", "text": "Earlier, tool definitions — a full JSON schema of name, description and the exact parameter structure — had to sit in context for the whole conversation, while a skill was triggered just by matching a task to a plain-language description. So a skill's front-loaded footprint can be tiny, with the heavy content deferred until matched. Some environments have started applying the same progressive-disclosure trick to tools: a tool can be marked **deferred**, where only its name is visible at first and its full schema is pulled in on demand via a search call before it is usable."},
  {"type": "sub", "title": "Subagents", "items": [
    "**A subagent is a child process spawned by a main (orchestrator) agent.** It runs with its own isolated context, gets fine-grained or limited tool permissions, can execute in parallel with other subagents, and reports results back to the parent. Subagents come from ecosystems like Claude Code or the Agent SDK, or can be custom-built.",
    "**Subagents can be scoped to specific skills, just like the main agent.** The main agent orchestrates and can pull in whatever skills it needs, but each subagent can be restricted to only the skills relevant to its job — so permissions and knowledge access are controlled at both levels.",
    "**This combination is what makes subagents genuinely useful.** A code-reviewer subagent whose entire job is analysing a codebase leverages a skill that encodes exactly how your team wants code reviews done. The subagent supplies isolated, parallel execution; the skill supplies the procedural knowledge for that narrow task.",
  ]},
  {"type": "fig", "file": "f-009.jpg",
   "caption": "Customer Insight Analyzer: MCP servers bring in interview notes and survey responses, interview and survey analyzer subagents run the work, and a skill provides the guide for how to categorise feedback and summarise findings."},
  {"type": "fig", "file": "f-010.jpg",
   "caption": "The summary slide comparing all five primitives."},
  {"type": "table", "headers": ["Feature", "Skills", "Prompts", "Subagents", "MCP"],
   "rows": [
     ["What it provides", "Procedural knowledge", "Moment-to-moment instructions", "Task delegation", "Tool connectivity"],
     ["Persistence", "Across conversations", "Single conversation", "Across sessions", "Continuous connection"],
     ["Contains", "Instructions + code + assets", "Natural language", "Full agent logic", "Tool definitions"],
     ["When it loads", "Dynamically, as needed", "Each turn", "When invoked", "Always available"],
     ["Best for", "Specialised expertise", "Quick requests", "Specialised tasks", "Data access"],
   ], "caption": "Same content as the slide above, in text."},
  {"type": "bullets", "items": [
    "Prompts are the atomic unit — how you talk to a model — but they do not scale across teams or companies on their own. Skills solve that by bundling prompts, conversations, code and assets into something reusable. Subagents can then use those skills to carry out delegated tasks, and those subagents in turn draw on tools provided by the main agent.",
    "**The common thread is being deliberate about the context window.** Treat context as a shared, limited resource: subagents keep heavy work in their own isolated context instead of bloating the main one; MCP loads external data and tools only when connected; skills load their content progressively, only when a task matches. Different mechanisms, same goal — do not stuff everything into context all the time.",
    "**Where each one's memory lives.** Subagents can persist state across sessions between themselves and the parent agent; skills persist across conversations with the user or application. Rule of thumb: **use skills for procedural, predictable, repeatable workflows, and reserve subagents for full agentic reasoning**, only when a task genuinely needs specialised, isolated execution.",
  ]},
 ]},

{
 "id": "sn-claude", "title": "Claude Skills", "num": "04",
 "blurb": "The two tiers that ship with Claude, and the skill that builds other skills.",
 "blocks": [
  {"type": "bullets", "items": [
    "Two tiers of pre-built skills. **Document skills** (Excel, Word, PowerPoint, PDF) are built into Claude AI and Desktop, always on, and cannot be toggled off. **Example skills** (such as skill-creator) live in the same GitHub repository but are off by default under Settings → Capabilities — except skill-creator itself, which ships enabled.",
    "**skill-creator** is a skill that helps build other skills for you.",
  ]},
  {"type": "fig", "file": "f-011.jpg",
   "caption": "The skill-creator path: skill idea and examples, then init_skill.py scaffolds SKILL.md and folders, a package script zips it into a bundle, a validate script checks SKILL.md and frontmatter, and the result is a ready-to-use skill installed for future chats."},
 ]},

{
 "id": "sn-custom", "title": "Creating Custom Skills", "num": "05",
 "blurb": "The required and optional frontmatter, the body budget, and the freedom dial.",
 "blocks": [
  {"type": "bullets", "items": [
    "Every skill needs a **SKILL.md** with required YAML frontmatter — `name` and `description`, both character-capped, the name in `verb-ing` lowercase-hyphen form, and the description stating **what** it does and **when** to use it — plus optional fields such as license, compatibility and arbitrary metadata.",
    "Beyond the frontmatter there is no format restriction, but best practice is step-by-step instructions, explicit edge cases, under **500 lines**, and forward slashes even on Windows.",
    "Three optional folders extend it — `scripts/`, `references/`, `assets/` — all loaded only when needed. Progressive disclosure again.",
    "**Freedom vs determinism is the key design decision:** low freedom (exact sequence, no ambiguity) for best-practice-following tasks; high freedom (multiple valid colours, styles, fonts) for creative output.",
  ]},
 ]},

{
 "id": "sn-api", "title": "Skills with the Claude API", "num": "06",
 "blurb": "What Claude AI provides for free, and what you must wire up yourself.",
 "blocks": [
  {"type": "sub", "title": "Two things change versus Claude AI and Desktop", "items": [
    "Skills made in Claude AI or Desktop **do not carry over** to the API or Claude Code — separate environments.",
    "Claude AI and Desktop give you a sandboxed container plus internet access for free (Settings → Capabilities → \"Code execution and file creation\"). On the API you wire that up yourself with the **Code Execution Tool** (bash plus filesystem, sandboxed, no internet, pre-installed libraries only) and the **Files API** (upload inputs, download generated outputs by file_id).",
  ]},
  {"type": "bullets", "items": [
    "Anthropic is provisioning a container behind the scenes for you: a small Linux sandbox with its own filesystem where Claude can run bash commands, write and read files, and — importantly — reach the internet, so it can `pip install` a library it does not already have, or fetch something from the web mid-task. You never touch any of that plumbing; you just get the capability.",
    "**The API is the raw building block, not the finished product.** When building your own application against the Messages API, Anthropic does not assume you want a sandbox running by default — you must explicitly ask for one by adding the code execution tool to your request. Doing so spins up a genuinely isolated container per session: its own filesystem, its own bash shell, its own CPU, memory and disk allotment, walled off from the host machine and from every other customer's container.",
    "Claude still cannot download a new package at runtime there; it is stuck with whatever is pre-installed in the container image (pandas, numpy, scipy, matplotlib, `python-docx`, `python-pptx`, `pypdf` and so on).",
    "**Files still move in and out only via the Files API** — upload a file, reference it with a `container_upload` block, and pull generated output back out by its file ID. That mailbox-in, mailbox-out design has not changed.",
  ]},
  {"type": "fig", "file": "f-012.jpg",
   "caption": "The Agent SDK example: a main agent guided by the learning-a-tool skill dispatches docs_researcher, repo_analyzer and web_researcher in parallel, synthesises a learning guide, and writes it to Notion through MCP."},
  {"type": "bullets", "items": [
    "A main agent orchestrates three subagents — `docs_researcher`, `repo_analyzer`, `web_researcher` — each with its own scoped tools.",
    "A single skill, `learning-a-tool`, guides only the **main agent's** workflow: a research phase per subagent, then organising findings into progressive levels via a separate progressive-learning reference file (overview → install → concepts → patterns → next steps), then a fixed output structure.",
    "Getting this running requires explicitly listing **every tool any subagent needs** under the main agent's `allowed_tools` — subagents inherit nothing by default — plus adding the `Task` tool to dispatch subagents and the `Skill` tool to read skills from `.claude/skills/`.",
  ]},
 ]},

{
 "id": "sn-code", "title": "Skills with Claude Code", "num": "07",
 "blurb": "CLAUDE.md versus a skill, and the one nuance about subagents worth remembering.",
 "blocks": [
  {"type": "bullets", "items": [
    "**CLAUDE.md versus a skill is a real design decision, not just two file types.** CLAUDE.md is always in context, every conversation, so it is for things true of the whole project — tech stack, architecture, where files live. A skill is for a subset of conventions relevant to one recurring task, such as \"how we add a CLI command\", loaded only when that task comes up. The rule of thumb: **if it needs to be everywhere, it goes in CLAUDE.md; if it is only relevant to one repeatable job, make it a skill.**",
    "**Subagents do not inherit skills from their parent.** A skill must be explicitly assigned to each subagent, by name, in its config.",
    "**The single most important nuance:** skills behave differently depending on who is using them. When the *main agent* uses a skill it is read progressively — SKILL.md first, then any referenced files only as needed. When a *subagent* is dispatched with a skill attached, the **entire SKILL.md is preloaded upfront**, with no progressive disclosure of anything beyond that file. That is a meaningfully different cost and behaviour profile, worth remembering when deciding what to put directly in a subagent's SKILL.md versus what to push into a referenced file.",
  ]},
 ]},
]
