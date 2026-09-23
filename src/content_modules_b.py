"""Agent Skills course content - modules B (7-13)."""

MODULES_B = [
{
 "id": "m7", "num": "07", "title": "Skills with the Claude Messages API",
 "lesson": "Skills with the Claude API", "duration_min": 20,
 "objective": "Run a custom skill programmatically: upload it, mount it in a container, feed it a file, and download what it produced.",
 "key_points": [
   "Two facts to internalise first: skills created in Claude.ai/Desktop are **not** visible to the API or Claude Code, and the API gives you **no filesystem** until you ask for one.",
   "Skills on the API therefore require the **code execution tool** — it supplies the sandboxed container, the bash shell and the filesystem that skills need to exist at all.",
   "Request a skill by passing `container={\"skills\": [...]}`, each entry `{type, skill_id, version}` with `type` either `anthropic` (built-in) or `custom`.",
   "Version can be `\"latest\"` or a pinned timestamp. **Pin in production**; `latest` silently moves under you.",
   "Uploaded custom skills mount inside the container at `/skills/<skill-name>/`.",
   "The **Files API** moves data in and out: upload input files, reference them in the message, and download generated artefacts by `file_id`.",
   "Betas historically required: `skills-2025-10-02`, `code-execution-2025-08-25`, `files-api-2025-04-14`. The Skills API has since gone GA — its header is now optional, and newer code-execution tool versions exist.",
   "Deleting a skill is two-step: delete every **version** first, then the skill.",
 ],
 "deep_dive": [
   "The clearest way to understand this lesson is as an inventory of what Claude.ai was quietly providing. In Claude.ai, Settings → Capabilities → 'code execution and file creation' is on by default; switch it off and skills stop working entirely. That single toggle is a container, a filesystem, a shell and internet-enabled package installs. On the Messages API you must request the container explicitly, and you get a stricter one.",
   "Sandbox constraints are worth memorising because they shape what a skill can legally do: Python 3.11 on Linux x86-64, roughly 5 GiB RAM, 5 GiB of workspace disk and one CPU, file access confined to the workspace, and — the one that bites — **no internet connection**. There is no `pip install` at runtime; if your script imports something that is not pre-installed, it fails. This restriction is specific to the API container; Claude.ai and Desktop do have network access and can install packages.",
   "The end-to-end shape of a request is worth holding as a five-part checklist: (1) the model, (2) the beta headers, (3) `container.skills` naming which skills to mount, (4) `tools` including the code execution tool, (5) messages that reference uploaded files by `file_id`. Miss the code execution tool and the request fails outright with a 400 telling you skills need it.",
   "Reading the response is the other half of the skill. A single call comes back as a sequence of blocks — text, `server_tool_use`, `code_execution_tool_result`, `bash_code_execution_result` — and the useful move is to format them so you can watch the trace. In the course's practice-questions run you can literally see progressive disclosure happen: SKILL.md is read, the input `.tex` is read, then and only then the markdown template in `assets/` is read because markdown was requested. The LaTeX template beside it is never opened.",
   "The second run composes a custom skill with a built-in one. `analyzing-time-series` runs `diagnose.py` and `visualize.py` inside the container, writes `summary.txt` and plots, and then the built-in **docx** skill turns the findings into a Word report with the plots embedded. Two SKILL.md files are read in full; only the parts of the docx skill needed for markdown-to-Word conversion are pulled in beyond that. One request, two skills, three generated files, one downloadable artefact.",
   "The deletion dance — list versions, delete each, then delete the skill — exists because pinned versions are first-class objects. It is annoying interactively and correct architecturally: a production request pinned to a timestamp should not break because someone tidied up.",
 ],
 "spec_box": [
   ("Hard requirement", "code execution tool"),
   ("Skills per container", "up to 8"),
   ("Mount path", "/skills/<skill-name>/"),
   ("Sandbox", "Python 3.11 · ~5 GiB RAM · ~5 GiB disk · 1 CPU"),
   ("Network in API container", "none — no runtime pip install"),
   ("Files API max size", "500 MB per file"),
   ("Skill size", "~10 MB including bundled resources"),
   ("Delete order", "all versions → then skill"),
 ],
 "artifacts": [
   {"title": "A complete skills request", "lang": "python", "code": """from anthropic import Anthropic
from anthropic.lib import files_from_dir

client = Anthropic()

# 1. upload the custom skill folder
skill = client.beta.skills.create(
    files=files_from_dir("skills/analyzing-time-series"),
    betas=["skills-2025-10-02"],
)

# 2. upload the input file
f = client.beta.files.upload(
    file=open("data/retail_sales.csv", "rb"),
    betas=["files-api-2025-04-14"],
)

# 3. one request: custom skill + built-in docx skill
resp = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["skills-2025-10-02",
           "code-execution-2025-08-25",
           "files-api-2025-04-14"],
    container={"skills": [
        {"type": "custom",    "skill_id": skill.id, "version": "latest"},
        {"type": "anthropic", "skill_id": "docx",   "version": "latest"},
    ]},
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": [
        {"type": "container_upload", "file_id": f.id},
        {"type": "text", "text":
         "Analyze this time series and produce a Word report with the plots."},
    ]}],
)""",
    "caption": "Five moving parts: model, betas, container.skills, the code execution tool, and a container_upload block pointing at the Files API id."},
   {"title": "Listing and deleting", "lang": "python", "code": """# only my own skills, not the built-ins
for s in client.beta.skills.list(source="custom", betas=["skills-2025-10-02"]):
    print(s.id, s.display_title)

# deletion is two-step
for v in client.beta.skills.versions.list(skill_id=skill.id):
    client.beta.skills.versions.delete(skill_id=skill.id, version=v.version)
client.beta.skills.delete(skill_id=skill.id)""",
    "caption": "`source=\"custom\"` keeps the built-in catalogue out of your listing. Versions must go before the skill."},
 ],
 "gotchas": [
   "Version drift: the course was recorded while Skills was in beta. The Skills API is now GA (header optional), and code execution has newer tool strings than `code_execution_20250825`. Keep the exact strings for reproducibility but treat them as dated.",
   "No internet in the API container means every script dependency must be pre-installed. Test your scripts inside the container, not on your laptop.",
   "Uploaded files never expire — they count against your organisation's storage until explicitly deleted.",
   "A skill without the code execution tool is a 400 error, not a degraded response.",
 ],
 "visual": "api-architecture",
},

{
 "id": "m8", "num": "08", "title": "Skills in Claude Code, and Wiring Them to Subagents",
 "lesson": "Skills with Claude Code", "duration_min": 20,
 "objective": "Place skills correctly in a repository, distinguish CLAUDE.md from a skill, and split a development loop across subagents that each carry their own skill.",
 "key_points": [
   "Project skills live in `.claude/skills/<skill-name>/SKILL.md`; personal skills in `~/.claude/skills/`.",
   "`/skills` lists what is available **and how many tokens the metadata costs** — a rare, useful piece of instrumentation.",
   "New or renamed skills are discovered at startup: **quit and relaunch Claude Code** or they will not appear.",
   "`CLAUDE.md` is always in context and describes the whole project (stack, architecture, conventions). A skill is loaded on demand for one job. Conventions that apply everywhere go in CLAUDE.md; conventions that apply only when adding a command go in a skill.",
   "The demo splits the job three ways: `adding-cli-command` (how we write commands), `generating-cli-tests` (how we test them), `reviewing-cli-command` (how we verify the first two).",
   "Coding skills work best when they prescribe *patterns*, not intentions: which decorator, which type-annotation style, which display helper, which exit codes, which help text.",
   "Subagents are single markdown files in `.claude/agents/` with frontmatter `name, description, tools, model, color` and optional `skills`.",
   "**Subagents do not inherit the parent's skills** — attach them explicitly. And a skill attached to a subagent is injected **in full at dispatch**, with no further progressive disclosure.",
   "Restrict subagent tools deliberately: the reviewer got `Bash, Glob, Grep, Read`; the test runner additionally needed `Edit` and `Write`.",
 ],
 "deep_dive": [
   "The reviewing skill is the most interesting of the three because it is not a producer — it is an evaluator. It carries a checklist (right location, right decorator, registered correctly, type annotations present, flags and options in the required form, error handling, exit codes, destructive-command confirmation), positive and negative examples, a catalogue of mistakes with their fixes, and a fixed output format ending in a summary and suggested fixes. Effectively it is a unit test for the other two skills, written in prose, and running it as part of the workflow is what makes the loop self-correcting.",
   "Positive **and** negative examples matter more in coding skills than anywhere else. Libraries usually offer several valid ways to do the same thing — several ways to annotate a decorated argument in Typer, several ways to structure a pytest fixture. A skill that only shows the preferred form still leaves the model free to pattern-match on the codebase; a skill that also shows the rejected form removes the ambiguity.",
   "The subagent argument in this lesson is fundamentally about context, not capability. Testing a CLI interactively means running add, list, edit, invalid-input and not-found cases over and over, and every one of those transcripts lands in the main window. Pushing generation-and-running into a subagent keeps the parent's context clean and returns only the verdict. The parent stays on development; the children absorb the noise.",
   "The final demo is the one to remember: a `clear.py` command written by someone who ignored all the conventions. The reviewer subagent finds six critical issues and four warnings — wrong console output method instead of the shared display helper, flags in the wrong format, incorrect exit codes, missing registration in `__init__.py`. The parent agent then fixes them and the test subagent generates and runs tests. That is the shape of a real quality gate: a review skill that knows your conventions, a subagent to run it cheaply, and a parent that only sees the diff and the verdict.",
   "Two practical notes on skill-to-subagent wiring. The documented path is the `skills:` field in the subagent's frontmatter. There is a second documented path where the skill itself specifies how to fork into a subagent. And there is a live caveat worth knowing: multiple reports indicate the `skills:` field does not always inject as documented, while filesystem-capable subagents can often discover `.claude/skills/` on their own. Verify behaviour in your version rather than assuming either way.",
 ],
 "spec_box": [
   ("Project skills", ".claude/skills/<name>/SKILL.md"),
   ("Personal skills", "~/.claude/skills/<name>/SKILL.md"),
   ("Subagents", ".claude/agents/<name>.md"),
   ("Agent frontmatter", "name, description, tools, model, color, skills"),
   ("List command", "/skills (shows token cost)"),
   ("Pick-up", "restart Claude Code"),
   ("Subagent skills", "full SKILL.md injected at dispatch"),
   ("Nesting", "subagents cannot spawn subagents"),
 ],
 "artifacts": [
   {"title": "A subagent that carries a skill", "lang": "markdown", "code": """---
name: code-reviewer
description: Reviews code for quality, security and convention compliance. Use after a feature is implemented, or when the user asks for a code review.
tools: Bash, Glob, Grep, Read
model: inherit
color: purple
skills: reviewing-cli-command
---

You are a code reviewer maintaining high standards.

## When invoked
1. Identify what changed.
2. Apply the review checklist from your skill.
3. Report findings grouped as CRITICAL / WARNING / SUGGESTION.

## Output format
- Issues found, each with file:line and a suggested fix
- A one-paragraph summary and a pass/fail verdict""",
    "caption": "Deliberately generic prompt, specific skill. The agent is reusable across projects; the skill carries the house conventions."},
   {"title": "CLAUDE.md vs SKILL.md - where a rule belongs", "lang": "text", "code": """CLAUDE.md  (always in context)
  - stack: Python, Typer, dataclasses, Rich, JSON persistence, uv
  - architecture: cli.py entry point; one file per command under commands/
  - models.py = dataclasses; storage.py = persistence; display.py = output
  - conventions that apply to EVERY conversation

.claude/skills/adding-cli-command/SKILL.md  (loaded on demand)
  - which Typer annotation style to use for decorated arguments
  - how to register a command in commands/__init__.py
  - short + long flag forms, required help text
  - confirmation prompt before any destructive delete
  - conventions that apply ONLY when adding a command""",
    "caption": "The test: would this rule be useful on a turn that has nothing to do with the task? If no, it is a skill, not CLAUDE.md."},
 ],
 "gotchas": [
   "Forgetting the restart is the single most common 'my skill disappeared' report in Claude Code.",
   "Do not assume a subagent inherited anything. Tools and skills are both explicit.",
   "A subagent with `Write` and `Bash` and no permission gate can change your repository unattended. Grant the minimum set.",
   "In recent Claude Code, custom slash commands and skills have converged — `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` can both surface as `/deploy`.",
 ],
 "visual": "claude-code-layout",
},

{
 "id": "m9", "num": "09", "title": "Skills with the Claude Agent SDK",
 "lesson": "Skills with the Claude Agent SDK", "duration_min": 20,
 "objective": "Build a multi-agent research application where a skill drives the orchestrator, and get the two configuration details right that silently break skills in the SDK.",
 "key_points": [
   "The Agent SDK is Claude Code's harness, programmatically: same loop, your code.",
   "Architecture built in the lesson: an orchestrator plus three subagents — `docs_researcher`, `repo_analyzer`, `web_researcher` — coordinated by a `learning-a-tool` skill.",
   "Skills live where Claude Code puts them: `.claude/skills/<name>/SKILL.md`, relative to the working directory.",
   "**Two things are required and both are easy to miss**: `\"Skill\"` must be in `allowed_tools`, and `setting_sources` must include `\"user\"` and/or `\"project\"`. `allowed_tools=[\"Skill\"]` alone loads nothing.",
   "`\"Task\"` must also be in `allowed_tools` or no subagent can ever be dispatched.",
   "Read-only tools (Read, Grep, Glob) are permitted by default; `Write`, `Bash`, `WebSearch`, `WebFetch` must be granted explicitly.",
   "Subagents are declared as a dict of `AgentDefinition(description, prompt, tools, model)`; a tool a subagent needs must **also** appear in the parent's `allowed_tools`.",
   "MCP servers are wired with `mcp_servers={...}` and their tools allowed as `mcp__<server>__*`.",
   "The orchestrator prompt should say what to do **if a skill is provided and matches** — follow its instructions precisely — and what to do if none does.",
 ],
 "deep_dive": [
   "The choice of subject in the demo is doing real work: MinerU, an open-source PDF-extraction library the model knows little about. That forces genuine research across documentation, the GitHub repository and community content, rather than recall. It is a good template for evaluating any research agent — pick something outside the training data and see whether the architecture, not the memory, carries it.",
   "The `learning-a-tool` skill is a pure orchestration skill, and that is a category worth naming. It is attached to no subagent. Its job is to tell the main agent what each researcher should look for, then how to fold three research streams into one artefact: a fixed directory tree, progressive learning levels (overview and motivation → installation → core concepts → practical patterns → where to go next), a resources file and runnable code examples. The skill defers the level definitions to a reference file, so the body stays a workflow rather than a curriculum.",
   "Plan-first is worth copying. The demo asks for the plan before execution, sees the parallel research phase, the structure and the intended output, approves it, and only then spends tokens on three subagents cloning repositories and searching the web. For any expensive multi-agent run, a plan gate is the cheapest insurance you can buy.",
   "Cost engineering shows up here in a way the earlier lessons do not reach: the subagents are pinned to a cheaper, faster model while the orchestrator stays on a stronger one. Research subagents do retrieval and extraction — bounded tasks with clear success criteria — and do not need the orchestrator's synthesis ability. That split roughly halves the cost of a run.",
   "The last step is the whole-course composition: an MCP server writes the generated `resources.md` into an existing Notion sub-page, converted into native Notion blocks in batches. One application now uses a skill for procedure, subagents for parallel isolated research, and MCP for the destination system. That is the full stack the course set out to teach.",
   "The security coda is not decoration. The demo grants `Write` and `Bash` with no confirmation step, which is fine in a sandbox and wrong in anything shared. The SDK provides the primitives to fix it — a runtime permission callback, permission modes, and hooks — and the honest framing is that Claude Code's interactive approval prompts are a *feature you have to rebuild* when you leave Claude Code.",
 ],
 "spec_box": [
   ("Skills dir", ".claude/skills/ relative to cwd"),
   ("Required tool", '"Skill" in allowed_tools'),
   ("Required config", 'setting_sources=["user","project"]'),
   ("Subagent dispatch", '"Task" in allowed_tools'),
   ("Default-allowed tools", "Read, Grep, Glob"),
   ("Must grant", "Write, Bash, WebSearch, WebFetch"),
   ("MCP tool pattern", "mcp__<server>__*"),
   ("Agent model options", "sonnet · opus · haiku · inherit"),
 ],
 "artifacts": [
   {"title": "The options object that actually loads skills", "lang": "python", "code": """from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition,
)

options = ClaudeAgentOptions(
    system_prompt=prompts["main_agent"],
    model="sonnet",

    # BOTH of these are required for skills to load
    setting_sources=["user", "project"],
    allowed_tools=[
        "Skill",        # <- without this, skills are invisible
        "Task",         # <- without this, no subagent can be dispatched
        "Read", "Grep", "Glob",
        "Write", "Bash", "WebSearch", "WebFetch",
        "mcp__notion__*",
    ],

    mcp_servers={"notion": {
        "command": "npx",
        "args": ["-y", "@notionhq/notion-mcp-server"],
        "env": {"NOTION_TOKEN": os.environ["NOTION_TOKEN"]},
    }},

    agents={
        "docs_researcher": AgentDefinition(
            description="Finds and extracts information from official documentation.",
            prompt=prompts["docs_researcher"],
            tools=["WebSearch", "WebFetch"],
            model="haiku",
        ),
        "repo_analyzer": AgentDefinition(
            description="Clones and analyses repository structure and source.",
            prompt=prompts["repo_analyzer"],
            tools=["WebSearch", "Bash", "Read", "Grep", "Glob"],
            model="haiku",
        ),
        "web_researcher": AgentDefinition(
            description="Finds articles, videos and community content.",
            prompt=prompts["web_researcher"],
            tools=["WebSearch", "WebFetch"],
            model="haiku",
        ),
    },
)""",
    "caption": "The two lines that cause most 'skills do not work in the SDK' reports are `setting_sources` and `\"Skill\"`. A subagent's tools must also be in the parent's allow-list."},
   {"title": "Orchestrator prompt: how to handle a skill", "lang": "markdown", "code": """You orchestrate three subagents: docs_researcher, repo_analyzer, web_researcher.

If a skill is available and matches the user's request, follow that skill's
instructions precisely — its workflow, structure and output format override
your own defaults.

If no skill matches, fall back to: dispatch relevant subagents in parallel,
then synthesise their findings into a single answer.""",
    "caption": "In a bespoke agent, skills may or may not be present. Say explicitly what precedence they take when they are."},
 ],
 "gotchas": [
   "`allowed_tools=[\"Skill\"]` without `setting_sources` loads no skills and produces no error — it just behaves as if you had written none.",
   "`cwd` must point at the directory containing `.claude/skills/`, or project skills will not be found.",
   "Granting a tool to a subagent does nothing unless the parent also allows it.",
   "Write and Bash without a permission callback means an unattended agent can modify your filesystem. Rebuild the approval gate before shipping.",
 ],
 "visual": "agent-sdk-wiring",
},

{
 "id": "m10", "num": "10", "title": "Evaluating Skills Like Software",
 "lesson": "Enrichment (extends Lessons 4-5)", "duration_min": 14,
 "objective": "Put a measurable quality gate around a skill: trigger rate, behavioural assertions, token and latency deltas against a no-skill baseline.",
 "key_points": [
   "Three failure modes to test separately: **it did not fire**, **it fired and did the wrong thing**, **it fired, worked, and cost more than it was worth**.",
   "Trigger testing is a description problem: run each query several times (three is the usual minimum) because triggering is stochastic.",
   "Include **should-not-fire** queries. A skill that fires on everything is as broken as one that never fires.",
   "Behavioural assertions must be objectively checkable — file exists at path, LaTeX compiles, all four question types present, steps ran in order.",
   "Always run a **baseline**: the same queries with the skill disabled. The skill's value is the delta, not the absolute score.",
   "Measure tokens and duration alongside pass rate; report means with standard deviations across repeats.",
   "Split train/test when optimising a description (the standard loop uses 60/40) so you are not overfitting your own eval set.",
   "Close with **human review** and a **cross-model** pass — a skill tuned on one model can regress on another.",
 ],
 "deep_dive": [
   "The course gets you to a serviceable harness by hand; the ecosystem now has a better default. `skill-creator`'s evaluation scripts dispatch a with-skill subagent and a baseline subagent in the same turn, collect token counts and durations from task notifications, grade against a rubric, and aggregate into a benchmark file with means and standard deviations plus the delta against the previous iteration. Its description-optimisation loop runs up to five iterations, evaluates each candidate three times per query, and selects on a held-out split. Copy that structure rather than inventing one.",
   "Grading schema discipline matters more than it sounds: the reviewer tooling depends on specific field names (`text`, `passed`, `evidence`). Whatever harness you build, fix the schema early — an eval set whose results cannot be diffed between iterations is an eval set you will stop running.",
   "There is an honest caveat to publish alongside any skill benchmark: community-scale data suggests average public-skill quality is mediocre, while *curated* skills measurably lift agent pass rates. The implication for practice is that the existence of a skill proves nothing; only the delta over baseline does.",
   "For teams, the highest-value assertion is usually not accuracy but **consistency**: does the skill produce the same structure, the same file tree, the same section order, on ten consecutive runs? That is the property you bought by writing a skill instead of a prompt, and it is the one worth regression-testing when the skill changes.",
 ],
 "spec_box": [
   ("Repeats per query", "3 minimum"),
   ("Train/test split", "60 / 40"),
   ("Iterations (loop)", "up to 5"),
   ("Baseline", "same queries, skill disabled"),
   ("Metrics", "pass_rate · tokens · duration (mean ± sd)"),
   ("Grading fields", "text · passed · evidence"),
   ("Closing gates", "human review + cross-model"),
 ],
 "artifacts": [
   {"title": "An eval set that tests routing as well as behaviour", "lang": "json", "code": """{
  "should_fire": [
    "Run the weekly campaign analysis on this CSV",
    "What was our ROAS by channel last week?",
    "Reallocate next month's budget using our rules"
  ],
  "should_not_fire": [
    "What does ROAS stand for?",
    "Write a tweet about our new campaign",
    "Convert this CSV to JSON"
  ],
  "assertions": [
    "reads SKILL.md before answering",
    "reads references/budget_reallocation_rules.md only on reallocation queries",
    "reports funnel metrics against the stated benchmarks",
    "output contains executive summary, funnel and efficiency sections"
  ],
  "repeats": 3
}""",
    "caption": "Definitions, not vibes. The should_not_fire block is what stops description inflation from quietly hijacking unrelated requests."},
 ],
 "gotchas": [
   "Evaluating a skill without a baseline tells you the model is competent, not that the skill helped.",
   "A single run tells you nothing about trigger reliability — triggering varies between identical requests.",
   "Optimising a description against your whole eval set overfits it. Hold some queries back.",
   "Assertions written as 'output is good' cannot be graded. Write assertions a script could check.",
 ],
 "visual": "eval-loop",
},

{
 "id": "m11", "num": "11", "title": "Security, Trust and Governance",
 "lesson": "Enrichment (extends Lesson 7)", "duration_min": 14,
 "objective": "Treat a skill as executable third-party content: audit it before install, bound what it can do at runtime, and govern distribution inside an organisation.",
 "key_points": [
   "A skill is **executable content**. Installing one is closer to installing a package than to reading a document.",
   "Three distinct risks: **prompt injection** through skill text or fetched content, **arbitrary code execution** through bundled scripts, and **supply-chain risk** in third-party skills.",
   "Highest-risk pattern to look for: a skill that fetches an external URL and then acts on what it finds.",
   "Independent audits of public skill registries have found large fractions with at least one security flaw and a non-trivial number of confirmed malicious payloads. Treat public catalogues as untrusted by default.",
   "Install only from sources you trust, and read the whole folder — SKILL.md, every script, every asset — before enabling it.",
   "Bound capability at runtime, not in prose: subagent tool allow-lists, permission callbacks, permission modes, hooks.",
   "Never put credentials, tokens or customer data inside a skill; skills get zipped, shared and installed elsewhere.",
   "Spec guidance forbids XML-like tags in `name`/`description` precisely because that field is injected into a prompt.",
 ],
 "deep_dive": [
   "The reason skills are a sharper security surface than prompts is progressive disclosure itself: the reviewer approving a skill reads the description, the agent reads the body, and something further down may read a reference file or execute a script nobody opened. Any audit that stops at SKILL.md has inspected the least dangerous file in the folder.",
   "The second-order risk is subtler. A skill that instructs the agent to fetch a URL and follow the instructions it finds has effectively delegated its own contents to whoever controls that URL. Even with a benign author, that is a mutable, unversioned dependency inside a trusted code path. Prefer bundled reference files over fetched ones wherever the content is stable.",
   "For organisational rollout, the controls that actually work are boring: a reviewed internal registry rather than free installation from public catalogues; skills in version control with code review, since a SKILL.md diff is as readable as any other diff; version pinning in production so behaviour does not change silently; and an explicit owner per skill, because an unowned skill encoding house conventions will drift out of date and quietly produce non-compliant output.",
   "The runtime controls deserve one blunt statement: **nothing you write in a SKILL.md constrains what an agent can do.** The body is advisory text to a model. If a step must not write files, must not reach the network, or must not run shell commands, that is enforced by tool allow-lists, permission hooks and sandbox configuration. Skills express intent; the harness expresses authority.",
 ],
 "spec_box": [
   ("Trust model", "skill = executable third-party content"),
   ("Audit surface", "SKILL.md + every script + every asset"),
   ("Top red flag", "fetches an external URL, then acts on it"),
   ("Enforcement", "tool allow-lists · permission hooks · sandbox"),
   ("Never store", "credentials, tokens, customer data"),
   ("Forbidden in metadata", "XML/angle-bracket tags"),
   ("Production", "pin versions; review in VCS; name an owner"),
 ],
 "artifacts": [
   {"title": "Pre-install audit checklist", "lang": "text", "code": """[ ] Source is trusted (internal registry, or a vendor repo you verified)
[ ] Read SKILL.md end to end - including any instruction to read or run more
[ ] Every file in scripts/ read: what it executes, what it writes, what it sends
[ ] Every file in references/ read: any instruction to fetch external content?
[ ] assets/ inspected - templates and images are content too
[ ] No credentials, tokens, endpoints or customer data embedded
[ ] No XML-like tags in name/description
[ ] Network need justified; prefer bundled over fetched
[ ] Tool surface it implies is acceptable (Bash? Write? WebFetch?)
[ ] Version pinned for production use; owner recorded""",
    "caption": "Ten minutes per skill. Applied once, before enabling, and again on any version bump."},
 ],
 "gotchas": [
   "Reviewing only SKILL.md is the standard mistake: the scripts are where execution lives.",
   "An internal skill can leak: the skill folder is copied, zipped and installed by other people, so anything embedded in it travels.",
   "Prose restrictions in a skill body are not controls. They are suggestions the model may follow.",
   "A skill that worked safely in Claude.ai (network available, package installs allowed) has different risk when it moves into a CI pipeline or an unattended agent.",
 ],
 "visual": "security-surface",
},

{
 "id": "m12", "num": "12", "title": "Portability, Ecosystem and What Is Still Moving",
 "lesson": "Enrichment (extends Lessons 2 and 4)", "duration_min": 12,
 "objective": "Write one folder that behaves the same in every host, and know which parts of the standard are stable enough to depend on.",
 "key_points": [
   "Roughly **40 skills-compatible products** now appear on the standard's official showcase: Claude Code, Claude.ai/Desktop, OpenAI Codex, GitHub Copilot, VS Code, Cursor, Gemini CLI, Amp, OpenCode, Goose, Kiro, Junie, Roo Code and more.",
   "Storage location differs by host: `~/.claude/skills/` and project `.claude/skills/` for Claude; `~/.codex/skills/` for Codex; others vary.",
   "For maximum portability, use **only** `name` + `description` plus plain markdown. Host-specific fields are silently ignored elsewhere.",
   "`allowed-tools` is experimental — honoured in some hosts, ignored in others. Do not rely on it as a control.",
   "**Always use forward slashes**, even on Windows.",
   "Keep file references one level deep and relative to the skill root.",
   "You will meet skills that predate the conventions. Read before copying; treat vendor repos as reference, not gospel.",
   "Governance of the standard is not settled: it was published openly and aligned with an industry foundation, but long-term stewardship remains an open question.",
 ],
 "deep_dive": [
   "Portability in practice comes down to a short conservatism rule: the further a feature is from 'markdown plus two frontmatter keys', the less likely it is to survive a move between hosts. Bodies, reference files and `scripts/` invoked by relative path are extremely portable. Frontmatter beyond the required pair, host-specific directory names, and any assumption about how skills are *surfaced* to the user are not.",
   "The scale of public catalogues is now large enough to be misleading. Community indexes list enormous numbers of scraped skills, but audits of quality and security paint a much less flattering picture than the raw counts suggest. Abundance is not a supply of expertise; treat public catalogues as a source of *examples*, and your own reviewed registry as the source of *dependencies*.",
   "Two moving parts are worth tracking specifically, because both were simplified in the course. First, API betas: the Skills API has gone GA and the code-execution tool has newer versions than the one shown. Second, the subagent skill-injection field, which is documented to preload full skill content but has open reports of not behaving that way. Anything you teach from the course should carry a date and a 'verify in your version' note on those two.",
   "The AGENTS.md / CLAUDE.md relationship is the last portability question people hit. Those files are project context that a host always loads; skills are on-demand procedure. If a convention must be honoured on every turn, it belongs in project context; if it applies to one class of task, it belongs in a skill. Getting that split right is what keeps both files small.",
 ],
 "spec_box": [
   ("Compatible products", "~40 on the official showcase"),
   ("Claude paths", "~/.claude/skills · .claude/skills"),
   ("Codex path", "~/.codex/skills"),
   ("Max-portability frontmatter", "name + description only"),
   ("allowed-tools", "experimental, host-dependent"),
   ("Paths", "forward slashes, relative, one level deep"),
   ("Standard published", "Dec 2025; stewardship open"),
 ],
 "artifacts": [
   {"title": "Portability rules of thumb", "lang": "text", "code": """SAFE EVERYWHERE
  SKILL.md with name + description
  markdown body, any structure
  references/, scripts/, assets/ by relative path
  forward slashes

HOST-DEPENDENT - check before relying on it
  allowed-tools               (experimental)
  subagent `skills:` field    (Claude Code; reports of inconsistency)
  plugin / marketplace install (Claude Code specific)
  container.skills + versions  (Claude API specific)

NOT PORTABLE - do not assume
  how the skill is shown to the user
  whether the host has network access
  which packages are pre-installed
  whether scripts may install dependencies at runtime""",
    "caption": "Write to the safe column; treat the middle column as a version-dated assumption; never build a workflow on the third."},
 ],
 "gotchas": [
   "Backslashes in paths work on your Windows machine and fail in every container.",
   "A skill that assumes internet access breaks in the API sandbox, which has none.",
   "Copying a vendor skill's folder conventions without reading them propagates pre-standard layouts.",
 ],
 "visual": "portability-matrix",
},

{
 "id": "m13", "num": "13", "title": "Applying This to Data-Operations Work",
 "lesson": "Applied synthesis", "duration_min": 14,
 "objective": "Translate the course's patterns into the shape of a repeatable, auditable data-quality workflow — and know which of your existing workflows should not become skills.",
 "key_points": [
   "The strongest candidates in data operations are **multi-step verification pipelines with a fixed order and a fixed output contract** — exactly the `analyzing-time-series` pattern.",
   "Split by loading tier: deterministic checks → `scripts/`; decision rules, rulebooks and interpretation guides → `references/`; output templates, schemas and column contracts → `assets/`.",
   "The SKILL.md becomes a **sequencer and output contract**, not a rulebook: which script, in which order, what to report, where files land.",
   "Reviewer skills are undervalued: a `reviewing-*` skill plus a restricted subagent gives you a cheap, consistent QA pass that keeps its noise out of the main context.",
   "Attach the reviewer to a subagent with read-only tools so it cannot silently fix what it is supposed to report.",
   "MCP handles the data plane (warehouses, ticketing, document stores); the skill handles the method; subagents handle parallel per-entity work.",
   "For anything with an audit trail, name the output tree explicitly in the skill — reproducible paths are what make a run reviewable months later.",
   "Not everything should be a skill: genuinely one-off analysis, fast-changing exploratory work, and anything whose 'convention' is still being argued about.",
 ],
 "deep_dive": [
   "The mapping from the course to operational data work is unusually direct. A batch verification pipeline is a sequence of independent checks over a keyed dataset, each with a decision rule and a residual set for human judgement. That is a fixed workflow with a non-deterministic reasoning step in the middle — the precise shape where a skill outperforms both a prompt (not repeatable) and a pure script (cannot reason about edge cases).",
   "The loading-tier split is the design decision that pays off most. Deterministic checks — schema validation, duplicate detection, coordinate range tests, join integrity — belong in Python, where they cost only their output and cannot drift between runs. Methodology and decision rules belong in `references/`, read only when a case actually needs adjudicating. Column contracts and report skeletons belong in `assets/`. What remains in SKILL.md is short: the order, the skip conditions, and the output contract.",
   "A specific high-value pattern: give every batch skill a named output tree and make the skill responsible for producing it. When a question arrives three months later about why a particular row was flagged, the difference between 'there is a results directory with a fixed layout' and 'it was in a chat somewhere' is the difference between a two-minute answer and a re-run.",
   "On reviewer skills: the course's `reviewing-cli-command` is worth transplanting wholesale. A `reviewing-batch-output` skill that carries the checklist — required columns present, flag values within the permitted set, residuals counted, remarks populated for every flagged row, output paths correct — attached to a read-only subagent, gives you a consistent pre-delivery gate. Read-only matters: a reviewer that can edit will quietly fix problems instead of surfacing them, and your error rate becomes invisible.",
   "Finally, the negative case. Skills add a maintenance surface: a folder to own, a convention to keep current, a version to pin. If a workflow runs twice, or its rules are still under debate, a prompt in a shared doc is the correct tool and a skill is premature. The threshold that matters is not complexity — it is **repetition plus a settled convention.**",
 ],
 "spec_box": [
   ("Best-fit workload", "ordered multi-check pipeline with a fixed output"),
   ("scripts/", "deterministic checks, validation, joins"),
   ("references/", "methodology, decision rules, rulebooks"),
   ("assets/", "column contracts, report and remarks templates"),
   ("SKILL.md", "sequence + skip conditions + output contract"),
   ("Reviewer subagent tools", "read-only (Read, Grep, Glob, Bash)"),
   ("Do not skillify", "one-off analysis, unsettled conventions"),
 ],
 "artifacts": [
   {"title": "A batch-verification skill, structured by loading tier", "lang": "text", "code": """verifying-batch-quality/
├── SKILL.md              # order of checks, skip rules, output contract
├── scripts/
│   ├── validate_schema.py    # required columns, dtypes, permitted flag values
│   ├── run_checks.py         # deterministic checks -> checks.json
│   └── summarise.py          # -> summary.txt + residuals.csv
├── references/
│   ├── methodology.md        # scope rules, read only when adjudicating
│   └── decision_rules.md     # per-flag TP/FP criteria
└── assets/
    ├── column_contract.json  # expected output schema
    └── remarks_template.md   # standard remark phrasing

results/
├── checks.json
├── summary.txt
├── residuals.csv        # the only rows needing human judgement
└── flagged/*.csv""",
    "caption": "Deterministic work in scripts, judgement material in references, contracts in assets. The skill body is a page long."},
 ],
 "gotchas": [
   "A skill that encodes a methodology needs an owner and a review date, or it will keep producing confidently non-compliant output after the methodology changes.",
   "Giving a reviewer subagent write access destroys the signal you built it for.",
   "Skills do not fix data-access problems. If the agent cannot reach the warehouse, that is MCP or credentials, not a SKILL.md section.",
   "Repetition plus a settled convention is the bar. Complexity alone is not.",
 ],
 "visual": "batch-pipeline",
},
]
