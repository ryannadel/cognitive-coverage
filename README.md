# 🧠 Cognitive Coverage

**Like test coverage, but for understanding.**

Cognitive Coverage is a [GitHub Copilot skill](https://docs.github.com/en/copilot) that generates a measurement and learning system for any project — codebases, research papers, documentation wikis, or general knowledge domains. It produces three coordinated artifacts that help you track, teach, and verify genuine system understanding.

## The Problem

Technical debt is well understood. But there's a parallel form of debt that's harder to measure: **cognitive debt** — the gap between what a system does and what the people responsible for it actually understand.

Generative AI has accelerated this dramatically:

> *When a developer writes code from scratch, even messy code, the friction means they build at least a partial mental model. When an AI generates that same code, the developer may accept it without building the same understanding. At scale, this creates an accumulation of not knowing. The code works, but the mental models are missing.*

Cognitive Coverage closes that gap.

## What It Produces

| Artifact | File | Purpose |
|----------|------|---------|
| **Teaching Guide** | `learning-guide.html` | Interactive HTML with sections, source snippets, mental models, and quiz |
| **Coverage Manifest** | `cognitive-coverage.json` | Machine-readable inventory tracking understanding across 3 axes |
| **Coverage Dashboard** | `cognitive-coverage.html` | Visual status board with gap analysis and teaching guide links |

### Three Coverage Axes

| Axis | Codebase | Research | Documentation |
|------|----------|----------|---------------|
| **Files** | Source files | Papers & sources | Documents & pages |
| **Concepts** | Algorithms & patterns | Theories & methods | Topics & processes |
| **Flows** | Data flows | Argument chains | Workflows & procedures |

Each axis has three status levels (e.g., `uncovered → read → understood`). Status terminology adapts automatically to the domain.

## Quick Start

### Install

```bash
# Unix / macOS / WSL
git clone https://github.com/YOUR_USERNAME/cognitive-coverage.git
cd cognitive-coverage
bash install.sh

# Windows PowerShell
git clone https://github.com/YOUR_USERNAME/cognitive-coverage.git
cd cognitive-coverage
.\install.ps1
```

This copies the skill definition to `~/.copilot/skills/cognitive-coverage/SKILL.md`.

### Use

Open any project in your IDE with GitHub Copilot and say:

> "Generate cognitive coverage for this project"

or

> "Create a learning guide for this codebase"

or

> "Help me understand this research collection"

The skill will:
1. Deep-read your entire project
2. Extract concepts, flows, and key abstractions
3. Generate all three artifacts in the project root

### Manual Install

If you prefer not to clone, just copy `skill/SKILL.md` to:

```
~/.copilot/skills/cognitive-coverage/SKILL.md
```

## How It Works

```
  ┌──────────────────────┐
  │   Teaching Guide     │──── quiz answers ────┐
  │  learning-guide.html │                      │
  └──────────┬───────────┘                      │
             │ "Learn" links                    ▼
  ┌──────────┴───────────┐              localStorage
  │  Coverage Dashboard  │◄──── reads ──────────┘
  │ cognitive-coverage   │
  │       .html          │
  └──────────┬───────────┘
             │ reads
  ┌──────────┴───────────┐
  │  Coverage Manifest   │
  │ cognitive-coverage   │
  │       .json          │
  └──────────────────────┘
```

1. **Dashboard** loads the manifest and renders coverage status
2. **Gap report** shows uncovered items with "Launch Teaching" buttons
3. Clicking a button opens the **teaching guide** at the relevant section
4. Answering quiz questions correctly writes results to **localStorage**
5. Returning to the dashboard **syncs** quiz results and upgrades coverage
6. You can also **manually** set status via buttons on each card
7. **Export** the updated manifest as JSON anytime

See [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md) for the full deep dive.

## Domains

The skill auto-detects the project domain and adapts terminology:

- **`codebase`** — Source code projects (TypeScript, Python, Rust, Go, Java, etc.)
- **`research`** — Paper collections, literature reviews, datasets
- **`documentation`** — Wikis, knowledge bases, runbooks, guides
- **`knowledge`** — General-purpose (anything else)

## Examples

See the `examples/` directory for sample manifests:

- [`examples/codebase/`](examples/codebase/) — REST API project
- [`examples/research/`](examples/research/) — Transformer architecture paper review
- [`examples/documentation/`](examples/documentation/) — Platform engineering wiki

## Schema

The manifest format is defined by a JSON Schema:

```
schemas/cognitive-coverage.schema.json
```

Use it to validate manifests programmatically or in CI.

## Project Structure

```
cognitive-coverage/
├── README.md                          # This file
├── LICENSE                            # MIT
├── CONTRIBUTING.md                    # How to contribute
├── install.sh                         # Unix/macOS/WSL installer
├── install.ps1                        # Windows installer
├── skill/
│   └── SKILL.md                       # The Copilot skill definition
├── schemas/
│   └── cognitive-coverage.schema.json # JSON Schema for manifests
├── examples/
│   ├── codebase/                      # TypeScript REST API example
│   ├── research/                      # ML paper review example
│   └── documentation/                 # Platform wiki example
├── docs/
│   └── HOW-IT-WORKS.md               # Detailed system documentation
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── pull_request_template.md
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas for contributions:
- New domain vocabularies (legal, medical, academic)
- Improved quiz question patterns
- Dashboard visualization improvements
- Additional example manifests
- Integrations with other tools

## License

[MIT](LICENSE)

---

*Built to fight cognitive debt — one concept at a time.*