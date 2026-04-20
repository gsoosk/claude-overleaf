# claude-overleaf

A Claude skill that lets Claude act as a co-author for papers living on Overleaf. Tell Claude what you want written; it edits the `.tex` files and pushes changes to Overleaf automatically.

## Quickstart

Install once, then just use `/overleaf-sync` in any Claude session:

```bash
bash install.sh
```

That's it. You don't need to run any setup manually — Claude will handle everything.

## How it works

When you type `/overleaf-sync` in a Claude session, Claude will:

1. **Check if the repo is already connected to Overleaf**
2. **If not, run first-time setup automatically** — Claude will ask you for:
   - Your **Overleaf Project ID** (from the URL: `https://www.overleaf.com/project/[PROJECT_ID]`)
   - Your **Overleaf Git Token** (Overleaf → Account Settings → Git Integration)
   - Then it installs the GitHub Actions workflow, adds the `overleaf` remote, and guides you to add two GitHub secrets
3. **Sync state** — fetch any changes made directly in Overleaf before starting
4. **Ask what you want written or edited**

From that point on, every edit Claude makes is automatically committed and pushed to Overleaf. You only need to **refresh the Overleaf browser tab** to see the result.

## What Claude handles automatically

| Claude does this | Without you asking |
|---|---|
| `git pull` + fetch from Overleaf | Before every edit session |
| Read existing `.tex` files | To understand structure and style |
| Write or edit content | As instructed |
| `git add` + `git commit` + `git push` | After every edit |

## Conflict handling

If someone edits in Overleaf and Claude pushes at the same time:
- **On push**: Claude's edits win (`-X ours`)
- **On hourly pull**: Overleaf edits win (`-X theirs`)
- Conflicts never block the workflow — always auto-resolved

## Repository layout

```
claude-overleaf/
├── SKILL.md                    ← Claude skill definition (auto-triggered)
├── commands/
│   └── overleaf-sync.md        ← /overleaf-sync slash command
├── install.sh                  ← Installs skill + command to ~/.claude/
├── scripts/
│   └── setup.py               ← First-time repo setup (Claude runs this)
├── templates/
│   └── overleaf-sync.yml      ← GitHub Actions workflow template
└── references/
    └── troubleshooting.md     ← Failure modes and fixes
```

## Security

- Never share your Overleaf Git token in plain text
- If a token is exposed, regenerate it immediately: Overleaf → Account Settings → Git Integration → regenerate, then update the `OVERLEAF_GIT_TOKEN` GitHub secret

Based on [feamster/overleaf-sync](https://github.com/feamster/overleaf-sync).
