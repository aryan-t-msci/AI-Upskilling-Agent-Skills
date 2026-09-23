#!/usr/bin/env python3
"""Generate the quiz app FROM the workbook.

The workbook is the single source of truth. Edit Agent-Skills-Quiz-Bank.xlsx —
questions, options, correct letter, rationale, or any value on the Config sheet —
then run this script. It reads the file and rebuilds the app. It never writes to
the workbook, so your edits are safe.
"""
import json, pathlib
import os
OUT = os.environ.get("BUNDLE_OUT", "/mnt/user-data/outputs")   # repo root when run from src/

from openpyxl import load_workbook

XLSX = pathlib.Path(f"{OUT}/Agent-Skills-Quiz-Bank.xlsx")
HTML = pathlib.Path(f"{OUT}/agent-skills-quiz.html")

# ═══════════════════════════════════════════════════════════════════
# Read the workbook back — the app is generated from the file, not the module
# ═══════════════════════════════════════════════════════════════════
rb = load_workbook(XLSX, data_only=True)

cfg = {}
cs = rb["Config"]
for r in range(5, cs.max_row + 1):
    k = cs.cell(row=r, column=1).value
    if k:
        cfg[k] = cs.cell(row=r, column=2).value

qs = rb["Question Bank"]
bank = []
for r in range(5, qs.max_row + 1):
    if not qs.cell(row=r, column=1).value:
        continue
    g = lambda c: qs.cell(row=r, column=c).value
    bank.append({
        "id": g(1), "domain": g(2), "domainName": g(3), "difficulty": g(4),
        "kind": (g(5) or "applied"), "q": g(6),
        "options": {"A": g(7), "B": g(8), "C": g(9), "D": g(10)},
        "correct": g(11), "rationale": g(12), "trap": g(13),
    })

doms = {}
ds = rb["Domains"]
for r in range(5, ds.max_row + 1):
    if ds.cell(row=r, column=1).value:
        doms[ds.cell(row=r, column=1).value] = ds.cell(row=r, column=2).value

# ── validate what came out of the workbook ────────────────────────────────
# build_quiz_bank.py enforces the bank's design, but it only runs when the bank
# is generated from Python. Rows added straight into the workbook bypass it, so
# check them here instead of shipping a quiet problem.
errors, warnings = [], []
clean = []
for q in bank:
    where = q["id"] or "(row with no ID)"
    if not q["q"] or not all(q["options"].get(k) for k in "ABCD"):
        errors.append(f"{where}: needs a question and all four options")
        continue
    if q["correct"] not in ("A", "B", "C", "D"):
        errors.append(f"{where}: Correct must be a single letter A-D, found {q['correct']!r}")
        continue
    if q["kind"] not in ("applied", "recall"):
        warnings.append(f"{where}: Kind {q['kind']!r} is not applied or recall — treated as applied")
        q["kind"] = "applied"
    if not q["trap"]:
        warnings.append(f"{where}: no Distractor note, so the review will show an empty near-miss")
    if q["domain"] not in doms:
        warnings.append(f"{where}: domain {q['domain']!r} is not on the Domains sheet, "
                        f"so this question will NEVER be drawn while stratify_by_domain=1")
    clean.append(q)

ids = [q["id"] for q in clean]
dupes = sorted({i for i in ids if ids.count(i) > 1})
if dupes:
    warnings.append(f"duplicate IDs: {', '.join(dupes)}")

# can the draw actually be satisfied from each domain?
N = int(cfg.get("questions_per_attempt", 20))
if str(cfg.get("stratify_by_domain")) == "1" and doms:
    per = N // len(doms)
    n_rec = max(1, round(per * 0.2))
    for code, label in doms.items():
        pool = [q for q in clean if q["domain"] == code]
        rec = sum(1 for q in pool if q["kind"] == "recall")
        app = len(pool) - rec
        if len(pool) < per:
            warnings.append(f"{code}: only {len(pool)} questions but the draw wants {per}")
        elif rec < n_rec or app < per - n_rec:
            warnings.append(f"{code}: draw wants {per - n_rec} applied + {n_rec} recall, "
                            f"pool has {app} applied + {rec} recall — it will top up from the domain instead")

if errors:
    print("\nSKIPPED ROWS — fix these in the workbook:")
    for e in errors:
        print("  ✗", e)
if warnings:
    print("\nWARNINGS:")
    for w in warnings:
        print("  !", w)

bank = clean
from collections import Counter
print("\nread back from workbook:", len(bank), "questions ·",
      dict(Counter(q["domain"] for q in bank)), "·",
      f"{round(100 * sum(1 for q in bank if q['kind'] == 'applied') / max(1, len(bank)))}% applied")
print("config:", cfg)

DATA = {"config": cfg, "bank": bank, "domains": doms}

TPL = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Skills — Applied Quiz</title>
<style>
:root{
  --blue:#1A3FD6; --smokey:#0626A9; --sky:#7188EF; --ice:#F4F5FD; --powder:#AEBAF0;
  --green:#118A5E; --green-bg:#F1FAF6; --red:#C8271A; --red-bg:#FDF3F1;
  --gold:#A35C00; --gold-bg:#FFFBF4;
  --ink:#111318; --charcoal:#4D4D4D; --lead:#707070; --flint:#999;
  --silver:#E6E6E6; --dove:#F5F5F5; --bg:#fff;
  --sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:var(--sans);color:var(--ink);background:var(--bg);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
code{font-family:var(--mono);font-size:.86em;background:var(--ice);padding:.1em .34em;border-radius:2px;color:var(--smokey)}
.shell{max-width:880px;margin:0 auto;padding:0 24px 80px}

/* top bar */
.bar{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--silver);margin-bottom:34px}
.bar .in{max-width:880px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;gap:16px}
.bar b{font-size:14px;font-weight:650;letter-spacing:-.01em}
.bar .sp{margin-left:auto;display:flex;align-items:center;gap:18px}
.clock{font-family:var(--mono);font-size:19px;font-weight:600;color:var(--smokey);font-variant-numeric:tabular-nums}
.clock.warn{color:var(--gold)}
.clock.crit{color:var(--red)}
.qcount{font-family:var(--mono);font-size:13px;color:var(--lead)}
.track{height:3px;background:var(--silver)}
.track i{display:block;height:100%;background:var(--blue);transition:width .2s}

h1{font-size:34px;line-height:1.14;letter-spacing:-.025em;font-weight:690;margin:34px 0 14px;max-width:24ch}
h2{font-size:22px;font-weight:660;letter-spacing:-.015em;margin:38px 0 12px}
p{max-width:70ch}
.lede{font-size:17.5px;color:var(--charcoal);max-width:64ch}

.rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;background:var(--silver);border:1px solid var(--silver);border-radius:4px;overflow:hidden;margin:26px 0}
.rules div{background:#fff;padding:14px 16px}
.rules dt{font-size:11.5px;color:var(--lead);margin-bottom:3px}
.rules dd{margin:0;font-size:15px;font-weight:560}
.rules dd span{font-family:var(--mono);color:var(--smokey)}

.warnbox{border-left:3px solid var(--gold);background:var(--gold-bg);padding:14px 18px;margin:24px 0;max-width:70ch}
.warnbox b{display:block;font-size:12px;color:var(--gold);margin-bottom:4px}
.warnbox p{margin:0;font-size:15px}

.btn{font:inherit;font-size:15px;font-weight:560;cursor:pointer;border:1px solid var(--silver);background:#fff;color:var(--charcoal);padding:11px 20px;border-radius:3px}
.btn:hover:not(:disabled){border-color:var(--blue);color:var(--blue)}
.btn:disabled{opacity:.45;cursor:default}
.btn.primary{background:var(--blue);border-color:var(--blue);color:#fff}
.btn.primary:hover:not(:disabled){background:var(--smokey);border-color:var(--smokey);color:#fff}
.btn.big{font-size:16px;padding:13px 28px}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:28px}

/* question */
.meta{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:12.5px;color:var(--lead);margin-bottom:14px}
.tag{border:1px solid var(--silver);background:var(--dove);border-radius:999px;padding:2px 10px;font-size:11.5px;color:var(--charcoal)}
.stem{font-size:21px;line-height:1.42;font-weight:600;letter-spacing:-.012em;margin:0 0 26px;max-width:62ch}
.opts{display:flex;flex-direction:column;gap:9px;max-width:68ch}
.opt{display:grid;grid-template-columns:30px 1fr;gap:12px;text-align:left;font:inherit;font-size:15.4px;line-height:1.5;
     cursor:pointer;padding:14px 16px;border:1px solid var(--silver);border-radius:3px;background:#fff;color:var(--ink)}
.opt:hover{border-color:var(--powder);background:#FCFDFF}
.opt .k{font-family:var(--mono);font-size:12.5px;color:var(--flint);padding-top:3px}
.opt[aria-pressed="true"]{border-color:var(--blue);background:var(--ice);box-shadow:inset 0 0 0 1px var(--blue)}
.opt[aria-pressed="true"] .k{color:var(--blue);font-weight:700}
.hint{font-size:13px;color:var(--flint);margin-top:18px}

/* results */
.score{border:1px solid var(--silver);border-radius:5px;padding:28px 32px;margin:10px 0 30px;display:flex;gap:40px;flex-wrap:wrap;align-items:flex-end}
.score .big{font-size:56px;font-weight:700;letter-spacing:-.035em;line-height:.95}
.score .big em{font-style:normal;font-size:20px;color:var(--lead);font-weight:500}
.tally{display:flex;gap:26px;flex-wrap:wrap;font-size:14px}
.tally div span{display:block;font-family:var(--mono);font-size:22px;font-weight:600;line-height:1.2}
.tally .c span{color:var(--green)} .tally .w span{color:var(--red)} .tally .s span{color:var(--lead)}

.dstat{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1px;background:var(--silver);border:1px solid var(--silver);border-radius:4px;overflow:hidden;margin-bottom:34px}
.dstat div{background:#fff;padding:13px 16px}
.dstat dt{font-size:11.5px;color:var(--lead);margin-bottom:2px}
.dstat dd{margin:0;font-family:var(--mono);font-size:15px;color:var(--smokey)}

.item{border:1px solid var(--silver);border-left-width:3px;border-radius:3px;padding:18px 22px;margin-bottom:14px}
.item.ok{border-left-color:var(--green);background:var(--green-bg)}
.item.no{border-left-color:var(--red);background:var(--red-bg)}
.item.sk{border-left-color:var(--flint);background:var(--dove)}
.item .h{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;font-size:12px;color:var(--lead);margin-bottom:8px}
.item .h b{font-family:var(--mono);font-size:12px;color:var(--charcoal)}
.item .h .v{font-weight:650;font-size:12px}
.item.ok .h .v{color:var(--green)} .item.no .h .v{color:var(--red)} .item.sk .h .v{color:var(--lead)}
.item .qq{font-size:16px;font-weight:600;line-height:1.45;margin:0 0 12px;max-width:66ch}
.ans{font-size:14.6px;margin:0 0 5px;max-width:70ch}
.ans i{font-style:normal;display:inline-block;min-width:118px;color:var(--lead);font-size:12.5px}
.why{border-top:1px solid rgba(0,0,0,.07);margin-top:12px;padding-top:11px}
.why p{font-size:14.2px;margin:0 0 7px;max-width:70ch}
.why p:last-child{margin:0}
.why b{font-size:11.5px;color:var(--smokey);display:block;margin-bottom:2px}

@media print{
  .bar,.noprint{display:none !important}
  body{font-size:11pt}
  .shell{max-width:none;padding:0}
  h1{font-size:22pt;margin-top:0}
  .item{break-inside:avoid;page-break-inside:avoid;background:#fff !important;border-color:#bbb}
  .score{break-inside:avoid}
  a{text-decoration:none;color:#000}
}
@media (max-width:640px){
  h1{font-size:27px} .stem{font-size:19px} .score{gap:24px} .score .big{font-size:44px}
}
:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
</style>
</head>
<body>
<div class="bar noprint" id="bar" hidden>
  <div class="in">
    <b>Agent Skills — applied quiz</b>
    <div class="sp"><span class="qcount" id="qc"></span><span class="clock" id="clk">10:00</span></div>
  </div>
  <div class="track"><i id="trk" style="width:0%"></i></div>
</div>
<div class="shell" id="app"></div>

<script>
const DATA = __DATA__;
const CFG = DATA.config, BANK = DATA.bank, DOMS = DATA.domains;
const N        = +CFG.questions_per_attempt || 20;
const SECS     = Math.round((+CFG.time_limit_minutes || 10) * 60);
const M_OK     = +CFG.mark_correct ?? 1;
const M_NO     = +CFG.mark_incorrect ?? -1;
const M_SK     = +CFG.mark_skipped ?? 0;
const STRAT    = String(CFG.stratify_by_domain) === "1";
const ALLOWSK  = String(CFG.allow_skip) === "1";
const LETTERS  = ["A","B","C","D"];

const $ = s => document.querySelector(s);
const esc = s => String(s == null ? "" : s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
const md  = s => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>");
const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
const mmss = s => String(Math.floor(s/60)).padStart(2,"0") + ":" + String(s%60).padStart(2,"0");

/* ---- draw a fresh paper: reshuffled on every load, refresh and retake ---- */
function drawPaper(){
  let picked = [];
  if (STRAT) {
    const codes = shuffle(Object.keys(DOMS));
    const per = Math.floor(N / codes.length);              // 5 per domain at N=20
    const nRec = Math.max(1, Math.round(per * 0.2));       // 1 recall, 4 applied
    codes.forEach(c => {
      const pool = BANK.filter(q => q.domain === c);
      const rec = shuffle(pool.filter(q => q.kind === "recall")).slice(0, nRec);
      const app = shuffle(pool.filter(q => q.kind !== "recall")).slice(0, per - rec.length);
      let dom = rec.concat(app);
      if (dom.length < per) {                              // thin domain: top up from anything left
        const used = new Set(dom.map(q => q.id));
        dom = dom.concat(shuffle(pool.filter(q => !used.has(q.id))).slice(0, per - dom.length));
      }
      picked = picked.concat(dom);
    });
    const used = new Set(picked.map(q => q.id));
    picked = picked.concat(shuffle(BANK.filter(q => !used.has(q.id))).slice(0, N - picked.length));
  } else {
    picked = shuffle(BANK.slice()).slice(0, N);
  }
  return shuffle(picked).slice(0, N).map(q => {
    const order = shuffle(LETTERS.slice());       // option order shuffled per question
    return {
      src: q,
      order,                                      // display slot i shows original letter order[i]
      shown: order.map((L, i) => ({ slot: LETTERS[i], orig: L, text: q.options[L] })),
      correctSlot: LETTERS[order.indexOf(q.correct)],
      given: null,                                // slot letter chosen, or null
    };
  });
}

let paper = drawPaper();
let idx = 0, left = SECS, timer = null, phase = "intro", sel = null;

/* ---------------- intro ---------------- */
function intro(){
  $("#bar").hidden = true;
  return `
  <h1>Applied quiz — Agent Skills in practice</h1>
  <p class="lede">Twenty questions drawn at random from a bank of ${BANK.length}, across four applied domains.
  Several options in each question are close to right. The facts in the stem are always stated straight — the
  difficulty is in the judgement, not in the wording.</p>

  <dl class="rules">
    <div><dt>Questions</dt><dd><span>${N}</span> drawn fresh each attempt</dd></div>
    <div><dt>Time limit</dt><dd><span>${Math.round(SECS/60)} minutes</span> for the whole paper</dd></div>
    <div><dt>Marking</dt><dd><span>${M_OK >= 0 ? "+" : ""}${M_OK}</span> correct &nbsp; <span>${M_NO}</span> wrong &nbsp; <span>${M_SK}</span> skipped</dd></div>
    <div><dt>Score range</dt><dd><span>${N*M_NO}</span> to <span>+${N*M_OK}</span></dd></div>
  </dl>

  <div class="warnbox">
    <b>Read before starting</b>
    <p>One question appears at a time and <strong>cannot be revisited</strong> once you move on. The clock starts
    when you press Start and does not pause. At zero the paper submits itself and marks whatever you reached.
    ${ALLOWSK ? "Because a wrong answer costs " + Math.abs(M_NO) + " mark, skipping is worth " + M_SK + " and is sometimes the right play." : "An answer is required before you can advance."}</p>
  </div>

  <h2>Domains in the draw</h2>
  <dl class="dstat">
    ${Object.entries(DOMS).map(([c,n]) => `<div><dt>${esc(n)}</dt><dd>${BANK.filter(q=>q.domain===c).length} in bank</dd></div>`).join("")}
  </dl>

  <div class="row"><button class="btn primary big" id="go">Start the ${Math.round(SECS/60)}-minute paper</button>
  <button class="btn" id="reshuffle">Draw a different set</button></div>
  <p class="hint">Refreshing this page also reshuffles the paper and the option order.
  Each paper takes four scenario questions and one factual question per domain, so roughly
  ${Math.round((1 - 1/(N/Object.keys(DOMS).length))*100)}% of what you see is applied.
  &nbsp;·&nbsp; <a href="agent-skills-study-app.html">Open the study app</a> if you want to revise first.</p>`;
}

/* ---------------- question ---------------- */
function question(){
  const it = paper[idx], q = it.src;
  $("#bar").hidden = false;
  $("#qc").textContent = `Question ${idx+1} of ${paper.length}`;
  $("#trk").style.width = (idx / paper.length * 100) + "%";
  return `
  <div class="meta">
    <span class="tag">${esc(q.domainName)}</span>
    <span>Difficulty ${q.difficulty}</span><span>·</span>
    <span>${M_OK >= 0 ? "+" : ""}${M_OK} correct, ${M_NO} wrong${ALLOWSK ? ", " + M_SK + " skipped" : ""}</span>
  </div>
  <p class="stem">${md(q.q)}</p>
  <div class="opts" id="opts">
    ${it.shown.map(o => `
      <button class="opt" data-slot="${o.slot}" aria-pressed="${sel === o.slot}">
        <span class="k">${o.slot}</span><span>${md(o.text)}</span>
      </button>`).join("")}
  </div>
  <div class="row">
    <button class="btn primary" id="next" ${sel ? "" : "disabled"}>
      ${idx === paper.length - 1 ? "Submit paper" : "Lock answer and continue"}
    </button>
    ${ALLOWSK ? `<button class="btn" id="skip">Skip (${M_SK})</button>` : ""}
  </div>
  <p class="hint">Once you continue you cannot come back to this question.</p>`;
}

function bindQuestion(){
  document.querySelectorAll(".opt").forEach(b => b.onclick = () => {
    sel = b.dataset.slot;
    document.querySelectorAll(".opt").forEach(x => x.setAttribute("aria-pressed", String(x.dataset.slot === sel)));
    $("#next").disabled = false;
  });
  $("#next").onclick = () => advance(sel);
  const sk = $("#skip"); if (sk) sk.onclick = () => advance(null);
}

function advance(slot){
  paper[idx].given = slot;
  sel = null;
  if (idx === paper.length - 1) { finish("completed"); return; }
  idx++; render();
}

/* ---------------- timer ---------------- */
function startClock(){
  left = SECS;
  tick();
  timer = setInterval(() => { left--; tick(); if (left <= 0) finish("time"); }, 1000);
}
function tick(){
  const c = $("#clk"); if (!c) return;
  c.textContent = mmss(Math.max(0, left));
  c.className = "clock" + (left <= 30 ? " crit" : left <= 120 ? " warn" : "");
}

/* ---------------- results ---------------- */
function finish(reason){
  if (timer) { clearInterval(timer); timer = null; }
  phase = "done"; paper.endReason = reason; render();
}

function results(){
  $("#bar").hidden = true;
  const marked = paper.map(it => {
    const state = it.given === null ? "sk" : (it.given === it.correctSlot ? "ok" : "no");
    return { it, state, mark: state === "ok" ? M_OK : state === "no" ? M_NO : M_SK };
  });
  const total = marked.reduce((a, m) => a + m.mark, 0);
  const nOk = marked.filter(m => m.state === "ok").length;
  const nNo = marked.filter(m => m.state === "no").length;
  const nSk = marked.filter(m => m.state === "sk").length;
  const max = paper.length * M_OK;
  const pct = Math.round((nOk / paper.length) * 100);

  const byDom = {};
  marked.forEach(m => {
    const d = m.it.src.domainName;
    byDom[d] = byDom[d] || { ok: 0, n: 0 };
    byDom[d].n++; if (m.state === "ok") byDom[d].ok++;
  });

  const label = { ok: "Correct", no: "Incorrect", sk: "Skipped" };
  const when = new Date().toLocaleString();

  return `
  <h1>${total} out of ${max}</h1>
  <p class="lede">${paper.endReason === "time"
      ? "Time ran out and the paper submitted itself. Questions you never reached are marked as skipped."
      : "Paper submitted."} Attempted ${nOk + nNo} of ${paper.length}, ${pct}% of the paper answered correctly.</p>

  <div class="score">
    <div><div class="big">${total}<em> / ${max}</em></div></div>
    <div class="tally">
      <div class="c"><span>${nOk}</span>correct &nbsp;(${nOk * M_OK >= 0 ? "+" : ""}${nOk * M_OK})</div>
      <div class="w"><span>${nNo}</span>incorrect &nbsp;(${nNo * M_NO})</div>
      <div class="s"><span>${nSk}</span>skipped &nbsp;(${nSk * M_SK})</div>
    </div>
  </div>

  <h2>By domain</h2>
  <dl class="dstat">
    ${Object.entries(byDom).map(([d, v]) => `<div><dt>${esc(d)}</dt><dd>${v.ok} / ${v.n} correct</dd></div>`).join("")}
  </dl>

  <div class="row noprint">
    <button class="btn primary" id="pdf">Download as PDF</button>
    <button class="btn" id="again">Take a fresh paper</button>
    <a class="btn" href="agent-skills-study-app.html">Back to the study app</a>
  </div>
  <p class="hint noprint" id="pdfnote">Opens your browser's print dialogue — choose <em>Save as PDF</em> as the
  destination. The score and the full review are included; the buttons are not.</p>

  <h2>Full review</h2>
  <p style="font-size:13.5px;color:var(--lead);margin:0 0 18px">Attempted ${when}. Every question you saw, what you
  chose, what was correct, and why the closest wrong option fails.</p>

  ${marked.map((m, i) => {
    const it = m.it, q = it.src;
    const given = it.given ? it.shown.find(o => o.slot === it.given) : null;
    const corr = it.shown.find(o => o.slot === it.correctSlot);
    return `
    <div class="item ${m.state}">
      <div class="h"><b>${esc(q.id)}</b><span>Q${i+1}</span><span>·</span><span>${esc(q.domainName)}</span>
        <span>·</span><span class="v">${label[m.state]} (${m.mark >= 0 ? "+" : ""}${m.mark})</span></div>
      <p class="qq">${md(q.q)}</p>
      <p class="ans"><i>Your answer</i>${given ? esc(given.slot) + " — " + md(given.text) : "<em>not answered</em>"}</p>
      ${m.state === "ok" ? "" : `<p class="ans"><i>Correct answer</i>${esc(corr.slot)} — ${md(corr.text)}</p>`}
      <div class="why">
        <p><b>Why</b>${md(q.rationale)}</p>
        <p><b>The near-miss</b>${md(q.trap)}</p>
      </div>
    </div>`;
  }).join("")}`;
}

/* ---------------- PDF ----------------
   A preview pane runs this file inside a sandboxed iframe, where printing is
   blocked. Three tiers: print directly when we are the top-level page; else
   hand over a standalone printable file; else open one in a new tab.          */
function printableHtml(){
  const css = document.querySelector("style").textContent;
  const node = $("#app").cloneNode(true);
  node.querySelectorAll(".noprint").forEach(n => n.remove());
  return "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
    + "<title>Agent Skills quiz — result</title><style>" + css + "</style></head>"
    + "<body><div class=\"shell\">" + node.innerHTML + "</div>"
    + "<scr" + "ipt>window.addEventListener('load',function(){setTimeout(function(){window.print();},350);});</scr" + "ipt>"
    + "</body></html>";
}
function note(msg){ const n = $("#pdfnote"); if (n) n.innerHTML = msg; }
function savePdf(){
  const framed = (() => { try { return window.self !== window.top; } catch (e) { return true; } })();
  if (!framed) {
    try { window.print(); return; } catch (e) { /* fall through */ }
  }
  try {
    const blob = new Blob([printableHtml()], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "agent-skills-quiz-result.html";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    note("A printable results file was downloaded. Open it in your browser — it opens the print dialogue itself, "
       + "and you choose <em>Save as PDF</em>. Preview panes block printing directly, so this is the way round it.");
    return;
  } catch (e) { /* fall through */ }
  try {
    const w = window.open("", "_blank");
    if (w) { w.document.write(printableHtml()); w.document.close(); return; }
  } catch (e) { /* fall through */ }
  note("This preview blocks both printing and downloads. Open <code>agent-skills-quiz.html</code> directly in a "
     + "browser and the PDF button works normally.");
}

/* ---------------- render ---------------- */
function render(){
  const app = $("#app");
  if (phase === "intro") {
    app.innerHTML = intro();
    $("#go").onclick = () => { phase = "quiz"; idx = 0; sel = null; render(); startClock(); };
    $("#reshuffle").onclick = () => { paper = drawPaper(); render(); };
  } else if (phase === "quiz") {
    app.innerHTML = question(); bindQuestion();
    window.scrollTo(0, 0);
  } else {
    app.innerHTML = results();
    $("#pdf").onclick = savePdf;
    $("#again").onclick = () => { paper = drawPaper(); idx = 0; left = SECS; sel = null; phase = "intro"; render(); };
    window.scrollTo(0, 0);
  }
}

window.addEventListener("beforeunload", e => { if (phase === "quiz") { e.preventDefault(); e.returnValue = ""; } });
render();
</script>
</body>
</html>
"""

HTML.write_text(TPL.replace("__DATA__", json.dumps(DATA, ensure_ascii=False)), encoding="utf-8")
print("app written:", HTML.name, HTML.stat().st_size, "bytes")
