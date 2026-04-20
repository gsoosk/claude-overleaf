# claude-overleaf

A Claude skill for bidirectional sync between GitHub repositories and Overleaf projects.

## What it does

- Installs a GitHub Actions workflow that pushes every commit to Overleaf automatically
- Pulls Overleaf changes back to GitHub every hour
- Keeps a local `overleaf` git remote for direct verification
- Enforces a clean pull-before-edit / push-after-edit habit

Based on [feamster/overleaf-sync](https://github.com/feamster/overleaf-sync).

## Install the skill

```bash
bash install.sh
```

This symlinks `SKILL.md` and supporting files into `~/.claude/skills/overleaf-sync/`.

## Set up sync for a repo (one-time)

```bash
python3 scripts/setup.py /path/to/repo \
  --overleaf-id YOUR_PROJECT_ID \
  --commit
```

Then add two GitHub secrets at `https://github.com/OWNER/REPO/settings/secrets/actions`:

| Secret | Value |
|---|---|
| `OVERLEAF_PROJECT_ID` | from `https://www.overleaf.com/project/[ID]` |
| `OVERLEAF_GIT_TOKEN` | from Overleaf → Account Settings → Git Integration |

## Daily workflow

```bash
git pull                          # get any Overleaf changes first
# ... edit .tex files ...
git add . && git commit -m "..." && git push   # auto-syncs to Overleaf
```

Refresh the Overleaf browser tab after ~30 seconds to see the changes.

## Repository layout

```
claude-overleaf/
├── SKILL.md                  # Claude skill definition
├── install.sh                # Installs skill to ~/.claude/skills/
├── scripts/
│   └── setup.py              # One-time repo setup script
├── templates/
│   └── overleaf-sync.yml     # GitHub Actions workflow template
└── references/
    └── troubleshooting.md    # Common failure modes and fixes
```
