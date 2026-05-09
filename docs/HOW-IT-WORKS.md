# How Cognitive Coverage Works

## The Problem: Cognitive Debt

Technical debt is well understood — messy code, missing tests, outdated dependencies. But there's a parallel form of debt that's harder to measure: **cognitive debt**.

Cognitive debt is the gap between what a system does and what the people responsible for it actually understand about how it works.

This gap has always existed (inherited codebases, staff turnover, undocumented systems). But generative AI has accelerated it dramatically:

> When a developer writes code from scratch, even messy code, the friction and effort mean they build at least a partial mental model along the way. When an AI generates that same code, the developer may accept it without building the same level of understanding. At scale, across a team, and over time, this creates an accumulation of not knowing across the team. The code works, but the understanding and mental models of how the system behaves and how to reason about it are missing or flawed.

Cognitive Coverage is a system for measuring and closing that gap.

## Agent Compatibility

The skill instructions in `skill/SKILL.md` are plain markdown — no platform-specific APIs or tool bindings. Any AI coding agent that can read files, follow instructions, and write output can use them.

| Agent | How to install |
|-------|---------------|
| GitHub Copilot | Run `install.sh` / `install.ps1` to copy to `~/.copilot/skills/` |
| Claude Code | Copy to `.claude/skills/cognitive-coverage/SKILL.md` (project) or `~/.claude/skills/cognitive-coverage/SKILL.md` (personal) |
| OpenAI Codex | Copy to `.agents/skills/cognitive-coverage/SKILL.md` (project) or `~/.agents/skills/cognitive-coverage/SKILL.md` (personal) |
| Other agents | Copy into whatever instruction mechanism your agent supports |

## The Three Artifacts

Cognitive Coverage produces three coordinated artifacts:

### 1. Teaching Guide (`learning-guide.html`)

A self-contained interactive HTML page that teaches the project from first principles:

- **Structured sections** that build understanding incrementally
- **Source-anchored snippets** — every code block or quote comes from the actual project with file paths
- **Mental model callouts** — analogies that build intuition, not just knowledge
- **Warning boxes** — things that are easy to misunderstand
- **Interactive quiz** — 10-20 questions that verify genuine comprehension
- **Coverage sync** — quiz answers write to localStorage, feeding back to the dashboard

### 2. Coverage Manifest (`cognitive-coverage.json`)

A machine-readable JSON file that inventories the project across three axes:

| Axis | What it tracks | Status progression |
|------|---------------|-------------------|
| **Files** | Source files, papers, documents | uncovered → partial → complete |
| **Concepts** | Algorithms, theories, topics | uncovered → taught → quiz-verified |
| **Flows** | Data flows, argument chains, workflows | uncovered → traced → verified |

The manifest also contains:
- **Domain type** (codebase, research, documentation, knowledge) — determines terminology
- **Quiz mapping** — links each quiz question to the concepts, flows, and files it tests
- **Summary statistics** — pre-computed coverage percentages

### 3. Coverage Dashboard (`cognitive-coverage.html`)

A visual status board that reads the manifest and shows:

- **Overall coverage percentage** with a donut chart
- **Three-axis summary** with color-coded progress bars
- **File heat map** — each file as a card, colored red/amber/green by status
- **Concept cards** — with status badges, related files, and manual status controls
- **Flow timelines** — step-by-step diagrams for each traced flow
- **Gap report** — all uncovered items with "Launch Teaching" buttons

## How the Pieces Connect

```
┌─────────────────────────────────────────────────────────────┐
│                    learning-guide.html                        │
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
1. Dashboard loads manifest → renders coverage status
2. User clicks "Learn" on a gap → opens teaching guide at the relevant section
3. User answers quiz in the guide → correct answers write to localStorage
4. User returns to dashboard → syncs quiz results → upgrades coverage status
5. User can also manually mark items via status buttons on the dashboard
6. Dashboard can export updated manifest as JSON

### MCP Layer

The optional MCP server exposes the manifest to agents over stdio. It reads `./cognitive-coverage.json` by default, or a path passed with `--manifest`.

The server does not regenerate the guide, dashboard, or manifest. It only reads manifest data and lets an agent update one item status with `mark_status`, rewriting the JSON file atomically.

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

### GitHub Copilot

```bash
# Unix/macOS/WSL
bash install.sh

# Windows PowerShell
.\install.ps1
```

### Claude Code

```bash
# Project skill (this project only)
mkdir -p .claude/skills/cognitive-coverage
cp skill/SKILL.md .claude/skills/cognitive-coverage/SKILL.md

# Personal skill (all your projects)
mkdir -p ~/.claude/skills/cognitive-coverage
cp skill/SKILL.md ~/.claude/skills/cognitive-coverage/SKILL.md
```

Then invoke with `/cognitive-coverage` or let Claude auto-detect it.

### OpenAI Codex

```bash
# Project skill (this repo only)
mkdir -p .agents/skills/cognitive-coverage
cp skill/SKILL.md .agents/skills/cognitive-coverage/SKILL.md

# Personal skill (all your projects)
mkdir -p ~/.agents/skills/cognitive-coverage
cp skill/SKILL.md ~/.agents/skills/cognitive-coverage/SKILL.md
```

Then invoke with ```-coverage``` or let Codex auto-detect it.

### Other Agents

Copy `skill/SKILL.md` into your agent's instruction mechanism and ask it to generate cognitive coverage for your project.

## JSON Schema

The `schemas/cognitive-coverage.schema.json` file provides a formal JSON Schema (2020-12 draft) for validating manifests. Use it with any JSON Schema validator to ensure your manifests are well-formed.
