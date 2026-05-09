# Cognitive Coverage

**Like test coverage, but for understanding.**

Cognitive Coverage is a skill for AI coding agents that generates a measurement and learning system for any project — codebases, research papers, documentation wikis, or general knowledge domains. It produces three coordinated artifacts that help you track, teach, and verify genuine system understanding.

Works with any AI coding agent that supports custom instructions, including:
- **GitHub Copilot** (as a Copilot skill)
- **Claude Code** (as a custom command or CLAUDE.md instructions)
- **OpenAI Codex** (as a system prompt)
- **Any LLM-powered agent** with file access and markdown instruction support

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

### Large Codebases and Knowledge Bases

For large projects, Cognitive Coverage switches from a single exhaustive pass to **Large Corpus Mode**:

1. Inventory the full corpus first
2. Cluster sources into areas and focused learning modules
3. Prioritize critical flows, entry points, security/data boundaries, and highly referenced material
4. Generate `learning-guide.html` as the overview map
5. Generate optional `learning-guides/<module-id>.html` pages for deeper modules
6. Keep uncovered areas visible as explicit dashboard gaps

This keeps the first run honest and useful: high-priority understanding is taught immediately, while lower-priority areas remain tracked instead of being hidden inside an oversized guide.

### Three Coverage Axes

| Axis | Codebase | Research | Documentation |
|------|----------|----------|---------------|
| **Files** | Source files | Papers & sources | Documents & pages |
| **Concepts** | Algorithms & patterns | Theories & methods | Topics & processes |
| **Flows** | Data flows | Argument chains | Workflows & procedures |

Each axis has three status levels (e.g., `uncovered → read → understood`). Status terminology adapts automatically to the domain.

## Quick Start

### Option 1: GitHub Copilot

```bash
# Unix / macOS / WSL
git clone https://github.com/ryannadel/cognitive-coverage.git
cd cognitive-coverage
bash install.sh

# Windows PowerShell
git clone https://github.com/ryannadel/cognitive-coverage.git
cd cognitive-coverage
.\install.ps1
```

This copies the skill definition to `~/.copilot/skills/cognitive-coverage/SKILL.md`.

Then open any project with Copilot and say:

> "Generate cognitive coverage for this project"

### Option 2: Claude Code

Claude Code has native skill support. Install as a project or personal skill:

```bash
# Project skill (this project only)
mkdir -p .claude/skills/cognitive-coverage
cp skill/SKILL.md .claude/skills/cognitive-coverage/SKILL.md

# Personal skill (all your projects)
mkdir -p ~/.claude/skills/cognitive-coverage
cp skill/SKILL.md ~/.claude/skills/cognitive-coverage/SKILL.md
```

Then invoke with `/cognitive-coverage` or just ask Claude to "generate cognitive coverage" — it will auto-detect the skill from the description.

See the [Claude Code skills docs](https://code.claude.com/docs/en/skills) for more on skill placement and configuration.

### Option 3: OpenAI Codex

Codex has native skill support via the `.agents/skills/` directory:

```bash
# Project skill (this repo only)
mkdir -p .agents/skills/cognitive-coverage
cp skill/SKILL.md .agents/skills/cognitive-coverage/SKILL.md

# Personal skill (all your projects)
mkdir -p ~/.agents/skills/cognitive-coverage
cp skill/SKILL.md ~/.agents/skills/cognitive-coverage/SKILL.md
```

Then invoke with ```-coverage``` or let Codex auto-detect it from the description. Works in Codex CLI, IDE extension, and Codex app.

See the [Codex skills docs](https://developers.openai.com/codex/skills) for more on skill placement and configuration.

### Option 4: Any Other Agent

The skill is just a markdown file (`skill/SKILL.md`) that tells an AI agent how to analyze a project and generate the three artifacts. If your agent can:

1. Read files in a project directory
2. Follow markdown instructions
3. Write output files

...then it can run Cognitive Coverage. Copy `skill/SKILL.md` into whatever instruction mechanism your agent supports.

### Manual Install

If you prefer not to clone, just copy `skill/SKILL.md` to the appropriate location for your agent:

| Agent | Location |
|-------|----------|
| GitHub Copilot | `~/.copilot/skills/cognitive-coverage/SKILL.md` |
| Claude Code | `.claude/skills/cognitive-coverage/SKILL.md` (project) or `~/.claude/skills/cognitive-coverage/SKILL.md` (personal) |
| OpenAI Codex | `.agents/skills/cognitive-coverage/SKILL.md` (project) or `~/.agents/skills/cognitive-coverage/SKILL.md` (personal) |
| Other | Wherever your agent reads instruction files |

## MCP Integration (optional)

Cognitive Coverage also ships an optional MCP stdio server for agents that can call tools during a session. The skill still works without MCP; the server only exposes an existing `cognitive-coverage.json` manifest.

```bash
uv --directory /path/to/cognitive-coverage/mcp run python server.py \
  --manifest /path/to/your/project/cognitive-coverage.json
```

The server provides hierarchy-aware tools:

| Tool | Purpose |
|------|---------|
| `list_uncovered` | List files, concepts, or flows still at their first status |
| `list_areas` | List large-corpus areas and their modules |
| `get_area` | Return one area with modules and grouped files/concepts/flows |
| `next_learning_targets` | Suggest priority-ordered uncovered items to learn next |
| `get_concept` | Return a concept's description, files, quiz IDs, and status |
| `get_flow` | Return a flow's steps, file references, quiz IDs, and status |
| `coverage_summary` | Return the manifest summary and one-line synopsis |
| `find_by_file` | Return concepts and flows that reference a file path |
| `mark_status` | Update one item status and rewrite the manifest atomically |

Example host config:

```json
{
  "mcpServers": {
    "cognitive-coverage": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/cognitive-coverage/mcp",
        "run",
        "python",
        "server.py",
        "--manifest",
        "/path/to/your/project/cognitive-coverage.json"
      ]
    }
  }
}
```

Once installed, ask your agent:

> "Use `coverage_summary`, then `list_uncovered` for concepts."

See [mcp/README.md](mcp/README.md) for Claude Code, Codex, and Cursor setup.

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
├── install.sh                         # Copilot installer (Unix/macOS/WSL)
├── install.ps1                        # Copilot installer (Windows)
├── skill/
│   └── SKILL.md                       # The skill instructions (works with any agent)
├── mcp/
│   ├── server.py                      # Optional MCP stdio server
│   ├── test_server.py                 # MCP smoke tests
│   └── pyproject.toml                 # MCP server dependencies
├── schemas/
│   └── cognitive-coverage.schema.json # JSON Schema for manifests
├── examples/
│   ├── codebase/                      # TypeScript REST API example
│   ├── research/                      # ML paper review example
│   ├── documentation/                 # Platform wiki example
│   ├── mcp-config-claude-code.json    # Claude Code MCP config snippet
│   └── mcp-config-codex.json          # Codex MCP config snippet
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
- Install scripts for other agents
- Integrations with other tools

## License

[MIT](LICENSE)

---

*Built to fight cognitive debt — one concept at a time.*
