#!/usr/bin/env python3
"""MSCI-branded Excel bundle: quiz bank, flashcards, spec cheat sheet, glossary, scoring tracker."""
import sys, pathlib
import os
OUT = os.environ.get("BUNDLE_OUT", "/mnt/user-data/outputs")   # repo root when run from src/

sys.path.insert(0, "/home/claude")
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from content_modules_a import MODULES_A
from content_modules_b import MODULES_B
from content_cards import FLASHCARDS, GLOSSARY
from content_quiz import QUIZ

MODULES = MODULES_A + MODULES_B
MT = {m["id"]: f'{m["num"]} {m["title"]}' for m in MODULES}

# --- MSCI palette (openpyxl: no '#') ---
BLUE, SMOKEY, ICE, POWDER = "1A3FD6", "0626A9", "F4F5FD", "AEBAF0"
DOVE, WHITE, SILVER, LEAD, CHARCOAL = "F5F5F5", "FFFFFF", "E6E6E6", "707070", "4D4D4D"
GOLD = "DB7C00"

thin = Side(style="thin", color=SILVER)
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
TOPLEAD = Border(left=thin, right=thin, top=Side(style="thin", color=LEAD), bottom=thin)

F_TITLE = Font(name="Arial", size=15, bold=True, color=SMOKEY)
F_SUB = Font(name="Arial", size=10, color=LEAD)
F_HDR_N = Font(name="Arial", size=10, bold=True, color="000000")   # neutral header
F_HDR_B = Font(name="Arial", size=10, bold=True, color=WHITE)      # brand header
F_BODY = Font(name="Arial", size=10)
F_MONO = Font(name="Arial", size=10, color=SMOKEY)
F_BOLD = Font(name="Arial", size=10, bold=True)
F_NOTE = Font(name="Arial", size=9, color=LEAD)

FILL_N = PatternFill("solid", fgColor=DOVE)
FILL_B = PatternFill("solid", fgColor=BLUE)
FILL_Z = PatternFill("solid", fgColor=DOVE)
FILL_W = PatternFill("solid", fgColor=WHITE)
FILL_IN = PatternFill("solid", fgColor=ICE)

TOP = Alignment(vertical="top", wrap_text=True)
TOPL = Alignment(vertical="top", horizontal="left", wrap_text=True)
TOPR = Alignment(vertical="top", horizontal="right")
TOPC = Alignment(vertical="top", horizontal="center")

wb = Workbook()


def sheet(name, title, subtitle):
    ws = wb.create_sheet(name) if wb.sheetnames != ["Sheet"] else wb.active
    if ws.title == "Sheet":
        ws.title = name
    ws.sheet_view.showGridLines = False
    ws["A1"] = title
    ws["A1"].font = F_TITLE
    ws["A2"] = subtitle
    ws["A2"].font = F_SUB
    ws.row_dimensions[1].height = 22
    ws.row_dimensions[3].height = 6
    return ws


def header(ws, row, cols, brand=False):
    for i, c in enumerate(cols, start=1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = F_HDR_B if brand else F_HDR_N
        cell.fill = FILL_B if brand else FILL_N
        cell.border = BOX
        cell.alignment = TOPL
    ws.row_dimensions[row].height = 26


def body(ws, start, rows, widths, right_cols=(), heights=None):
    for r, vals in enumerate(rows):
        rr = start + r
        fill = FILL_Z if r % 2 == 0 else FILL_W
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=rr, column=c, value=v)
            cell.font = F_BODY
            cell.fill = fill
            cell.border = BOX
            cell.alignment = TOPR if c in right_cols else TOPL
        if heights:
            ws.row_dimensions[rr].height = heights
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ---------------------------------------------------------------- Read Me
ws = sheet("Read Me", "Agent Skills With Anthropic — Assessment Bundle",
           "Companion workbook to the course notes, deck and interactive study app. Sourced from the DeepLearning.AI course transcripts, the published Agent Skills specification and Anthropic's documentation.")
rows = [
    ["Quiz Bank", f"{len(QUIZ)} assessment items: multiple choice, true or false, short answer and applied scenarios. Includes the correct answer and a rationale for every item.", "Trainer reference and self-test"],
    ["Flashcards", f"{len(FLASHCARDS)} prompt-and-answer pairs for spaced rehearsal, tagged by module and theme.", "Daily recall drill"],
    ["Spec Cheat Sheet", "Every hard limit, path, directory name and API string drawn from the 14 modules.", "Look-up during build work"],
    ["Glossary", f"{len(GLOSSARY)} terms defined in one line each.", "Onboarding a new team member"],
    ["Score Tracker", "Enter 1 for correct and 0 for missed against each item. Totals and per-module breakdowns calculate automatically.", "Track a cohort or your own retakes"],
]
header(ws, 4, ["Sheet", "What it contains", "Primary use"])
body(ws, 5, rows, [22, 88, 34], heights=44)

ws["A12"] = "How to use the score tracker"
ws["A12"].font = F_BOLD
notes = [
    ["Edit only the Score column (column F) on the Score Tracker sheet. Every other cell is a formula or a label."],
    ["Enter 1 for a correct answer and 0 for a missed one. Leave the cell empty for an item you skipped."],
    ["Example: for item Q01, if the learner answered correctly, F5 = 1. If the learner missed it, F5 = 0."],
    ["Input cells are shaded pale blue. Totals recalculate as you type, and attempted items exclude blanks."],
    ["Short-answer and applied items are self-graded against the model answer on the Quiz Bank sheet."],
]
header(ws, 13, ["Instruction"])
body(ws, 14, notes, [110], heights=32)

ws["A21"] = "Difficulty scale"
ws["A21"].font = F_BOLD
header(ws, 22, ["Level", "Meaning"])
body(ws, 23, [["1", "Recall — a named fact, limit or path"],
              ["2", "Apply — use the concept on a described situation"],
              ["3", "Judgement — choose between primitives, or defend a design"]], [22, 88], heights=18)

ws["A28"] = "Point-in-time note: API beta headers, code execution tool version strings and subagent skill-injection behaviour were accurate to the course recording and to documentation reviewed in September 2026. Verify these against current documentation before teaching them as fact."
ws["A28"].font = F_NOTE
ws["A28"].alignment = TOPL

# ---------------------------------------------------------------- Quiz Bank
ws = sheet("Quiz Bank", "Quiz Bank",
           "Fifty items across 14 modules. Options are blank for true or false, short answer and applied items.")
cols = ["ID", "Module", "Module title", "Type", "Difficulty", "Question",
        "Option A", "Option B", "Option C", "Option D", "Correct answer", "Rationale"]
header(ws, 4, cols)
rows = []
for q in QUIZ:
    o = q.get("options") or ([] if q["type"] != "tf" else ["True", "False"])
    o = list(o) + [""] * (4 - len(o))
    rows.append([q["id"], MT[q["module"]].split(" ")[0], MT[q["module"]][3:], q["type"],
                 q["difficulty"], q["q"], o[0], o[1], o[2], o[3], q["answer"], q["rationale"]])
body(ws, 5, rows, [7, 7, 30, 9, 10, 62, 30, 30, 30, 30, 62, 78], right_cols=(5,), heights=None)
for r in range(5, 5 + len(rows)):
    ws.row_dimensions[r].height = 58
ws.freeze_panes = "A5"
ws.auto_filter.ref = f"A4:L{4+len(rows)}"

# ---------------------------------------------------------------- Flashcards
ws = sheet("Flashcards", "Flashcards",
           "Prompt on the left, answer on the right. Tag groups cards by theme for targeted drilling.")
header(ws, 4, ["ID", "Module", "Module title", "Tag", "Prompt", "Answer"])
rows = [[f"C{i:03d}", MT[m].split(" ")[0], MT[m][3:], t, f, b]
        for i, (m, f, b, t) in enumerate(FLASHCARDS, start=1)]
body(ws, 5, rows, [8, 7, 30, 12, 62, 84])
for r in range(5, 5 + len(rows)):
    ws.row_dimensions[r].height = 40
ws.freeze_panes = "A5"
ws.auto_filter.ref = f"A4:F{4+len(rows)}"

# ---------------------------------------------------------------- Spec Cheat Sheet
ws = sheet("Spec Cheat Sheet", "Spec Cheat Sheet",
           "Hard limits, directory names, paths and API strings, in module order.")
header(ws, 4, ["Module", "Module title", "Fact", "Value"])
rows = [[m["num"], m["title"], k, v] for m in MODULES for (k, v) in m["spec_box"]]
body(ws, 5, rows, [9, 40, 34, 52])
for r in range(5, 5 + len(rows)):
    ws.row_dimensions[r].height = 18
    ws.cell(row=r, column=4).font = F_MONO
ws.freeze_panes = "A5"
ws.auto_filter.ref = f"A4:D{4+len(rows)}"

# ---------------------------------------------------------------- Glossary
ws = sheet("Glossary", "Glossary", "One line per term, written for someone joining the work mid-stream.")
header(ws, 4, ["Term", "Definition"])
body(ws, 5, [[t, d] for (t, d) in GLOSSARY], [30, 118])
for r in range(5, 5 + len(GLOSSARY)):
    ws.row_dimensions[r].height = 32

# ---------------------------------------------------------------- Score Tracker
ws = sheet("Score Tracker", "Score Tracker",
           "Enter 1 for correct or 0 for missed in the Score column only. Everything else is calculated.")
header(ws, 4, ["ID", "Module", "Type", "Difficulty", "Question", "Score"])
n = len(QUIZ)
for i in range(n):
    r = 5 + i
    src = 5 + i
    fill = FILL_Z if i % 2 == 0 else FILL_W
    vals = [f"='Quiz Bank'!A{src}", f"='Quiz Bank'!B{src}", f"='Quiz Bank'!D{src}",
            f"='Quiz Bank'!E{src}", f"='Quiz Bank'!F{src}"]
    for c, v in enumerate(vals, start=1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.font = F_BODY
        cell.fill = fill
        cell.border = BOX
        cell.alignment = TOPR if c == 4 else TOPL
    sc = ws.cell(row=r, column=6)
    sc.font = F_BOLD
    sc.fill = FILL_IN
    sc.border = BOX
    sc.alignment = TOPC
    ws.row_dimensions[r].height = 30
last = 4 + n
tr = last + 1
ws.cell(row=tr, column=1, value="Total").font = F_BOLD
ws.cell(row=tr, column=5, value="Correct out of attempted").font = F_BOLD
ws.cell(row=tr, column=6, value=f"=SUM(F5:F{last})").font = F_BOLD
for c in range(1, 7):
    cell = ws.cell(row=tr, column=c)
    cell.border = TOPLEAD
    cell.fill = FILL_W
    if c == 5:
        cell.alignment = TOPL
    if c == 6:
        cell.alignment = TOPC
for i, w in enumerate([8, 8, 10, 10, 74, 9], start=1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "A5"

# summary blocks to the right
sr = 4
ws.cell(row=sr, column=8, value="Summary").font = F_TITLE
for j, (lbl, formula) in enumerate([
    ("Items in bank", f"=COUNTA(A5:A{last})"),
    ("Attempted", f"=COUNT(F5:F{last})"),
    ("Correct", f"=SUM(F5:F{last})"),
    ("Score", f'=IFERROR(SUM(F5:F{last})/COUNT(F5:F{last}),0)'),
], start=0):
    r = sr + 2 + j
    a = ws.cell(row=r, column=8, value=lbl)
    b = ws.cell(row=r, column=9, value=formula)
    a.font = F_BODY; b.font = F_BOLD
    a.fill = b.fill = FILL_Z if j % 2 == 0 else FILL_W
    a.border = b.border = BOX
    a.alignment = TOPL; b.alignment = TOPR
    if lbl == "Score":
        b.number_format = "0.0%"

hr = sr + 8
ws.cell(row=hr, column=8, value="By module").font = F_BOLD
header_cells = ["Module", "Attempted", "Correct", "Score"]
for i, c in enumerate(header_cells):
    cell = ws.cell(row=hr + 1, column=8 + i, value=c)
    cell.font = F_HDR_N; cell.fill = FILL_N; cell.border = BOX; cell.alignment = TOPL
for k, m in enumerate(MODULES):
    r = hr + 2 + k
    num = m["num"]
    vals = [num,
            f'=COUNTIFS($B$5:$B${last},$H{r},$F$5:$F${last},"<>")',
            f'=SUMIFS($F$5:$F${last},$B$5:$B${last},$H{r})',
            f'=IFERROR(SUMIFS($F$5:$F${last},$B$5:$B${last},$H{r})/COUNTIFS($B$5:$B${last},$H{r},$F$5:$F${last},"<>"),"-")']
    for c, v in enumerate(vals):
        cell = ws.cell(row=r, column=8 + c, value=v)
        cell.font = F_BODY
        cell.fill = FILL_Z if k % 2 == 0 else FILL_W
        cell.border = BOX
        cell.alignment = TOPL if c == 0 else TOPR
        if c == 3:
            cell.number_format = "0.0%"
tr2 = hr + 2 + len(MODULES)
for c, v in enumerate(["Total",
                       f'=COUNT($F$5:$F${last})',
                       f'=SUM($F$5:$F${last})',
                       f'=IFERROR(SUM($F$5:$F${last})/COUNT($F$5:$F${last}),"-")']):
    cell = ws.cell(row=tr2, column=8 + c, value=v)
    cell.font = F_BOLD; cell.border = TOPLEAD; cell.fill = FILL_W
    cell.alignment = TOPL if c == 0 else TOPR
    if c == 3:
        cell.number_format = "0.0%"

byt_r = tr2 + 2
ws.cell(row=byt_r, column=8, value="By item type").font = F_BOLD
for i, c in enumerate(header_cells):
    cell = ws.cell(row=byt_r + 1, column=8 + i, value=["Type", "Attempted", "Correct", "Score"][i])
    cell.font = F_HDR_N; cell.fill = FILL_N; cell.border = BOX; cell.alignment = TOPL
for k, t in enumerate(["mcq", "tf", "short", "applied"]):
    r = byt_r + 2 + k
    vals = [t,
            f'=COUNTIFS($C$5:$C${last},$H{r},$F$5:$F${last},"<>")',
            f'=SUMIFS($F$5:$F${last},$C$5:$C${last},$H{r})',
            f'=IFERROR(SUMIFS($F$5:$F${last},$C$5:$C${last},$H{r})/COUNTIFS($C$5:$C${last},$H{r},$F$5:$F${last},"<>"),"-")']
    for c, v in enumerate(vals):
        cell = ws.cell(row=r, column=8 + c, value=v)
        cell.font = F_BODY
        cell.fill = FILL_Z if k % 2 == 0 else FILL_W
        cell.border = BOX
        cell.alignment = TOPL if c == 0 else TOPR
        if c == 3:
            cell.number_format = "0.0%"

for i, w in enumerate([22, 12, 10, 10], start=8):
    ws.column_dimensions[get_column_letter(i)].width = w

nr = byt_r + 8
ws.cell(row=nr, column=8, value="Score is correct divided by attempted, so blanks do not count against the learner.").font = F_NOTE

for name in wb.sheetnames:
    w = wb[name]
    w.page_setup.orientation = "landscape"
    w.page_setup.fitToWidth = 1
    w.page_setup.fitToHeight = 0
    w.sheet_properties.pageSetUpPr.fitToPage = True

out = pathlib.Path(f"{OUT}/Agent-Skills-Assessment-Bundle.xlsx")
wb.save(out)
print("saved", out, out.stat().st_size, "bytes; sheets:", wb.sheetnames)
