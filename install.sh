#!/usr/bin/env bash
# Install the overleaf-sync skill and /overleaf-sync command to ~/.claude/
# Usage: bash install.sh

set -e

SKILL_DIR="$HOME/.claude/skills/overleaf-sync"
CMD_DIR="$HOME/.claude/commands"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing overleaf-sync..."

# Skill: create dir and symlink all components
mkdir -p "$SKILL_DIR"
ln -sf "$REPO_DIR/SKILL.md"    "$SKILL_DIR/SKILL.md"
ln -sf "$REPO_DIR/scripts"     "$SKILL_DIR/scripts"
ln -sf "$REPO_DIR/templates"   "$SKILL_DIR/templates"
ln -sf "$REPO_DIR/references"  "$SKILL_DIR/references"
echo "✓ Skill installed → $SKILL_DIR"

# Command: /overleaf-sync
mkdir -p "$CMD_DIR"
ln -sf "$REPO_DIR/commands/overleaf-sync.md" "$CMD_DIR/overleaf-sync.md"
echo "✓ Command installed → $CMD_DIR/overleaf-sync.md"

echo ""
echo "Done. Use /overleaf-sync in any Claude session to get started."
