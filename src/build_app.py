#!/usr/bin/env python3
"""Assemble the single-file interactive study app."""
import json, pathlib, sys
import os
OUT = os.environ.get("BUNDLE_OUT", "/mnt/user-data/outputs")   # repo root when run from src/

sys.path.insert(0, "/home/claude")

from content_modules_a import MODULES_A
from content_modules_b import MODULES_B
from content_cards import FLASHCARDS, GLOSSARY
from content_quiz import QUIZ
from content_shortnotes import SHORT_NOTES

MODULES = MODULES_A + MODULES_B

import base64
FIG_DIR = pathlib.Path(__file__).resolve().parent / "figures"
FIGS = {}
for blk in (b for sec in SHORT_NOTES for b in sec["blocks"] if b["type"] == "fig"):
    f = FIG_DIR / blk["file"]
    if not f.exists():
        raise SystemExit(f"missing figure: {f}")
    FIGS[blk["file"]] = "data:image/jpeg;base64," + base64.b64encode(f.read_bytes()).decode()

DATA = {
    "modules": MODULES,
    "shortnotes": SHORT_NOTES,
    "figs": FIGS,
    "cards": [{"module": m, "front": f, "back": b, "tag": t} for (m, f, b, t) in FLASHCARDS],
    "quiz": QUIZ,
    "glossary": [{"term": t, "def": d} for (t, d) in GLOSSARY],
}

diagrams_js = pathlib.Path("/home/claude/diagrams.js").read_text()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Skills with Anthropic — Study Bundle</title>
<style>
:root{
  --blue:#1A3FD6; --smokey:#0626A9; --sky:#7188EF; --powder:#AEBAF0; --ice:#F4F5FD;
  --gold:#DB7C00; --gold-t:#A35C00; --green:#118A5E; --red:#E02C1C;
  --charcoal:#4D4D4D; --lead:#707070; --flint:#999; --smoke:#CCC; --silver:#E6E6E6; --dove:#F5F5F5;
  --ink:#111318; --bg:#FFFFFF;
  --sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  --rail: 274px;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  font-family:var(--sans); color:var(--ink); background:var(--bg);
  font-size:15.5px; line-height:1.62; -webkit-font-smoothing:antialiased;
}
a{color:var(--blue)}
code{font-family:var(--mono); font-size:.86em; background:var(--ice); padding:.1em .34em; border-radius:2px; color:var(--smokey)}
strong{font-weight:650}

/* ---------- shell ---------- */
.wrap{display:grid; grid-template-columns:var(--rail) minmax(0,1fr); min-height:100vh}
.rail{
  border-right:1px solid var(--silver); background:var(--dove);
  position:sticky; top:0; height:100vh; overflow-y:auto; padding:22px 0 40px;
}
.brand{padding:0 20px 18px; border-bottom:1px solid var(--silver); margin-bottom:14px}
.brand h1{font-size:16px; line-height:1.3; margin:0 0 4px; font-weight:680; letter-spacing:-.01em}
.brand p{margin:0; font-size:11.5px; color:var(--lead); line-height:1.45}
.modes{display:flex; flex-wrap:wrap; gap:4px; padding:0 14px 16px}
.mode{
  font:inherit; font-size:12.5px; font-weight:550; cursor:pointer;
  border:1px solid var(--silver); background:#fff; color:var(--charcoal);
  padding:5px 10px; border-radius:3px;
}
.mode[aria-current="true"]{background:var(--blue); border-color:var(--blue); color:#fff}
.mode.ext{text-decoration:none; border-style:dashed; color:var(--blue)}
.mode.ext:hover{border-style:solid; background:#fff}
.callout{border-left:3px solid var(--blue); background:var(--ice); padding:16px 20px; margin:24px 0; max-width:74ch}
.callout h4{margin:0 0 6px; font-size:13px; color:var(--smokey); font-weight:650}
.callout p{margin:0 0 10px; font-size:14.6px}
.callout p:last-child{margin:0}
.callout a{font-weight:600}
.railsec{padding:0 14px}
.railsec h2{font-size:11px; color:var(--lead); font-weight:600; margin:14px 6px 8px; letter-spacing:.02em}
.navitem{
  display:grid; grid-template-columns:26px 1fr; gap:8px; width:100%; text-align:left;
  font:inherit; font-size:13px; cursor:pointer; border:0; background:transparent;
  padding:7px 6px; border-radius:3px; color:var(--charcoal); line-height:1.35;
  border-left:2px solid transparent;
}
.navitem:hover{background:#fff}
.navitem[aria-current="true"]{background:#fff; color:var(--ink); font-weight:600; border-left-color:var(--blue)}
.navnum{font-family:var(--mono); font-size:11px; color:var(--flint); padding-top:2px}
.navitem[aria-current="true"] .navnum{color:var(--blue)}

/* ---------- main ---------- */
main{padding:38px 46px 90px; max-width:1000px}
.eyebrow{font-size:12px; color:var(--lead); margin:0 0 10px; display:flex; gap:10px; align-items:center; flex-wrap:wrap}
.pill{border:1px solid var(--silver); border-radius:999px; padding:2px 9px; font-size:11px; color:var(--charcoal); background:var(--dove)}
h2.mt{font-size:29px; line-height:1.18; margin:0 0 16px; font-weight:690; letter-spacing:-.02em; max-width:24ch}
h3{font-size:14px; font-weight:640; margin:38px 0 12px; color:var(--ink)}
h3:first-of-type{margin-top:28px}
.objective{
  border-left:3px solid var(--blue); background:var(--ice);
  padding:14px 18px; margin:0 0 30px; font-size:15px; max-width:74ch;
}
.objective b{display:block; font-size:11.5px; color:var(--smokey); font-weight:650; margin-bottom:3px}
ul.kp{list-style:none; margin:0; padding:0; max-width:78ch}
ul.kp li{position:relative; padding:0 0 11px 20px; font-size:15px}
ul.kp li::before{content:""; position:absolute; left:2px; top:.62em; width:6px; height:6px; background:var(--sky); border-radius:1px}
.prose p{max-width:76ch; margin:0 0 15px}
.gotchas{border:1px solid var(--gold); border-radius:4px; padding:4px 18px 14px; margin:12px 0 0; background:#FFFCF7}
.gotchas h4{font-size:12px; color:var(--gold-t); margin:14px 0 8px; font-weight:650}
.gotchas ul{margin:0; padding-left:18px}
.gotchas li{margin-bottom:8px; font-size:14.4px; max-width:74ch}

/* short notes */
.lede2{font-size:16.5px; color:var(--charcoal); max-width:66ch; margin:0 0 26px}
.snsub{margin:24px 0 6px}
.snsub h4{margin:0 0 8px; font-size:13px; font-weight:650; color:var(--smokey)}
.snfig{margin:24px 0 26px}
.snfig img{width:100%; height:auto; display:block; border:1px solid var(--silver); border-radius:4px; background:#fff}
.snfig figcaption{font-size:12.6px; color:var(--lead); margin-top:8px; max-width:74ch; line-height:1.55}
.figcap{font-size:12.6px; color:var(--lead); margin-top:8px; max-width:74ch}
.figmiss{border:1px dashed var(--smoke); border-radius:4px; padding:26px; text-align:center; color:var(--flint); font-size:13px}
.snnote{border-left:3px solid var(--sky); background:var(--ice); padding:14px 18px; margin:22px 0; font-size:14.8px; max-width:76ch; line-height:1.6}
.railsec p a{color:var(--blue)}

/* spec box */
.spec{display:grid; grid-template-columns:repeat(auto-fill,minmax(232px,1fr)); gap:1px; background:var(--silver); border:1px solid var(--silver); border-radius:3px; overflow:hidden}
.spec div{background:#fff; padding:9px 12px}
.spec dt{font-size:11px; color:var(--lead); margin-bottom:2px}
.spec dd{margin:0; font-family:var(--mono); font-size:12.4px; color:var(--smokey); line-height:1.4}

/* artifacts */
.art{margin:0 0 22px; border:1px solid var(--silver); border-radius:4px; overflow:hidden}
.art header{display:flex; justify-content:space-between; align-items:center; gap:12px; background:var(--dove); border-bottom:1px solid var(--silver); padding:8px 12px}
.art header span{font-size:12.5px; font-weight:600}
.art header em{font-family:var(--mono); font-style:normal; font-size:10.5px; color:var(--lead)}
.art pre{margin:0; padding:14px 16px; overflow-x:auto; background:#fff}
.art code{background:none; padding:0; color:var(--ink); font-size:12.4px; line-height:1.6}
.art footer{padding:9px 14px; border-top:1px solid var(--silver); font-size:13px; color:var(--charcoal); background:#FCFCFD; max-width:none}
.copy{font:inherit; font-size:11px; cursor:pointer; border:1px solid var(--smoke); background:#fff; padding:3px 8px; border-radius:2px; color:var(--charcoal)}
.copy:hover{border-color:var(--blue); color:var(--blue)}

/* diagram */
figure{margin:0 0 30px}
figure svg{width:100%; height:auto; border:1px solid var(--silver); border-radius:4px; background:#fff; display:block}
figcaption{font-size:12.6px; color:var(--lead); margin-top:8px; max-width:70ch}
.d-h{font:600 13px var(--sans); fill:var(--charcoal)}
.d-hw{font:600 13px var(--sans); fill:#fff}
.d-l{font:500 12px var(--sans); fill:var(--ink)}
.d-lw{font:500 12px var(--sans); fill:#fff}
.d-s{font:400 10.6px var(--sans); fill:var(--lead)}
.d-sw{font:400 10.6px var(--sans); fill:#E3E8FB}

.pager{display:flex; justify-content:space-between; gap:12px; margin-top:52px; border-top:1px solid var(--silver); padding-top:18px}
.pager button{font:inherit; font-size:13px; cursor:pointer; background:#fff; border:1px solid var(--silver); border-radius:3px; padding:8px 14px; color:var(--charcoal); max-width:46%; text-align:left}
.pager button:hover:not(:disabled){border-color:var(--blue); color:var(--blue)}
.pager button:disabled{opacity:.4; cursor:default}
.pager small{display:block; font-size:10.5px; color:var(--flint)}

/* ---------- short notes ---------- */
function snBlock(b){
  if(b.type==='bullets') return `<ul class="kp">${b.items.map(i=>`<li>${md(i)}</li>`).join('')}</ul>`;
  if(b.type==='sub') return `<div class="snsub"><h4>${esc(b.title)}</h4>
    <ul class="kp">${b.items.map(i=>`<li>${md(i)}</li>`).join('')}</ul></div>`;
  if(b.type==='code') return `<div class="art">
    <header><span>Structure</span><em>${esc(b.lang)}</em></header>
    <pre><code>${esc(b.code)}</code></pre>
    ${b.caption?`<footer>${md(b.caption)}</footer>`:''}</div>`;
  if(b.type==='fig'){
    const src = DATA.figs[b.file];
    return `<figure class="snfig">${src?`<img src="${src}" alt="${esc(b.caption||b.file)}" loading="lazy">`
      :`<div class="figmiss">figure ${esc(b.file)} not inlined</div>`}
      ${b.caption?`<figcaption>${md(b.caption)}</figcaption>`:''}</figure>`;
  }
  if(b.type==='table') return `<table class="ref">
    <thead><tr>${b.headers.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead>
    <tbody>${b.rows.map(r=>`<tr>${r.map((c,i)=>`<td${i===0?' style="font-weight:600"':''}>${md(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>
    ${b.caption?`<p class="figcap">${md(b.caption)}</p>`:''}`;
  if(b.type==='note') return `<div class="snnote">${md(b.text)}</div>`;
  return '';
}
function notesView(){
  const sec = DATA.shortnotes[state.sn];
  const prev = DATA.shortnotes[state.sn-1], next = DATA.shortnotes[state.sn+1];
  return `
  <p class="eyebrow"><span class="pill">Short notes ${sec.num}</span><span>condensed · figures from the source write-up</span></p>
  <h2 class="mt">${esc(sec.title)}</h2>
  <p class="lede2">${md(sec.blurb)}</p>
  ${sec.blocks.map(snBlock).join('')}
  <div class="pager">
    <button id="snp" ${prev?'':'disabled'}>${prev?`<small>Previous · ${prev.num}</small>${esc(prev.title)}`:'<small>Start</small>—'}</button>
    <button id="snn" ${next?'':'disabled'} style="text-align:right">${next?`<small>Next · ${next.num}</small>${esc(next.title)}`:'<small>End of short notes</small>—'}</button>
  </div>`;
}
function bindNotes(){
  const a=$('#snp'), b=$('#snn');
  if(a) a.onclick=()=>{ if(state.sn>0){state.sn--; render(); window.scrollTo(0,0);} };
  if(b) b.onclick=()=>{ if(state.sn<DATA.shortnotes.length-1){state.sn++; render(); window.scrollTo(0,0);} };
}

/* ---------- flashcards ---------- */
.toolbar{display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:22px; padding-bottom:18px; border-bottom:1px solid var(--silver)}
select,.btn{font:inherit; font-size:13px; padding:6px 11px; border:1px solid var(--silver); border-radius:3px; background:#fff; color:var(--charcoal); cursor:pointer}
.btn.primary{background:var(--blue); border-color:var(--blue); color:#fff; font-weight:550}
.btn:hover{border-color:var(--blue)}
.counter{font-family:var(--mono); font-size:12px; color:var(--lead); margin-left:auto}
.card{
  border:1px solid var(--silver); border-radius:5px; min-height:270px; padding:34px 38px;
  display:flex; flex-direction:column; justify-content:center; cursor:pointer; background:#fff;
  position:relative;
}
.card:hover{border-color:var(--powder)}
.card .side{font-size:11px; color:var(--flint); position:absolute; top:12px; left:16px; font-family:var(--mono)}
.card .tagp{position:absolute; top:10px; right:16px}
.card .q{font-size:22px; line-height:1.34; font-weight:600; max-width:34ch; letter-spacing:-.01em}
.card .a{font-size:16.5px; line-height:1.6; max-width:52ch}
.card.flipped{background:var(--ice); border-color:var(--powder)}
.cardnav{display:flex; gap:10px; margin-top:16px; align-items:center; flex-wrap:wrap}
.hintline{font-size:12px; color:var(--flint); margin-top:14px}

/* ---------- quiz ---------- */
.qhead{display:flex; justify-content:space-between; align-items:baseline; gap:14px; margin-bottom:6px}
.qhead .qn{font-family:var(--mono); font-size:12px; color:var(--lead)}
.qtext{font-size:19.5px; line-height:1.42; font-weight:600; margin:6px 0 20px; max-width:62ch; letter-spacing:-.01em}
.opts{display:flex; flex-direction:column; gap:8px; max-width:62ch}
.opt{font:inherit; font-size:14.6px; text-align:left; cursor:pointer; padding:11px 14px; border:1px solid var(--silver); border-radius:3px; background:#fff; line-height:1.45}
.opt:hover:not(:disabled){border-color:var(--blue)}
.opt:disabled{cursor:default}
.opt.correct{border-color:var(--green); background:#F2FAF6; font-weight:550}
.opt.wrong{border-color:var(--red); background:#FEF4F2}
.verdict{margin:20px 0 0; padding:14px 18px; border-radius:4px; border-left:3px solid var(--blue); background:var(--ice); max-width:74ch}
.verdict h5{margin:0 0 6px; font-size:12px; color:var(--smokey); font-weight:650}
.verdict p{margin:0 0 10px; font-size:14.6px; line-height:1.58}
.verdict p:last-child{margin:0}
.model{border:1px dashed var(--powder); border-radius:4px; padding:14px 18px; margin:18px 0 0; background:#FCFDFF; max-width:74ch}
.model h5{margin:0 0 6px; font-size:12px; color:var(--smokey); font-weight:650}
.selfgrade{display:flex; gap:8px; margin-top:14px; flex-wrap:wrap}
.score{font-family:var(--mono); font-size:12px; color:var(--lead)}
.bar{height:3px; background:var(--silver); border-radius:2px; overflow:hidden; margin:18px 0 26px}
.bar i{display:block; height:100%; background:var(--blue); transition:width .25s}
.result{border:1px solid var(--silver); border-radius:5px; padding:26px 30px; margin-bottom:24px}
.result .big{font-size:42px; font-weight:700; letter-spacing:-.03em; line-height:1}
.result .big span{font-size:18px; color:var(--lead); font-weight:500}
table.rev{width:100%; border-collapse:collapse; font-size:13.4px; margin-top:8px}
table.rev th{text-align:left; font-size:11px; color:var(--lead); font-weight:600; padding:7px 10px; background:var(--dove); border-bottom:1px solid var(--silver)}
table.rev td{padding:8px 10px; border-bottom:1px solid var(--silver); vertical-align:top}
table.rev tr:nth-child(even) td{background:var(--dove)}
.tick{color:var(--green); font-weight:650}
.cross{color:var(--red); font-weight:650}

/* ---------- reference ---------- */
table.ref{width:100%; border-collapse:collapse; font-size:13.6px}
table.ref th{text-align:left; font-size:11px; color:var(--lead); font-weight:600; padding:8px 10px; background:var(--dove); border-bottom:1px solid var(--silver); position:sticky; top:0}
table.ref td{padding:8px 10px; border-bottom:1px solid var(--silver); vertical-align:top}
table.ref td.k{font-family:var(--mono); font-size:12.4px; color:var(--smokey); white-space:nowrap}
table.ref td.m{font-family:var(--mono); font-size:12.4px}
.gl dt{font-weight:640; font-size:14.6px; margin-top:16px}
.gl dd{margin:3px 0 0; color:var(--charcoal); max-width:76ch; font-size:14.4px}

@media (max-width:900px){
  .wrap{grid-template-columns:1fr}
  .rail{position:static; height:auto; border-right:0; border-bottom:1px solid var(--silver)}
  main{padding:26px 20px 70px}
  h2.mt{font-size:24px}
  .card{padding:26px 22px; min-height:230px}
  .card .q{font-size:19px}
}
@media (prefers-reduced-motion:reduce){*{transition:none !important}}
:focus-visible{outline:2px solid var(--blue); outline-offset:2px}
</style>
</head>
<body>
<div class="wrap">
  <aside class="rail">
    <div class="brand">
      <h1>Agent Skills with Anthropic</h1>
      <p>Course study bundle — 14 modules, __NCARDS__ flashcards, __NQUIZ__ assessment items</p>
    </div>
    <div class="modes" role="tablist">
      <button class="mode" data-mode="study" aria-current="true">Study</button>
      <button class="mode" data-mode="notes">Short notes</button>
      <button class="mode" data-mode="cards">Flashcards</button>
      <button class="mode" data-mode="quiz">Quiz</button>
      <button class="mode" data-mode="ref">Reference</button>
      <a class="mode ext" href="agent-skills-quiz.html" target="_blank" rel="noopener"
         title="Opens the separate 10-minute timed paper">Timed paper</a>
    </div>
    <div class="railsec" id="railbody"></div>
  </aside>
  <main id="main"></main>
</div>

<script>
const DATA = __DATA__;
__DIAGRAMS__

/* ---------- helpers ---------- */
const $ = (s,r=document)=>r.querySelector(s);
const esc = s => String(s).replace(/[&<>]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const md = s => esc(s).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/`([^`]+)`/g,'<code>$1</code>');
const byId = id => DATA.modules.find(m=>m.id===id);
const shuf = a => { for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
const modTitle = id => { const m=byId(id); return m ? m.num+' · '+m.title : id; };

let state = { mode:'study', mod:0, sn:0,
  cards:{ list:[], i:0, flipped:false, known:new Set(), filter:'all' },
  quiz:{ list:[], i:0, answers:[], done:false, fmod:'all', ftype:'all' } };

/* ---------- rail ---------- */
function renderRail(){
  const rb = $('#railbody');
  document.querySelectorAll('.mode').forEach(b=>b.setAttribute('aria-current', String(b.dataset.mode===state.mode)));
  if(state.mode==='study'){
    rb.innerHTML = '<h2>Modules</h2>' + DATA.modules.map((m,i)=>
      `<button class="navitem" data-i="${i}" aria-current="${i===state.mod}">
         <span class="navnum">${m.num}</span><span>${esc(m.title)}</span></button>`).join('');
    rb.querySelectorAll('.navitem').forEach(b=>b.onclick=()=>{ state.mod=+b.dataset.i; render(); window.scrollTo(0,0); });
  } else if(state.mode==='notes'){
    rb.innerHTML = '<h2>Short notes</h2>' + DATA.shortnotes.map((sec,i)=>
      `<button class="navitem" data-sn="${i}" aria-current="${i===state.sn}">
         <span class="navnum">${sec.num}</span><span>${esc(sec.title)}</span></button>`).join('')
      + `<h2>Source</h2><p style="font-size:12.4px;color:var(--lead);padding:0 6px;line-height:1.55">
         Condensed write-up of the course, with the figures from it inlined. Shorter than the
         module notes and in the original lesson order — use it to revise fast, and the
         <a href="#" data-goto="study">Study</a> section when you want the depth.</p>`;
    rb.querySelectorAll('.navitem').forEach(b=>b.onclick=()=>{ state.sn=+b.dataset.sn; render(); window.scrollTo(0,0); });
    const g=rb.querySelector('[data-goto]');
    if(g) g.onclick=e=>{ e.preventDefault(); state.mode='study'; render(); window.scrollTo(0,0); };
  } else if(state.mode==='cards'){
    rb.innerHTML = `<h2>How to use</h2><p style="font-size:12.4px;color:var(--lead);padding:0 6px;line-height:1.55">
      Click the card to flip. Mark <b>Know it</b> to drop it from the deck for this session, or <b>Review</b> to keep it in rotation.
      Filter by module to drill one topic. Progress is kept for this session only.</p>
      <h2>Keyboard</h2><p style="font-size:12.4px;color:var(--lead);padding:0 6px;line-height:1.55">
      <code>space</code> flip · <code>→</code> next · <code>←</code> back · <code>k</code> know it</p>`;
  } else if(state.mode==='quiz'){
    rb.innerHTML = `<h2>Format</h2><p style="font-size:12.4px;color:var(--lead);padding:0 6px;line-height:1.55">
      Multiple choice and true/false are graded automatically. Short-answer and applied items show a model answer you grade yourself —
      those are the ones worth writing out before revealing.</p>
      <h2>Difficulty</h2><p style="font-size:12.4px;color:var(--lead);padding:0 6px;line-height:1.55">
      1 recall · 2 apply · 3 judgement</p>
      <h2>Timed paper</h2><p style="font-size:12.4px;color:var(--lead);padding:0 6px;line-height:1.55">
      For the graded version — 20 questions, 10 minutes, negative marking — use
      <a href="agent-skills-quiz.html" target="_blank" rel="noopener">the timed paper</a>.</p>`;
  } else {
    rb.innerHTML = `<h2>Reference</h2><p style="font-size:12.4px;color:var(--lead);padding:0 6px;line-height:1.55">
      Every hard limit, path and API string from the course in one table, then the glossary and the full gotcha index.</p>`;
  }
}

/* ---------- study ---------- */
function studyView(){
  const m = DATA.modules[state.mod];
  const dg = DIAGRAMS[m.visual];
  const prev = DATA.modules[state.mod-1], next = DATA.modules[state.mod+1];
  return `
  <p class="eyebrow"><span class="pill">Module ${m.num}</span><span>${esc(m.lesson)}</span><span>·</span><span>${m.duration_min} min</span></p>
  <h2 class="mt">${esc(m.title)}</h2>
  <div class="objective"><b>What you should be able to do after this</b>${md(m.objective)}</div>

  <h3>Key points</h3>
  <ul class="kp">${m.key_points.map(k=>`<li>${md(k)}</li>`).join('')}</ul>

  ${dg?`<h3>${esc(dg.title)}</h3><figure>${dg.svg}<figcaption>${esc(dg.caption)}</figcaption></figure>`:''}

  <h3>Reference facts</h3>
  <dl class="spec">${m.spec_box.map(([k,v])=>`<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>

  <h3>In depth</h3>
  <div class="prose">${m.deep_dive.map(p=>`<p>${md(p)}</p>`).join('')}</div>

  ${m.artifacts.length?`<h3>Artifacts</h3>`+m.artifacts.map((a,i)=>`
    <div class="art">
      <header><span>${esc(a.title)}</span><em>${esc(a.lang)}</em>
        <button class="copy" data-art="${state.mod}-${i}">Copy</button></header>
      <pre><code id="art-${state.mod}-${i}">${esc(a.code)}</code></pre>
      <footer>${md(a.caption)}</footer>
    </div>`).join(''):''}

  <div class="gotchas"><h4>Gotchas</h4><ul>${m.gotchas.map(g=>`<li>${md(g)}</li>`).join('')}</ul></div>

  <div class="pager">
    <button id="pv" ${prev?'':'disabled'}>${prev?`<small>Previous · ${prev.num}</small>${esc(prev.title)}`:'<small>Start of course</small>—'}</button>
    <button id="nx" ${next?'':'disabled'} style="text-align:right">${next?`<small>Next · ${next.num}</small>${esc(next.title)}`:'<small>End of course</small>—'}</button>
  </div>`;
}
function bindStudy(){
  const pv=$('#pv'), nx=$('#nx');
  if(pv) pv.onclick=()=>{ if(state.mod>0){state.mod--; render(); window.scrollTo(0,0);} };
  if(nx) nx.onclick=()=>{ if(state.mod<DATA.modules.length-1){state.mod++; render(); window.scrollTo(0,0);} };
  document.querySelectorAll('.copy').forEach(b=>b.onclick=async()=>{
    const t = $('#art-'+b.dataset.art).textContent;
    try{ await navigator.clipboard.writeText(t); b.textContent='Copied'; }
    catch(e){ b.textContent='Select and copy'; }
    setTimeout(()=>b.textContent='Copy', 1600);
  });
}

/* ---------- short notes ---------- */
function snBlock(b){
  if(b.type==='bullets') return `<ul class="kp">${b.items.map(i=>`<li>${md(i)}</li>`).join('')}</ul>`;
  if(b.type==='sub') return `<div class="snsub"><h4>${esc(b.title)}</h4>
    <ul class="kp">${b.items.map(i=>`<li>${md(i)}</li>`).join('')}</ul></div>`;
  if(b.type==='code') return `<div class="art">
    <header><span>Structure</span><em>${esc(b.lang)}</em></header>
    <pre><code>${esc(b.code)}</code></pre>
    ${b.caption?`<footer>${md(b.caption)}</footer>`:''}</div>`;
  if(b.type==='fig'){
    const src = DATA.figs[b.file];
    return `<figure class="snfig">${src?`<img src="${src}" alt="${esc(b.caption||b.file)}" loading="lazy">`
      :`<div class="figmiss">figure ${esc(b.file)} not inlined</div>`}
      ${b.caption?`<figcaption>${md(b.caption)}</figcaption>`:''}</figure>`;
  }
  if(b.type==='table') return `<table class="ref">
    <thead><tr>${b.headers.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead>
    <tbody>${b.rows.map(r=>`<tr>${r.map((c,i)=>`<td${i===0?' style="font-weight:600"':''}>${md(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>
    ${b.caption?`<p class="figcap">${md(b.caption)}</p>`:''}`;
  if(b.type==='note') return `<div class="snnote">${md(b.text)}</div>`;
  return '';
}
function notesView(){
  const sec = DATA.shortnotes[state.sn];
  const prev = DATA.shortnotes[state.sn-1], next = DATA.shortnotes[state.sn+1];
  return `
  <p class="eyebrow"><span class="pill">Short notes ${sec.num}</span><span>condensed · figures from the source write-up</span></p>
  <h2 class="mt">${esc(sec.title)}</h2>
  <p class="lede2">${md(sec.blurb)}</p>
  ${sec.blocks.map(snBlock).join('')}
  <div class="pager">
    <button id="snp" ${prev?'':'disabled'}>${prev?`<small>Previous · ${prev.num}</small>${esc(prev.title)}`:'<small>Start</small>—'}</button>
    <button id="snn" ${next?'':'disabled'} style="text-align:right">${next?`<small>Next · ${next.num}</small>${esc(next.title)}`:'<small>End of short notes</small>—'}</button>
  </div>`;
}
function bindNotes(){
  const a=$('#snp'), b=$('#snn');
  if(a) a.onclick=()=>{ if(state.sn>0){state.sn--; render(); window.scrollTo(0,0);} };
  if(b) b.onclick=()=>{ if(state.sn<DATA.shortnotes.length-1){state.sn++; render(); window.scrollTo(0,0);} };
}

/* ---------- flashcards ---------- */
function cardDeck(){
  const f = state.cards.filter;
  return DATA.cards.filter(c=>f==='all'||c.module===f);
}
function cardsView(){
  const c = state.cards;
  if(!c.list.length){ c.list = cardDeck().map((x,i)=>i); c.i=0; }
  const deck = cardDeck();
  const live = c.list.filter(i=>!c.known.has(deck[i].front));
  if(!live.length){
    return `<p class="eyebrow"><span class="pill">Flashcards</span></p><h2 class="mt">Deck clear</h2>
      <p class="prose" style="max-width:60ch">You marked every card in this selection as known. Reset the deck, or switch filter to drill another module.</p>
      <div class="cardnav"><button class="btn primary" id="reset">Reset deck</button></div>` + filterBar(true);
  }
  if(c.i>=live.length) c.i = 0;
  const card = deck[live[c.i]];
  const pct = Math.round((c.known.size/deck.length)*100);
  return filterBar() + `
    <div class="bar"><i style="width:${pct}%"></i></div>
    <div class="card ${c.flipped?'flipped':''}" id="card" tabindex="0" role="button" aria-label="Flashcard, click to flip">
      <span class="side">${c.flipped?'answer':'prompt'} · ${c.i+1} / ${live.length}</span>
      <span class="tagp pill">${esc(modTitle(card.module).split(' · ')[0])} ${esc(card.tag)}</span>
      ${c.flipped?`<div class="a">${md(card.back)}</div>`:`<div class="q">${md(card.front)}</div>`}
    </div>
    <div class="cardnav">
      <button class="btn" id="back">Back</button>
      <button class="btn primary" id="flip">${c.flipped?'Hide answer':'Show answer'}</button>
      <button class="btn" id="next">Next</button>
      <button class="btn" id="know">Know it</button>
      <span class="counter">${c.known.size} known / ${deck.length} in deck</span>
    </div>
    <p class="hintline">${esc(modTitle(card.module))}</p>`;
}
function filterBar(plain){
  const mods = [...new Set(DATA.cards.map(c=>c.module))];
  return `<p class="eyebrow"><span class="pill">Flashcards</span><span>rehearse until the answer arrives before you finish reading the prompt</span></p>
  ${plain?'':'<h2 class="mt">Recall drill</h2>'}
  <div class="toolbar">
    <label style="font-size:12px;color:var(--lead)">Module</label>
    <select id="cf"><option value="all">All modules</option>
      ${mods.map(m=>`<option value="${m}" ${state.cards.filter===m?'selected':''}>${esc(modTitle(m))}</option>`).join('')}</select>
    <button class="btn" id="shuffle">Shuffle</button>
    <button class="btn" id="reset">Reset progress</button>
  </div>`;
}
function bindCards(){
  const c = state.cards;
  const cf=$('#cf'); if(cf) cf.onchange=()=>{ c.filter=cf.value; c.list=[]; c.i=0; c.flipped=false; render(); };
  const sh=$('#shuffle'); if(sh) sh.onclick=()=>{ c.list=shuf(cardDeck().map((x,i)=>i)); c.i=0; c.flipped=false; render(); };
  const rs=$('#reset'); if(rs) rs.onclick=()=>{ c.known=new Set(); c.list=[]; c.i=0; c.flipped=false; render(); };
  const flip=()=>{ c.flipped=!c.flipped; render(); };
  const card=$('#card'); if(card){ card.onclick=flip; card.onkeydown=e=>{ if(e.key===' '||e.key==='Enter'){e.preventDefault(); flip();} }; card.focus({preventScroll:true}); }
  const fb=$('#flip'); if(fb) fb.onclick=flip;
  const nb=$('#next'); if(nb) nb.onclick=()=>{ c.i++; c.flipped=false; render(); };
  const bb=$('#back'); if(bb) bb.onclick=()=>{ c.i=Math.max(0,c.i-1); c.flipped=false; render(); };
  const kb=$('#know'); if(kb) kb.onclick=()=>{
    const deck=cardDeck(); const live=c.list.filter(i=>!c.known.has(deck[i].front));
    if(live.length) c.known.add(deck[live[c.i]].front);
    c.flipped=false; render();
  };
}

/* ---------- quiz ---------- */
function quizPool(){
  return DATA.quiz.filter(q=>(state.quiz.fmod==='all'||q.module===state.quiz.fmod)
                          && (state.quiz.ftype==='all'||q.type===state.quiz.ftype));
}
function quizView(){
  const q = state.quiz;
  if(!q.list.length){
    const mods=[...new Set(DATA.quiz.map(x=>x.module))];
    return `<p class="eyebrow"><span class="pill">Assessment</span><span>${DATA.quiz.length} items</span></p>
    <h2 class="mt">Test what actually stuck</h2>
    <div class="prose"><p>Pick a scope and start. Multiple-choice and true/false are graded for you; short-answer and applied
    items reveal a model answer and rationale for you to grade yourself. Write your answer down before revealing — recognising
    a good answer is much easier than producing one.</p></div>
    <div class="callout">
      <h4>Looking for the timed test instead?</h4>
      <p>This section is open-ended practice: no clock, no penalty, revisit anything. The separate
      <strong>timed paper</strong> is the assessment — 20 questions drawn from a bank of 48 in 10 minutes,
      +1 for a correct answer and &minus;1 for a wrong one, one question at a time with no going back.</p>
      <p><a href="agent-skills-quiz.html" target="_blank" rel="noopener">Open the timed paper</a>
      &nbsp;·&nbsp; both files need to sit in the same folder for the link to work.</p>
    </div>
    <div class="toolbar">
      <label style="font-size:12px;color:var(--lead)">Module</label>
      <select id="qm"><option value="all">All modules</option>
        ${mods.map(m=>`<option value="${m}" ${q.fmod===m?'selected':''}>${esc(modTitle(m))}</option>`).join('')}</select>
      <label style="font-size:12px;color:var(--lead)">Type</label>
      <select id="qt">
        <option value="all">All types</option>
        <option value="mcq" ${q.ftype==='mcq'?'selected':''}>Multiple choice</option>
        <option value="tf" ${q.ftype==='tf'?'selected':''}>True / false</option>
        <option value="short" ${q.ftype==='short'?'selected':''}>Short answer</option>
        <option value="applied" ${q.ftype==='applied'?'selected':''}>Applied scenario</option>
      </select>
      <button class="btn primary" id="start">Start — ${quizPool().length} items</button>
    </div>`;
  }
  if(q.done) return quizResult();
  const item = q.list[q.i];
  const ans = q.answers[q.i];
  const pct = Math.round((q.i/q.list.length)*100);
  let body='';
  if(item.type==='mcq'||item.type==='tf'){
    const opts = item.type==='tf' ? ['True','False'] : item.options;
    body = `<div class="opts">${opts.map(o=>{
      let cls=''; if(ans){ if(o===item.answer) cls='correct'; else if(o===ans.given) cls='wrong'; }
      return `<button class="opt ${cls}" data-o="${esc(o)}" ${ans?'disabled':''}>${md(o)}</button>`;
    }).join('')}</div>`;
    if(ans) body += `<div class="verdict"><h5>${ans.correct?'Correct':'Not quite — the answer is: '+esc(item.answer)}</h5><p>${md(item.rationale)}</p></div>`;
  } else {
    if(!ans) body = `<div class="prose"><p style="color:var(--lead)">Write your answer, then reveal the model answer and grade yourself honestly.</p></div>
      <button class="btn primary" id="reveal">Reveal model answer</button>`;
    else body = `<div class="model"><h5>Model answer</h5><p>${md(item.answer)}</p></div>
      <div class="verdict"><h5>Why this matters</h5><p>${md(item.rationale)}</p></div>
      ${ans.given===null?`<div class="selfgrade">
        <button class="btn" data-g="1">I had this</button>
        <button class="btn" data-g="0">I missed it</button></div>`:''}`;
  }
  return `<p class="eyebrow"><span class="pill">${item.type==='mcq'?'Multiple choice':item.type==='tf'?'True / false':item.type==='short'?'Short answer':'Applied'}</span>
    <span>${esc(modTitle(item.module))}</span><span>·</span><span>difficulty ${item.difficulty}</span></p>
  <div class="bar"><i style="width:${pct}%"></i></div>
  <div class="qhead"><span class="qn">${item.id} — ${q.i+1} of ${q.list.length}</span>
    <span class="score">${q.answers.filter(a=>a&&a.correct).length} correct so far</span></div>
  <p class="qtext">${md(item.q)}</p>
  ${body}
  <div class="pager">
    <button id="qp" ${q.i?'':'disabled'}><small>Previous</small>Back one item</button>
    <button id="qn" style="text-align:right" ${ans?'':'disabled'}><small>${q.i===q.list.length-1?'Finish':'Next'}</small>${q.i===q.list.length-1?'See results':'Next item'}</button>
  </div>`;
}
function quizResult(){
  const q=state.quiz;
  const auto = q.list.map((it,i)=>({it,a:q.answers[i]})).filter(x=>x.a && x.a.given!==null);
  const got = auto.filter(x=>x.a.correct).length;
  const pct = auto.length?Math.round(got/auto.length*100):0;
  const weak = {};
  auto.filter(x=>!x.a.correct).forEach(x=>{ weak[x.it.module]=(weak[x.it.module]||0)+1; });
  const weakList = Object.entries(weak).sort((a,b)=>b[1]-a[1]);
  return `<p class="eyebrow"><span class="pill">Results</span></p>
  <h2 class="mt">${pct}% on graded items</h2>
  <div class="result"><div class="big">${got}<span> / ${auto.length} graded</span></div>
    <p class="prose" style="margin:12px 0 0">${q.list.length-auto.length} item(s) left ungraded.
    ${weakList.length?'Weakest areas below — revisit those modules before re-running.':'No graded misses in this run.'}</p></div>
  ${weakList.length?`<h3>Where to go back</h3><ul class="kp">${weakList.map(([m,n])=>`<li>${esc(modTitle(m))} — ${n} missed</li>`).join('')}</ul>`:''}
  <h3>Item review</h3>
  <table class="rev"><thead><tr><th>#</th><th>Item</th><th>Module</th><th>Result</th></tr></thead><tbody>
  ${q.list.map((it,i)=>{ const a=q.answers[i];
    const r = !a ? '<span style="color:var(--flint)">skipped</span>'
      : a.given===null ? '<span style="color:var(--flint)">self-graded, unmarked</span>'
      : a.correct ? '<span class="tick">correct</span>' : '<span class="cross">missed</span>';
    return `<tr><td class="m">${it.id}</td><td>${esc(it.q.slice(0,96))}${it.q.length>96?'…':''}</td><td>${esc(modTitle(it.module).split(' · ')[0])}</td><td>${r}</td></tr>`;
  }).join('')}</tbody></table>
  <div class="pager"><button id="again"><small>Restart</small>Run a new set</button><span></span></div>`;
}
function bindQuiz(){
  const q=state.quiz;
  const qm=$('#qm'); if(qm) qm.onchange=()=>{ q.fmod=qm.value; render(); };
  const qt=$('#qt'); if(qt) qt.onchange=()=>{ q.ftype=qt.value; render(); };
  const st=$('#start'); if(st) st.onclick=()=>{
    // copy each item and shuffle its options — the answer is stored as the option
    // text, so grading is unaffected and the correct one stops sitting in one place
    q.list = shuf(quizPool().map(it => it.type === 'mcq'
      ? Object.assign({}, it, { options: shuf(it.options.slice()) })
      : Object.assign({}, it)));
    q.answers = new Array(q.list.length).fill(null); q.i=0; q.done=false; render();
  };
  document.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{
    const item=q.list[q.i], given=b.dataset.o;
    q.answers[q.i]={given, correct:given===item.answer}; render();
  });
  const rv=$('#reveal'); if(rv) rv.onclick=()=>{ q.answers[q.i]={given:null, correct:false}; render(); };
  document.querySelectorAll('[data-g]').forEach(b=>b.onclick=()=>{
    q.answers[q.i]={given:'self', correct:b.dataset.g==='1'}; render();
  });
  const qp=$('#qp'); if(qp) qp.onclick=()=>{ q.i=Math.max(0,q.i-1); render(); window.scrollTo(0,0); };
  const qn=$('#qn'); if(qn) qn.onclick=()=>{
    if(q.i===q.list.length-1){ q.done=true; } else { q.i++; }
    render(); window.scrollTo(0,0);
  };
  const ag=$('#again'); if(ag) ag.onclick=()=>{ q.list=[]; q.answers=[]; q.i=0; q.done=false; render(); };
}

/* ---------- reference ---------- */
function refView(){
  const rows=[]; DATA.modules.forEach(m=>m.spec_box.forEach(([k,v])=>rows.push([m.num,k,v])));
  const gotchas=[]; DATA.modules.forEach(m=>m.gotchas.forEach(g=>gotchas.push([m,g])));
  return `<p class="eyebrow"><span class="pill">Reference</span><span>${rows.length} facts · ${DATA.glossary.length} terms · ${gotchas.length} gotchas</span></p>
  <h2 class="mt">Everything worth looking up twice</h2>
  <h3>Limits, paths and API strings</h3>
  <table class="ref"><thead><tr><th>Mod</th><th>Fact</th><th>Value</th></tr></thead><tbody>
  ${rows.map(([n,k,v])=>`<tr><td class="m">${n}</td><td>${esc(k)}</td><td class="k">${esc(v)}</td></tr>`).join('')}
  </tbody></table>
  <h3>Glossary</h3>
  <dl class="gl">${DATA.glossary.map(g=>`<dt>${esc(g.term)}</dt><dd>${md(g.def)}</dd>`).join('')}</dl>
  <h3>Gotcha index</h3>
  <table class="ref"><thead><tr><th>Mod</th><th>Gotcha</th></tr></thead><tbody>
  ${gotchas.map(([m,g])=>`<tr><td class="m">${m.num}</td><td>${md(g)}</td></tr>`).join('')}
  </tbody></table>`;
}

/* ---------- render ---------- */
function render(){
  renderRail();
  const el=$('#main');
  if(state.mode==='study'){ el.innerHTML=studyView(); bindStudy(); }
  else if(state.mode==='notes'){ el.innerHTML=notesView(); bindNotes(); }
  else if(state.mode==='cards'){ el.innerHTML=cardsView(); bindCards(); }
  else if(state.mode==='quiz'){ el.innerHTML=quizView(); bindQuiz(); }
  else { el.innerHTML=refView(); }
}
document.querySelectorAll('.mode').forEach(b=>b.onclick=()=>{ state.mode=b.dataset.mode; render(); window.scrollTo(0,0); });
document.addEventListener('keydown', e=>{
  if(state.mode!=='cards') return;
  const tag=(e.target.tagName||'').toLowerCase(); if(tag==='select'||tag==='input') return;
  if(e.key==='ArrowRight'){ const b=$('#next'); if(b) b.click(); }
  if(e.key==='ArrowLeft'){ const b=$('#back'); if(b) b.click(); }
  if(e.key.toLowerCase()==='k'){ const b=$('#know'); if(b) b.click(); }
});
render();
</script>
</body>
</html>
"""

out = (HTML
       .replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
       .replace("__DIAGRAMS__", diagrams_js)
       .replace("__NCARDS__", str(len(DATA["cards"])))
       .replace("__NQUIZ__", str(len(DATA["quiz"]))))

p = pathlib.Path(f"{OUT}/agent-skills-study-app.html")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(out, encoding="utf-8")
print("modules:", len(DATA["modules"]), "cards:", len(DATA["cards"]), "quiz:", len(DATA["quiz"]),
      "glossary:", len(DATA["glossary"]))
print("bytes:", p.stat().st_size)
