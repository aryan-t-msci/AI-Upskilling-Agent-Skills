#!/usr/bin/env python3
"""Flatten the content spine into doc_data.json for build_docx.js.

Selects up to three 'check yourself' items per module (easiest first) and builds
the appendix answer key from the same selection, so the two never drift apart.

Run from src/:  python3 make_doc_data.py   ->  writes doc_data.json beside it
"""
import json, os, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from content_modules_a import MODULES_A
from content_modules_b import MODULES_B
from content_cards import FLASHCARDS, GLOSSARY
from content_quiz import QUIZ

MODULES = MODULES_A + MODULES_B
MT = {m["id"]: m["num"] + " " + m["title"] for m in MODULES}

checks, answers = {}, []
for m in MODULES:
    items = sorted((q for q in QUIZ if q["module"] == m["id"]),
                   key=lambda q: (q["difficulty"], q["id"]))[:3]
    checks[m["id"]] = [{
        "id": q["id"], "q": q["q"],
        "options": (q.get("options") if q["type"] == "mcq"
                    else (["True", "False"] if q["type"] == "tf" else None)),
    } for q in items]
    for q in items:
        answers.append({"id": q["id"], "mod": MT[q["module"]], "q": q["q"],
                        "answer": q["answer"], "rationale": q["rationale"]})

data = {
    "modules": MODULES,
    "glossary": [{"term": t, "def": d} for t, d in GLOSSARY],
    "specAll": [[m["num"], k, v] for m in MODULES for k, v in m["spec_box"]],
    "checks": checks,
    "answers": answers,
    "nCards": len(FLASHCARDS),
    "nQuiz": len(QUIZ),
}

out = pathlib.Path(os.environ.get("DOC_DATA", HERE / "doc_data.json"))
out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
print(f"doc_data.json written: {len(MODULES)} modules, "
      f"{sum(len(v) for v in checks.values())} check-yourself items, "
      f"{len(data['specAll'])} spec facts")
