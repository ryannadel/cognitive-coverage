# Cognitive Coverage — Copilot Skill Installer (Windows)
#
# This script installs the skill for GitHub Copilot.
# For other agents, see README.md for platform-specific instructions.
$ErrorActionPreference = "Stop"

$SkillDir = Join-Path $env:USERPROFILE ".copilot\skills\cognitive-coverage"

Write-Host "🧠 Installing Cognitive Coverage skill for GitHub Copilot..." -ForegroundColor Cyan

# Create skill directory
if (-not (Test-Path $SkillDir)) {
    New-Item -ItemType Directory -Path $SkillDir -Force | Out-Null
}

# Copy skill file
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item (Join-Path $ScriptDir "skill\SKILL.md") (Join-Path $SkillDir "SKILL.md") -Force

Write-Host "✅ Installed to $SkillDir\SKILL.md" -ForegroundColor Green
Write-Host ""
Write-Host "Usage: Ask Copilot to generate a 'cognitive coverage' or 'learning guide' for any project."
Write-Host "The skill works with codebases, research papers, documentation, and general knowledge."
Write-Host ""
Write-Host "For other agents (Claude Code, OpenAI Codex, etc.), see README.md."