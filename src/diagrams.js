/* Concept diagrams. All colours come from CSS vars so they follow the theme.
   Each entry: { title, caption, svg } */
const DIAGRAMS = {

"skill-anatomy": {
title: "Anatomy of a skill folder",
caption: "One required file. Three conventional directories, each mapping to a different loading mechanic.",
svg: `<svg viewBox="0 0 720 340" role="img" aria-label="Skill folder anatomy">
<rect x="20" y="20" width="240" height="300" rx="4" fill="var(--ice)" stroke="var(--powder)"/>
<text x="36" y="48" class="d-h">skill-folder/</text>
<rect x="36" y="62" width="208" height="46" rx="3" fill="var(--blue)"/>
<text x="48" y="82" class="d-lw">SKILL.md</text>
<text x="48" y="99" class="d-sw">required · name + description</text>
<rect x="36" y="120" width="208" height="38" rx="3" fill="#fff" stroke="var(--silver)"/>
<text x="48" y="138" class="d-l">scripts/</text><text x="48" y="152" class="d-s">code to execute</text>
<rect x="36" y="168" width="208" height="38" rx="3" fill="#fff" stroke="var(--silver)"/>
<text x="48" y="186" class="d-l">references/</text><text x="48" y="200" class="d-s">docs read on demand</text>
<rect x="36" y="216" width="208" height="38" rx="3" fill="#fff" stroke="var(--silver)"/>
<text x="48" y="234" class="d-l">assets/</text><text x="48" y="248" class="d-s">templates · logos · schemas</text>
<text x="36" y="286" class="d-s">folder name must match</text>
<text x="36" y="302" class="d-s">frontmatter name</text>

<path d="M262 84 H320" stroke="var(--blue)" stroke-width="1.5"/>
<path d="M262 139 H320" stroke="var(--lead)" stroke-width="1.5" stroke-dasharray="3 3"/>
<path d="M262 187 H320" stroke="var(--lead)" stroke-width="1.5" stroke-dasharray="3 3"/>
<path d="M262 235 H320" stroke="var(--lead)" stroke-width="1.5" stroke-dasharray="3 3"/>

<text x="330" y="48" class="d-h">what it costs you</text>
<rect x="330" y="62" width="368" height="46" rx="3" fill="#fff" stroke="var(--blue)"/>
<text x="342" y="82" class="d-l">~100 tokens always · full body on match</text>
<text x="342" y="99" class="d-s">the only permanent cost of installing a skill</text>
<rect x="330" y="120" width="368" height="38" rx="3" fill="var(--dove)" stroke="var(--silver)"/>
<text x="342" y="138" class="d-l">output only — source is never tokenised</text>
<text x="342" y="152" class="d-s">cheapest tier · also the most deterministic</text>
<rect x="330" y="168" width="368" height="38" rx="3" fill="var(--dove)" stroke="var(--silver)"/>
<text x="342" y="186" class="d-l">full length, at read time</text>
<text x="342" y="200" class="d-s">suits conditional + bulky material</text>
<rect x="330" y="216" width="368" height="38" rx="3" fill="var(--dove)" stroke="var(--silver)"/>
<text x="342" y="234" class="d-l">often nothing — consumed by code</text>
<text x="342" y="248" class="d-s">one file per output format, not inline</text>
<text x="330" y="288" class="d-s">Filing a payload is really a token-budgeting</text>
<text x="330" y="304" class="d-s">decision. Pick the directory by cost profile.</text>
</svg>`},

"prompt-to-skill": {
title: "From repeated prompt to packaged asset",
caption: "The four costs the marketing walkthrough exposes, and where each one goes.",
svg: `<svg viewBox="0 0 720 320" role="img" aria-label="Prompt to skill">
<rect x="20" y="24" width="300" height="200" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="36" y="48" class="d-h">every week, by hand</text>
<rect x="36" y="60" width="268" height="30" rx="3" fill="var(--dove)"/><text x="46" y="80" class="d-l">turn 1 · quality + funnel spec</text>
<rect x="36" y="96" width="268" height="30" rx="3" fill="var(--dove)"/><text x="46" y="116" class="d-l">turn 2 · efficiency metrics spec</text>
<rect x="36" y="132" width="268" height="30" rx="3" fill="var(--dove)"/><text x="46" y="152" class="d-l">turn 3 · paste reallocation rules</text>
<rect x="36" y="168" width="268" height="40" rx="3" fill="#fff" stroke="var(--gold)"/>
<text x="46" y="185" class="d-l" fill="var(--gold-t)">all three stay in context</text>
<text x="46" y="200" class="d-s">for the rest of the conversation</text>

<path d="M330 124 H396" stroke="var(--blue)" stroke-width="2"/>
<path d="M388 118 l8 6 -8 6" fill="var(--blue)"/>
<text x="334" y="114" class="d-s">package</text>

<rect x="406" y="24" width="294" height="200" rx="4" fill="var(--ice)" stroke="var(--powder)"/>
<text x="422" y="48" class="d-h">once, as a folder</text>
<rect x="422" y="60" width="262" height="56" rx="3" fill="var(--blue)"/>
<text x="434" y="80" class="d-lw">SKILL.md</text>
<text x="434" y="97" class="d-sw">input · quality · funnel · efficiency</text>
<text x="434" y="111" class="d-sw">benchmarks · output format</text>
<rect x="422" y="124" width="262" height="46" rx="3" fill="#fff" stroke="var(--silver)"/>
<text x="434" y="142" class="d-l">references/budget_reallocation_rules.md</text>
<text x="434" y="158" class="d-s">read only when reallocation is asked about</text>
<rect x="422" y="178" width="262" height="30" rx="3" fill="#fff" stroke="var(--silver)"/>
<text x="434" y="197" class="d-l">shareable · editable · versionable</text>

<text x="20" y="256" class="d-h">the four costs</text>
<text x="20" y="278" class="d-s">repetition → SKILL.md body</text>
<text x="20" y="296" class="d-s">tacit knowledge → written down, reviewable</text>
<text x="390" y="278" class="d-s">context pollution → conditional reference file</text>
<text x="390" y="296" class="d-s">no distribution → a folder you can zip and ship</text>
</svg>`},

"progressive-disclosure": {
title: "Three loading tiers",
caption: "Metadata is the only permanent cost. Everything else is earned by a match or a directive.",
svg: `<svg viewBox="0 0 720 330" role="img" aria-label="Progressive disclosure tiers">
<rect x="24" y="30" width="660" height="78" rx="4" fill="var(--blue)"/>
<text x="44" y="58" class="d-hw">TIER 1 · metadata</text>
<text x="44" y="80" class="d-lw">name + description, for every installed skill</text>
<text x="44" y="98" class="d-sw">loaded at session start · ~100 tokens each · this is the standing tax</text>
<text x="600" y="72" class="d-hw" text-anchor="end">always</text>

<path d="M54 108 V132" stroke="var(--lead)" stroke-width="1.5"/>
<path d="M48 124 l6 8 6 -8" fill="var(--lead)"/>
<text x="70" y="126" class="d-s">description matches the request</text>

<rect x="24" y="136" width="660" height="72" rx="4" fill="var(--sky)"/>
<text x="44" y="162" class="d-hw">TIER 2 · instructions</text>
<text x="44" y="184" class="d-lw">the full SKILL.md body</text>
<text x="44" y="200" class="d-sw">target under ~500 lines / ~5,000 tokens</text>
<text x="600" y="176" class="d-hw" text-anchor="end">on match</text>

<path d="M54 208 V232" stroke="var(--lead)" stroke-width="1.5"/>
<path d="M48 224 l6 8 6 -8" fill="var(--lead)"/>
<text x="70" y="226" class="d-s">the body explicitly tells the agent to read or run it</text>

<rect x="24" y="236" width="322" height="74" rx="4" fill="var(--powder)"/>
<text x="44" y="262" class="d-h">TIER 3a · resources</text>
<text x="44" y="282" class="d-l">references/ and assets/</text>
<text x="44" y="298" class="d-s">costs full length when read</text>

<rect x="362" y="236" width="322" height="74" rx="4" fill="var(--ice)" stroke="var(--powder)"/>
<text x="382" y="262" class="d-h">TIER 3b · scripts</text>
<text x="382" y="282" class="d-l">executed, not read</text>
<text x="382" y="298" class="d-s">only stdout enters context</text>
</svg>`},

"ecosystem-map": {
title: "Where each primitive sits",
caption: "The distinguishing question is what each one costs you when it is not being used.",
svg: `<svg viewBox="0 0 720 340" role="img" aria-label="Skills, tools, MCP, subagents">
<rect x="230" y="26" width="260" height="60" rx="4" fill="var(--blue)"/>
<text x="360" y="52" class="d-hw" text-anchor="middle">main agent</text>
<text x="360" y="72" class="d-sw" text-anchor="middle">bash + filesystem · the simple harness</text>

<rect x="24" y="130" width="196" height="96" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="40" y="154" class="d-h">MCP servers</text>
<text x="40" y="176" class="d-l">connectivity</text>
<text x="40" y="192" class="d-s">warehouses · Drive · Notion</text>
<text x="40" y="212" class="d-s" fill="var(--gold-t)">cost: always in context</text>

<rect x="244" y="130" width="232" height="96" rx="4" fill="var(--ice)" stroke="var(--blue)"/>
<text x="260" y="154" class="d-h">skills</text>
<text x="260" y="176" class="d-l">procedural knowledge</text>
<text x="260" y="192" class="d-s">which tools, what order, what standard</text>
<text x="260" y="212" class="d-s" fill="var(--gold-t)">cost: ~100 tokens idle</text>

<rect x="500" y="130" width="196" height="96" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="516" y="154" class="d-h">subagents</text>
<text x="516" y="176" class="d-l">isolated context</text>
<text x="516" y="192" class="d-s">parallel · restricted tools</text>
<text x="516" y="212" class="d-s" fill="var(--gold-t)">cost: nothing until dispatched</text>

<path d="M122 130 V100 H290 V86" stroke="var(--lead)" stroke-width="1.5" fill="none"/>
<path d="M360 130 V86" stroke="var(--blue)" stroke-width="1.5"/>
<path d="M598 130 V100 H430 V86" stroke="var(--lead)" stroke-width="1.5" fill="none"/>

<rect x="500" y="244" width="196" height="40" rx="3" fill="var(--dove)" stroke="var(--silver)"/>
<text x="516" y="262" class="d-l">may carry their own skills</text>
<text x="516" y="277" class="d-s">not inherited · injected in full</text>
<path d="M598 226 V244" stroke="var(--lead)" stroke-width="1.5" stroke-dasharray="3 3"/>

<text x="24" y="264" class="d-h">tools</text>
<text x="24" y="284" class="d-s">the lower layer under all of this — hammer</text>
<text x="24" y="300" class="d-s">and saw. Skills are how to build the bookshelf.</text>
<text x="24" y="322" class="d-s" fill="var(--gold-t)">tool definitions: always in context</text>
</svg>`},

"marketplace-flow": {
title: "Getting vendor skills into each harness",
caption: "Same repository, four different install paths — and three separate stores.",
svg: `<svg viewBox="0 0 720 300" role="img" aria-label="Skill install paths">
<rect x="250" y="20" width="220" height="50" rx="4" fill="var(--blue)"/>
<text x="360" y="42" class="d-hw" text-anchor="middle">anthropics/skills</text>
<text x="360" y="60" class="d-sw" text-anchor="middle">document-skills · example-skills</text>

<path d="M300 70 V100 H120 V124" stroke="var(--lead)" stroke-width="1.5" fill="none"/>
<path d="M360 70 V124" stroke="var(--lead)" stroke-width="1.5"/>
<path d="M420 70 V100 H600 V124" stroke="var(--lead)" stroke-width="1.5" fill="none"/>

<rect x="24" y="124" width="192" height="120" rx="4" fill="var(--ice)" stroke="var(--powder)"/>
<text x="40" y="148" class="d-h">Claude.ai / Desktop</text>
<text x="40" y="170" class="d-l">document skills: built in</text>
<text x="40" y="186" class="d-s">always on, not toggleable</text>
<text x="40" y="206" class="d-l">example skills: toggle</text>
<text x="40" y="222" class="d-s">off by default · skill-creator on</text>
<text x="40" y="238" class="d-s">custom: upload a zip</text>

<rect x="264" y="124" width="192" height="120" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="280" y="148" class="d-h">Claude Code</text>
<text x="280" y="170" class="d-l">ships with none</text>
<text x="280" y="188" class="d-s">/plugin marketplace add</text>
<text x="280" y="204" class="d-s">install collections</text>
<text x="280" y="220" class="d-s">→ .claude/settings.json</text>
<text x="280" y="238" class="d-s" fill="var(--gold-t)">then restart</text>

<rect x="504" y="124" width="192" height="120" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="520" y="148" class="d-h">API / Agent SDK</text>
<text x="520" y="170" class="d-l">API: upload + mount</text>
<text x="520" y="186" class="d-s">container.skills, max 8</text>
<text x="520" y="206" class="d-l">SDK: on disk</text>
<text x="520" y="222" class="d-s">.claude/skills + Skill tool</text>
<text x="520" y="238" class="d-s">+ setting_sources</text>

<rect x="24" y="258" width="672" height="30" rx="3" fill="var(--dove)" stroke="var(--silver)"/>
<text x="40" y="277" class="d-l">Three separate stores: a skill uploaded in Claude.ai is invisible to the API and to Claude Code.</text>
</svg>`},

"freedom-dial": {
title: "Degrees of freedom",
caption: "Set the dial by asking whether variation is a defect or the point.",
svg: `<svg viewBox="0 0 720 260" role="img" aria-label="Degrees of freedom dial">
<rect x="40" y="70" width="640" height="14" rx="7" fill="var(--dove)" stroke="var(--silver)"/>
<rect x="40" y="70" width="200" height="14" rx="7" fill="var(--blue)"/>
<rect x="480" y="70" width="200" height="14" rx="7" fill="var(--gold)"/>
<circle cx="240" cy="77" r="6" fill="var(--blue)"/>
<circle cx="480" cy="77" r="6" fill="var(--gold)"/>
<text x="40" y="58" class="d-h">low freedom</text>
<text x="680" y="58" class="d-h" text-anchor="end">high freedom</text>

<rect x="40" y="104" width="290" height="126" rx="4" fill="var(--ice)" stroke="var(--powder)"/>
<text x="56" y="128" class="d-h">when variation is a defect</text>
<text x="56" y="150" class="d-s">compliance · house style · audit trails</text>
<text x="56" y="168" class="d-l">exact numbered sequence</text>
<text x="56" y="184" class="d-l">fixed output template in assets/</text>
<text x="56" y="200" class="d-l">explicit reasons a step may be skipped</text>
<text x="56" y="218" class="d-l">named output tree</text>

<rect x="390" y="104" width="290" height="126" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="406" y="128" class="d-h">when variation is the point</text>
<text x="406" y="150" class="d-s">concepts · design · creative range</text>
<text x="406" y="168" class="d-l">goals and constraints, not steps</text>
<text x="406" y="184" class="d-l">palette ranges, not hex values</text>
<text x="406" y="200" class="d-l">guardrails instead of scripts</text>
<text x="406" y="218" class="d-l">many acceptable outputs</text>
</svg>`},

"api-architecture": {
title: "Skills on the Messages API",
caption: "What Claude.ai was quietly providing, assembled by hand.",
svg: `<svg viewBox="0 0 720 340" role="img" aria-label="API architecture for skills">
<rect x="24" y="24" width="200" height="120" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="40" y="48" class="d-h">your request</text>
<text x="40" y="70" class="d-s">model</text>
<text x="40" y="88" class="d-s">betas: skills · code-exec · files</text>
<text x="40" y="106" class="d-s">container.skills [ ≤ 8 ]</text>
<text x="40" y="124" class="d-s">tools: code_execution</text>

<path d="M224 84 H286" stroke="var(--blue)" stroke-width="2"/>
<path d="M278 78 l8 6 -8 6" fill="var(--blue)"/>

<rect x="286" y="24" width="410" height="200" rx="4" fill="var(--ice)" stroke="var(--blue)"/>
<text x="302" y="48" class="d-h">execution container (sandbox)</text>
<text x="302" y="68" class="d-s">Python 3.11 · ~5 GiB RAM · ~5 GiB disk · 1 CPU · no internet</text>

<rect x="302" y="82" width="180" height="60" rx="3" fill="var(--blue)"/>
<text x="314" y="102" class="d-lw">/skills/&lt;name&gt;/</text>
<text x="314" y="119" class="d-sw">custom + built-in, mounted</text>
<text x="314" y="134" class="d-sw">SKILL.md read from here</text>

<rect x="496" y="82" width="184" height="60" rx="3" fill="#fff" stroke="var(--silver)"/>
<text x="508" y="102" class="d-l">bash + filesystem</text>
<text x="508" y="119" class="d-s">runs scripts, writes files</text>
<text x="508" y="134" class="d-s">no runtime pip install</text>

<rect x="302" y="154" width="378" height="56" rx="3" fill="#fff" stroke="var(--silver)"/>
<text x="314" y="174" class="d-l">workspace → output dir</text>
<text x="314" y="192" class="d-s">generated artefacts get a file_id you can download</text>

<rect x="24" y="244" width="672" height="76" rx="4" fill="var(--dove)" stroke="var(--silver)"/>
<text x="40" y="266" class="d-h">Files API</text>
<text x="40" y="288" class="d-l">upload input → container_upload block → skill reads it → output file_id → download</text>
<text x="40" y="308" class="d-s">Files persist until deleted · 500 MB max per file · skill size ~10 MB incl. bundled resources</text>
</svg>`},

"claude-code-layout": {
title: "A Claude Code project with skills and subagents",
caption: "Always-on project context versus on-demand procedure, and who is allowed to touch what.",
svg: `<svg viewBox="0 0 720 340" role="img" aria-label="Claude Code project layout">
<rect x="24" y="24" width="280" height="290" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="40" y="48" class="d-h">repository</text>
<rect x="40" y="60" width="248" height="42" rx="3" fill="var(--blue)"/>
<text x="52" y="78" class="d-lw">CLAUDE.md</text>
<text x="52" y="94" class="d-sw">always in context · stack, architecture</text>
<text x="40" y="126" class="d-l">.claude/skills/</text>
<rect x="52" y="134" width="236" height="26" rx="3" fill="var(--ice)" stroke="var(--powder)"/><text x="62" y="151" class="d-s">adding-cli-command</text>
<rect x="52" y="164" width="236" height="26" rx="3" fill="var(--ice)" stroke="var(--powder)"/><text x="62" y="181" class="d-s">generating-cli-tests</text>
<rect x="52" y="194" width="236" height="26" rx="3" fill="var(--ice)" stroke="var(--powder)"/><text x="62" y="211" class="d-s">reviewing-cli-command</text>
<text x="40" y="242" class="d-l">.claude/agents/</text>
<rect x="52" y="250" width="236" height="26" rx="3" fill="var(--dove)" stroke="var(--silver)"/><text x="62" y="267" class="d-s">code-reviewer.md</text>
<rect x="52" y="280" width="236" height="26" rx="3" fill="var(--dove)" stroke="var(--silver)"/><text x="62" y="297" class="d-s">test-generator-runner.md</text>

<rect x="330" y="24" width="366" height="76" rx="4" fill="var(--blue)"/>
<text x="346" y="48" class="d-hw">parent agent — stays on development</text>
<text x="346" y="70" class="d-sw">uses adding-cli-command · receives only verdicts and diffs</text>
<text x="346" y="88" class="d-sw">its window never fills with test transcripts</text>

<path d="M420 100 V128" stroke="var(--lead)" stroke-width="1.5"/><path d="M414 120 l6 8 6 -8" fill="var(--lead)"/>
<path d="M600 100 V128" stroke="var(--lead)" stroke-width="1.5"/><path d="M594 120 l6 8 6 -8" fill="var(--lead)"/>
<text x="346" y="120" class="d-s">Task</text>

<rect x="330" y="132" width="176" height="110" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="344" y="154" class="d-h">code-reviewer</text>
<text x="344" y="174" class="d-s">skill: reviewing-cli-command</text>
<text x="344" y="194" class="d-l">Bash Glob Grep Read</text>
<text x="344" y="212" class="d-s" fill="var(--gold-t)">read-only on purpose</text>
<text x="344" y="230" class="d-s">reports, never silently fixes</text>

<rect x="520" y="132" width="176" height="110" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="534" y="154" class="d-h">test-runner</text>
<text x="534" y="174" class="d-s">skill: generating-cli-tests</text>
<text x="534" y="194" class="d-l">+ Edit Write</text>
<text x="534" y="212" class="d-s">must create test files</text>
<text x="534" y="230" class="d-s">runs pytest, returns summary</text>

<rect x="330" y="254" width="366" height="60" rx="4" fill="var(--dove)" stroke="var(--silver)"/>
<text x="346" y="276" class="d-l">Subagents inherit nothing. Tools and skills are both explicit.</text>
<text x="346" y="296" class="d-s">A skill attached here is injected in full at dispatch — no further progressive disclosure.</text>
</svg>`},

"agent-sdk-wiring": {
title: "The two lines that make skills work in the SDK",
caption: "Both are required. Either one alone loads nothing, and fails silently.",
svg: `<svg viewBox="0 0 720 300" role="img" aria-label="Agent SDK wiring">
<rect x="24" y="24" width="332" height="150" rx="4" fill="var(--ice)" stroke="var(--blue)"/>
<text x="40" y="48" class="d-h">ClaudeAgentOptions</text>
<rect x="40" y="60" width="300" height="34" rx="3" fill="var(--blue)"/>
<text x="52" y="82" class="d-lw">setting_sources = ["user","project"]</text>
<rect x="40" y="100" width="300" height="34" rx="3" fill="var(--blue)"/>
<text x="52" y="122" class="d-lw">allowed_tools = ["Skill", "Task", ...]</text>
<text x="40" y="156" class="d-s">missing either one → no skills, no error message</text>

<rect x="376" y="24" width="320" height="150" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="392" y="48" class="d-h">also required</text>
<text x="392" y="72" class="d-l">"Task"</text><text x="440" y="72" class="d-s">or no subagent can be dispatched</text>
<text x="392" y="94" class="d-l">Write · Bash</text><text x="470" y="94" class="d-s">not default-allowed</text>
<text x="392" y="116" class="d-l">WebSearch · WebFetch</text><text x="392" y="132" class="d-s">grant explicitly; Read/Grep/Glob are default</text>
<text x="392" y="156" class="d-s" fill="var(--gold-t)">a subagent's tool must ALSO be in the parent's list</text>

<rect x="24" y="190" width="216" height="94" rx="4" fill="var(--dove)" stroke="var(--silver)"/>
<text x="40" y="212" class="d-h">.claude/skills/</text>
<text x="40" y="232" class="d-l">learning-a-tool</text>
<text x="40" y="250" class="d-s">attached to no subagent —</text>
<text x="40" y="266" class="d-s">it directs the orchestrator</text>

<rect x="256" y="190" width="440" height="94" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="272" y="212" class="d-h">agents = { … AgentDefinition … }</text>
<text x="272" y="234" class="d-l">docs_researcher</text><text x="400" y="234" class="d-s">WebSearch WebFetch · haiku</text>
<text x="272" y="252" class="d-l">repo_analyzer</text><text x="400" y="252" class="d-s">Bash Read Grep Glob · haiku</text>
<text x="272" y="270" class="d-l">web_researcher</text><text x="400" y="270" class="d-s">WebSearch WebFetch · haiku</text>
</svg>`},

"eval-loop": {
title: "Evaluating a skill",
caption: "Three separate failure modes, and the baseline that turns a score into a value.",
svg: `<svg viewBox="0 0 720 320" role="img" aria-label="Skill evaluation loop">
<rect x="24" y="24" width="200" height="76" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="40" y="48" class="d-h">eval set</text>
<text x="40" y="68" class="d-l">should-fire queries</text>
<text x="40" y="86" class="d-l">should-NOT-fire queries</text>

<path d="M224 62 H300" stroke="var(--lead)" stroke-width="1.5"/><path d="M292 56 l8 6 -8 6" fill="var(--lead)"/>

<rect x="300" y="24" width="180" height="76" rx="4" fill="var(--blue)"/>
<text x="316" y="48" class="d-hw">with skill</text>
<text x="316" y="68" class="d-sw">× 3 repeats minimum</text>
<text x="316" y="86" class="d-sw">triggering is stochastic</text>

<rect x="500" y="24" width="196" height="76" rx="4" fill="var(--dove)" stroke="var(--silver)"/>
<text x="516" y="48" class="d-h">baseline · skill off</text>
<text x="516" y="68" class="d-s">same queries, same repeats</text>
<text x="516" y="86" class="d-s">the skill's value is the delta</text>

<path d="M390 100 V130" stroke="var(--lead)" stroke-width="1.5"/><path d="M384 122 l6 8 6 -8" fill="var(--lead)"/>
<path d="M598 100 V130" stroke="var(--lead)" stroke-width="1.5"/><path d="M592 122 l6 8 6 -8" fill="var(--lead)"/>

<rect x="24" y="134" width="672" height="82" rx="4" fill="var(--ice)" stroke="var(--powder)"/>
<text x="40" y="158" class="d-h">three failure modes, measured separately</text>
<text x="40" y="182" class="d-l">did not fire</text><text x="40" y="200" class="d-s">→ description problem: trigger rate</text>
<text x="264" y="182" class="d-l">fired, did the wrong thing</text><text x="264" y="200" class="d-s">→ behaviour: checkable assertions</text>
<text x="500" y="182" class="d-l">fired, cost too much</text><text x="500" y="200" class="d-s">→ tokens + duration vs baseline</text>

<rect x="24" y="230" width="326" height="72" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="40" y="252" class="d-h">tuning the description</text>
<text x="40" y="272" class="d-l">60 / 40 train-test split</text>
<text x="40" y="290" class="d-s">select on held-out queries or you overfit</text>

<rect x="370" y="230" width="326" height="72" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="386" y="252" class="d-h">closing gates</text>
<text x="386" y="272" class="d-l">human review · cross-model pass</text>
<text x="386" y="290" class="d-s">and regression-test consistency of structure</text>
</svg>`},

"security-surface": {
title: "The audit surface of a skill",
caption: "SKILL.md is the least dangerous file in the folder.",
svg: `<svg viewBox="0 0 720 300" role="img" aria-label="Skill security surface">
<rect x="24" y="24" width="320" height="180" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="40" y="48" class="d-h">what a reviewer usually reads</text>
<rect x="40" y="60" width="288" height="34" rx="3" fill="var(--ice)" stroke="var(--powder)"/>
<text x="52" y="82" class="d-l">description — in the settings list</text>
<rect x="40" y="100" width="288" height="34" rx="3" fill="var(--ice)" stroke="var(--powder)"/>
<text x="52" y="122" class="d-l">SKILL.md — skimmed</text>
<text x="40" y="160" class="d-s">Everything below is read by the agent,</text>
<text x="40" y="178" class="d-s">often by nobody else.</text>

<rect x="376" y="24" width="320" height="180" rx="4" fill="var(--ice)" stroke="var(--blue)"/>
<text x="392" y="48" class="d-h">what must actually be audited</text>
<rect x="392" y="60" width="288" height="32" rx="3" fill="var(--blue)"/>
<text x="404" y="81" class="d-lw">scripts/ — what it runs, writes, sends</text>
<rect x="392" y="98" width="288" height="32" rx="3" fill="var(--sky)"/>
<text x="404" y="119" class="d-lw">references/ — any instruction to fetch?</text>
<rect x="392" y="136" width="288" height="32" rx="3" fill="var(--powder)"/>
<text x="404" y="157" class="d-l">assets/ — templates and images are content</text>
<text x="392" y="188" class="d-s" fill="var(--gold-t)">top red flag: fetches a URL, then acts on it</text>

<rect x="24" y="220" width="672" height="64" rx="4" fill="var(--dove)" stroke="var(--silver)"/>
<text x="40" y="242" class="d-h">enforcement lives outside the skill</text>
<text x="40" y="264" class="d-l">tool allow-lists · permission callbacks · permission modes · hooks · sandbox config</text>
<text x="40" y="280" class="d-s">Nothing written in a SKILL.md body constrains what an agent is able to do.</text>
</svg>`},

"portability-matrix": {
title: "What travels between hosts",
caption: "Write to the safe column; date-stamp the middle one; never depend on the third.",
svg: `<svg viewBox="0 0 720 280" role="img" aria-label="Portability matrix">
<rect x="24" y="24" width="216" height="220" rx="4" fill="var(--ice)" stroke="var(--blue)"/>
<text x="40" y="48" class="d-h">safe everywhere</text>
<text x="40" y="76" class="d-l">name + description</text>
<text x="40" y="96" class="d-l">plain markdown body</text>
<text x="40" y="116" class="d-l">scripts/ references/ assets/</text>
<text x="40" y="136" class="d-l">relative paths</text>
<text x="40" y="156" class="d-l">forward slashes</text>
<text x="40" y="196" class="d-s">~40 compatible products:</text>
<text x="40" y="214" class="d-s">Claude Code · Codex · Copilot</text>
<text x="40" y="230" class="d-s">VS Code · Cursor · Gemini CLI</text>

<rect x="252" y="24" width="216" height="220" rx="4" fill="#fff" stroke="var(--gold)"/>
<text x="268" y="48" class="d-h">host-dependent</text>
<text x="268" y="76" class="d-l">allowed-tools</text><text x="268" y="92" class="d-s">experimental</text>
<text x="268" y="116" class="d-l">subagent skills: field</text><text x="268" y="132" class="d-s">reports of inconsistency</text>
<text x="268" y="156" class="d-l">plugin marketplace</text><text x="268" y="172" class="d-s">Claude Code only</text>
<text x="268" y="196" class="d-l">container.skills</text><text x="268" y="212" class="d-s">Claude API only</text>
<text x="268" y="234" class="d-s">verify in your version</text>

<rect x="480" y="24" width="216" height="220" rx="4" fill="var(--dove)" stroke="var(--silver)"/>
<text x="496" y="48" class="d-h">never assume</text>
<text x="496" y="76" class="d-l">how the skill is surfaced</text>
<text x="496" y="102" class="d-l">that the host has network</text>
<text x="496" y="128" class="d-l">which packages exist</text>
<text x="496" y="154" class="d-l">that pip install works</text>
<text x="496" y="196" class="d-s">Storage differs too:</text>
<text x="496" y="214" class="d-s">~/.claude/skills</text>
<text x="496" y="230" class="d-s">~/.codex/skills</text>
</svg>`},

"batch-pipeline": {
title: "A verification pipeline as a skill",
caption: "Deterministic work in scripts, judgement material in references, contracts in assets.",
svg: `<svg viewBox="0 0 720 320" role="img" aria-label="Batch verification skill structure">
<rect x="24" y="24" width="200" height="60" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="40" y="48" class="d-h">batch in</text>
<text x="40" y="68" class="d-s">keyed records · flags · references</text>

<path d="M224 54 H286" stroke="var(--blue)" stroke-width="2"/><path d="M278 48 l8 6 -8 6" fill="var(--blue)"/>

<rect x="286" y="24" width="410" height="60" rx="4" fill="var(--blue)"/>
<text x="302" y="48" class="d-hw">SKILL.md — sequence + skip rules + output contract</text>
<text x="302" y="68" class="d-sw">one page. not the rulebook, not the statistics, not the templates.</text>

<rect x="24" y="106" width="216" height="118" rx="4" fill="var(--ice)" stroke="var(--powder)"/>
<text x="40" y="130" class="d-h">scripts/</text>
<text x="40" y="152" class="d-l">validate_schema.py</text>
<text x="40" y="170" class="d-l">run_checks.py</text>
<text x="40" y="188" class="d-l">summarise.py</text>
<text x="40" y="210" class="d-s">deterministic · output only</text>

<rect x="252" y="106" width="216" height="118" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="268" y="130" class="d-h">references/</text>
<text x="268" y="152" class="d-l">methodology.md</text>
<text x="268" y="170" class="d-l">decision_rules.md</text>
<text x="268" y="196" class="d-s">read only when a case</text>
<text x="268" y="212" class="d-s">actually needs adjudicating</text>

<rect x="480" y="106" width="216" height="118" rx="4" fill="#fff" stroke="var(--silver)"/>
<text x="496" y="130" class="d-h">assets/</text>
<text x="496" y="152" class="d-l">column_contract.json</text>
<text x="496" y="170" class="d-l">remarks_template.md</text>
<text x="496" y="196" class="d-s">consumed by code,</text>
<text x="496" y="212" class="d-s">not read as instructions</text>

<rect x="24" y="242" width="672" height="66" rx="4" fill="var(--dove)" stroke="var(--silver)"/>
<text x="40" y="264" class="d-h">named output tree — this is what makes a run auditable months later</text>
<text x="40" y="286" class="d-l">results/ checks.json · summary.txt · residuals.csv · flagged/*.csv</text>
<text x="40" y="302" class="d-s">Reviewer skill + read-only subagent gives a consistent pre-delivery gate that reports instead of fixing.</text>
</svg>`},
};
