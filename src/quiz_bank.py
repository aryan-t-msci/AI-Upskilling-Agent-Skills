"""Agent Skills applied question bank — v2.

Design constraints, asserted at build time:
  * 48 questions: 12 per domain, 16 per difficulty level (4 per domain per level)
  * kind = "applied" (a scenario carries the question) or "recall" (a stated fact)
    38 applied / 10 recall — the 80/20 split. Each paper draws 4 applied plus
    1 recall per domain, so the ratio holds in every attempt, not just the bank.
  * exactly one correct option, and at least one deliberate near-miss
  * the stem never misstates a fact in order to create the trap

Scenarios are framed in the kind of data work this material gets used for:
ACWI IMI coverage, GICS classification, issuer hierarchies, ESG ratings and
controversies, transition and physical risk, scenario analysis, regulatory
reporting, index review cycles, and vendor-partnered collection QA. The Agent
Skills concept under test is always what decides the answer.
"""

DOMAINS = {
    "GEO": "Geospatial and asset location",
    "ESG": "ESG data and ratings operations",
    "CLI": "Sustainability and climate",
    "QPT": "Quality process transformation",
    "SKL": "Agent Skills and Claude Code workflow",
}

QUESTIONS = [
# ══════════════════════════════════ GEO — geospatial and asset location
dict(id="GEO01", domain="GEO", difficulty=1, kind="recall",
 q="A physical-asset QA skill bundles a 700-line Python checker in scripts/. The agent runs it over a batch and reports the findings. What does that 700-line file contribute to the context window?",
 options={
  "A": "Nothing — only the script's output enters context; the source is never read into it",
  "B": "Its full length, because the agent must read a script before it can execute it",
  "C": "Roughly 100 tokens, the same metadata cost as the skill itself",
  "D": "Its full length on the first run, then nothing on later runs in the same session"},
 correct="A",
 rationale="Scripts are the cheapest tier of progressive disclosure. The agent invokes the file and receives its standard output; the code itself is never tokenised.",
 trap="The “Its full length, because the agent must read a script…” option is the intuitive model — you read code to run it — and it is exactly how reference files behave. Execution is not reading, which is why deterministic work belongs in scripts/."),

dict(id="GEO02", domain="GEO", difficulty=1, kind="recall",
 q="You attach a coordinate-review skill to a subagent in Claude Code so the reviewer runs in its own context. What happens to progressive disclosure for that skill?",
 options={
  "A": "It stops applying — the full SKILL.md is injected when the subagent is dispatched",
  "B": "It applies as usual: metadata first, then the body once the subagent's task matches",
  "C": "It applies more aggressively, because the subagent has a smaller context budget",
  "D": "It applies to the body but not to reference files, which are preloaded alongside it"},
 correct="A",
 rationale="A skill preloaded onto a subagent arrives whole at dispatch, so budget for the entire body rather than roughly 100 tokens of metadata.",
 trap="The “It applies as usual: metadata first” option is what most people answer, because it is true in every other context. The subagent path is the documented exception."),

dict(id="GEO03", domain="GEO", difficulty=1, kind="recall",
 q="Your team keeps a skill in a folder named verifying-asset-coordinates. Which frontmatter is valid?",
 options={
  "A": "name: verifying-asset-coordinates, with a description up to 1,024 characters",
  "B": "name: verifying_asset_coordinates, with a description up to 1,024 characters",
  "C": "name: Verifying-Asset-Coordinates, with a description up to 500 characters",
  "D": "name: gsai-coordinates, with a description up to 1,024 characters"},
 correct="A",
 rationale="name is lowercase letters, digits and hyphens, at most 64 characters, and must match the parent folder name. description may run to 1,024 characters.",
 trap="The “name: gsai-coordinates” option is internally valid and reads like a sensible short internal name, but the name must match the folder, so this skill will not load."),

dict(id="GEO04", domain="GEO", difficulty=1, kind="applied",
 q="An analyst adds a new coordinate-precision skill under .claude/skills/ in the batch-QA repository, confirms the frontmatter is valid, and finds it absent from /skills. What is the most likely cause?",
 options={
  "A": "Claude Code discovers skills at startup, so the session needs restarting",
  "B": "Project skills must be registered in .claude/settings.json before they appear",
  "C": "The skill has not fired yet, and /skills lists only skills used in the session",
  "D": "An existing skill has an overlapping description, which suppresses the new one"},
 correct="A",
 rationale="Discovery happens when Claude Code starts. Quit, relaunch, and the skill appears in the list with its metadata token cost.",
 trap="The “Project skills must be registered in…” option points at a real file that does real work — it records installed plugin collections. Hand-written project skills need no entry there."),

dict(id="GEO05", domain="GEO", difficulty=2, kind="applied",
 q="A rooftop-coordinate QA skill runs a land-water test using a bundled Natural Earth polygon layer. The script reads the layer; the agent never needs to see its contents. Where does the layer belong?",
 options={
  "A": "assets/ — a data file consumed by code rather than instructions read by the agent",
  "B": "references/ — it is reference data the skill consults, so it sits with the reference material",
  "C": "scripts/ — it is used only by the script, so it should sit beside the code that opens it",
  "D": "Outside the skill entirely, with SKILL.md documenting the path the analyst must supply"},
 correct="A",
 rationale="assets/ is for files consumed by code or embedded in output: templates, schemas, logos, data files. The geometry is read by Python, never by the model.",
 trap="The “references/ — it is reference data the skill consults” option is tempting because the layer is 'reference data' in everyday language. references/ holds documents the agent reads into context, and loading polygons into a context window is both meaningless and enormously expensive."),

dict(id="GEO06", domain="GEO", difficulty=2, kind="applied",
 q="A footprint-matching skill needs building footprints pulled from cloud storage part-way through the run. The pipeline invokes it through the Messages API with the code execution tool. What follows?",
 options={
  "A": "The footprints must be staged into the container with the request, or the workflow must move to a host with network access",
  "B": "The storage endpoint should be declared in the skill's compatibility field so the container opens that route",
  "C": "The download should be wrapped in the code execution tool, which may reach allow-listed endpoints",
  "D": "The download should be delegated to a subagent, which runs outside the sandbox and can reach the network"},
 correct="A",
 rationale="The API code-execution container has no internet connection at all. Either the data arrives with the request, or the workflow runs somewhere networked.",
 trap="The “The download should be wrapped in the code execution tool” option is the most credible miss, because the code execution tool is precisely where an outbound call would live. There is no allow-list to add to — the connection is absent, not filtered."),

dict(id="GEO07", domain="GEO", difficulty=2, kind="applied",
 q="An address-normalisation rulebook for Korean and Japanese addresses runs to several thousand words and is irrelevant to roughly 90% of batches. How should the skill handle it?",
 options={
  "A": "Place it in references/ and have the body read the whole file only when the batch contains KR or JP rows",
  "B": "Place it in references/ and have the body read it at the start of every run, so behaviour stays consistent",
  "C": "Condense it to a dozen lines inside SKILL.md so the rules are always available to the agent",
  "D": "Move it into scripts/ as a Python dictionary, since normalisation rules are logic rather than prose"},
 correct="A",
 rationale="Conditional plus bulky is the signature of a references/ file, and the body needs an explicit directive naming the condition and instructing a full read.",
 trap="The “Place it in references/ and have the body read it at the…” option uses the right directory and throws away the benefit: a file read unconditionally is just a long SKILL.md split across two files."),

dict(id="GEO08", domain="GEO", difficulty=2, kind="applied",
 q="Which description will most reliably fire a footprint-matching skill when an analyst asks for help in ordinary language?",
 options={
  "A": "\"Match physical assets to building footprints. Use when the user asks about footprint matching, building footprints, rooftop linking, or associating assets with structures.\"",
  "B": "\"Advanced geospatial entity resolution supporting deterministic and probabilistic linkage across heterogeneous spatial datasets at scale.\"",
  "C": "\"I can help match assets to building footprints, and I will explain the blocking and scoring approach as I work through the batch.\"",
  "D": "\"Footprint matching for the physical assets team. Owner: data quality. Version 2.1. Methodology documented on the internal wiki.\""},
 correct="A",
 rationale="A description must say what the skill does and when to use it, in the third person, using the words a user would actually type. The “Match physical assets to building footprints. Use when…” option does all three.",
 trap="The “Advanced geospatial entity resolution supporting…” option reads as the most expert and is the usual instinct on technical work. It contains almost none of the phrases an analyst types and states no trigger condition, so it routes nothing."),

dict(id="GEO09", domain="GEO", difficulty=3, kind="applied",
 q="A verification pass over roughly 88,000 asset records must produce an identical output structure every run, so a reviewer can reconstruct months later why a particular row was flagged. Which design delivers that?",
 options={
  "A": "A skill whose SKILL.md fixes the step order and names the exact output tree every run must produce",
  "B": "A subagent dedicated to verification, so the work runs in a clean isolated context every time",
  "C": "A detailed prompt kept in the team's shared document and pasted at the start of each run",
  "D": "An MCP server exposing each verification check as a separate tool the agent calls in turn"},
 correct="A",
 rationale="Repeatability in a non-deterministic system comes from explicit sequencing plus a named output contract. Reproducible paths are what make a run auditable later.",
 trap="The “A subagent dedicated to verification” option confuses isolation with repeatability. A subagent buys a separate window and tighter permissions; it says nothing about whether the output looks the same twice."),

dict(id="GEO10", domain="GEO", difficulty=3, kind="applied",
 q="Four analysts must all apply the same coordinate-QA method, and each batch also needs several independent per-country investigations running at once. What do you build?",
 options={
  "A": "One skill carrying the method, plus subagents to parallelise the per-country investigations",
  "B": "One subagent per country, each with the method written into its own system prompt",
  "C": "One skill per analyst, so each can adapt the method to the countries they own",
  "D": "One skill that spawns nested subagents per country as it works through the batch"},
 correct="A",
 rationale="Shared expertise is a skill; isolated parallel execution is a subagent. The two compose, and that composition is the standard pattern.",
 trap="The “One skill that spawns nested subagents per country as it…” option describes a topology that does not exist. A subagent has no dispatch tool, so subagents cannot spawn further subagents."),

dict(id="GEO11", domain="GEO", difficulty=3, kind="applied",
 q="A shared satellite-imagery check skill instructs the agent to fetch a configuration file from an external URL and apply the check thresholds it finds there. What is the principal objection?",
 options={
  "A": "The skill's effective instructions are controlled by whoever controls that URL — a mutable, unversioned dependency inside a trusted path",
  "B": "External fetches are slow, so the skill will time out on large asset batches",
  "C": "The URL will not resolve in the API sandbox, so the skill only works in Claude Code",
  "D": "Thresholds are configuration and belong in metadata, so the skill will fail specification validation"},
 correct="A",
 rationale="Fetch-then-act is the top red flag in a skill audit: it delegates the skill's contents to an outside party and leaves nothing you can pin, review or reproduce.",
 trap="The “The URL will not resolve in the API sandbox” option is factually true — the API container has no network — but it describes an inconvenience. The real exposure appears precisely where the fetch does succeed."),

dict(id="GEO12", domain="GEO", difficulty=3, kind="applied",
 q="A matching cascade must run blocking, then deterministic matching, then manual-review triage, in that order, returning identical numbers on identical input. How should the work be split?",
 options={
  "A": "Deterministic stages in scripts/, with SKILL.md fixing the order, the skip conditions and the output tree",
  "B": "All three stages as numbered prose steps in SKILL.md, so the agent can adapt each stage to the batch",
  "C": "Each stage as its own skill, chained by the agent in whatever order the request implies",
  "D": "The entire cascade in one script, with SKILL.md reduced to a single line naming that script"},
 correct="A",
 rationale="Scripts give determinism and cost only their output; SKILL.md contributes the sequence, the skip conditions and the output contract. This is the most transplantable pattern in the course.",
 trap="The “The entire cascade in one script” option is close and sometimes defensible, but it discards what a skill is for. With no stated order, skip rules or output contract there is nothing to follow and nothing to review."),

# ══════════════════════════════════ ESG — data and ratings operations
dict(id="ESG01", domain="ESG", difficulty=1, kind="recall",
 q="A colleague built a controversy-screening skill in Claude.ai and confirms it works there. Your API-based ratings pipeline cannot see it. Why?",
 options={
  "A": "Claude.ai, the API and Claude Code keep separate skill stores; the folder must be installed in each",
  "B": "Skills built in Claude.ai are personal and must be shared with your account before any host loads them",
  "C": "The pipeline is missing the beta header that exposes skills created in the web app",
  "D": "API requests see only skills published to the vendor repository, never custom ones"},
 correct="A",
 rationale="The three stores are independent. This is the most common confusion when a workflow moves out of the web app and into code.",
 trap="The “The pipeline is missing the beta header that exposes…” option names a header that genuinely was required for skills on the API and is now optional post-GA. It never bridged the stores."),

dict(id="ESG02", domain="ESG", difficulty=1, kind="recall",
 q="One API request needs your ratings-analysis skill, the built-in spreadsheet and document skills, and three further custom skills. Which limit should you check first?",
 options={
  "A": "A container accepts up to eight skills per request, custom and built-in counted together",
  "B": "A container accepts up to three custom skills alongside any number of built-in ones",
  "C": "There is no count limit, only a combined size ceiling of roughly 10 MB",
  "D": "Only one custom skill may be mounted per request; built-ins are unrestricted"},
 correct="A",
 rationale="Up to eight skills may be mounted in a single container, with no distinction between custom and built-in.",
 trap="The “There is no count limit” option cites a real figure — roughly 10 MB is the per-skill size ceiling including bundled resources — as though it replaced the count limit. Both exist, independently."),

dict(id="ESG03", domain="ESG", difficulty=1, kind="applied",
 q="An issuer-report skill must emit either a markdown summary for internal review or a formatted Word document for a client. How should the two templates be handled?",
 options={
  "A": "One template file per format in assets/, so only the requested format is ever loaded",
  "B": "Both templates inline in SKILL.md, so the agent can compare them and choose correctly",
  "C": "Both templates in references/, read together at the start of every run",
  "D": "Neither — describe the desired structure in prose and let the agent produce the format"},
 correct="A",
 rationale="Templates are consumed in the output rather than read as instructions, and one file per format means the unused one costs nothing.",
 trap="The “Both templates inline in SKILL.md” option is tempting because the agent does have to choose between them. It needs the choice rule in the body and the chosen file on disk, not both files in context."),

dict(id="ESG04", domain="ESG", difficulty=1, kind="applied",
 q="Your team has fifteen ESG skills installed. An analyst asks an unrelated question about a spreadsheet formula. Roughly what do those fifteen skills cost on that turn?",
 options={
  "A": "About 1,500 tokens of metadata — name and description for each, loaded whether or not they fire",
  "B": "Nothing, because unmatched skills contribute no tokens at all",
  "C": "Fifteen SKILL.md bodies, because all bodies load at session start and are evicted as context fills",
  "D": "The body of the closest-matching skill, loaded as a precaution in case it proves relevant"},
 correct="A",
 rationale="Tier one is metadata for every installed skill, roughly 100 tokens each. That fixed cost is the reason to prune a library you no longer use.",
 trap="The “Nothing, because unmatched skills contribute no tokens at…” option is how people usually paraphrase 'skills cost nothing until they fire'. Bodies cost nothing; metadata is cheap and bounded, not free."),

dict(id="ESG05", domain="ESG", difficulty=2, kind="applied",
 q="Your ratings repository has conventions that apply on every turn — the stack, the module layout, naming — and scoring conventions that matter only when someone reviews a rating. Where does each belong?",
 options={
  "A": "Stack and layout in CLAUDE.md; scoring conventions in a skill that loads when a review is requested",
  "B": "Both in CLAUDE.md, so nothing depends on whether a skill happens to trigger",
  "C": "Both in a skill, keeping CLAUDE.md minimal and the context window clean",
  "D": "Stack and layout in a skill; scoring conventions in CLAUDE.md, because correctness matters more there"},
 correct="A",
 rationale="Ask whether the rule is useful on a turn unrelated to the task. Always-relevant project facts go in CLAUDE.md; task-specific conventions go in a skill.",
 trap="The “Both in CLAUDE.md, so nothing depends on whether a skill…” option does guarantee availability and feels safer. It also puts a scoring rulebook into every unrelated turn, which is the cost progressive disclosure exists to remove."),

dict(id="ESG06", domain="ESG", difficulty=2, kind="applied",
 q="Issuer disclosure data sits in a warehouse the agent cannot currently reach, and the team wants it analysed the way the ESG methodology prescribes. What do you need?",
 options={
  "A": "An MCP server for the warehouse, plus a skill encoding the methodology for using it",
  "B": "A skill containing the warehouse credentials and connection logic in its scripts",
  "C": "An MCP server alone — once the data is reachable the analysis follows from the model's knowledge",
  "D": "A skill alone, since skills define new capabilities including reaching external systems"},
 correct="A",
 rationale="MCP supplies secure connectivity; the skill supplies the procedural knowledge for using it well. They are complementary layers.",
 trap="The “A skill containing the warehouse credentials and…” option is wrong in a specific and dangerous way: skills get zipped, shared and installed elsewhere, so embedded credentials travel with them."),

dict(id="ESG07", domain="ESG", difficulty=2, kind="applied",
 q="An ESG analysis skill described as \"Use for any request involving data, metrics, reporting or analysis\" now fires on unrelated spreadsheet questions. What is the right fix?",
 options={
  "A": "Narrow the description to the specific work, and keep should-not-fire cases in the eval set so the regression is caught if it returns",
  "B": "Leave the description and add an opening line to the body telling the agent to stop if the request is unrelated",
  "C": "Make the description longer and more specific, since routing improves with more information",
  "D": "Rename the skill so it sorts later and is considered only after the others"},
 correct="A",
 rationale="Over-triggering is a description problem with a description fix, and negative eval cases are what stop the fix regressing silently.",
 trap="The “Leave the description and add an opening line to the body…” option starts from a true premise — the body can bail out — but by then the body has loaded and the turn has paid for it. Routing happens before the body is read."),

dict(id="ESG08", domain="ESG", difficulty=2, kind="applied",
 q="You want a guarantee that a widely shared ESG skill can never write files. What actually provides that guarantee?",
 options={
  "A": "The tool allow-list of the agent or subagent running it, together with the host's permission controls",
  "B": "The skill's allowed-tools frontmatter field, which restricts it to the tools named there",
  "C": "A prominent instruction at the top of SKILL.md stating that the skill must not write files",
  "D": "Keeping all its code in references/ rather than scripts/, so nothing in the folder is executable"},
 correct="A",
 rationale="Skills express intent; the harness expresses authority. Enforcement comes from tool allow-lists, permission callbacks and sandbox configuration.",
 trap="The “The skill's allowed-tools frontmatter field” option is the closest miss because allowed-tools exists and does concern permissions. It is experimental — honoured in some hosts, silently ignored in others — so it documents an intention rather than enforcing it."),

dict(id="ESG09", domain="ESG", difficulty=3, kind="applied",
 q="Your controversy-screening skill passes 18 of 20 eval cases on the first attempt. What does that score alone establish about the skill?",
 options={
  "A": "Very little, until the same cases are run with the skill disabled and the two are compared",
  "B": "That it is ready to ship, since 90% clears any reasonable threshold",
  "C": "That the description is well tuned, because the skill fired on every case",
  "D": "That it will behave consistently on other models, since a high score generalises"},
 correct="A",
 rationale="A skill's value is the delta over a no-skill baseline. Without one you have measured the model's competence, not the skill's contribution.",
 trap="The “That the description is well tuned” option conflates two independent things. A strong behavioural score says nothing about trigger reliability, which is stochastic and has to be measured over repeats."),

dict(id="ESG10", domain="ESG", difficulty=3, kind="applied",
 q="To save review cycles you give a rating-review subagent the Write and Edit tools so it can correct convention breaches as it finds them. What is the consequence?",
 options={
  "A": "Breaches get fixed silently, so the true error rate in the upstream process becomes invisible",
  "B": "The subagent will exhaust its context window, because editing requires reading whole files first",
  "C": "The parent agent loses the ability to edit while the subagent holds those files open",
  "D": "The review skill stops triggering, because reviewers are read-only by specification"},
 correct="A",
 rationale="A reviewer exists to surface problems. Give it write access and it becomes a second author, and the signal you built it for disappears.",
 trap="The “The review skill stops triggering” option invents a rule. Nothing in the specification constrains a reviewer's tools, which is exactly why the allow-list is a decision you have to get right."),

dict(id="ESG11", domain="ESG", difficulty=3, kind="applied",
 q="An ESG methodology is revised. A skill encoding the previous rules is still installed across the team. What failure should you plan for?",
 options={
  "A": "It keeps producing confidently non-compliant output until somebody updates it",
  "B": "It stops triggering, because its description no longer matches current terminology",
  "C": "It errors out, because its reference files no longer match the live methodology",
  "D": "Nothing — the model's own knowledge of the revised methodology overrides an outdated skill"},
 correct="A",
 rationale="A matched skill is followed, not sanity-checked. Encoded methodology needs a named owner and a review date or it silently drifts out of compliance.",
 trap="The “Nothing — the model's own knowledge of the revised…” option inverts the mechanism. A matched skill's instructions take precedence over the model's defaults; that is the entire reason for writing one."),

dict(id="ESG12", domain="ESG", difficulty=3, kind="applied",
 q="A vendor partner runs first-pass data collection and your team runs second-pass QA. Both sides should work to the same conventions, but the vendor must not be able to change them. What is the right arrangement?",
 options={
  "A": "Version the skill in your repository, pin the version both sides run, and keep a named owner for changes",
  "B": "Share the skill folder and ask the vendor to keep their copy in sync with yours",
  "C": "Give the vendor a copy with allowed-tools restricted so the skill cannot be modified",
  "D": "Keep the conventions in your CLAUDE.md, which the vendor's agents read when they open the repository"},
 correct="A",
 rationale="Skills are reviewable artefacts. Version control, a pinned version and a named owner is what makes a shared convention both consistent and controlled.",
 trap="The “Give the vendor a copy with allowed-tools restricted so…” option misreads allowed-tools twice: it concerns which tools a skill may pre-approve, not who may edit the file, and it is experimental besides."),

# ══════════════════════════════════ CLI — sustainability and climate
dict(id="CLI01", domain="CLI", difficulty=1, kind="recall",
 q="Put the three loading tiers in the order they are paid for, for a climate-analytics skill.",
 options={
  "A": "Name and description at session start; the SKILL.md body on match; reference files and scripts only when the body directs it",
  "B": "The SKILL.md body at session start; name and description on match; reference files and scripts at the end of the run",
  "C": "Everything in the folder at session start, with unused parts evicted as the window fills",
  "D": "Name and description at session start; every reference file on match; the body only if a script needs it"},
 correct="A",
 rationale="Metadata always, body on match, resources on direction. Every decision about where to file a payload follows from that order.",
 trap="The “Name and description at session start; every reference…” option keeps the right first tier and inverts the rest. Reference files are the last thing loaded, not something that arrives with a match."),

dict(id="CLI02", domain="CLI", difficulty=1, kind="recall",
 q="A script inside a climate skill downloads the newest scenario dataset from a public URL at run time. It works in Claude Desktop and fails through the Messages API. What explains the difference?",
 options={
  "A": "The API container has no network access, while the desktop environment does",
  "B": "The API container blocks unsigned downloads that the desktop environment permits",
  "C": "The request is missing the files beta header, which authorises external data access",
  "D": "The dataset exceeded the container's one-CPU limit during decompression"},
 correct="A",
 rationale="No internet in the API sandbox is the most common cause of a script that passes locally and fails there. Claude.ai and Desktop containers do have network access.",
 trap="The “The request is missing the files beta header” option names a real header used for moving files in and out through the Files API. It has nothing to do with outbound access from inside the container."),

dict(id="CLI03", domain="CLI", difficulty=1, kind="recall",
 q="Which part of a climate skill can carry the most material for the least context cost?",
 options={
  "A": "A script, because only its output enters context and its source is never tokenised",
  "B": "A reference file, because it loads on demand rather than at session start",
  "C": "The description, because it is capped at 1,024 characters and always available",
  "D": "The SKILL.md body, because it is compressed before being added to context"},
 correct="A",
 rationale="Scripts are the cheapest tier: a long file can cost a few dozen tokens of standard output.",
 trap="The “A reference file, because it loads on demand rather than…” option is genuinely cheap and the usual answer. On demand still means the full length lands in context the moment it is read; a script's source never does."),

dict(id="CLI04", domain="CLI", difficulty=1, kind="applied",
 q="A guide explaining how to read transition-risk and physical-risk outputs runs long, and applying only part of it would produce misleading conclusions. What should SKILL.md instruct?",
 options={
  "A": "Read the entire file in references/ before interpreting any scenario result",
  "B": "Skim the file in references/ for the relevant scenario and ignore the rest, to save tokens",
  "C": "Load the file at session start so it is always available when scenarios come up",
  "D": "Nothing — put the guide in assets/, which is loaded automatically when needed"},
 correct="A",
 rationale="When a reference file is long and must not be partially applied, the body should say explicitly that the whole file is to be read.",
 trap="The “Skim the file in references/ for the relevant scenario…” option applies the token-saving instinct in the one place it does harm. The saving comes from reading the file conditionally, not from reading only part of it."),

dict(id="CLI05", domain="CLI", difficulty=2, kind="applied",
 q="A physical-risk skill computes hazard exposure for an asset list using a fixed model. The same input must yield the same numbers every run, and those numbers may be challenged a year later. Where does the computation belong?",
 options={
  "A": "In scripts/, so the method cannot drift between runs and only the results enter context",
  "B": "In SKILL.md as a precise prose statement of the formulae, so the agent can show its working",
  "C": "In references/, so the agent reads the method fresh each time it computes",
  "D": "In assets/ as a spreadsheet the agent fills in, so the formulae stay visible to reviewers"},
 correct="A",
 rationale="Determinism and cost both point to scripts/. The method cannot vary between runs, and the source never consumes context.",
 trap="The “In SKILL.md as a precise prose statement of the formulae” option sounds rigorous and appears to help auditability. Prose formulae are re-derived by a non-deterministic model on every run, which is the opposite of reproducible."),

dict(id="CLI06", domain="CLI", difficulty=2, kind="applied",
 q="Your custom transition-risk skill produces the analysis, and the team wants it delivered as a formatted slide deck. What is the intended approach?",
 options={
  "A": "Compose — the custom skill produces the analysis and hands off to the built-in presentation skill for the file",
  "B": "Extend the custom skill with slide-generation scripts so one skill owns the whole workflow",
  "C": "Have the agent describe the slides and build the deck by hand, since file generation is not a skill concern",
  "D": "Merge the two skills into one folder so the agent never has to choose between them"},
 correct="A",
 rationale="Your domain logic, the vendor's file-format mechanics. That division is the fastest reliable way to get value from skills.",
 trap="The “Extend the custom skill with slide-generation scripts so…” option is the instinct toward self-sufficiency. It means rebuilding a maintained capability while making your own skill larger and harder to review."),

dict(id="CLI07", domain="CLI", difficulty=2, kind="applied",
 q="A climate-reporting SKILL.md has grown to roughly 900 lines covering methodology, output formats and worked examples. What should you do?",
 options={
  "A": "Keep the body as a sequence and move methodology, formats and examples into references/ and assets/",
  "B": "Leave it — 900 lines is acceptable because the whole body loads only when the skill fires",
  "C": "Split it into nine skills of about 100 lines each, one per methodology section",
  "D": "Compress the prose until it fits, because the specification rejects bodies above 500 lines"},
 correct="A",
 rationale="Around 500 lines is the practical ceiling, and the remedy is relocation: move each payload into the directory matching its loading profile.",
 trap="The “Compress the prose until it fits” option is close on the number and wrong on the mechanism. The 500-line figure is guidance rather than a validation rule, and compressing prose destroys content instead of moving it."),

dict(id="CLI08", domain="CLI", difficulty=2, kind="applied",
 q="A colleague proposes a skill that will \"let the agent query the scenario provider's API directly\", in a harness that currently has no HTTP tool. What is the accurate assessment?",
 options={
  "A": "A skill cannot grant an ability the harness lacks — it can bundle a script, but something in the harness must execute it and reach the network",
  "B": "Correct as stated: bundled scripts are described as new capabilities, so the skill supplies the access",
  "C": "Correct, provided the endpoint is declared in the skill's compatibility field",
  "D": "Correct, because the Skill tool includes network access wherever it is enabled"},
 correct="A",
 rationale="Tools give capability; skills give procedural knowledge and can package code. Without an execution tool and network access, the script cannot run or reach anything.",
 trap="The “Correct as stated: bundled scripts are described as new…” option quotes real language — new capabilities is exactly how bundled scripts are described. The skill supplies the code, not the ability to execute it."),

dict(id="CLI09", domain="CLI", difficulty=3, kind="applied",
 q="A regulatory climate-reporting pipeline calls a skill through the API each quarter, and the output is filed externally. How should the skill version be specified?",
 options={
  "A": "Pinned to a specific version, so behaviour cannot change between filings without a deployment",
  "B": "Set to latest, so each filing automatically benefits from the newest corrections",
  "C": "Omitted, which holds the version that was current when the pipeline was written",
  "D": "Pinned in production and set to latest in testing, so issues surface before they reach a filing"},
 correct="A",
 rationale="Pin in production. latest moves silently, and a filed output that changed without a deployment is extremely hard to explain afterwards.",
 trap="The “Pinned in production and set to latest in testing” option sounds like good hygiene but guarantees the two environments differ. Testing against a version you will not ship is testing the wrong artefact."),

dict(id="CLI10", domain="CLI", difficulty=3, kind="applied",
 q="You plan to dispatch three subagents in parallel, each preloaded with a 4,000-token climate methodology skill. What should you budget for?",
 options={
  "A": "The full body in each subagent, because a preloaded skill is injected whole at dispatch",
  "B": "About 100 tokens per subagent, because only metadata crosses the dispatch boundary",
  "C": "One copy of the body, shared across the three subagents by the parent",
  "D": "Nothing extra, because subagent context is separate and does not count against the run"},
 correct="A",
 rationale="Progressive disclosure does not apply inside a dispatched subagent. The whole SKILL.md arrives at startup and persists for the subagent's life.",
 trap="The “Nothing extra, because subagent context is separate and…” option pairs a true premise with a wrong conclusion. The context is indeed separate from the parent's, but it is still consumed and still paid for."),

dict(id="CLI11", domain="CLI", difficulty=3, kind="applied",
 q="A climate-data skill fires on only about 60% of the requests that should trigger it. What is the most productive first move?",
 options={
  "A": "Rewrite the description to state what and when, in the third person, using the words analysts actually type",
  "B": "Move the most important instructions out of the body and into the description so routing can see them",
  "C": "Cut the body below 500 lines, since oversized skills are deprioritised during routing",
  "D": "Install the skill at user scope rather than project scope, which raises its routing priority"},
 correct="A",
 rationale="Routing happens on metadata alone, so under-triggering is almost always a description problem — and descriptions may be a little pushy about when to fire.",
 trap="The “Move the most important instructions out of the body and…” option starts from the right diagnosis and overshoots. The description carries the trigger condition, not the procedure; packing instructions into a 1,024-character routing key degrades both jobs."),

dict(id="CLI12", domain="CLI", difficulty=3, kind="applied",
 q="Two teams disagree about a climate skill: one wants an exact prescribed report structure, the other wants room to vary the narrative per client. How should this be resolved?",
 options={
  "A": "Set the degrees of freedom by section — fixed sequence and template where variation is a defect, goals and constraints where it is the point",
  "B": "Split into two skills with near-identical descriptions and let routing pick whichever fits the request",
  "C": "Write the strict version, since predictability is the whole reason to build a skill",
  "D": "Write the loose version and rely on review to catch structural deviations before delivery"},
 correct="A",
 rationale="Degrees of freedom is a dial set by asking whether variation is a defect or the point — and it can be set differently for different parts of one skill.",
 trap="The “Split into two skills with near-identical descriptions…” option is the tempting organisational compromise and produces the worst outcome: two near-identical descriptions actively degrade routing, so neither fires reliably."),

# ══════════════════════════════════ QPT — quality process transformation
dict(id="QPT01", domain="QPT", difficulty=1, kind="recall",
 q="What does the /skills command give you beyond the list of available skills?",
 options={
  "A": "The token cost of their metadata",
  "B": "How many times each has fired in the session",
  "C": "The size of each skill folder on disk",
  "D": "Which subagents have inherited each skill"},
 correct="A",
 rationale="It lists what is available together with the metadata token cost — the standing overhead of your skill library.",
 trap="The “Which subagents have inherited each skill” option describes something that cannot happen: subagents do not inherit a parent's skills at all."),

dict(id="QPT02", domain="QPT", difficulty=1, kind="recall",
 q="An orchestrator declares three QA subagents with good descriptions and restricted tools, and never dispatches any of them. Which omission explains it?",
 options={
  "A": "Task is missing from the parent's allowed tools, so there is no way to dispatch a subagent",
  "B": "The subagents were declared after the system prompt was set, so they were ignored",
  "C": "The subagents inherited no tools and were therefore skipped as unusable",
  "D": "Each subagent must be given at least one skill before it can be invoked"},
 correct="A",
 rationale="Task is the dispatch tool. Without it in the parent's allow-list, declared agents can never be invoked.",
 trap="The “The subagents inherited no tools and were therefore…” option sounds like plausible defensive behaviour. Subagent tools are declared explicitly, and a thin tool list produces a limited subagent rather than a skipped one."),

dict(id="QPT03", domain="QPT", difficulty=1, kind="applied",
 q="You are reviewing a third-party batch-QA skill before enabling it for the team. Which part of the folder most deserves your attention?",
 options={
  "A": "Everything in scripts/, because that is where execution actually happens",
  "B": "SKILL.md, because it governs everything the skill does",
  "C": "The description, because it determines when the skill will run",
  "D": "The frontmatter, because invalid fields are the usual sign of a poorly built skill"},
 correct="A",
 rationale="SKILL.md is the least dangerous file in the folder. The scripts are what run, write, and potentially send data off the machine.",
 trap="The “SKILL.md, because it governs everything the skill does” option is where nearly every review stops, and that is the mistake: the body may simply instruct the agent to run something nobody opened."),

dict(id="QPT04", domain="QPT", difficulty=1, kind="applied",
 q="Your QA eval set contains twenty requests that should trigger the skill. What must be added before the set is credible?",
 options={
  "A": "Requests that should not trigger it, so over-triggering is caught as explicitly as under-triggering",
  "B": "One request per QA check, so coverage matches the skill's scope exactly",
  "C": "Requests taken only from real analyst traffic, so the set reflects production usage",
  "D": "Requests for every model you deploy on, making the set model-specific"},
 correct="A",
 rationale="A skill that fires on everything is as broken as one that never fires, and only negative cases detect that failure.",
 trap="The “Requests taken only from real analyst traffic” option is good practice and easy to agree with, but a set built purely from requests that should succeed cannot detect hijacking of unrelated ones."),

dict(id="QPT05", domain="QPT", difficulty=2, kind="applied",
 q="Why should each query in a skill eval set be run at least three times?",
 options={
  "A": "Because triggering is stochastic, so one run tells you nothing about reliability",
  "B": "Because the first run warms the container and is unrepresentatively slow",
  "C": "Because three runs are the minimum before a pass rate can be computed",
  "D": "Because the model caches the skill body after the first run, changing later results"},
 correct="A",
 rationale="Identical requests do not trigger identically. Repeats give a trigger rate you can act on rather than a coin flip.",
 trap="The “Because the first run warms the container and is…” option is a real phenomenon in timing measurements and a sensible-sounding reason. It affects duration, not whether the skill fired."),

dict(id="QPT06", domain="QPT", difficulty=2, kind="applied",
 q="What does a reviewing-* skill contribute to a workflow that already has skills for producing the work?",
 options={
  "A": "It acts as a test written in prose: a checklist, examples of mistakes with their fixes, and a fixed output format",
  "B": "It validates the other skills' frontmatter and folder structure before they are allowed to run",
  "C": "It removes the need to evaluate the producing skills, since every run is now reviewed",
  "D": "It fires automatically after any other skill completes, as the specification requires"},
 correct="A",
 rationale="A review skill is an evaluator rather than a producer, and running it inside the workflow is what makes the loop self-correcting.",
 trap="The “It removes the need to evaluate the producing skills” option is the most attractive wrong answer. Per-run review catches individual defects and says nothing about trigger reliability or cost against a baseline."),

dict(id="QPT07", domain="QPT", difficulty=2, kind="applied",
 q="You want one QA skill folder to behave identically in Claude Code, Codex and Cursor, which different teams use. What do you restrict yourself to?",
 options={
  "A": "name and description, a plain markdown body, and relative paths written with forward slashes",
  "B": "Full frontmatter including allowed-tools, so each host receives explicit permissions",
  "C": "A single SKILL.md with no subdirectories, since directory conventions vary between hosts",
  "D": "Host-specific copies of the folder, because no single layout works across all three"},
 correct="A",
 rationale="The required pair plus plain markdown and relative forward-slash paths is what every compatible host reads. Extra frontmatter is silently ignored elsewhere.",
 trap="The “A single SKILL.md with no subdirectories” option over-corrects. scripts/, references/ and assets/ reached by relative path are part of the standard and travel fine; backslashes are what break."),

dict(id="QPT08", domain="QPT", difficulty=2, kind="applied",
 q="A QA workflow currently lives as a long prompt in a shared document. Which observation most strongly argues for turning it into a skill now?",
 options={
  "A": "It runs every week on a convention the team has settled, and three people now paste it",
  "B": "It is the most technically complex workflow the team runs",
  "C": "Its output is reviewed by a manager, so consistency of wording matters",
  "D": "The shared document has grown long and is hard to navigate"},
 correct="A",
 rationale="The threshold is repetition plus a settled convention. Both are present, and the cost of pasting is already being paid by several people.",
 trap="The “It is the most technically complex workflow the team runs” option states the criterion people usually reach for. Complexity alone never justifies a skill — a complex one-off is still a one-off."),

dict(id="QPT09", domain="QPT", difficulty=3, kind="applied",
 q="You maintain nine distinct QA checks, usually run in different combinations depending on the batch. How should they be packaged?",
 options={
  "A": "Several small, clearly named skills with distinct scopes, composed as each job requires",
  "B": "One omnibus QA skill covering all nine checks, so the agent never has to choose",
  "C": "One skill per requesting team, bundling the checks that team usually needs",
  "D": "Nine subagents, one per check, dispatched together on every batch"},
 correct="A",
 rationale="Decomposition wins. Systems handle well over a hundred skills, and small named skills route better and review more easily than one that tries to do everything.",
 trap="The “One omnibus QA skill covering all nine checks” option removes a choice the model makes well and replaces it with a large body that loads in full whenever any single check is needed."),

dict(id="QPT10", domain="QPT", difficulty=3, kind="applied",
 q="You wrap a QA workflow in an Agent SDK service. allowed_tools contains Skill, Task, Read, Write and Bash, the .claude/skills folder is correct, and no skill ever loads or errors. What is missing?",
 options={
  "A": "setting_sources, naming project or user as the place to load skills from",
  "B": "A beta header enabling skills for SDK sessions",
  "C": "An explicit skills path in the options, pointing at the folder",
  "D": "permission_mode, which must permit skill loading before the Skill tool takes effect"},
 correct="A",
 rationale="Skills in the SDK need both the Skill tool and setting_sources. Omit the latter and nothing loads, with no error to explain why.",
 trap="The “An explicit skills path in the options” option is close to a real requirement — the working directory must contain the .claude/skills folder — but there is no separate path option, and setting one would not substitute for setting_sources."),

dict(id="QPT11", domain="QPT", difficulty=3, kind="applied",
 q="After a quarter of use, analysts report a batch-QA skill is \"working well\", but downstream defect rates have not moved. What is the most useful next step?",
 options={
  "A": "Run the eval set with and without the skill and compare pass rate, tokens and duration",
  "B": "Survey the analysts in more detail, since they are closest to the work",
  "C": "Expand the skill to cover more checks, since the current scope is evidently too narrow",
  "D": "Tighten the description, since satisfaction without effect suggests it is not firing"},
 correct="A",
 rationale="Perceived usefulness is not measured value. Only a baseline comparison separates the skill's contribution from the model's underlying competence.",
 trap="The “Tighten the description” option is a reasonable hypothesis and might even prove right, but acting on it without a baseline means tuning a skill whose effect has never been measured."),

dict(id="QPT12", domain="QPT", difficulty=3, kind="applied",
 q="Interactive testing of a QA command is filling the main context with repeated run transcripts and slowing everything down. What is the correct restructuring?",
 options={
  "A": "Move test generation and review into subagents carrying their own skills, so the parent receives only verdicts and diffs",
  "B": "Move the test instructions into CLAUDE.md so they need not be re-read on each run",
  "C": "Shorten the QA skill so each invocation consumes less of the window",
  "D": "Run the tests in a second session and paste the results back into the first"},
 correct="A",
 rationale="Subagents exist for exactly this: isolated context for noisy work, with the parent staying on the main task and seeing only the outcome.",
 trap="The “Move the test instructions into CLAUDE.md” option addresses the wrong cost. The transcripts are the problem, not the instructions — and moving instructions into CLAUDE.md puts them into every unrelated turn as well."),
# ══════════════════════════════════ added from the condensed course write-up
# One question per (domain x difficulty) cell, so the bank stays balanced at
# 15 per domain and 20 per difficulty level.

dict(id="GEO13", domain="GEO", difficulty=1, kind="recall",
 q="What does Claude AI or Desktop provision for you that you must arrange yourself on the Messages API?",
 options={
  "A": "A sandboxed container with a filesystem, a bash shell and internet access, so a library can be installed mid-task",
  "B": "A sandboxed container with a filesystem and bash, but with internet access disabled in both environments",
  "C": "Nothing — both environments are identical, and the difference is only which skills are pre-installed",
  "D": "A larger context window, which is what allows document skills to run there"},
 correct="A",
 rationale="Claude AI and Desktop provision the container behind the scenes under Settings then Capabilities, and it can reach the network, so a package can be installed or a file fetched mid-task. On the API you request the container yourself and it has no internet.",
 trap="The “A sandboxed container with a filesystem and bash” option gets the container right and the network wrong, which matters most: a script that installs a dependency works in the desktop app and fails on the API."),

dict(id="GEO14", domain="GEO", difficulty=2, kind="applied",
 q="You need a boundary file analysed by a skill on the API, and you want the resulting flagged-rows CSV back. What is the path in and out?",
 options={
  "A": "Upload through the Files API, reference it in the message with a container_upload block, and pull the generated file back out by its file ID",
  "B": "Attach the file as a message attachment, and read the result from the response text",
  "C": "Place both files in the skill's assets/ folder, which is synchronised with the container in both directions",
  "D": "Mount a local directory into the container, since the code execution tool exposes the host filesystem"},
 correct="A",
 rationale="Files move in and out only through the Files API: upload, reference with a container_upload block, then download generated output by file ID. Mailbox in, mailbox out.",
 trap="The “Place both files in the skill's assets/ folder” option is plausible because assets/ genuinely does travel into the container with the skill. It is one-way and fixed at upload — it is not a sync channel for run outputs."),

dict(id="GEO15", domain="GEO", difficulty=3, kind="applied",
 q="A coordinate-reformatting skill should only read and rewrite files, never reach the shell or network. Its SKILL.md declares an allowed-tools list. What have you actually achieved?",
 options={
  "A": "A declared restriction that constrains and documents intent where the host honours the field — but the guarantee still comes from the harness's own tool permissions",
  "B": "A hard guarantee in every skills-compatible host, since allowed-tools is part of the required frontmatter",
  "C": "Nothing at all, because frontmatter cannot express anything about tools",
  "D": "A restriction on which tools exist in the session, removing them for the rest of the conversation"},
 correct="A",
 rationale="A skill can act as both a capability unlock and a capability limiter: allowed-tools scopes what may be used while the skill is active, which makes behaviour more constrained and auditable. The field is optional and experimental, so enforcement ultimately rests with the harness.",
 trap="The “A hard guarantee in every skills-compatible host” option overstates a real feature. allowed-tools is optional and honoured inconsistently across hosts, so treating it as a guarantee is exactly the mistake to avoid on a skill you share."),

dict(id="ESG13", domain="ESG", difficulty=1, kind="recall",
 q="Across the five primitives, how does persistence differ between a skill and a subagent?",
 options={
  "A": "A skill persists across conversations with the user or application; a subagent can persist state across sessions between itself and the parent agent",
  "B": "Both persist only for the length of a single conversation",
  "C": "A skill persists for one conversation; a subagent persists indefinitely once created",
  "D": "Neither persists — both are rebuilt from scratch on every turn"},
 correct="A",
 rationale="Skills persist across conversations, which is why they distribute expertise. Subagents persist across sessions between themselves and the parent, which is a different kind of memory.",
 trap="The “A skill persists for one conversation; a subagent…” option inverts the two. It is the skill that spans conversations; the subagent's continuity is with its parent."),

dict(id="ESG14", domain="ESG", difficulty=2, kind="applied",
 q="A quarterly ESG pack needs issuer analysis done your way and then a formatted workbook, and the result must look the same every quarter. How do you get predictability out of a non-deterministic system?",
 options={
  "A": "Stack the skills: name which skills apply and the order of steps, so the analysis skill hands off to the document skill the same way each time",
  "B": "Lower the temperature on the request, which makes the output deterministic",
  "C": "Run the whole pack in a single subagent, since isolated context produces consistent results",
  "D": "Put both the analysis and the workbook mechanics into one skill, since a single skill cannot contradict itself"},
 correct="A",
 rationale="Skills are not standalone add-ons. Referencing which skills apply and the order of steps is how a multi-part workflow becomes consistent and repeatable.",
 trap="The “Put both the analysis and the workbook mechanics into one…” option sounds like it removes ambiguity and instead rebuilds a maintained capability inside your own skill, making it longer and harder to review — the opposite of the composition pattern."),

dict(id="ESG15", domain="ESG", difficulty=3, kind="applied",
 q="Your team connects an MCP server to the disclosure warehouse and the agent can now query it. Results are inconsistent between analysts. What is missing, in the terms the course uses?",
 options={
  "A": "The recipe — MCP supplied the ingredients and the tools, but nothing yet encodes the repeatable steps for turning that data into the output you want",
  "B": "More MCP servers, since a single connector cannot express a full methodology",
  "C": "A larger context window, since inconsistency comes from the data not fitting",
  "D": "Nothing structural — inconsistency between analysts is inherent to a non-deterministic model"},
 correct="A",
 rationale="MCP brings the ingredients, tools and data; skills provide the recipe — the repeatable steps that reliably produce the output you actually want. Access without method is exactly this failure.",
 trap="The “Nothing structural” option is the fatalistic reading and is half true: models are non-deterministic. That is the reason to write explicit steps, not a reason to accept variance."),

dict(id="CLI13", domain="CLI", difficulty=1, kind="recall",
 q="Which statement about libraries in the API code-execution container is correct?",
 options={
  "A": "You get whatever is pre-installed in the container image — pandas, numpy, scipy, matplotlib, python-docx, python-pptx, pypdf and similar — and cannot add to it at run time",
  "B": "Any package on PyPI can be installed at run time, as long as it is pure Python",
  "C": "Only the standard library is present; every third-party package must be bundled in the skill",
  "D": "Packages are installed automatically when a script imports them"},
 correct="A",
 rationale="The container ships with a fixed image and no network, so scripts must live within the pre-installed set.",
 trap="The “Only the standard library is present; every third-party…” option is the over-cautious version and would be a sensible design, but it is wrong: a useful analytical stack is already present, which is why most scripts work without bundling anything."),

dict(id="CLI14", domain="CLI", difficulty=2, kind="applied",
 q="A climate agent has grown to a dozen connected tools whose JSON schemas sit in context all conversation. Some hosts now let a tool be marked deferred. What does that buy you?",
 options={
  "A": "Only the tool's name is visible up front, and its full schema is pulled in on demand before use — the same progressive-disclosure trick skills use",
  "B": "The tool runs in a subagent instead of the main agent, keeping its output out of the main window",
  "C": "The tool is disabled until a skill explicitly requests it, which removes it from the permission set",
  "D": "The tool's schema is compressed, reducing its token cost by roughly half"},
 correct="A",
 rationale="Tool definitions traditionally had to sit in context for the whole conversation. Deferring a tool front-loads only its name and fetches the schema when it is actually needed.",
 trap="The “The tool is disabled until a skill explicitly requests it” option confuses disclosure with permission. Deferring changes when the definition is loaded, not whether the agent is allowed to call it."),

dict(id="CLI15", domain="CLI", difficulty=3, kind="applied",
 q="In the research agent, the learning-a-tool skill is attached to the orchestrator and to none of the three subagents. Why is that the right arrangement?",
 options={
  "A": "The skill's job is the workflow — which subagent researches what, and how findings are organised into a fixed output — which is the orchestrator's responsibility, not a researcher's",
  "B": "Subagents cannot carry skills, so the orchestrator is the only place a skill can be attached",
  "C": "Attaching it to the subagents would make each one load it progressively, tripling the token cost",
  "D": "Skills attached to a subagent are ignored unless the subagent also has the Skill tool"},
 correct="A",
 rationale="It is an orchestration skill: it defines the research phase per subagent, how findings are folded into progressive levels, and the output structure. The subagents only need scoped tools and a clear brief.",
 trap="The “Attaching it to the subagents would make each one load it…” option has the mechanics backwards. A skill attached to a subagent is preloaded in full at dispatch rather than read progressively, so the cost concern is real but the reason given is wrong."),

dict(id="QPT13", domain="QPT", difficulty=1, kind="recall",
 q="Put the skill-creator pipeline in order.",
 options={
  "A": "Skill idea and examples, then init_skill.py scaffolds SKILL.md and folders, then a package script zips it into a bundle, then a validate script checks SKILL.md and frontmatter",
  "B": "Skill idea and examples, then a validate script checks the idea, then init_skill.py scaffolds, then a package script zips it",
  "C": "init_skill.py scaffolds, then the package script zips, then the skill is installed, then examples are added",
  "D": "A package script bundles the idea, then init_skill.py expands it, then validation runs on the installed skill"},
 correct="A",
 rationale="Scaffold, package, validate, then install for future chats. Validation runs against the built skill, which is why it comes after packaging.",
 trap="The “Skill idea and examples” option is the tempting order because validating early feels like good practice. There is nothing to validate until the files exist."),

dict(id="QPT14", domain="QPT", difficulty=2, kind="applied",
 q="A colleague wants to add skills to an in-house agent that has a model, a chat loop and a set of HTTP tools, but no filesystem and no shell. What do you tell them?",
 options={
  "A": "Skills cannot work there yet — reading a skill folder and executing bundled scripts is done by filesystem and bash tools, which the agent does not have",
  "B": "Skills will work, because the Skill tool provides its own file access wherever it is enabled",
  "C": "Skills will work for instructions but not for scripts, which need to be rewritten as HTTP tools",
  "D": "Skills will work if the folders are passed inline in the system prompt instead of read from disk"},
 correct="A",
 rationale="Tools are what power the ability to generate, read and load skills in the first place. Filesystem access and an execution tool are the floor, not an optimisation.",
 trap="The “Skills will work if the folders are passed inline in the…” option is a reasonable-sounding workaround and defeats the purpose: pasting folders inline reinstates the full context cost that progressive disclosure exists to avoid, and bundled scripts still cannot run."),

dict(id="QPT15", domain="QPT", difficulty=3, kind="applied",
 q="A review subagent should apply your review conventions but must not be able to follow the deployment skill it would otherwise discover. What does the design give you?",
 options={
  "A": "Control at both levels — restrict the subagent's tools, and scope it to only the skills relevant to its job rather than everything the parent can reach",
  "B": "Nothing — a subagent inherits the parent's skills, so any skill the parent has is reachable",
  "C": "Automatic protection, because a subagent can only load the single skill named first in its config",
  "D": "Protection only if the deployment skill declares an allowed-tools list excluding review work"},
 correct="A",
 rationale="Subagents get fine-grained tool permissions and can be scoped to specific skills, so permission and knowledge access are both controlled at the main-agent and subagent level.",
 trap="The “Nothing — a subagent inherits the parent's skills” option states the opposite of the actual behaviour. Subagents inherit nothing by default, which is why assignment is explicit — and why scoping works."),

# ══════════════════════════════════ SKL — Agent Skills and Claude Code workflow
# Ten questions contributed from the updated workbook, plus five written to
# complete the 15-per-domain / 5-per-difficulty grid.

dict(id="SKL01", domain="SKL", difficulty=1, kind="recall",
 q="A colleague on MSCI's Coverage team installs a new battlecard Skill, but notices Claude never seems to load the whole file until she actually asks about competitor positioning. What explains this?",
 options={
  "A": "Progressive disclosure — only the short name and description sit in the system prompt; the full body loads only when the description matches the request",
  "B": "Lazy loading of MCP servers, which defer their tool schemas the same way skills defer their instructions",
  "C": "Hook-based triggering, where a PreToolUse hook decides which skill file to open",
  "D": "Subagent isolation, since the battlecard content is generated fresh inside a temporary subagent each time"},
 correct="A",
 rationale="A skill's header (name + description) is loaded at startup so Claude always knows it exists; the full instructions are only read into context once Claude judges the description relevant to the current request.",
 trap="The “Lazy loading of MCP servers” option borrows real vocabulary from a different mechanism. MCP tool deferral and skill disclosure are separate systems that happen to share the same underlying motivation of saving context."),

dict(id="SKL02", domain="SKL", difficulty=2, kind="applied",
 q="The Index Research team wants a standing rule: every time someone edits an index-levels CSV, a validation script must run automatically, no matter what Claude is reasoning about at the time. Which mechanism fits?",
 options={
  "A": "A Hook (e.g. PreToolUse or PostToolUse) tied to the file-edit event, since hooks fire deterministically regardless of the model's reasoning",
  "B": "A Skill whose description mentions CSV validation, since Claude will pattern-match the file type and run it",
  "C": "A slash command the analyst types before saving the file",
  "D": "An entry in CLAUDE.md instructing Claude to always validate CSVs"},
 correct="A",
 rationale="Hooks bind an exact command to an exact event (PreToolUse, PostToolUse, SessionStart, etc.) and always fire, independent of the model's judgment. A Skill or a CLAUDE.md line is still a suggestion the model interprets.",
 trap="The skill-description and CLAUDE.md options both rely on Claude choosing to act correctly every time. The team's requirement is 'no matter what Claude is thinking', which only a hook guarantees."),

dict(id="SKL03", domain="SKL", difficulty=1, kind="recall",
 q="A new analyst joins the MSCI ONE platform team and clones its repository. She notices Claude already follows the team's commit-message conventions without her typing anything, and that a teammate on a different project does not get this behaviour. Where do these conventions most likely live?",
 options={
  "A": "In .claude/skills inside the repository, i.e. a project skill shared automatically through Git",
  "B": "In her personal .claude/skills folder, which happens to sync across machines",
  "C": "In a slash command that only she has permission to trigger",
  "D": "In a subagent's frontmatter that lists the conventions as a skill"},
 correct="A",
 rationale="Project skills sit in .claude/skills inside the repo and are versioned with it, so anyone who clones the repository inherits them automatically — unlike personal skills, which are scoped to one user's machine.",
 trap="The “In her personal .claude/skills folder” option would explain the analyst's own behaviour but not why a teammate on a different project sees none of it; personal skills follow the user everywhere, not the project."),

dict(id="SKL04", domain="SKL", difficulty=2, kind="applied",
 q="MSCI's compliance function wants one set of documentation standards enforced across every team and repository, overriding any personal preference an individual engineer has configured locally. Which mechanism fits, and why?",
 options={
  "A": "Enterprise managed settings, because they sit at the top of the priority order and override personal, project, and plugin skills",
  "B": "Personal skills, because each engineer can be asked to install the same one manually",
  "C": "Plugins, because marketplace distribution reaches the most people",
  "D": "Project skills, because Git sharing guarantees everyone on a given repo sees them"},
 correct="A",
 rationale="The priority order for name conflicts is Enterprise (highest) > Personal > Project > Plugins. Only an enterprise-managed setting can guarantee a standard holds even against a conflicting personal or project skill.",
 trap="The “Project skills, because Git sharing guarantees everyone…” option is close but incomplete: project skills only reach people who clone that specific repository, and a personal skill of the same name would still need to lose the conflict, which project-level sharing cannot force."),

dict(id="SKL05", domain="SKL", difficulty=2, kind="applied",
 q="An engineer builds a SARC-submission Skill and writes the description 'Helps with security stuff.' Teammates report Claude almost never picks it up when they ask about SARC forms. What is the most likely root cause?",
 options={
  "A": "The description lacks the specific trigger phrases (like 'SARC', 'SARA review', 'security architecture submission') that match how people actually phrase the request",
  "B": "The SKILL.md is missing a scripts/ folder, so Claude has nothing executable to run",
  "C": "The skill needs an explicit model field to be considered for matching",
  "D": "The skill folder is sitting at the skills root instead of inside its own named directory"},
 correct="A",
 rationale="Claude matches requests against the description text specifically, so a vague description with no domain trigger phrases will rarely fire even when the skill itself is well built. This is the single most common cause of a skill 'not triggering.'",
 trap="The “The skill folder is sitting at the skills root instead of…” option describes a real failure mode (a skill won't load at all if SKILL.md isn't inside a named directory), but here the report is that it rarely triggers, not that it never loads — pointing to the description, not the folder structure."),

dict(id="SKL06", domain="SKL", difficulty=1, kind="recall",
 q="A quant on the Barra Models team ships a Skill containing scripts/compute_risk.py for standard risk statistics. She wants Claude to use the script's output directly rather than re-derive the math each time. What should her SKILL.md instruct Claude to do?",
 options={
  "A": "Run the script and treat its output as the answer, without reading the script's source into context",
  "B": "Read the script's full contents into context before every use, so it can double-check the logic",
  "C": "Rewrite the script's logic manually each time to keep the calculation auditable",
  "D": "Ignore the script whenever the model's own reasoning would give a similar result"},
 correct="A",
 rationale="Scripts are meant to be executed like a calculator: press the button, trust the tested code, and only the output consumes tokens. Telling Claude to run rather than read the script is exactly what keeps results consistent and cheap.",
 trap="The “Read the script's full contents into context before every…” option is the tempting-but-wrong instinct — reading the script to 'verify' it defeats the purpose of bundling deterministic, pre-tested code and reintroduces the token cost the script was meant to avoid."),

dict(id="SKL07", domain="SKL", difficulty=2, kind="applied",
 q="A product manager for MSCI's ESG Manager platform needs Claude to dig through roughly 20 scattered design docs and Jira tickets and return one clean summary, without filling up the main conversation with all the intermediate searching. What should she ask Claude to use?",
 options={
  "A": "A subagent, which does the reading and searching in its own isolated context and hands back only a summary",
  "B": "A Hook, which intercepts each file read and compresses it before it reaches the main context",
  "C": "A line in CLAUDE.md instructing Claude to summarise concisely",
  "D": "A slash command that opens all 20 documents in one call"},
 correct="A",
 rationale="A subagent is a separate, temporary instance with its own fresh context window. It does the messy digging there, and only a summary crosses back into the main conversation — exactly the isolation the PM needs.",
 trap="The “A line in CLAUDE.md instructing Claude to summarise…” option would reduce verbosity but does nothing to stop the 20 documents themselves from consuming the main context window; the isolation, not the tone, is the actual requirement here."),

dict(id="SKL08", domain="SKL", difficulty=3, kind="applied",
 q="Two engineers each independently create a Skill named report-builder inside the same MSCI repository — one saves it as a personal skill, the other commits it as a project skill. No plugin or enterprise version of the name exists. Which one does Claude use, and why?",
 options={
  "A": "The personal skill wins, because the priority order for name conflicts ranks Personal above Project",
  "B": "The project skill wins, because Git-shared skills always take precedence over anything local to one user",
  "C": "Whichever skill was created most recently wins, since Claude always prefers the latest timestamp",
  "D": "Neither loads, and Claude Code refuses to start until the name conflict is manually resolved"},
 correct="A",
 rationale="The stated priority order is Enterprise > Personal > Project > Plugins. With no enterprise override present, the personal skill takes precedence over the project skill of the same name.",
 trap="The “The project skill wins” option assumes 'shared beats local,' which is a reasonable guess but inverts the actual documented order — project skills are convenient for team-wide sharing, but they don't outrank a personal skill in a conflict."),

dict(id="SKL09", domain="SKL", difficulty=1, kind="recall",
 q="A team lead wants junior analysts to be able to manually kick off one very specific, on-demand action — 'regenerate this week's NPS summary' — and never wants it to run automatically in the background. What is the right tool?",
 options={
  "A": "A slash command, since it is triggered by name, on demand, by the person typing it",
  "B": "A Skill, since Claude will reach for it automatically whenever NPS is mentioned",
  "C": "A line in CLAUDE.md, since that loads automatically every session",
  "D": "A Hook, since it fires whenever a specific event occurs"},
 correct="A",
 rationale="Slash commands are the one mechanism triggered explicitly by the user typing /name — a deliberate, on-demand action rather than something Claude decides to reach for or something that fires on an event.",
 trap="The “A Skill, since Claude will reach for it automatically…” option is the natural-sounding wrong answer here: a Skill is picked up automatically when Claude judges it relevant, which is the opposite of 'only when someone explicitly types the command.'"),

dict(id="SKL10", domain="SKL", difficulty=2, kind="applied",
 q="A custom subagent defined in .claude/agents is built to help onboard new engineers, but it cannot access any of the team's installed Skills even though they clearly exist in the project. What is the most likely explanation?",
 options={
  "A": "Skills are not inherited automatically; they must be explicitly listed in the subagent's frontmatter skills field",
  "B": "Subagents can never access skills under any circumstances, by design",
  "C": "The skills folder needs a model field added before any subagent can see it",
  "D": "Only Enterprise-tier skills are ever visible to a custom subagent"},
 correct="A",
 rationale="Subagents don't automatically see the parent's skills — a custom subagent must explicitly list which skills it can use in its own frontmatter. Built-in agents (Explorer, Plan, Verify) can't access skills at all, but custom ones defined in .claude/agents can, once listed.",
 trap="The “Subagents can never access skills under any circumstances” option overstates the restriction: custom subagents in .claude/agents can use skills, just not automatically — the gap here is a missing frontmatter entry, not a hard platform limit."),

dict(id="SKL11", domain="SKL", difficulty=1, kind="applied",
 q="Your team installs a plugin that bundles a skill called deploy, and the repository already has its own deploy skill in .claude/skills/. Both remain usable. Why is there no collision?",
 options={
  "A": "Plugin skills are always namespaced as plugin-name:skill-name, so the plugin's version never competes with a personal or project skill of the same name",
  "B": "Claude renames whichever skill was installed second, appending a numeric suffix",
  "C": "Plugin skills load only when the project has no skill of the same name, so the repository version silently wins",
  "D": "Both are loaded and Claude asks the user which one to use each time either is triggered"},
 correct="A",
 rationale="Plugin skills carry their plugin's namespace, which is exactly why namespacing exists: a plugin's /my-kit:deploy and your project's /deploy coexist rather than shadowing each other.",
 trap="The \u201cPlugin skills load only when the project has no skill\u201d option describes the behaviour of same-scope name conflicts, where precedence really does pick one winner. Namespacing removes the conflict rather than resolving it."),

dict(id="SKL12", domain="SKL", difficulty=3, kind="applied",
 q="A skill triggers an irreversible action — publishing a dataset to a downstream consumer. It works, but it occasionally fires when an analyst was only asking a question about publishing. What is the right control?",
 options={
  "A": "Set disable-model-invocation on the skill so it can only be run deliberately by name, and leave the description as it is",
  "B": "Narrow the description until the false triggers stop, since routing is always a description problem",
  "C": "Move the skill to enterprise scope, where it will only run for authorised users",
  "D": "Add a line at the top of the body telling Claude to confirm with the user before publishing"},
 correct="A",
 rationale="Auto-invocation is a convenience that should be switched off for destructive or irreversible work. Restricting the skill to explicit invocation removes the failure mode rather than making it rarer.",
 trap="The \u201cNarrow the description until the false triggers stop\u201d option is the right instinct for an ordinary over-triggering problem and the wrong one here. Tuning reduces the rate; for an irreversible action you want the rate to be zero, which only manual invocation guarantees."),

dict(id="SKL13", domain="SKL", difficulty=3, kind="applied",
 q="Twelve repositories across three teams all need the same set of data-quality skills, kept in step as the methodology changes. Copying .claude/skills into each repo has already drifted. What is the recommended distribution route?",
 options={
  "A": "Package the skills as a plugin and distribute it through a marketplace, so every repository installs a versioned copy and updates propagate",
  "B": "Move them to personal skills in each engineer's home directory, since personal skills apply across all projects",
  "C": "Keep one canonical repository and have the others reference it through a relative path in SKILL.md",
  "D": "Put the skills in each repository's CLAUDE.md so they load automatically wherever the repo is cloned"},
 correct="A",
 rationale="Plugins and marketplaces are the documented route for sharing skills across teams and projects with versioning and easy updates. Project skills reach only the repository they sit in.",
 trap="The \u201cMove them to personal skills in each engineer's home directory\u201d option is true about scope — personal skills do apply everywhere — and fails on the actual requirement. It multiplies the copies rather than removing them, and nothing keeps twelve home directories in step."),

dict(id="SKL14", domain="SKL", difficulty=3, kind="applied",
 q="A repository has both .claude/commands/release.md and .claude/skills/release/SKILL.md, left over from a migration. Both surface as /release. What should the team know?",
 options={
  "A": "Custom commands were merged into skills, so both still work and the skill takes precedence on a name conflict — the command file should be retired to remove the ambiguity",
  "B": "The command file takes precedence because it is the older, more specific mechanism",
  "C": "Claude Code refuses to start while a command and a skill share a name",
  "D": "They are separate namespaces, so /release runs the command and the skill is unreachable"},
 correct="A",
 rationale="Slash commands and skills converged: files in .claude/commands/ keep working and support the same frontmatter, and when both exist the skill wins. Keeping both around is a maintenance trap rather than a functional one.",
 trap="The \u201cThe command file takes precedence because it is the older, more specific mechanism\u201d option applies a reasonable general principle — specific beats general — that does not hold here. Skills are the recommended form for new work, and they win."),

dict(id="SKL15", domain="SKL", difficulty=3, kind="applied",
 q="Compliance mandates one documentation standard that no individual may override. The team ships it as a project skill in the repository. Why is that insufficient, and what fixes it?",
 options={
  "A": "A personal skill of the same name outranks a project skill, so an individual can silently override it — the mandate belongs in enterprise-managed configuration, or in a namespaced plugin skill that cannot be shadowed",
  "B": "Project skills are not version-controlled, so the standard will drift — committing it to git is the fix",
  "C": "Project skills only load for the person who created them, so it must be converted to a personal skill for each team member",
  "D": "Project skills cannot contain documentation standards, only code conventions — the standard belongs in CLAUDE.md"},
 correct="A",
 rationale="The precedence order for name conflicts runs enterprise, then personal, then project, which surprises most people: a personal skill beats the repository's. Anything genuinely mandatory has to sit above that, or avoid the collision entirely through plugin namespacing.",
 trap="The \u201cProject skills are not version-controlled\u201d option inverts one of their main advantages — living in .claude/skills/ is precisely what puts them under version control. Drift is not the problem here; override is."),
]
