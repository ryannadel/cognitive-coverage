#!/usr/bin/env bash
# Cognitive Coverage — Copilot Skill Installer (Unix/macOS/WSL)
#
# This script installs the skill for GitHub Copilot.
# For other agents, see README.md for platform-specific instructions.
set -euo pipefail

SKILL_DIR="${HOME}/.copilot/skills/cognitive-coverage"

echo "🧠 Installing Cognitive Coverage skill for GitHub Copilot..."

# Create skill directory
mkdir -p "${SKILL_DIR}"

# Determine script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy skill file
cp "${SCRIPT_DIR}/skill/SKILL.md" "${SKILL_DIR}/SKILL.md"

echo "✅ Installed to ${SKILL_DIR}/SKILL.md"
echo ""
echo "Usage: Ask Copilot to generate a 'cognitive coverage' or 'learning guide' for any project."
echo "The skill works with codebases, research papers, documentation, and general knowledge."
echo ""
echo "For other agents (Claude Code, OpenAI Codex, etc.), see README.md."