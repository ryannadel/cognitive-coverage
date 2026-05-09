# Cognitive Coverage MCP Server

This directory contains an optional MCP stdio server for `cognitive-coverage.json`.

The skill still works without MCP. Install this server only when you want an agent to query or update the manifest during a coding session.

## Tools

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
| `mark_status` | Update one file, concept, flow, area, or module status and rewrite the manifest atomically |

## Run Locally

```bash
cd mcp
uv run python server.py --manifest ../examples/codebase/cognitive-coverage.json
```

If you do not pass `--manifest`, the server reads `./cognitive-coverage.json` from the current working directory.

## Claude Code

Add a server entry to your Claude Code MCP config:

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

See `examples/mcp-config-claude-code.json` for the same snippet.

## OpenAI Codex

The Codex CLI reads MCP servers from `~/.codex/config.toml` under `[mcp_servers.<name>]` (TOML, not JSON). Add this entry:

```toml
[mcp_servers.cognitive-coverage]
command = "uv"
args = [
  "--directory",
  "/path/to/cognitive-coverage/mcp",
  "run",
  "python",
  "server.py",
  "--manifest",
  "/path/to/your/project/cognitive-coverage.json",
]
```

See `examples/mcp-config-codex.toml` for the same snippet.

## Cursor

Add the server under Cursor's MCP server settings:

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

## Smoke Test

```bash
uv --directory mcp run pytest
```
