---
name: cognitive-coverage
description: >
  Generate a cognitive coverage system for any project: a JSON manifest tracking understanding
  across files, concepts, and data flows; an interactive HTML teaching guide with quiz; and an
  HTML dashboard showing coverage status with gap analysis. Works for codebases, research paper
  collections, documentation wikis, and any knowledge domain. Use when someone wants to understand
  a project they didn't create, reduce cognitive debt, track what they've understood, or generate
  a learning guide. Triggers: 'explain this codebase', 'cognitive coverage', 'learning guide',
  'teaching guide', 'cognitive debt', 'system understanding', 'codebase quiz', 'coverage dashboard',
  'help me understand this project', 'codebase walkthrough', 'track understanding', 'knowledge map',
  'research coverage', 'documentation guide'.
---

# Cognitive Coverage — Skill Instructions

You generate a **cognitive coverage system** — three coordinated artifacts that help people build genuine understanding of projects, codebases, research corpora, or documentation they didn't create.

## Philosophy

> When AI generates code, a developer may accept it without building a mental model.
> When a team inherits a codebase, research corpus, or documentation set, they may skim without
> truly understanding. Over time this creates **cognitive debt** — the system works (or the
> knowledge exists), but the understanding and mental models are missing or flawed.
>
> Cognitive coverage closes that gap by producing structured, quiz-verified learning materials
> anchored to the actual source material.

## The Three Artifacts

| # | Artifact | File | Purpose |
|---|----------|------|---------|
| 1 | Teaching Guide | `learning-guide.html` | Interactive HTML with sections, code/content snippets, mental models, quiz |
| 2 | Coverage Manifest | `cognitive-coverage.json` | Machine-readable inventory of what needs to be understood |
| 3 | Coverage Dashboard | `cognitive-coverage.html` | Visual status board with gap analysis and teaching guide links |

Generate them in order: Guide → Manifest → Dashboard.

---

## Phase 0: Domain Detection

Before analyzing content, detect the project domain:

### Detection Rules

| Signal | Domain |
|--------|--------|
| Source code files (.ts, .py, .rs, .go, .java, .js, .rb, .cs, .cpp, etc.) | `codebase` |
| Research papers (.pdf), bibliographies (.bib), datasets (.csv, .parquet) | `research` |
| Documentation (.md, .mdx, .rst, .adoc), wiki structure, docs/ folders | `documentation` |
| Mixed signals | Ask the user or use `hybrid` |
| No clear signals (plain files, notes) | `knowledge` (general) |

### Domain Vocabulary

Each domain uses adapted terminology for the three coverage axes:

```
CODEBASE:
  files_label: "Source Files"
  concepts_label: "Concepts & Patterns"
  flows_label: "Data Flows"
  file_statuses: ["uncovered", "read", "understood"]
  concept_statuses: ["uncovered", "taught", "quiz-verified"]
  flow_statuses: ["uncovered", "traced", "verified"]

RESEARCH:
  files_label: "Papers & Sources"
  concepts_label: "Theories & Methods"
  flows_label: "Argument Chains"
  file_statuses: ["unread", "skimmed", "comprehended"]
  concept_statuses: ["unfamiliar", "introduced", "quiz-verified"]
  flow_statuses: ["unknown", "followed", "verified"]

DOCUMENTATION:
  files_label: "Documents & Pages"
  concepts_label: "Topics & Processes"
  flows_label: "Workflows & Procedures"
  file_statuses: ["unread", "browsed", "internalized"]
  concept_statuses: ["unfamiliar", "reviewed", "quiz-verified"]
  flow_statuses: ["unknown", "walked-through", "verified"]

KNOWLEDGE (general):
  files_label: "Sources"
  concepts_label: "Key Ideas"
  flows_label: "Connections & Sequences"
  file_statuses: ["unseen", "encountered", "mastered"]
  concept_statuses: ["unknown", "introduced", "quiz-verified"]
  flow_statuses: ["unknown", "traced", "verified"]
```

State the detected domain at the start of your output so the user can confirm or override.

---

## Phase 1: Deep Content Analysis

Before writing anything, you MUST thoroughly read and understand the project:

### For Codebases
1. **Discover structure**: List all files (excluding node_modules, dist, .git, vendor, build artifacts). Map the file tree.
2. **Identify the stack**: Read package.json / requirements.txt / go.mod / Cargo.toml etc.
3. **Read foundational files first**: Config, types/interfaces, data models, schemas.
4. **Read core logic next**: Business logic, algorithms, decision-making.
5. **Read integration layers**: API routes, controllers, middleware, database access.
6. **Read the UI/presentation layer** (if any).
7. **Read supporting files**: Utilities, helpers, seed data, environment config.
8. **Check for specs/docs**: README, spec files, design docs, comments.

### For Research
1. **Inventory sources**: List all papers, datasets, bibliographies, notes.
2. **Identify the field**: What domain/discipline? What's the research question?
3. **Read foundational papers first**: Seminal works, surveys, methodology papers.
4. **Read primary results**: Key findings papers, experimental results.
5. **Read supporting materials**: Datasets, statistical methods, replication notes.
6. **Map citation relationships**: What cites what? What builds on what?

### For Documentation
1. **Map the structure**: Table of contents, navigation hierarchy, cross-references.
2. **Identify scope**: What system/process/domain does this document?
3. **Read overview/intro pages first**: Architecture, getting started, core concepts.
4. **Read detailed pages**: API references, configuration, advanced topics.
5. **Read operational pages**: Troubleshooting, FAQs, runbooks.
6. **Map dependencies**: What pages assume knowledge from other pages?

**Do NOT start writing the guide until you have read every significant source.** Partial understanding produces misleading guides.

---

## Phase 2: Concept Extraction

From your analysis, identify:

1. **The "Why"** — What problem does this project solve? What's the core insight or purpose?
2. **Key abstractions** — What are the 4-8 main concepts someone must understand?
3. **The critical flow** — What's the most important end-to-end behavior or argument? Trace it completely.
4. **Structure** — How is information/state organized? What are the key entities?
5. **Decision points** — Where are choices made that affect behavior or conclusions?
6. **Boundaries** — What are the guardrails, limitations, access controls, or scope limits?
7. **Configuration surface** — What can be changed vs. what is fixed?
8. **Common misconceptions** — What would someone likely get wrong?

---
## Phase 3: Teaching Guide Generation

Generate a single self-contained HTML file (`learning-guide.html`) with no external dependencies.

### Required Sections

1. **Why This Exists** — Problem statement in plain language. No jargon assumed.
2. **The Big Picture** — Cast of characters / key entities / domain overview.
3. **Architecture / Structure Map** — Visual diagram (text/CSS-based) of how things relate.
4. **Core Model** — Data model, state shape, entity relationships, or conceptual framework.
5. **Core Algorithm / Decision Flow / Central Argument** — The most important behavior or reasoning chain, traced step by step.
6. **[3-6 additional concept sections]** — One per major subsystem, theory, or topic area, each with:
   - Snippets from the actual source material (with source path labels)
   - A "Mental Model" callout with an analogy
   - A "Warning/Key Insight" box for things easy to misunderstand
7. **Interactive Knowledge Quiz** — 10-20 questions testing comprehension

### Required UI Components

#### Concept Cards
```html
<div class="concept-card">
  <h4>Title</h4>
  <p>Explanation with <code>references</code>.</p>
</div>
```

#### Mental Model Callouts
```html
<div class="mental-model">
  <strong>Mental Model:</strong> Analogy building intuition, not just knowledge.
</div>
```

#### Warning / Key Insight Boxes
```html
<div class="warning-box">
  <strong>Key insight:</strong> Something easy to misunderstand or with non-obvious implications.
</div>
```

#### Source Snippets with References
```html
<div class="code-label">path/to/source — contextName()</div>
<pre><span class="kw">keyword</span> <span class="fn">name</span>(...) {
  <span class="cm">// explanation</span>
}</pre>
```

For non-code domains, use `<pre>` or `<blockquote>` with the source path label. The key is always attributing content to its source.

#### Flow Diagrams (CSS-based, no images)
```html
<div class="flow-diagram">
  <span class="flow-accent">Step 1</span> → Description<br>
  <span class="flow-accent">Step 2</span> → Description<br>
</div>
```

#### Navigation Sidebar
```html
<nav class="toc-sidebar">
  <h2>Cognitive Map</h2>
  <div class="toc-section-label">Section Group</div>
  <a href="#section-id">Section Title</a>
</nav>
```

### Quiz Requirements

The quiz is critical — it verifies genuine understanding, not just reading.

#### Quiz Rules
1. **10-20 questions** covering all major sections
2. **Multiple choice** (3-4 options per question)
3. **Every question maps to a specific concept** taught in the guide
4. **Explanations revealed on answer** — citing the specific source
5. **Score tracking** with visible counter and progress bar
6. **Reset button** to retake
7. **Mix question types**:
   - Structure questions (where is X defined/discussed?)
   - Logic questions (what does this function compute / what does this theory claim?)
   - Behavior questions (what happens when X occurs / what follows from Y?)
   - Boundary questions (what prevents X / what are the limits?)
   - System thinking questions (if you change X, what cascading effect?)
8. **localStorage sync** — write quiz results to shared coverage state

#### Quiz Implementation
```html
<div class="quiz-card" data-quiz="q1">
  <h4>Q1 — Category</h4>
  <p class="question">Question text?</p>
  <ul class="quiz-options">
    <li onclick="selectAnswer(this,'q1',false)">Wrong answer</li>
    <li onclick="selectAnswer(this,'q1',true)">Correct answer</li>
    <li onclick="selectAnswer(this,'q1',false)">Wrong answer</li>
  </ul>
  <div class="quiz-explanation" id="q1-exp">
    Explanation referencing <code>specific source</code>.
  </div>
</div>
```

#### Quiz JavaScript (with Coverage Sync)
```javascript
var score=0, answered=0, total=N, answeredSet=new Set();
var LS_KEY='cognitive-coverage-state';

function syncQuizResult(qId, isCorrect) {
  var state;
  try { state = JSON.parse(localStorage.getItem(LS_KEY)) || {}; } catch(e) { state = {}; }
  if (!state.quizResults) state.quizResults = {};
  state.quizResults[qId] = { correct: isCorrect, timestamp: new Date().toISOString() };
  localStorage.setItem(LS_KEY, JSON.stringify(state));
}

function selectAnswer(li, qId, isCorrect) {
  if (answeredSet.has(qId)) return;
  answeredSet.add(qId); answered++;
  var opts = li.parentElement.querySelectorAll('li');
  opts.forEach(function(o) { o.style.pointerEvents='none'; o.style.opacity='0.6'; });
  if (isCorrect) { li.classList.add('correct'); li.style.opacity='1'; score++; }
  else { li.classList.add('incorrect'); li.style.opacity='1'; }
  document.getElementById(qId+'-exp').classList.add('visible');
  document.getElementById('score-value').textContent = score;
  document.getElementById('prog-fill').style.width = (answered/total*100)+'%';
  syncQuizResult(qId, isCorrect);
}

function resetQuiz() {
  score=0; answered=0; answeredSet.clear();
  document.getElementById('score-value').textContent = '0';
  document.getElementById('prog-fill').style.width = '0%';
  document.querySelectorAll('.quiz-card').forEach(function(c) {
    c.querySelectorAll('li').forEach(function(l) {
      l.classList.remove('correct','incorrect');
      l.style.pointerEvents=''; l.style.opacity='';
    });
    c.querySelector('.quiz-explanation').classList.remove('visible');
  });
  var state;
  try { state = JSON.parse(localStorage.getItem(LS_KEY)) || {}; } catch(e) { state = {}; }
  if (state.quizResults) { state.quizResults = {}; localStorage.setItem(LS_KEY, JSON.stringify(state)); }
}
```

Include a **coverage sync banner** at the top of the quiz section:
```html
<div id="coverage-sync-banner">
  <strong>Coverage Sync Active</strong> — Quiz results sync to the
  <a href="cognitive-coverage.html">Coverage Dashboard</a> automatically.
</div>
```
## CSS Theme

Use this dark theme. Do NOT use external CSS frameworks or fonts.

```css
:root {
  --bg: #0a1628;
  --surface: #111d2e;
  --surface2: #162438;
  --border: rgba(100,160,220,0.15);
  --text: #d0dff0;
  --text-dim: #7a96b0;
  --accent: #5bb8ff;
  --accent2: #3dd68c;
  --warn: #ffb347;
  --danger: #ff6b6b;
  --code-bg: #0d1926;
  --green-bg: rgba(61,214,140,0.08);
  --amber-bg: rgba(255,179,71,0.08);
  --red-bg: rgba(255,107,107,0.08);
  --blue-bg: rgba(91,184,255,0.06);
}
```

### Syntax Highlighting Classes (inline, no library)
```css
.kw { color: #c792ea; }   /* keywords */
.fn { color: #82aaff; }   /* function/method names */
.str { color: #c3e88d; }  /* strings */
.cm { color: #546e7a; font-style: italic; }  /* comments */
.tp { color: #ffcb6b; }   /* types */
.num { color: #f78c6c; }  /* numbers */
```

Apply as `<span>` elements inside `<pre>` blocks. Do NOT use a syntax highlighting library.

---

## Phase 4: Coverage Manifest (`cognitive-coverage.json`)

Generate a JSON manifest that inventories the project into trackable units.

### Schema

```json
{
  "version": 1,
  "project": "project-name",
  "domain": "codebase|research|documentation|knowledge",
  "generatedAt": "ISO-8601",
  "updatedAt": null,
  "labels": {
    "files": "Source Files",
    "concepts": "Concepts & Patterns",
    "flows": "Data Flows"
  },
  "statusLabels": {
    "files": ["uncovered", "read", "understood"],
    "concepts": ["uncovered", "taught", "quiz-verified"],
    "flows": ["uncovered", "traced", "verified"]
  },
  "summary": {
    "files": { "total": 0, "covered": 0, "percentage": 0 },
    "concepts": { "total": 0, "covered": 0, "percentage": 0 },
    "flows": { "total": 0, "covered": 0, "percentage": 0 },
    "overall": 0
  },
  "files": [{
    "path": "relative/path",
    "status": "uncovered",
    "description": "One-line description",
    "relatedConcepts": ["concept-id"],
    "complexity": "core|supporting|config",
    "guideSection": "section-anchor-id",
    "updatedAt": null
  }],
  "concepts": [{
    "id": "kebab-case-id",
    "name": "Human Name",
    "description": "What and why",
    "status": "uncovered",
    "files": ["file1.ts"],
    "quizIds": ["q1"],
    "guideSection": "section-anchor-id",
    "updatedAt": null
  }],
  "flows": [{
    "id": "flow-id",
    "name": "Flow Name",
    "description": "End-to-end description",
    "status": "uncovered",
    "steps": [{ "description": "Step desc", "file": "source-path" }],
    "quizIds": ["q4"],
    "guideSection": "section-anchor-id",
    "updatedAt": null
  }],
  "quizMapping": {
    "q1": { "concepts": ["concept-id"], "flows": ["flow-id"], "files": ["file-path"] }
  }
}
```

### Manifest Rules
1. Every significant source file/document becomes a file entry
2. Extract 8-15 concepts from the analysis
3. Identify 3-7 end-to-end flows, argument chains, or processes
4. Map every quiz question to concepts, flows, and files via `quizMapping`
5. Use the same section anchor IDs as the teaching guide
6. All statuses start at the first level (uncovered/unread/unseen/unfamiliar/unknown)
7. Include `domain`, `labels`, and `statusLabels` so the dashboard adapts vocabulary

### Optional MCP Access
If the host agent has the Cognitive Coverage MCP server installed, it can query and update this manifest mid-session via tools such as `coverage_summary`, `list_uncovered`, `find_by_file`, and `mark_status`.
The skill itself does not require MCP.
Do not assume MCP is available unless the host exposes those tools.

---

## Phase 5: Coverage Dashboard (`cognitive-coverage.html`)

Generate a self-contained HTML dashboard.

### Dashboard Features
1. **Overall coverage donut chart** (canvas-based)
2. **Three-axis summary bar** with domain-adapted labels and percentage bars
3. **Tabbed interface** — Files, Concepts, Flows, Gap Report
4. **File cards** colored by status (red/amber/green) with complexity badges
5. **Concept cards** with status badges, related files, quiz links, manual status controls
6. **Flow timelines** — horizontal step diagrams per flow
7. **Gap report** — all uncovered items with "Launch Teaching" links to guide sections
8. **Status controls** — clickable buttons to manually set status per item
9. **Export/Import** — load manifest via file input, export updated JSON
10. **localStorage sync** — reads/writes to `cognitive-coverage-state`
11. **Domain-adaptive labels** — reads `labels` and `statusLabels` from manifest

### Bidirectional Integration
- Dashboard "Learn" buttons → `learning-guide.html#section-id`
- Teaching guide quiz answers → localStorage → dashboard reads on load
- Shared localStorage key: `cognitive-coverage-state`

The dashboard MUST read `labels` and `statusLabels` from the manifest to display domain-appropriate terminology.

---

## Writing Style

1. **Teach, don't document.** Use "here's how to think about it" not API-reference style.
2. **Mental models over signatures.** Every major concept needs an analogy.
3. **Trace flows end-to-end.** Show how data/ideas move through the system.
4. **Call out what's surprising.** What would someone misunderstand?
5. **Use the actual source.** Every snippet must come from real content with the real path. Never invent examples.
6. **Keep snippets focused.** Show the 5-15 lines that matter.
7. **Build incrementally.** Each section builds on the previous. Don't forward-reference unexplained concepts.

---

## Cognitive Debt Framing

Always include this callout near the top of the guide:

```html
<div class="warning-box">
  <strong>Why this guide exists.</strong> When AI generates code — or when you inherit
  a project, paper collection, or documentation set you didn't create — you may accept
  it without building a mental model of how it actually works. Over time this creates
  <em>cognitive debt</em>: the system works, but the understanding is missing or flawed.
  This guide closes that gap, one concept at a time, with pointers to the exact source
  material that matters.
</div>
```

---

## File Writing Strategy

The HTML files will typically be 20-50KB. Due to shell/tool limitations with large strings:

1. **Write in parts** — Break each HTML file into 3-6 chunks using file append operations.
2. **Verify** each file after writing: check file size, first lines, last lines.
3. Save all three files in the project root (or user-specified directory):
   - `learning-guide.html`
   - `cognitive-coverage.json`
   - `cognitive-coverage.html`

---

## Quality Checklist

Before delivering, verify:

### Teaching Guide
- [ ] Every significant source is referenced at least once
- [ ] Core flow / argument / algorithm traced end-to-end
- [ ] At least 3 mental model callouts and 3 warning boxes
- [ ] Snippets reference real source paths
- [ ] Quiz has 10+ questions spanning all sections
- [ ] Quiz includes localStorage sync to coverage state
- [ ] HTML is valid and self-contained

### Coverage Manifest
- [ ] Every significant source has an entry
- [ ] 8+ concepts extracted with meaningful descriptions
- [ ] 3+ flows traced with step-by-step breakdowns
- [ ] Every quiz question mapped in quizMapping
- [ ] guideSection anchors match the teaching guide
- [ ] `domain`, `labels`, `statusLabels` fields present

### Coverage Dashboard
- [ ] Donut chart renders correctly
- [ ] Three axis bars display with domain-adapted labels
- [ ] File/concept/flow cards render with status controls
- [ ] Gap report lists uncovered items with "Learn" links
- [ ] Export produces valid JSON
- [ ] localStorage sync reads quiz results on load
- [ ] Status terminology matches the domain
