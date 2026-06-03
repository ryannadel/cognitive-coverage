# How Cognitive Coverage Works

## The Problem: Cognitive Debt

Technical debt is well understood — messy code, missing tests, outdated dependencies. But there's a parallel form of debt that's harder to measure: **cognitive debt**.

Cognitive debt is the gap between what a system does and what the people responsible for it actually understand about how it works.

This gap has always existed (inherited codebases, staff turnover, undocumented systems). But generative AI has accelerated it dramatically:

> When a developer writes code from scratch, even messy code, the friction and effort mean they build at least a partial mental model along the way. When an AI generates that same code, the developer may accept it without building the same level of understanding. At scale, across a team, and over time, this creates an accumulation of not knowing across the team. The code works, but the understanding and mental models of how the system behaves and how to reason about it are missing or flawed.

Cognitive Coverage is a system for measuring and closing that gap.

## Agent Compatibility

The skill instructions in `skills/cognitive-coverage/SKILL.md` are plain markdown — no platform-specific APIs or tool bindings. Any AI coding agent that can read files, follow instructions, and write output can use them.

| Agent | How to install |
|-------|---------------|
| GitHub Copilot | `gh skill install ryannadel/cognitive-coverage cognitive-coverage --agent github-copilot --scope user` |
| Claude Code | `npx skills add ryannadel/cognitive-coverage --skill cognitive-coverage -g -a claude-code` |
| OpenAI Codex | `npx skills add ryannadel/cognitive-coverage --skill cognitive-coverage -g -a codex` |
| Other agents | Use `skills/cognitive-coverage/SKILL.md` as the source skill file |

## The Artifacts

Cognitive Coverage produces coordinated artifacts:

### 1. Teaching Guide (`cognitive-coverage/learning-guide.html`)

A self-contained interactive HTML page that teaches the project from first principles:

- **Structured sections** that build understanding incrementally
- **Learning-level controls** for difficulty (`beginner`, `intermediate`, `advanced`) and depth (`overview`, `standard`, `deep-dive`)
- **Source-anchored snippets** — every code block or quote comes from the actual project with file paths
- **Mental model callouts** — analogies that build intuition, not just knowledge
- **Warning boxes** — things that are easy to misunderstand
- **Interactive quiz** — 10-20 questions that verify genuine comprehension
- **Coverage sync** — quiz answers write to localStorage, feeding back to the dashboard

### 2. Coverage Manifest (`cognitive-coverage/cognitive-coverage.json`)

A machine-readable JSON file that inventories the project across three axes:

| Axis | What it tracks | Status progression |
|------|---------------|-------------------|
| **Files** | Source files, papers, documents | uncovered → partial → complete |
| **Concepts** | Algorithms, theories, topics | uncovered → taught → quiz-verified |
| **Flows** | Data flows, argument chains, workflows | uncovered → traced → verified |

The manifest also contains:
- **Domain type** (codebase, research, documentation, knowledge) — determines terminology
- **Quiz mapping** — links each quiz question to the concepts, flows, and files it tests
- **Learning levels** — optional difficulty/depth metadata for guide sections, quiz questions, and learning targets
- **Summary statistics** — pre-computed coverage percentages
- **Optional hierarchy** — areas, modules, dependencies, priorities, and source summaries for large corpora

### 3. Coverage Dashboard (`cognitive-coverage/cognitive-coverage.html`)

A visual status board that reads the manifest and shows:

- **Overall coverage percentage** with a donut chart
- **Three-axis summary** with color-coded progress bars
- **File heat map** — each file as a card, colored red/amber/green by status
- **Concept cards** — with status badges, related files, and manual status controls
- **Flow timelines** — step-by-step diagrams for each traced flow
- **Gap report** — all uncovered items with "Launch Teaching" buttons
- **Difficulty/depth filters** — narrow the guide, quiz progress, and gaps to the learner's current path

### 4. Artifact Launcher (`cognitive-coverage/cognitive-coverage-open.html`)

A lightweight landing page that links to the teaching guide, dashboard, and manifest. The coding agent opens this file automatically after generation so users can start from one obvious entry point. By default, all generated outputs live together in the target project's `cognitive-coverage/` folder.

## Artifact Writing Reliability

The skill requires four generated files, so artifact writing must be treated as part of the deliverable rather than a best-effort final step. The most common failure mode is using shell syntax that does not match the active terminal, especially Bash heredocs such as `python - <<'PY'` while running in PowerShell.

The skill now instructs agents to:

- Detect the active shell before choosing multiline syntax
- Avoid Bash heredocs in PowerShell
- Avoid placing full HTML documents in one giant quoted shell argument
- Prefer native file-write tools, then safe chunked terminal writes, then short temporary writer scripts
- Keep HTML chunks small and verify every artifact before reporting success
- Generate the launcher only after the guide, manifest, and dashboard are present

This makes artifact generation recoverable: if one write method fails, the agent should switch to a safer fallback and still complete the files.

## How the Pieces Connect

```
┌─────────────────────────────────────────────────────────────┐
│              cognitive-coverage-open.html                     │
│        Opens automatically and links to every artifact         │
└────────────────────────────────────┬──────────────────────────┘
                                     │ links
                                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    learning-guide.html                      │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐  │
│  │ Sections │  │ Snippets │  │ Warnings │  │ Quiz + Sync │  │
│  └─────────┘  └──────────┘  └──────────┘  └──────┬──────┘  │
│                                                    │         │
└────────────────────────────────────────────────────┼─────────┘
                                                     │ writes
                                                     ▼
                                              localStorage
                                        (cognitive-coverage-state)
                                                     ▲
                                                     │ reads
┌────────────────────────────────────────────────────┼─────────┐
│                 cognitive-coverage.html             │         │
│  ┌────────┐  ┌──────────┐  ┌───────┐  ┌──────────┼──────┐  │
│  │ Donut  │  │ Axis Bars│  │ Cards │  │ Sync Engine     │  │
│  └────────┘  └──────────┘  └───────┘  └─────────────────┘  │
│       ▲           ▲            ▲                             │
│       └───────────┴────────────┘                             │
│                    │ reads                                    │
└────────────────────┼─────────────────────────────────────────┘
                     │
              cognitive-coverage.json
              (source of truth manifest)
                     ▲
                     │ reads / writes
┌────────────────────┼─────────────────────────────────────────┐
│              optional MCP stdio server                         │
│  list_uncovered  get_concept  get_flow  coverage_summary       │
│  find_by_file    mark_status                                   │
└───────────────────────────────────────────────────────────────┘
```

**Data flow:**
1. Agent opens artifact launcher automatically after generation
2. User opens dashboard or learning guide from the launcher
3. Dashboard loads manifest → renders coverage status
4. User clicks "Learn" on a gap → opens teaching guide at the relevant section
5. User answers quiz in the guide → correct answers write to localStorage
6. User returns to dashboard → syncs quiz results → upgrades coverage status
7. User can also manually mark items via status buttons on the dashboard
8. Dashboard can export updated manifest as JSON

## Learning Levels

Cognitive Coverage can adapt the same material to different learner needs without generating separate artifact sets by default. The manifest may include a `learningLevels` block with two independent axes:

| Axis | Default levels | Meaning |
|------|----------------|---------|
| **Difficulty** | `beginner`, `intermediate`, `advanced` | How much background the reader is expected to have |
| **Depth** | `overview`, `standard`, `deep-dive` | How much detail the material should reveal |

Difficulty and depth are intentionally separate. A beginner deep-dive can patiently unpack a foundational idea, while an advanced overview can summarize an expert-only subsystem quickly. The generated guide defaults to `beginner` + `standard` unless the user or manifest specifies otherwise.

Level metadata appears on files, concepts, flows, areas, modules, and quiz mappings. The guide uses it for progressive disclosure, the dashboard uses it for badges and gap filters, and MCP tools can return or filter next learning targets by difficulty/depth.

## Large Corpus Mode

Small projects can be taught in one pass. Large codebases, documentation portals, research collections, and hybrid knowledge bases need a staged workflow because "read everything and produce one guide" becomes unreliable and shallow.

Large Corpus Mode adds a hierarchy above the existing files/concepts/flows axes:

| Layer | Purpose |
|-------|---------|
| **Areas** | Major packages, services, bounded contexts, documentation sections, research themes, or knowledge domains |
| **Modules** | Focused teaching units inside an area, often emitted as `learning-guides/<module-id>.html` |
| **Dependencies** | Learning order and invalidation relationships between areas, modules, concepts, flows, and files |
| **Source summaries** | Persistent per-source notes that support incremental refreshes |

The recommended workflow is:

1. **Index** the corpus and cluster it into areas
2. **Prioritize** entry points, critical flows, security/data boundaries, highly referenced sources, and frequently changed areas
3. **Generate an overview** in `cognitive-coverage/learning-guide.html`
4. **Generate focused modules** for the highest-priority areas
5. **Expose gaps** in `cognitive-coverage/cognitive-coverage.html` so uncovered areas are visible instead of implied complete
6. **Refresh incrementally** when source hashes or modification times show that a learned area changed

Large Corpus Mode supports these run modes:

| Mode | Purpose |
|------|---------|
| `index` | Inventory, cluster, and prioritize only |
| `overview` | Generate the top-level guide, manifest, and dashboard |
| `area:<id>` | Generate or refresh one focused area/module |
| `refresh` | Re-read changed sources and update affected summaries |
| `refresh:since-last-run` | Diff from the last saved baseline and refresh only impacted sources and linked coverage items |
| `quiz-only` | Improve comprehension checks without regenerating all teaching content |

For deterministic incremental refreshes, manifests can store an `incremental` block with baseline metadata (timestamp, optional git ref, and source count) and the latest refresh impact lists (`changedSources`, `affectedAreas`, `affectedModules`). This works for any domain because "sources" include code files, documents, papers, runbooks, and other tracked corpus items.

The key quality rule is honesty: a first pass can be valuable without claiming complete understanding. High-priority areas should be taught; lower-priority or unvisited areas should remain explicit gaps.

### MCP Layer

The optional MCP server exposes the manifest to agents over stdio. It reads `./cognitive-coverage.json` by default, or a path passed with `--manifest`.

The server does not regenerate the guide, dashboard, or manifest. It only reads manifest data and lets an agent update one item status with `mark_status`, rewriting the JSON file atomically.
When a manifest includes large-corpus hierarchy, the server can also list areas, fetch one area with its grouped items, and recommend the next uncovered learning targets.

## Domain Adaptation

The system automatically adapts its vocabulary based on project type:

| Domain | Files axis | Concepts axis | Flows axis |
|--------|-----------|---------------|------------|
| Codebase | Source Files | Concepts & Patterns | Data Flows |
| Research | Papers & Sources | Theories & Methods | Argument Chains |
| Documentation | Documents & Pages | Topics & Processes | Workflows & Procedures |
| Knowledge | Sources | Key Ideas | Connections & Sequences |

Status labels also adapt (e.g., "uncovered/read/understood" for code vs "unread/skimmed/comprehended" for research).

## Installation

### Standard Skill Installers

```bash
# Install with npx skills
npx skills add ryannadel/cognitive-coverage --skill cognitive-coverage -g -a codex

# Install with GitHub CLI
gh skill install ryannadel/cognitive-coverage cognitive-coverage --agent codex --scope user
```

Use `--agent github-copilot`, `--agent claude-code`, or `--agent codex` with `gh skill install` to choose a host. With `npx skills`, change the `-a` value to the agent you want. Use `--scope project` or omit `-g` for project-level installs.

### Updates

```bash
# If installed with npx skills
npx skills update cognitive-coverage -g -y

# If installed with gh skill
gh skill update cognitive-coverage
```

If you installed with `npx skills` into project scope, omit `-g` when updating.

Then ask your agent to generate cognitive coverage for your project.

## JSON Schema

The `schemas/cognitive-coverage.schema.json` file provides a formal JSON Schema (2020-12 draft) for validating manifests. Use it with any JSON Schema validator to ensure your manifests are well-formed.
