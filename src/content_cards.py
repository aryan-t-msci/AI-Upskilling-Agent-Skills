"""Memory flashcards + glossary. front/back kept short enough to actually rehearse."""

FLASHCARDS = [
# --- foundations
("m0", "What is a skill, in one sentence?", "A folder of instructions — `SKILL.md` plus optional scripts, reference docs and assets — that gives an agent procedural knowledge on demand.", "core"),
("m0", "Minimum contents of a valid skill", "One file: `SKILL.md`, with `name` and `description` in YAML frontmatter, plus a markdown body.", "core"),
("m0", "Two tools an agent must have for skills to work", "Filesystem access (read/write files) and a bash-style execution tool.", "core"),
("m0", "The behavioural trigger for writing a skill", "You are retyping the same prompt across conversations — the prompt has become a workflow.", "core"),
("m0", "Four harnesses the course covers", "Claude.ai/Desktop, the Messages API, Claude Code, the Claude Agent SDK.", "core"),

# --- why skills
("m1", "Four costs of the prompt-based workflow that a skill removes", "Repetition, reliance on tacit knowledge, context pollution, and no way to share or version it.", "why"),
("m1", "Which part of the marketing workflow became a reference file, and why", "Budget reallocation rules — conditional (rarely asked) and bulky (thresholds and a framework). Conditional + bulky = `references/`.", "why"),
("m1", "Skill folder naming rules", "Lowercase letters, numbers and hyphens; gerund (`verb+ing`) form reads best; no reserved vendor words such as 'claude' or 'anthropic'.", "why"),
("m1", "How a skill is installed in Claude.ai", "Zip the skill folder, then Settings → Capabilities → Skills → Add, and upload the zip.", "why"),
("m1", "What made the Excel report possible without writing spreadsheet code", "Claude's built-in Excel document skill — a custom skill produced the analysis, a built-in skill produced the file.", "why"),
("m1", "Does a skill uploaded to Claude.ai work in the API?", "No. Claude.ai/Desktop skills are a separate store from the API and Claude Code; install the folder separately in each.", "why"),

# --- anatomy / spec
("m2", "Character limit on `name`", "64 characters. Lowercase alphanumeric plus hyphens; no leading, trailing or consecutive hyphens; must match the parent folder name.", "spec"),
("m2", "Character limit on `description`", "1,024 characters, and it must be non-empty.", "spec"),
("m2", "The two required frontmatter fields", "`name` and `description`. Everything else is optional.", "spec"),
("m2", "Optional spec frontmatter fields", "`license`, `compatibility` (≤500 chars), `metadata` (string→string map), and the experimental `allowed-tools`.", "spec"),
("m2", "What happens to unknown frontmatter fields?", "They are ignored, for forward compatibility. But invalid YAML, wrong casing or duplicate recognised keys stop the skill loading.", "spec"),
("m2", "The three conventional subdirectories and what each is for", "`scripts/` code to execute · `references/` docs to read on demand · `assets/` templates, logos, schemas used in output.", "spec"),
("m2", "Recommended size ceiling for the SKILL.md body", "About 500 lines, or under ~5,000 tokens. Push the rest into reference files.", "spec"),
("m2", "Three distinct things skills provide", "Domain expertise (our way), repeatable workflow (this order every time), and new capability (usually via bundled scripts).", "spec"),
("m2", "When was Agent Skills published as an open standard?", "December 2025, at agentskills.io, aligned with an industry foundation; long-term stewardship is still undecided.", "spec"),
("m2", "Why are XML-like tags banned from name/description?", "That text is injected into a prompt, so angle-bracket tags are a prompt-injection vector.", "spec"),

# --- progressive disclosure
("m3", "The three loading tiers", "1: metadata (name + description, always loaded). 2: the SKILL.md body, on match. 3: reference files, assets and scripts, only if the body directs it.", "pd"),
("m3", "Standing token cost of an installed skill", "About 100 tokens of metadata, per installed skill, whether or not it ever fires.", "pd"),
("m3", "Why are scripts the cheapest tier?", "The source code never enters context — only the script's output does.", "pd"),
("m3", "Reported token saving from progressive disclosure", "Roughly 70–90% versus loading the same material as static context.", "pd"),
("m3", "Why must the description be self-sufficient?", "Routing happens on metadata alone. Anything essential that lives only in the body is invisible at decision time.", "pd"),
("m3", "One place progressive disclosure does NOT apply", "A skill attached to a Claude Code subagent: the full SKILL.md is injected when the subagent is dispatched.", "pd"),
("m3", "What does 'context window as a public good' mean in practice?", "Every added token raises cost, fills the window faster and increases the risk of degraded, wrong answers — so loading is a design decision.", "pd"),

# --- ecosystem placement
("m4", "Tool vs skill, in one line", "A tool is a capability; a skill is the knowledge of which capabilities to use, in what order, to what standard.", "eco"),
("m4", "The carpentry analogy", "Tools are the hammer, saw and nails. The skill is how to build the bookshelf.", "eco"),
("m4", "Key context difference between tools and skills", "Tool definitions live in the context window permanently; skills are loaded progressively.", "eco"),
("m4", "What MCP provides that a skill does not", "Connectivity to external systems and data — databases, Drive, BigQuery, Notion. It brings tools, not method.", "eco"),
("m4", "What a subagent buys you", "An isolated context window, fine-grained tool permissions, and parallel execution.", "eco"),
("m4", "Skill or subagent? The decision rule", "Skills for procedural, predictable workflows. Subagents for full agentic logic, only when a task needs its own context.", "eco"),
("m4", "If many agents need the same expertise, what do you build?", "A skill. Not a subagent — subagents isolate, skills distribute.", "eco"),
("m4", "Two structural limits on Claude Code subagents", "They do not inherit the parent's skills, and they cannot spawn further subagents.", "eco"),

# --- prebuilt & skill-creator
("m5", "The four document skills", "docx, pdf, pptx, xlsx.", "prebuilt"),
("m5", "Where are document skills always on?", "Claude.ai and Claude Desktop — built in and not toggleable. Claude Code ships with none of them.", "prebuilt"),
("m5", "Which example skill is on by default in Claude?", "skill-creator. The other example skills are off by default.", "prebuilt"),
("m5", "How do you get vendor skills into Claude Code?", "`/plugin marketplace add anthropics/skills`, install the `document-skills` / `example-skills` collections, then restart Claude Code.", "prebuilt"),
("m5", "Where does Claude Code record installed skill plugins?", "`.claude/settings.json`, under `enabledPlugins`.", "prebuilt"),
("m5", "How do document skills manipulate Office files?", "Office files are ZIP+XML: unpack, edit the XML or run helper scripts, repack. Some paths shell out to headless LibreOffice.", "prebuilt"),
("m5", "What does skill-creator do beyond scaffolding?", "Packages, validates, benchmarks against a baseline, and optimises the description on a held-out split.", "prebuilt"),
("m5", "Why should descriptions be slightly 'pushy'?", "Models systematically under-trigger skills, so explicit 'use this whenever the user mentions X' language measurably improves firing.", "prebuilt"),
("m5", "Will a perfect description always fire?", "No. On a trivial one-step request the model just answers directly and skips the skill.", "prebuilt"),

# --- authoring
("m6", "What must a description contain?", "What the skill does and when to use it, in the third person, with the trigger keywords a user would actually type.", "authoring"),
("m6", "Degrees of freedom — how do you set the dial?", "Low freedom (exact sequence) for compliance and house style; high freedom for creative output such as colour, style and layout choices.", "authoring"),
("m6", "Where do output format templates belong?", "`assets/` — one file per format, so only the requested format is ever loaded.", "authoring"),
("m6", "The reusable architecture from the time-series skill", "Scripts for determinism, SKILL.md for sequence, references for interpretation.", "authoring"),
("m6", "Why forward slashes, always?", "Portability. Backslashes work on Windows and fail in every container and most other hosts.", "authoring"),
("m6", "One omnibus skill or several small ones?", "Several small, well-named, sequential skills. Systems handle 100+ skills; they do not handle one skill that tries to do everything.", "authoring"),
("m6", "What should a skill say about a step that may be skipped?", "Explicitly why it may be skipped. Unexplained optional steps get skipped for the wrong reasons.", "authoring"),
("m6", "Long reference file — what do you tell the agent?", "To read the entire file, not skim it.", "authoring"),

# --- API
("m7", "Why does the API require the code execution tool for skills?", "It supplies the sandboxed container, shell and filesystem that skills need in order to exist and run at all.", "api"),
("m7", "How are skills requested on the Messages API?", "`container={\"skills\": [{type, skill_id, version}, ...]}` with type `anthropic` or `custom`.", "api"),
("m7", "Where do uploaded custom skills mount in the container?", "`/skills/<skill-name>/`.", "api"),
("m7", "`latest` or a pinned version in production?", "Pinned. `latest` moves silently and changes behaviour without a deployment.", "api"),
("m7", "Three beta headers used in the lesson", "`skills-2025-10-02`, `code-execution-2025-08-25`, `files-api-2025-04-14` — and the Skills header is now optional post-GA.", "api"),
("m7", "The API sandbox constraint that breaks scripts most often", "No internet connection — so no runtime `pip install`; every dependency must be pre-installed.", "api"),
("m7", "Max skills per container", "8.", "api"),
("m7", "How do you delete a skill?", "Delete every version first, then delete the skill itself.", "api"),

# --- Claude Code
("m8", "Project vs personal skill locations", "Project: `.claude/skills/<name>/SKILL.md`. Personal: `~/.claude/skills/<name>/SKILL.md`.", "cc"),
("m8", "What does `/skills` show?", "The available skills and the token cost of their metadata.", "cc"),
("m8", "Created a new skill and it is not listed — why?", "Skills are discovered at startup. Quit and relaunch Claude Code.", "cc"),
("m8", "CLAUDE.md vs SKILL.md", "CLAUDE.md is always in context and describes the whole project; a skill loads on demand for one class of task.", "cc"),
("m8", "Why give a subagent a restricted tool list?", "It is the only real control on what the step can do — prose in a SKILL.md is advisory, tool allow-lists are enforcement.", "cc"),
("m8", "Why include positive AND negative examples in a coding skill?", "Libraries offer several valid forms; showing the rejected form removes the ambiguity the preferred form alone leaves open.", "cc"),
("m8", "What does a reviewer skill effectively act as?", "A unit test in prose for your other skills — a checklist, examples of mistakes with fixes, and a fixed output format.", "cc"),

# --- Agent SDK
("m9", "Two config requirements for skills in the Agent SDK", "`\"Skill\"` in `allowed_tools`, and `setting_sources` including `\"user\"` and/or `\"project\"`. Either alone loads nothing.", "sdk"),
("m9", "What is needed to dispatch a subagent in the SDK?", "`\"Task\"` in `allowed_tools`.", "sdk"),
("m9", "Which tools are allowed by default in the SDK?", "Read-only ones: Read, Grep, Glob. Write, Bash, WebSearch and WebFetch must be granted explicitly.", "sdk"),
("m9", "A subagent has a tool in its list but cannot use it — why?", "The parent's `allowed_tools` must also include it.", "sdk"),
("m9", "How are MCP tools allowed in the SDK?", "By pattern: `mcp__<server>__*`, or by naming individual tools.", "sdk"),
("m9", "What is an 'orchestration skill'?", "A skill attached to no subagent whose job is to tell the main agent which subagents to dispatch, what each should look for, and how to fold results into a fixed output.", "sdk"),
("m9", "Why were the research subagents on a cheaper model?", "Retrieval and extraction are bounded tasks with clear success criteria; synthesis needs the stronger model. The split roughly halved run cost.", "sdk"),
("m9", "What does Claude Code give you that a bespoke SDK agent does not?", "Interactive tool-approval prompts and interrupts. In the SDK you rebuild them with permission callbacks and hooks.", "sdk"),

# --- eval
("m10", "Three separate failure modes to test", "It did not fire; it fired and did the wrong thing; it fired, worked, and cost more than it was worth.", "eval"),
("m10", "Why run each eval query several times?", "Triggering is stochastic — one run tells you nothing about trigger reliability. Three repeats is the usual minimum.", "eval"),
("m10", "Why include should-not-fire queries?", "A skill that fires on everything is as broken as one that never fires; it hijacks unrelated requests.", "eval"),
("m10", "Why is a baseline run essential?", "Without it you are measuring the model's competence, not the skill's contribution. The value is the delta.", "eval"),
("m10", "Why split train/test when tuning a description?", "Otherwise you overfit your own eval set. The standard loop uses a 60/40 split and selects on the held-out portion.", "eval"),
("m10", "What property should a team regression-test most?", "Consistency — same structure, same file tree, same section order across runs. That is what a skill bought you over a prompt.", "eval"),

# --- security
("m11", "Why is a skill a sharper security surface than a prompt?", "It is executable content whose scripts and reference files may never be read by the person who approved it.", "sec"),
("m11", "The highest-risk skill pattern", "A skill that fetches an external URL and then acts on what it finds — a mutable, unversioned dependency inside a trusted path.", "sec"),
("m11", "What must an audit cover besides SKILL.md?", "Every script, every reference file and every asset. SKILL.md is the least dangerous file in the folder.", "sec"),
("m11", "Can a SKILL.md restrict what an agent may do?", "No. The body is advisory text. Authority comes from tool allow-lists, permission hooks and sandbox configuration.", "sec"),
("m11", "Four organisational controls for skills at scale", "A reviewed internal registry, skills in version control with code review, version pinning in production, and a named owner per skill.", "sec"),
("m11", "What must never go in a skill?", "Credentials, tokens, endpoints or customer data — skills get zipped, shared and installed elsewhere.", "sec"),

# --- portability
("m12", "How many products support the standard?", "Roughly 40 on the official showcase, including Claude Code, Codex, Copilot, VS Code, Cursor, Gemini CLI, Amp, OpenCode and Goose.", "port"),
("m12", "Maximum-portability skill definition", "`name` + `description` only, a plain markdown body, and relative paths with forward slashes.", "port"),
("m12", "Is `allowed-tools` dependable?", "No — it is experimental, honoured in some hosts and silently ignored in others. Never rely on it as a control.", "port"),
("m12", "Two parts of the course most likely to be dated", "The API beta headers and code-execution tool version, and the subagent `skills:` injection behaviour.", "port"),
("m12", "Where do Codex skills live?", "`~/.codex/skills/`. Storage location differs per host.", "port"),

# --- applied
("m13", "Best-fit data-operations workload for a skill", "An ordered multi-check verification pipeline with a fixed output contract and a reasoning step in the middle.", "applied"),
("m13", "How do you split a verification pipeline across tiers?", "Deterministic checks → `scripts/`; methodology and decision rules → `references/`; column contracts and templates → `assets/`.", "applied"),
("m13", "Why give a reviewer subagent read-only tools?", "A reviewer that can edit will quietly fix problems instead of reporting them, and your true error rate becomes invisible.", "applied"),
("m13", "The threshold for turning a workflow into a skill", "Repetition plus a settled convention. Complexity alone is not enough.", "applied"),
("m13", "Why name the output tree in the skill?", "Reproducible paths are what make a run auditable months later.", "applied"),
]

GLOSSARY = [
("Agent Skills", "Open standard, published December 2025, defining a skill as a folder containing SKILL.md plus optional scripts, references and assets."),
("SKILL.md", "The single required file in a skill: YAML frontmatter with name and description, followed by a markdown body of instructions."),
("Frontmatter", "The YAML block at the top of SKILL.md. `name` and `description` required; `license`, `compatibility`, `metadata` and `allowed-tools` optional."),
("Progressive disclosure", "Three-tier loading: metadata always, body on match, bundled resources only when directed. The mechanism that lets a system carry 100+ skills."),
("Metadata tier", "Name + description for every installed skill, ~100 tokens each, permanently in context. The only unavoidable cost of a skill."),
("references/", "Directory for documents the agent reads on demand. Cost is paid at read time, so it suits conditional and bulky material."),
("scripts/", "Directory for executable code. Cheapest tier: the source is never tokenised, only the output enters context."),
("assets/", "Directory for templates, logos, schemas and data files used in output rather than read as instructions."),
("Degrees of freedom", "Design dial for how much latitude a skill grants: low for compliance and exact sequence, high for creative variation."),
("skill-creator", "Anthropic's meta-skill: scaffolds, packages, validates, benchmarks against a baseline and optimises skill descriptions."),
("Document skills", "The built-in docx, pdf, pptx and xlsx skills. Always on in Claude.ai/Desktop; must be installed in Claude Code."),
("Plugin marketplace", "Claude Code mechanism for installing skill collections, e.g. `/plugin marketplace add anthropics/skills`. Records to .claude/settings.json."),
("Code execution tool", "API tool that supplies a sandboxed container, shell and filesystem. Required for skills on the Messages API."),
("Files API", "API for uploading inputs and downloading generated artefacts by file_id. Files do not expire until deleted."),
("container.skills", "Messages API parameter mounting skills into the execution container, each entry a type, skill_id and version."),
("MCP", "Model Context Protocol — connects agents to external systems and data. Supplies tools; skills supply the method for using them."),
("Subagent", "A child agent with its own context window and restricted tool set. Does not inherit parent skills; cannot spawn further subagents."),
("Task tool", "The tool that dispatches subagents. Must be in allowed_tools or no delegation is possible."),
("setting_sources", "Agent SDK option declaring where to load settings and skills from — 'user', 'project', or both. Required for skills to load."),
("AgentDefinition", "Agent SDK class describing a subagent: description, prompt, tools and model."),
("CLAUDE.md", "Project-level context file, always loaded. Holds conventions that apply on every turn, as opposed to task-specific skills."),
("Orchestration skill", "A skill attached to no subagent, whose purpose is to direct how the main agent dispatches and synthesises subagent work."),
("Baseline run", "The same eval queries with the skill disabled. A skill's value is the delta over baseline, not its absolute score."),
("Trigger rate", "How often a skill fires on queries that should fire it. Stochastic, so measured over repeated runs."),
]
