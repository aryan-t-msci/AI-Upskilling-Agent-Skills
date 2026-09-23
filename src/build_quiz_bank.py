#!/usr/bin/env python3
"""Write the quiz bank workbook from quiz_bank.py.

Run this to create the workbook, or to reset it after editing the Python source.
It OVERWRITES the xlsx, so do not run it if your edits live in the workbook.
To rebuild only the app from the workbook, run build_quiz_app.py instead.
"""
import sys, json, pathlib
import os
OUT = os.environ.get("BUNDLE_OUT", "/mnt/user-data/outputs")   # repo root when run from src/

sys.path.insert(0, "/home/claude")
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from quiz_bank import QUESTIONS, DOMAINS

# ---- design asserts: fail the build rather than ship an unbalanced bank ----
def _counts(key):
    d = {}
    for q in QUESTIONS:
        d[q[key]] = d.get(q[key], 0) + 1
    return d

_dom, _dif, _kind = _counts("domain"), _counts("difficulty"), _counts("kind")
assert len(set(_dom.values())) == 1, f"uneven questions per domain: {_dom}"
assert len(set(_dif.values())) == 1, f"uneven questions per difficulty: {_dif}"
for _d in DOMAINS:
    _sub = _counts_d = {}
    for q in QUESTIONS:
        if q["domain"] == _d:
            _sub[q["difficulty"]] = _sub.get(q["difficulty"], 0) + 1
    assert len(set(_sub.values())) == 1, f"{_d} uneven across difficulty: {_sub}"
    _ap = sum(1 for q in QUESTIONS if q["domain"] == _d and q["kind"] == "applied")
    _rc = sum(1 for q in QUESTIONS if q["domain"] == _d and q["kind"] == "recall")
    assert _ap >= 4 and _rc >= 1, f"{_d} cannot support a 4-applied + 1-recall draw: {_ap}/{_rc}"
# Spread the correct answer across A-D. Authoring puts the right answer first,
# which is convenient to write and useless to sit. Round-robin over list order is
# deterministic, so rebuilds are identical, and perfectly even by construction.
# Safe to do because no rationale or distractor note refers to an option letter.
_LET = "ABCD"
for _i, _q in enumerate(QUESTIONS):
    _target = _i % 4
    _correct_val = _q["options"][_q["correct"]]
    _others = [_q["options"][L] for L in _LET if L != _q["correct"]]
    _vals = _others[:_target] + [_correct_val] + _others[_target:]
    _q["options"] = dict(zip(_LET, _vals))
    _q["correct"] = _LET[_target]

_ans = _counts("correct")
assert max(_ans.values()) - min(_ans.values()) <= 1, f"uneven correct-answer spread: {_ans}"
for _d in DOMAINS:
    _sub = {}
    for q in QUESTIONS:
        if q["domain"] == _d:
            _sub[q["correct"]] = _sub.get(q["correct"], 0) + 1
    assert max(_sub.values()) - min(_sub.values()) <= 1, f"{_d} uneven correct spread: {_sub}"

_applied_pct = round(100 * _kind.get("applied", 0) / len(QUESTIONS))
assert 75 <= _applied_pct <= 85, f"applied share is {_applied_pct}%, target 80"
print(f"bank checks passed · {len(QUESTIONS)} questions · per domain {_dom} · "
      f"per difficulty {_dif} · {_applied_pct}% applied · correct answer {dict(sorted(_ans.items()))}")

XLSX = pathlib.Path(f"{OUT}/Agent-Skills-Quiz-Bank.xlsx")
HTML = pathlib.Path(f"{OUT}/agent-skills-quiz.html")

CONFIG = [
    ("questions_per_attempt", 20, "How many questions each attempt draws from the bank"),
    ("time_limit_minutes", 10, "Countdown length. The test auto-submits at zero"),
    ("mark_correct", 1, "Marks added for a correct answer"),
    ("mark_incorrect", -1, "Marks deducted for an incorrect answer"),
    ("mark_skipped", 0, "Marks for a skipped or unreached question"),
    ("stratify_by_domain", 1, "1 = draw an equal share from each domain, 0 = draw at random"),
    ("allow_skip", 1, "1 = show a Skip button, 0 = an answer is required to advance"),
]

# ─────────────────────────────────────────────── palette / styles
BLUE, SMOKEY, ICE, DOVE, SILVER, LEAD = "1A3FD6", "0626A9", "F4F5FD", "F5F5F5", "E6E6E6", "707070"
GREEN, GOLD = "118A5E", "A35C00"
thin = Side(style="thin", color=SILVER)
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
F_TITLE = Font(name="Arial", size=15, bold=True, color=SMOKEY)
F_SUB = Font(name="Arial", size=10, color=LEAD)
F_HDR = Font(name="Arial", size=10, bold=True, color="000000")
F_BODY = Font(name="Arial", size=10)
F_BOLD = Font(name="Arial", size=10, bold=True)
F_OK = Font(name="Arial", size=10, bold=True, color=GREEN)
F_NOTE = Font(name="Arial", size=9, color=LEAD)
FILL_H = PatternFill("solid", fgColor=DOVE)
FILL_Z = PatternFill("solid", fgColor=DOVE)
FILL_W = PatternFill("solid", fgColor="FFFFFF")
FILL_IN = PatternFill("solid", fgColor=ICE)
TOPL = Alignment(vertical="top", horizontal="left", wrap_text=True)
TOPC = Alignment(vertical="top", horizontal="center")

wb = Workbook()


def sheet(name, title, subtitle, first=False):
    ws = wb.active if first else wb.create_sheet(name)
    ws.title = name
    ws.sheet_view.showGridLines = False
    ws["A1"] = title; ws["A1"].font = F_TITLE
    ws["A2"] = subtitle; ws["A2"].font = F_SUB
    ws.row_dimensions[1].height = 22
    ws.row_dimensions[3].height = 6
    return ws


def header(ws, row, cols):
    for i, c in enumerate(cols, start=1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = F_HDR; cell.fill = FILL_H; cell.border = BOX; cell.alignment = TOPL
    ws.row_dimensions[row].height = 26


def rows_out(ws, start, rows, widths, heights=None, center_cols=()):
    for r, vals in enumerate(rows):
        rr = start + r
        fill = FILL_Z if r % 2 == 0 else FILL_W
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=rr, column=c, value=v)
            cell.font = F_BODY; cell.fill = fill; cell.border = BOX
            cell.alignment = TOPC if c in center_cols else TOPL
        if heights:
            ws.row_dimensions[rr].height = heights
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ─────────────────────────────────────────────── Read Me
ws = sheet("Read Me", "Agent Skills — Applied Quiz Bank",
           "Source of truth for the quiz app. Edit this workbook, re-run build_quiz.py, and the app rebuilds from it.", first=True)
header(ws, 4, ["Rule", "Setting"])
rows_out(ws, 5, [
    ["Questions per attempt", "20, drawn fresh from the bank on every page load"],
    ["Bank size", f"{len(QUESTIONS)} questions — {len(QUESTIONS)//len(DOMAINS)} per domain, {len(QUESTIONS)//3} per difficulty level"],
    ["Selection", "Per domain: 4 applied plus 1 recall, so every paper holds the same 80/20 split. Question and option order both shuffled"],
    ["Question kind", f"{_kind.get('applied',0)} applied (a scenario decides the answer) and {_kind.get('recall',0)} recall (a stated fact)"],
    ["Time limit", "10 minutes for the whole attempt. The test auto-submits when the clock reaches zero"],
    ["Marking", "+1 correct, -1 incorrect, 0 skipped or unreached. Score range -20 to +20"],
    ["Navigation", "One question on screen at a time. Once submitted, a question cannot be revisited"],
    ["Review", "Full per-question review after submission, with the correct answer and the reasoning"],
], [28, 92], heights=20)

ws["A14"] = "Authoring rules for new questions"
ws["A14"].font = F_BOLD
header(ws, 15, ["Rule"])
rows_out(ws, 16, [
    ["Exactly one option is correct. The other three must be wrong on the facts, not merely less good."],
    ["At least one distractor should be a near-miss: true in general but wrong for the situation, or containing a real number or field name used in the wrong place."],
    ["The stem must never misstate a fact to create the trap. Difficulty comes from the reader's judgement, not from misleading content."],
    ["Fill the Distractor note column with why the closest wrong option fails. It is shown to the learner in the review."],
    ["Keep the correct option in the Correct column as a single letter: A, B, C or D."],
    ["Never refer to an option by letter in the Rationale or Distractor note. The app shuffles option order on every attempt, so a letter means nothing by the time a learner reads the review. Quote the option's wording instead."],
    ["Set Kind to applied or recall. The app draws 4 applied and 1 recall per domain, so each domain needs at least 4 applied and 1 recall."],
    ["Keep the counts even: same number of questions per domain, and per difficulty level within each domain. The build fails if they drift."],
], [122], heights=32)

ws["A23"] = "To regenerate the app after editing: python3 build_quiz.py"
ws["A23"].font = F_NOTE

# ─────────────────────────────────────────────── Domains
ws = sheet("Domains", "Domains", "Question selection draws an equal share from each domain.")
header(ws, 4, ["Code", "Domain", "Questions in bank"])
counts = {k: sum(1 for q in QUESTIONS if q["domain"] == k) for k in DOMAINS}
rows_out(ws, 5, [[k, v, counts[k]] for k, v in DOMAINS.items()], [10, 44, 20], heights=18, center_cols=(1, 3))

# ─────────────────────────────────────────────── Config
ws = sheet("Config", "Config", "Read by the build script. Edit a value, re-run the build, and the app changes.")
header(ws, 4, ["Key", "Value", "What it controls"])
rows_out(ws, 5, [[k, v, d] for k, v, d in CONFIG], [26, 12, 76], heights=20, center_cols=(2,))
for r in range(5, 5 + len(CONFIG)):
    ws.cell(row=r, column=2).fill = FILL_IN
    ws.cell(row=r, column=2).font = F_BOLD

# ─────────────────────────────────────────────── Question Bank
ws = sheet("Question Bank", "Question Bank",
           "One correct option per question. Correct holds a single letter.")
cols = ["ID", "Domain", "Domain name", "Difficulty", "Kind", "Question",
        "Option A", "Option B", "Option C", "Option D", "Correct", "Rationale", "Distractor note"]
header(ws, 4, cols)
bank_rows = []
for q in QUESTIONS:
    assert q["correct"] in "ABCD", q["id"]
    assert set(q["options"]) == {"A", "B", "C", "D"}, q["id"]
    bank_rows.append([q["id"], q["domain"], DOMAINS[q["domain"]], q["difficulty"], q["kind"], q["q"],
                      q["options"]["A"], q["options"]["B"], q["options"]["C"], q["options"]["D"],
                      q["correct"], q["rationale"], q["trap"]])
rows_out(ws, 5, bank_rows, [9, 9, 30, 10, 10, 62, 46, 46, 46, 46, 9, 62, 62], heights=70,
         center_cols=(4, 5, 11))
for r in range(5, 5 + len(bank_rows)):
    ws.cell(row=r, column=11).font = F_OK
ws.freeze_panes = "A5"
ws.auto_filter.ref = f"A4:M{4+len(bank_rows)}"

for name in wb.sheetnames:
    w = wb[name]
    w.page_setup.orientation = "landscape"
    w.page_setup.fitToWidth = 1
    w.page_setup.fitToHeight = 0
    w.sheet_properties.pageSetUpPr.fitToPage = True

XLSX.parent.mkdir(parents=True, exist_ok=True)
wb.save(XLSX)
print("bank written:", XLSX.name, len(bank_rows), "questions")


print("next: python3 build_quiz_app.py  (regenerates the app from this workbook)")
