---
name: cognitive-coverage
license: MIT
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

You generate a **cognitive coverage system** — coordinated artifacts that help people build genuine understanding of projects, codebases, research corpora, or documentation they didn't create.

## Philosophy

> When AI generates code, a developer may accept it without building a mental model.
> When a team inherits a codebase, research corpus, or documentation set, they may skim without
> truly understanding. Over time this creates **cognitive debt** — the system works (or the
> knowledge exists), but the understanding and mental models are missing or flawed.
>
> Cognitive coverage closes that gap by producing structured, quiz-verified learning materials
> anchored to the actual source material.

## The Artifacts

| # | Artifact | File | Purpose |
|---|----------|------|---------|
| 1 | Teaching Guide | `cognitive-coverage/learning-guide.html` | Interactive HTML with sections, code/content snippets, mental models, level controls, quiz |
| 2 | Coverage Manifest | `cognitive-coverage/cognitive-coverage.json` | Machine-readable inventory of what needs to be understood |
| 3 | Coverage Dashboard | `cognitive-coverage/cognitive-coverage.html` | Visual status board with gap analysis and teaching guide links |
| 4 | Artifact Launcher | `cognitive-coverage/cognitive-coverage-open.html` | Lightweight landing page that links to every generated artifact |

Generate them in order: Guide → Manifest → Dashboard → Artifact Launcher. Save them in `cognitive-coverage/` by default unless the user specifies a different output directory. After verification, automatically open `cognitive-coverage/cognitive-coverage-open.html` in the user's default browser.

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

## Phase 1.5: Large Corpus Mode

Use **Large Corpus Mode** when a project is too large for a reliable single-pass guide. This applies to large codebases, monorepos, documentation portals, research collections, and mixed knowledge bases.

### When to switch modes

Before deep reading, estimate corpus size from the file tree:

- Total significant source count
- Directory/package/service boundaries
- Approximate line or token volume
- Number of domains, apps, packages, doc sections, papers, or workflows
- Whether one generated HTML guide would become too broad to teach well

Switch to Large Corpus Mode when the corpus appears too large to read and teach deeply in one context window, or when it naturally contains multiple bounded areas. State that you are using Large Corpus Mode and explain why.

### Large Corpus Workflow

1. **Index first** — inventory all significant sources, classify the domain, and cluster the project into high-level areas.
2. **Rank areas** — prioritize entry points, critical flows, security/data boundaries, high fan-in/fan-out modules, frequently changed sources, canonical docs, or highly referenced papers.
3. **Create modules** — break each area into focused teaching units that can be generated independently.
4. **Generate overview** — make `cognitive-coverage/learning-guide.html` the top-level map, learning path, and cross-area quiz by default.
5. **Generate focused guides** — when needed, write area modules as `learning-guides/<module-id>.html` with their own snippets, mental models, quiz, and localStorage sync.
6. **Track explicit gaps** — mark uncovered areas/modules as gaps instead of pretending the first pass covered everything.

### Run Modes

If the user asks for a partial or incremental run, use one of these modes:

| Mode | Purpose |
|------|---------|
| `index` | Inventory, cluster, and prioritize only; do not generate full teaching modules |
| `overview` | Generate the top-level guide, manifest, and dashboard |
| `area:<id>` | Generate or refresh one focused area/module |
| `refresh` | Re-read changed sources and update affected summaries, modules, concepts, and flows |
| `refresh:since-last-run` | Compare current sources to the last completed run baseline and refresh only impacted coverage items |
| `quiz-only` | Improve comprehension checks without regenerating all teaching content |

When using `refresh:since-last-run`, persist and reuse a deterministic baseline in the manifest:
- If git history is available, diff from the prior baseline commit/ref to the current ref.
- Otherwise compare `sourceHash` values (or modification timestamps when hashes are unavailable).
- Treat all domains the same way: "sources" can be code files, docs pages, papers, runbooks, or other tracked materials.
- If no valid baseline exists, do a normal `refresh`, then write a new baseline.

### Large Corpus Quality Standard

For large projects, "complete" means the first run is honest and navigable, not that every file is deeply taught. Verify that:

- Every significant source is inventoried or intentionally excluded
- Every high-level area has a description, priority, and gap status
- Critical flows are traced across area boundaries where possible
- Generated guides cover the highest-priority areas first
- Uncovered areas/modules are visible in the manifest and dashboard

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

### Learning Level Extraction

Assign every teachable concept, flow, area, module, and quiz question two independent learning levels:

- **Difficulty**: learner background required.
  - `beginner` — assumes little project/domain context; defines vocabulary and purpose.
  - `intermediate` — assumes the reader understands the main nouns and can follow mechanics.
  - `advanced` — assumes project fluency; focuses on edge cases, tradeoffs, failure modes, and extension points.
- **Depth**: amount of detail shown.
  - `overview` — shortest path to orientation and safe navigation.
  - `standard` — enough detail to reason about normal work.
  - `deep-dive` — implementation details, nuanced constraints, and second-order effects.

Difficulty and depth are orthogonal. For example, a beginner deep-dive can patiently unpack one foundational topic in detail, while an advanced overview can summarize an expert-only area quickly. Use `beginner` + `standard` as the default path unless the user requests a different audience.

---
## Phase 3: Teaching Guide Generation

Generate a single self-contained HTML file (`cognitive-coverage/learning-guide.html` by default) with no external dependencies.

### Required Sections

1. **The Big Picture** — Cast of characters / key entities / domain overview.
2. **Architecture / Structure Map** — Visual diagram (text/CSS-based) of how things relate.
3. **Core Model** — Data model, state shape, entity relationships, or conceptual framework.
4. **Core Algorithm / Decision Flow / Central Argument** — The most important behavior or reasoning chain, traced step by step.
5. **[3-6 additional concept sections]** — One per major subsystem, theory, or topic area, each with:
   - Snippets from the actual source material (with source path labels)
   - A "Mental Model" callout with an analogy
   - A "Warning/Key Insight" box for things easy to misunderstand
6. **Interactive Knowledge Quiz** — 10-20 questions testing comprehension across the generated difficulty/depth levels

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

#### Anchor and Navigation Integrity

The sidebar is a map of the actual guide, not a static template. Build it from the
sections you really emit in the document.

Rules:
1. Every sidebar link target (`href="#section-id"`) MUST match an actual
   `<section id="section-id">` in the same `learning-guide.html`.
2. Every major visible teaching section MUST appear in the sidebar exactly once.
   Do not include quiz cards, filter controls, banners, or internal sub-elements as
   top-level navigation entries.
3. If you rename, merge, split, or omit a section, update the sidebar label and
   anchor at the same time. Never leave placeholder or stale entries such as
   anchors copied from an earlier guide.
4. Use one canonical kebab-case section ID for each section and reuse it anywhere
   else that needs to link to that section, including manifest `guideSection`
   values and dashboard "Learn" links.
5. Before delivery, compare the set of sidebar anchors against the set of guide
   section IDs. The sets must match for all major teaching sections.

#### Learning Level Controls
```html
<div class="level-controls" aria-label="Learning level controls">
  <label>Difficulty
    <select id="difficulty-filter" onchange="applyLearningLevelFilters()">
      <option value="beginner">Beginner</option>
      <option value="intermediate">Intermediate</option>
      <option value="advanced">Advanced</option>
    </select>
  </label>
  <label>Depth
    <select id="depth-filter" onchange="applyLearningLevelFilters()">
      <option value="overview">Overview</option>
      <option value="standard" selected>Standard</option>
      <option value="deep-dive">Deep-dive</option>
    </select>
  </label>
</div>
```

Mark level-aware sections with attributes:
```html
<section id="auth" data-difficulty="intermediate" data-depth="standard">
  ...
</section>
```

The guide should remain useful with JavaScript disabled: default content must be visible, and filters should progressively enhance the page rather than hide everything.

```javascript
function applyLearningLevelFilters() {
  var difficulty = document.getElementById('difficulty-filter').value;
  var depth = document.getElementById('depth-filter').value;
  document.querySelectorAll('[data-difficulty][data-depth]').forEach(function(el) {
    var visible = el.dataset.difficulty === difficulty && el.dataset.depth === depth;
    var isDefault = el.dataset.difficulty === 'beginner' && el.dataset.depth === 'standard';
    el.hidden = !(visible || isDefault);
  });
}
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
7. **Level tags** — every question has `data-difficulty` and `data-depth`
8. **Mix question types**:
   - Structure questions (where is X defined/discussed?)
   - Logic questions (what does this function compute / what does this theory claim?)
   - Behavior questions (what happens when X occurs / what follows from Y?)
   - Boundary questions (what prevents X / what are the limits?)
   - System thinking questions (if you change X, what cascading effect?)
   - Application questions (if you needed to add/change/use X, which files/concepts/flows would
     you touch and what would you watch for?)
9. **localStorage sync** — write quiz results to shared coverage state, including difficulty/depth metadata

System thinking questions test second-order consequences. Application questions test the action a
reader would take first. Include at least one application question when the domain has concrete use
cases.

Balance quiz coverage across levels:

- Beginner questions should test vocabulary, orientation, and safe navigation.
- Intermediate questions should test normal mechanics and common change paths.
- Advanced questions should test boundaries, failure modes, tradeoffs, and cascading effects.
- Overview questions should validate the map; standard questions should validate reasoning; deep-dive questions should validate detailed comprehension.

#### Quiz Implementation
```html
<div class="quiz-card" data-quiz="q1" data-difficulty="beginner" data-depth="overview">
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

<div class="quiz-card" data-quiz="q5">
  <h4>Q5: Application</h4>
  <p class="question">If you needed to add SSO login, which source areas would you inspect first?</p>
  <ul class="quiz-options">
    <li onclick="selectAnswer(this,'q5',false)">Only the database schema, because login is persisted there</li>
    <li onclick="selectAnswer(this,'q5',true)">The auth middleware, user routes, server middleware chain, and auth flow</li>
    <li onclick="selectAnswer(this,'q5',false)">Only the route handler, because middleware already handles all auth modes</li>
  </ul>
  <div class="quiz-explanation" id="q5-exp">
    Application questions should map to every relevant source, for example
    <code>src/middleware/auth.ts</code>, <code>src/routes/users.ts</code>, and the auth flow.
  </div>
</div>
```

Map application questions to the files, concepts, and flows needed to take the action:
```json
"q5": {
  "type": "application",
  "question": "If you needed to add SSO login, which files and flows would you inspect first?",
  "concepts": ["architecture", "auth", "rest-patterns"],
  "flows": ["auth-flow", "crud-flow"],
  "files": ["src/server.ts", "src/routes/users.ts", "src/middleware/auth.ts", "src/db/schema.ts"]
}
```

#### Quiz JavaScript (with Coverage Sync)
```javascript
var score=0, answered=0, total=N, answeredSet=new Set();
var LS_KEY='cognitive-coverage-state';

function syncQuizResult(qId, isCorrect) {
  var card = document.querySelector('[data-quiz="'+qId+'"]');
  var state;
  try { state = JSON.parse(localStorage.getItem(LS_KEY)) || {}; } catch(e) { state = {}; }
  if (!state.quizResults) state.quizResults = {};
  state.quizResults[qId] = {
    correct: isCorrect,
    difficulty: card && card.dataset.difficulty,
    depth: card && card.dataset.depth,
    timestamp: new Date().toISOString()
  };
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

## Phase 4: Coverage Manifest (`cognitive-coverage/cognitive-coverage.json`)

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
    "flows": ["uncovered", "traced", "verified"],
    "areas": ["unmapped", "mapped", "understood"],
    "modules": ["planned", "generated", "verified"]
  },
  "largeCorpus": {
    "enabled": false,
    "reason": null,
    "runMode": "overview",
    "sourceCount": 0,
    "estimatedTokens": 0,
    "generatedModules": [],
    "pendingModules": []
  },
  "incremental": {
    "enabled": true,
    "strategy": "git-diff|source-hash|modified-time|manual",
    "baseline": {
      "capturedAt": "ISO-8601|null",
      "gitRef": "optional-commit-or-ref",
      "manifestUpdatedAt": "ISO-8601|null",
      "sourceCount": 0
    },
    "lastRefresh": {
      "mode": "refresh|refresh:since-last-run|overview|area:<id>|quiz-only|index|null",
      "ranAt": "ISO-8601|null",
      "changedSources": ["relative/source-path"],
      "affectedAreas": ["area-id"],
      "affectedModules": ["module-id"]
    }
  },
  "learningLevels": {
    "difficulty": [
      { "id": "beginner", "label": "Beginner", "description": "Defines vocabulary and purpose with minimal assumed context" },
      { "id": "intermediate", "label": "Intermediate", "description": "Explains mechanics for readers who know the main nouns" },
      { "id": "advanced", "label": "Advanced", "description": "Covers edge cases, tradeoffs, and extension points" }
    ],
    "depth": [
      { "id": "overview", "label": "Overview", "description": "Shortest path to orientation and safe navigation" },
      { "id": "standard", "label": "Standard", "description": "Enough detail to reason about normal work" },
      { "id": "deep-dive", "label": "Deep-dive", "description": "Implementation details and second-order effects" }
    ],
    "defaultDifficulty": "beginner",
    "defaultDepth": "standard"
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
    "difficulty": "beginner|intermediate|advanced",
    "depth": "overview|standard|deep-dive",
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
    "difficulty": "beginner|intermediate|advanced",
    "depth": "overview|standard|deep-dive",
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
    "difficulty": "beginner|intermediate|advanced",
    "depth": "overview|standard|deep-dive",
    "guideSection": "section-anchor-id",
    "updatedAt": null
  }],
  "areas": [{
    "id": "area-id",
    "name": "Area Name",
    "description": "Major package, service, doc section, paper cluster, or knowledge theme",
    "status": "unmapped",
    "difficulty": "beginner|intermediate|advanced",
    "depth": "overview|standard|deep-dive",
    "priority": "critical|high|medium|low",
    "rationale": "Why this area matters in the learning path",
    "guideSection": "section-anchor-id",
    "moduleIds": ["module-id"],
    "dependsOn": [],
    "updatedAt": null
  }],
  "modules": [{
    "id": "module-id",
    "areaId": "area-id",
    "name": "Focused Module Name",
    "description": "A teachable unit inside an area",
    "status": "planned",
    "difficulty": "beginner|intermediate|advanced",
    "depth": "overview|standard|deep-dive",
    "priority": "critical|high|medium|low",
    "guideFile": "learning-guides/module-id.html",
    "guideSection": "section-anchor-id",
    "filePaths": ["source-path"],
    "conceptIds": ["concept-id"],
    "flowIds": ["flow-id"],
    "dependsOn": [],
    "updatedAt": null
  }],
  "sourceSummaries": [{
    "path": "relative/source-path",
    "summary": "Persistent source synopsis for incremental refresh",
    "whyItMatters": "Why this source affects understanding",
    "areaId": "area-id",
    "moduleId": "module-id",
    "sourceHash": "optional-hash-or-revision",
    "updatedAt": null
  }],
  "quizMapping": {
    "q1": {
      "concepts": ["concept-id"],
      "flows": ["flow-id"],
      "files": ["file-path"],
      "difficulty": "beginner",
      "depth": "overview",
      "questionType": "structure",
      "prerequisites": []
    }
  }
}
```

### Manifest Rules
1. Every significant source file/document becomes a file entry
2. Extract 8-15 concepts from the analysis
3. Identify 3-7 end-to-end flows, argument chains, or processes
4. Map every quiz question to concepts, flows, and files via `quizMapping`
5. Use the same canonical section anchor IDs as the teaching guide; every
   `guideSection` value MUST point to an actual major `<section id="...">` in
   `learning-guide.html`
6. All statuses start at the first level (uncovered/unread/unseen/unfamiliar/unknown)
7. Include `domain`, `labels`, and `statusLabels` so the dashboard adapts vocabulary
8. Include `learningLevels` and tag teachable items plus quiz mappings with `difficulty` and `depth`
9. For incremental runs, persist an `incremental` baseline and record changed/affected sources in `lastRefresh`

### Optional MCP Access
If the host agent has the Cognitive Coverage MCP server installed, it can query and update this manifest mid-session via tools such as `coverage_summary`, `list_uncovered`, `find_by_file`, and `mark_status`.
The skill itself does not require MCP.
Do not assume MCP is available unless the host exposes those tools.

---

## Phase 5: Coverage Dashboard (`cognitive-coverage/cognitive-coverage.html`)

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
12. **Learning-level filters** — reads `learningLevels` and lets users filter gaps and quiz progress by difficulty/depth
13. **Level badges** — show difficulty/depth on files, concepts, flows, areas, modules, and quiz-linked cards

For Large Corpus Mode, add:

14. **Area overview** — cards for each area with priority, status, and module count
15. **Module drill-down** — links from area cards to focused guide files and sections
16. **Dependency-aware gaps** — show which uncovered areas block the most downstream understanding
17. **Next learning targets** — recommend the highest-priority uncovered areas, modules, concepts, or flows, respecting selected difficulty/depth when possible

### Bidirectional Integration
- Dashboard "Learn" buttons → `learning-guide.html#section-id`
- Teaching guide quiz answers → localStorage → dashboard reads on load
- Shared localStorage key: `cognitive-coverage-state`

Dashboard "Learn" links MUST use only canonical section IDs that exist in the generated
teaching guide. Do not render links to placeholder, omitted, or renamed sections.
The dashboard MUST read `labels` and `statusLabels` from the manifest to display domain-appropriate terminology.
The dashboard MUST read `learningLevels` when present, render difficulty/depth controls, and preserve existing behavior when the field is absent.
When `areas` or `modules` are present, the dashboard MUST render them as the top-level navigation layer before files/concepts/flows.

---

## Phase 6: Artifact Launcher (`cognitive-coverage/cognitive-coverage-open.html`)

Generate a small self-contained HTML landing page that makes every output easy to open after generation.

### Launcher Requirements
1. Link to `learning-guide.html` as the primary "Start learning" action.
2. Link to `cognitive-coverage.html` as the dashboard/status action.
3. Link to `cognitive-coverage.json` as the machine-readable manifest.
4. Include a short "Generated files" section listing all artifact filenames.
5. Keep the file dependency-free and safe to open directly from disk.
6. Use relative links only, so the artifact set remains portable if the user moves the folder.

### Automatic Open
After writing and verifying all artifacts, attempt to open `cognitive-coverage/cognitive-coverage-open.html` automatically using the host OS default browser:

```bash
# macOS
open cognitive-coverage/cognitive-coverage-open.html

# Windows PowerShell
Start-Process .\cognitive-coverage\cognitive-coverage-open.html

# Linux / WSL
xdg-open cognitive-coverage/cognitive-coverage-open.html
```

Use the command appropriate for the current environment. If automatic opening fails because the environment is headless, remote, or lacks a browser, do not treat that as generation failure. Instead, clearly tell the user which file to open manually and include the absolute or relative path.

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

## File Writing Strategy

The HTML files will typically be 20-50KB and may be larger in Large Corpus Mode. Avoid shell quoting failures by using this order of preference:

1. **Use native file-edit/write tools first** — If the host provides a file creation or patch tool, write the artifact with that tool instead of embedding a huge HTML string in a shell command.
2. **If shell is the only option, use a non-interactive writer** — Write a short temporary script outside the target project or use a language runtime to decode safe chunks. Pass chunks as JSON strings or base64 data; do not rely on interactive heredocs, unescaped quotes, or giant one-line shell strings.
3. **Keep chunks small and append deterministically** — Break each HTML file into chunks under roughly 8KB, write them in order, and fail loudly if any write command fails.
4. **Never stop after analysis just because the first write method fails** — Switch to the next writing method and complete the required artifacts.
5. **Clean up temporary writers** — Remove any temporary script after the artifacts are verified. Do not leave helper scripts in the target project unless the user explicitly asks for them.
6. **Verify** each file after writing: check that it exists, has non-zero size, starts with `<!DOCTYPE html>` for HTML artifacts, and ends with `</html>`.
7. Save all artifacts in `cognitive-coverage/` by default, or in the user-specified output directory:
   - `learning-guide.html`
   - `cognitive-coverage.json`
   - `cognitive-coverage.html`
   - `cognitive-coverage-open.html`
8. In Large Corpus Mode, also create focused modules under:
   - `learning-guides/<module-id>.html`
9. **Open the launcher** — Once verification passes, open `cognitive-coverage/cognitive-coverage-open.html` (or the equivalent launcher path in the user-specified output directory) automatically using the current OS default-browser command.

If a write attempt stalls or fails, report the failed method only after trying a safer fallback. The expected successful outcome is always the completed artifact files, not just a completed analysis.

### Shell-Safe Artifact Protocol

Follow this protocol when writing artifacts through a terminal:

1. **Identify the shell before choosing syntax.** PowerShell, Bash, and cmd.exe have different multiline rules.
2. **Never use Bash heredoc syntax in PowerShell.** Commands like `python - <<'PY'`, `cat <<EOF`, and `tee <<EOF` are Bash-only and can stall or fail in PowerShell.
3. **Do not place full HTML documents inside one shell argument.** Long quoted strings are fragile and hard to recover when quoting breaks.
4. **Use a temporary writer only as a controlled fallback.** Put it outside the target project when possible, keep it short, and delete it after the artifacts are verified.
5. **Write all required artifacts before opening anything.** Do not open the browser or report success until the guide, manifest, dashboard, and launcher all exist.

Preferred terminal fallback patterns:

```powershell
# PowerShell-safe chunk writing. Use Set-Content for the first chunk and
# Add-Content for later chunks. Do not use Bash-style << heredocs here.
$out = Join-Path (Get-Location) 'cognitive-coverage'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$target = Join-Path $out 'learning-guide.html'
Set-Content -Path $target -Encoding utf8 -Value @'
<!doctype html>
<!-- first chunk, keep under roughly 8KB -->
'@
Add-Content -Path $target -Encoding utf8 -Value @'
<!-- next chunk -->
</html>
'@
```

```bash
# Bash-safe chunk writing. Only use this in an actual Bash/sh environment.
mkdir -p cognitive-coverage
cat > cognitive-coverage/learning-guide.html <<'HTML'
<!doctype html>
<!-- first chunk, keep under roughly 8KB -->
HTML
cat >> cognitive-coverage/learning-guide.html <<'HTML'
<!-- next chunk -->
</html>
HTML
```

If the active shell is ambiguous or previous multiline writing failed, prefer a base64 or JSON-chunk writer in the available runtime:

```python
from pathlib import Path

out = Path("cognitive-coverage")
out.mkdir(exist_ok=True)
target = out / "learning-guide.html"
chunks = [
    "<!doctype html>\n",
    "<!-- next escaped chunk -->\n</html>\n",
]
target.write_text("".join(chunks), encoding="utf-8")
```

---

## Quality Checklist

Before delivering, verify:

### Teaching Guide
- [ ] Every significant source is referenced at least once
- [ ] Core flow / argument / algorithm traced end-to-end
- [ ] At least 3 mental model callouts and 3 warning boxes
- [ ] Snippets reference real source paths
- [ ] Every sidebar `href="#..."` target matches an actual major `<section id="...">`
- [ ] Every major visible teaching section appears in the sidebar exactly once
- [ ] Quiz has 10+ questions spanning all sections
- [ ] Quiz questions include difficulty/depth metadata and cover the intended learner path
- [ ] Quiz includes localStorage sync to coverage state
- [ ] Level controls work as progressive enhancement and leave default content visible
- [ ] HTML is valid and self-contained

### Coverage Manifest
- [ ] Every significant source has an entry
- [ ] 8+ concepts extracted with meaningful descriptions
- [ ] 3+ flows traced with step-by-step breakdowns
- [ ] Every quiz question mapped in quizMapping
- [ ] `learningLevels` defines difficulty/depth defaults and quiz mappings include level tags
- [ ] Every `guideSection` anchor matches an actual major teaching guide section
- [ ] `domain`, `labels`, `statusLabels` fields present
- [ ] Large Corpus Mode manifests include `areas`, `modules`, priorities, and source summaries when the corpus is too large for one pass

### Coverage Dashboard
- [ ] Donut chart renders correctly
- [ ] Three axis bars display with domain-adapted labels
- [ ] File/concept/flow cards render with status controls
- [ ] Gap report lists uncovered items with "Learn" links
- [ ] Every "Learn" link points to an actual canonical teaching guide section
- [ ] Export produces valid JSON
- [ ] localStorage sync reads quiz results on load
- [ ] Status terminology matches the domain
- [ ] Difficulty/depth badges and filters work when `learningLevels` is present

### Artifact Launcher
- [ ] Links to the teaching guide, dashboard, and manifest with relative paths
- [ ] Explains which artifact to open first
- [ ] Opens automatically after generation, or the user is given a clear manual path if auto-open is unavailable
