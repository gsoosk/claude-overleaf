#!/usr/bin/env bash
# Install the overleaf-sync skill to ~/.claude/skills/overleaf-sync/
# Usage: bash install.sh

set -e

SKILL_DIR="$HOME/.claude/skills/overleaf-sync"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing overleaf-sync skill..."

# Create skill directory
mkdir -p "$SKILL_DIR"

# Symlink SKILL.md, scripts, templates, references
ln -sf "$REPO_DIR/SKILL.md"    "$SKILL_DIR/SKILL.md"
ln -sf "$REPO_DIR/scripts"     "$SKILL_DIR/scripts"
ln -sf "$REPO_DIR/templates"   "$SKILL_DIR/templates"
ln -sf "$REPO_DIR/references"  "$SKILL_DIR/references"

echo "✓ Installed to $SKILL_DIR"
echo "  SKILL.md and all supporting files are symlinked from $REPO_DIR"
