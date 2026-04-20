# claude-overleaf

A Claude skill that lets Claude act as a co-author for papers living on Overleaf. The user describes what they want written; Claude edits the `.tex` files and handles all git sync automatically.

## What it does

- Claude pulls before every edit session and pushes after every change
- Changes appear in Overleaf within ~30 seconds of a push
- First-time setup installs a GitHub Actions workflow for bidirectional sync
- Overleaf → GitHub syncs every hour automatically

Based on [feamster/overleaf-sync](https://github.com/feamster/overleaf-sync).

## Install the skill

```bash
bash install.sh
```

Symlinks `SKILL.md` and supporting files into `~/.claude/skills/overleaf-sync/`.

## First-time setup for a repo

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

## How Claude uses this skill

When the user asks Claude to write or edit their Overleaf paper, Claude:

1. `git pull` — picks up any changes from Overleaf collaborators
2. Reads relevant `.tex` files
3. Makes the requested edits
4. `git add` + `git commit` + `git push` — syncs to Overleaf automatically

The user only needs to refresh the Overleaf browser tab to see the result.

## Repository layout

```
claude-overleaf/
├── SKILL.md                    ← Claude skill definition
├── install.sh                  ← Installs skill to ~/.claude/skills/
├── scripts/
│   └── setup.py               ← One-time repo setup
├── templates/
│   └── overleaf-sync.yml      ← GitHub Actions workflow template
└── references/
    └── troubleshooting.md     ← Common failure modes and fixes
```
