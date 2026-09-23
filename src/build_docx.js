const fs = require('fs');
const d = require('docx');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, TableOfContents,
  LevelFormat, Header, Footer, PageNumber, TabStopType
} = d;

const OUT = process.env.BUNDLE_OUT || '/mnt/user-data/outputs';
const DATA_PATH = process.env.DOC_DATA || '/home/claude/doc_data.json';
const DATA = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));

const BLUE='1A3FD6', SMOKEY='0626A9', ICE='F4F5FD', DOVE='F5F5F5', SILVER='E6E6E6',
      LEAD='707070', CHARCOAL='4D4D4D', GOLD='A35C00', GOLDBG='FFFBF4', CODEBG='F7F8FB';
const SANS='Calibri', HEAD='Calibri Light', MONO='Consolas';
const W = 9026;                       // A4 content width in DXA
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

/* ---------- inline markdown ---------- */
function runs(s, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(s)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: s.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith('**')) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), font: MONO, size: (base.size || 21) - 2, color: SMOKEY, ...{} }));
    last = re.lastIndex;
  }
  if (last < s.length) out.push(new TextRun({ text: s.slice(last), ...base }));
  return out;
}
const P = (s, o = {}) => new Paragraph({
  children: runs(s, { font: o.font || SANS, size: o.size || 21, color: o.color, italics: o.italics, bold: o.bold }),
  spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 276 },
  alignment: o.align, indent: o.indent, keepNext: o.keepNext,
});
const gap = (h = 120) => new Paragraph({ text: '', spacing: { after: h } });

/* ---------- box helpers ---------- */
function box(children, { bg, accent }) {
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    borders: {
      top: NONE, bottom: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE,
      left: accent ? { style: BorderStyle.SINGLE, size: 18, color: accent } : NONE,
    },
    rows: [new TableRow({ children: [new TableCell({
      width: { size: W, type: WidthType.DXA },
      shading: bg ? { type: ShadingType.CLEAR, fill: bg, color: 'auto' } : undefined,
      margins: { top: 160, bottom: 160, left: 220, right: 220 },
      children,
    })] })],
  });
}
function bullets(items, o = {}) {
  return items.map(t => new Paragraph({
    children: runs(t, { font: SANS, size: o.size || 21 }),
    numbering: { reference: o.ref || 'dots', level: 0 },
    spacing: { after: o.after ?? 90, line: 272 },
  }));
}
function h1(num, title) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [
      new TextRun({ text: num + '   ', font: MONO, size: 26, color: BLUE }),
      new TextRun({ text: title, font: HEAD, size: 32, color: SMOKEY, bold: false }),
    ],
    spacing: { before: 0, after: 80, line: 380 },
    indent: { left: 700, hanging: 700 },
  });
}
function h2(t) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text: t, font: SANS, size: 22, bold: true, color: CHARCOAL })],
    spacing: { before: 300, after: 120 },
    keepNext: true,
  });
}
function h1plain(t) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text: t, font: HEAD, size: 34, color: SMOKEY })],
    spacing: { before: 0, after: 160 },
  });
}
function rule() {
  return new Paragraph({ text: '', border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: SILVER } }, spacing: { after: 200 } });
}

/* ---------- tables ---------- */
function dataTable(headers, rows, widths, opts = {}) {
  const thin = { style: BorderStyle.SINGLE, size: 4, color: SILVER };
  const cell = (txt, w, o = {}) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: o.bg ? { type: ShadingType.CLEAR, fill: o.bg, color: 'auto' } : undefined,
    margins: { top: 80, bottom: 80, left: 130, right: 130 },
    children: [new Paragraph({
      children: runs(String(txt), { font: o.mono ? MONO : SANS, size: o.mono ? 18 : 19, bold: o.bold, color: o.color }),
      spacing: { after: 0, line: 252 },
    })],
  });
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: widths,
    borders: { top: thin, bottom: thin, left: thin, right: thin, insideHorizontal: thin, insideVertical: thin },
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => cell(h, widths[i], { bg: DOVE, bold: true })),
      }),
      ...rows.map((r, ri) => new TableRow({
        children: r.map((c, i) => cell(c, widths[i], {
          bg: ri % 2 === 0 ? 'FFFFFF' : DOVE,
          mono: opts.monoCols && opts.monoCols.includes(i),
          color: opts.monoCols && opts.monoCols.includes(i) ? SMOKEY : undefined,
        })),
      })),
    ],
  });
}
function codeBlock(a) {
  const lines = a.code.split('\n');
  return [
    new Paragraph({
      children: [
        new TextRun({ text: a.title, font: SANS, size: 19, bold: true, color: CHARCOAL }),
        new TextRun({ text: '   ' + a.lang, font: MONO, size: 16, color: LEAD }),
      ],
      spacing: { before: 200, after: 80 }, keepNext: true,
    }),
    box(lines.map(l => new Paragraph({
      children: [new TextRun({ text: l || ' ', font: MONO, size: 17, color: '1A1D24' })],
      spacing: { after: 0, line: 240 },
    })), { bg: CODEBG }),
    new Paragraph({
      children: runs(a.caption, { font: SANS, size: 18, color: LEAD, italics: true }),
      spacing: { before: 90, after: 200, line: 252 },
    }),
  ];
}

/* ---------- document body ---------- */
const body = [];

// cover
body.push(gap(1400));
body.push(new Paragraph({
  children: [new TextRun({ text: 'Agent Skills', font: HEAD, size: 76, color: SMOKEY })],
  spacing: { after: 0, line: 900 },
}));
body.push(new Paragraph({
  children: [new TextRun({ text: 'with Anthropic', font: HEAD, size: 76, color: BLUE })],
  spacing: { after: 300, line: 900 },
}));
body.push(new Paragraph({
  text: '', border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: BLUE } }, spacing: { after: 280 },
}));
body.push(new Paragraph({
  children: [new TextRun({ text: 'Study notes, worked artifacts and self-assessment', font: SANS, size: 28, color: CHARCOAL })],
  spacing: { after: 140 },
}));
body.push(P('Compiled from the DeepLearning.AI course taught by Elie Schoppik, the published Agent Skills specification, the anthropics/skills repository and Anthropic\'s platform documentation.', { size: 21, color: LEAD, after: 60 }));
body.push(P(`${DATA.modules.length} modules · ${DATA.nCards} flashcards · ${DATA.nQuiz} assessment items · September 2026`, { size: 20, color: LEAD, after: 600 }));
body.push(box([
  P('Point-in-time note', { bold: true, size: 20, after: 60, color: SMOKEY }),
  P('The API beta headers, the code execution tool version string and the behaviour of subagent skill injection were accurate to the course recording and to documentation reviewed in September 2026. All three are on a fast-moving surface. Verify them against current documentation before presenting them as fact.', { size: 19, after: 0 }),
], { bg: ICE, accent: BLUE }));
body.push(new Paragraph({ children: [new PageBreak()] }));

// how to use + TOC
body.push(h1plain('How to use these notes'));
body.push(P('Each module follows the same five-part shape, and the shape is the study method.', { after: 160 }));
body.push(...bullets([
  '**Objective** — what you should be able to do afterwards. Read it first, and again at the end as a check.',
  '**Key points** — the retainable claims, one line each. These are what the flashcards drill.',
  '**Reference facts** — the hard limits, paths and API strings. Do not memorise these; know that they exist and where to look.',
  '**In depth** — the reasoning behind the key points. This is the part that makes the facts stick, and the part worth reading slowly.',
  '**Artifacts and gotchas** — real code and file layouts, then the failure modes. The gotchas are disproportionately what separates someone who has watched the course from someone who has shipped a skill.',
]));
body.push(P('Every module ends with **Check yourself** — two or three prompts to answer from memory before moving on. Answers are in Appendix C. Retrieval practice beats re-reading by a wide margin, so resist the urge to look.', { before: 120, after: 200 }));
body.push(P('Modules 00 to 09 track the course lessons. Modules 10 to 13 are the enrichment layer: evaluation, security and governance, portability, and an applied module mapping the patterns onto batch data-verification work. Three subjects were promoted out of the lessons that buried them — progressive disclosure, evaluation and security — because each carries more weight than its original screen time suggests.', { after: 300 }));
body.push(h1plain('Contents'));
body.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));
body.push(P('If the list above is empty, click it and press F9 to build it.', { size: 18, color: LEAD, before: 120, after: 300 }));
body.push(h2('Course at a glance'));
body.push(dataTable(
  ['#', 'Module', 'Source lesson', 'Min'],
  DATA.modules.map(m => [m.num, m.title, m.lesson, String(m.duration_min)]),
  [700, 3900, 3626, 800],
));
body.push(new Paragraph({ children: [new PageBreak()] }));

// modules
DATA.modules.forEach((m, mi) => {
  body.push(h1(m.num, m.title));
  body.push(new Paragraph({
    children: [new TextRun({ text: `${m.lesson}  ·  about ${m.duration_min} minutes`, font: SANS, size: 18, color: LEAD })],
    spacing: { after: 160 },
  }));
  body.push(box([
    P('What you should be able to do after this', { bold: true, size: 19, after: 60, color: SMOKEY }),
    P(m.objective, { size: 21, after: 0 }),
  ], { bg: ICE, accent: BLUE }));
  body.push(gap(200));

  body.push(h2('Key points'));
  body.push(...bullets(m.key_points));

  body.push(h2('Reference facts'));
  body.push(dataTable(['Fact', 'Value'], m.spec_box, [3300, 5726], { monoCols: [1] }));

  body.push(h2('In depth'));
  m.deep_dive.forEach(p => body.push(P(p, { after: 140 })));

  if (m.artifacts.length) {
    body.push(h2('Artifacts'));
    m.artifacts.forEach(a => body.push(...codeBlock(a)));
  }

  body.push(h2('Gotchas'));
  body.push(box([
    ...bullets(m.gotchas, { size: 20, after: 70 }),
  ], { bg: GOLDBG, accent: GOLD }));

  const checks = DATA.checks[m.id] || [];
  if (checks.length) {
    body.push(h2('Check yourself'));
    const kids = [];
    checks.forEach((c, i) => {
      kids.push(new Paragraph({
        children: [
          new TextRun({ text: `${c.id}  `, font: MONO, size: 17, color: BLUE }),
          ...runs(c.q, { font: SANS, size: 20 }),
        ],
        spacing: { after: c.options ? 60 : 110, line: 264 },
      }));
      if (c.options) {
        c.options.forEach(o => kids.push(new Paragraph({
          children: runs(o, { font: SANS, size: 19, color: CHARCOAL }),
          numbering: { reference: 'dashes', level: 0 },
          spacing: { after: 40, line: 252 },
        })));
        kids.push(gap(60));
      }
    });
    kids.push(P('Answers in Appendix C.', { size: 18, color: LEAD, after: 0 }));
    body.push(box(kids, { bg: DOVE }));
  }

  if (mi < DATA.modules.length - 1) body.push(new Paragraph({ children: [new PageBreak()] }));
});

// Appendix A
body.push(new Paragraph({ children: [new PageBreak()] }));
body.push(h1plain('Appendix A — Specification cheat sheet'));
body.push(P('Every limit, path, directory name and API string from the course, in module order. Values in monospace are literal.', { after: 200 }));
body.push(dataTable(['#', 'Fact', 'Value'], DATA.specAll, [700, 3300, 5026], { monoCols: [2] }));

// Appendix B
body.push(new Paragraph({ children: [new PageBreak()] }));
body.push(h1plain('Appendix B — Glossary'));
DATA.glossary.forEach(g => {
  body.push(new Paragraph({
    children: [new TextRun({ text: g.term, font: SANS, size: 21, bold: true, color: SMOKEY })],
    spacing: { before: 140, after: 30 }, keepNext: true,
  }));
  body.push(P(g.def, { size: 20, after: 0 }));
});

// Appendix C
body.push(new Paragraph({ children: [new PageBreak()] }));
body.push(h1plain('Appendix C — Check yourself answers'));
body.push(P('Grade the short-answer and applied items against the substance of the model answer, not its wording.', { after: 200 }));
DATA.answers.forEach(a => {
  body.push(new Paragraph({
    children: [
      new TextRun({ text: a.id + '  ', font: MONO, size: 18, color: BLUE }),
      new TextRun({ text: a.mod, font: SANS, size: 18, color: LEAD }),
    ],
    spacing: { before: 180, after: 40 }, keepNext: true,
  }));
  body.push(P(a.q, { size: 19, color: CHARCOAL, after: 60, italics: true }));
  body.push(P('**Answer.** ' + a.answer, { size: 20, after: 50 }));
  body.push(P('**Why it matters.** ' + a.rationale, { size: 19, color: CHARCOAL, after: 0 }));
});

/* ---------- assemble ---------- */
const doc = new Document({
  creator: 'Course study bundle',
  title: 'Agent Skills with Anthropic — Study Notes',
  description: 'Study notes, artifacts and self-assessment compiled from the DeepLearning.AI course and the Agent Skills specification.',
  styles: {
    default: {
      document: { run: { font: SANS, size: 21, color: '1A1D24' }, paragraph: { spacing: { line: 276 } } },
      heading1: { run: { font: HEAD, size: 34, color: SMOKEY, bold: false }, paragraph: { spacing: { before: 0, after: 120 }, outlineLevel: 0 } },
      heading2: { run: { font: SANS, size: 22, bold: true, color: CHARCOAL }, paragraph: { spacing: { before: 300, after: 120 }, outlineLevel: 1 } },
    },
  },
  numbering: {
    config: [
      { reference: 'dots', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 340, hanging: 220 } }, run: { color: BLUE } } }] },
      { reference: 'dashes', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2013', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 560, hanging: 220 } }, run: { color: LEAD } } }] },
    ],
  },
  sections: [{
    properties: { titlePage: true, page: { margin: { top: 1440, bottom: 1300, left: 1440, right: 1440 } } },
    headers: { first: new Header({ children: [new Paragraph({ text: '' })] }), default: new Header({ children: [new Paragraph({
      children: [new TextRun({ text: 'Agent Skills with Anthropic — study notes', font: SANS, size: 16, color: LEAD })],
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: SILVER } },
      spacing: { after: 200 },
    })] }) },
    footers: { first: new Footer({ children: [new Paragraph({ text: '' })] }), default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: MONO, size: 16, color: LEAD })],
    })] }) },
    children: body,
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(OUT + '/Agent-Skills-Study-Notes.docx', b);
  console.log('written', b.length, 'bytes');
});
