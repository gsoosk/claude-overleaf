# claude-overleaf

A Claude skill that turns Claude into a co-author for papers living on Overleaf. Claude syncs with your Overleaf project, edits `.tex` files as instructed, and pushes changes back automatically — no manual git commands needed.

## Install

```bash
bash install.sh
```

This installs the skill and the `/overleaf-sync` command into `~/.claude/`. That's the only manual step required.

---

## Two ways to use this

### 1. The skill (always active after install)

Once installed, the skill activates automatically whenever you ask Claude to work on your paper. You don't need to invoke a command — just describe what you want:

> *"Write the introduction for my paper"*
> *"Edit the abstract to be more concise"*
> *"Help me write the related work section"*
> *"Add a paragraph explaining our evaluation setup"*
> *"I want you to edit my tex files"*
> *"Co-author my Overleaf paper with me"*

Claude will recognize the intent, sync with Overleaf, make the edit, and push — all without you touching git.

### 2. The `/overleaf-sync` command (explicit entry point)

Use `/overleaf-sync` when you want to explicitly start a writing session or run first-time setup on a new repo. Claude will:

1. Check if the repo is already connected to Overleaf
2. If not, **run first-time setup automatically** — asking only for:
   - **Overleaf Project ID** — from `https://www.overleaf.com/project/[PROJECT_ID]`
   - **Overleaf Git Token** — from Overleaf → Account Settings → Git Integration
3. Sync state with Overleaf before starting
4. Ask what you want written or edited

---

## What Claude handles automatically

| Action | When |
|---|---|
| `git pull` + fetch from Overleaf remote | Start of every session |
| Read relevant `.tex` files | Before every edit |
| Write or edit content | As instructed |
| `git add` + `git commit` + `git push` | After every edit |

Refresh the Overleaf browser tab after a push to see the result (~30 seconds).

---

## Conflict handling

If Overleaf has changes Claude hasn't seen yet (e.g., a collaborator edited directly in Overleaf):

1. Claude will **show you the conflicting sections** and ask which version to keep
2. After you decide, Claude applies the resolution, commits, and pushes

The GitHub Actions workflow also handles automated conflicts:
- **GitHub → Overleaf push**: GitHub version wins (`-X ours`)
- **Overleaf → GitHub hourly pull**: Overleaf version wins (`-X theirs`)

---

## Repository layout

```
claude-overleaf/
├── SKILL.md                    ← Skill definition (auto-activates on writing requests)
├── commands/
│   └── overleaf-sync.md        ← /overleaf-sync slash command
├── install.sh                  ← Installs skill + command to ~/.claude/
├── scripts/
│   └── setup.py               ← First-time repo setup (Claude runs this, not you)
├── templates/
│   └── overleaf-sync.yml      ← GitHub Actions workflow for bidirectional sync
└── references/
    └── troubleshooting.md     ← Failure modes and fixes
```

---

## Security

- Never share your Overleaf Git token in plain text
- If a token is ever exposed, regenerate it immediately:
  Overleaf → Account Settings → Git Integration → regenerate → update the `OVERLEAF_GIT_TOKEN` GitHub secret

Based on [feamster/overleaf-sync](https://github.com/feamster/overleaf-sync).
