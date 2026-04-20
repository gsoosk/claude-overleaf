---
name: overleaf-sync
description: This skill should be used when the user asks to "set up Overleaf sync", "sync Overleaf with GitHub", "connect Overleaf to GitHub", "push to Overleaf automatically", or wants bidirectional sync between a local LaTeX repo and an Overleaf project. Automates the full setup: GitHub Actions workflow, local remote, secrets, and daily edit workflow.
version: 1.0.0
---

# Overleaf Sync

Establishes bidirectional sync between a GitHub repository and an Overleaf project using GitHub Actions. After setup, every `git push` to GitHub automatically pushes to Overleaf; Overleaf changes pull back to GitHub every hour.

Based on [feamster/overleaf-sync](https://github.com/feamster/overleaf-sync).

---

## Role boundaries

**Does:**
- Run the one-time setup for any git repo (workflow file, local remote, GitHub secrets guidance)
- Guide the user through the two GitHub secrets required
- Enforce the pull-before-edit / push-after-edit daily habit
- Remind the user to refresh the Overleaf browser tab to see incoming changes
- Remind the user to regenerate the Overleaf Git token if it was ever exposed

**Does not:**
- Manage Overleaf project content or compilation
- Handle Overleaf's built-in GitHub Sync premium feature (this uses the Git integration instead)
- Push secrets — GitHub secrets must be added manually by the user

---

## One-time setup workflow

### Step 1 — Gather prerequisites

Ask the user for:
1. **Overleaf Project ID** — from the URL: `https://www.overleaf.com/project/[PROJECT_ID]`
2. **Overleaf Git Token** — from Overleaf → Account Settings → Git Integration → Generate token

### Step 2 — Run setup script

From inside the repo to sync:

```bash
python3 /path/to/claude-overleaf/scripts/setup.py /path/to/repo \
  --overleaf-id PROJECT_ID \
  --commit
```

This will:
- Create `.github/workflows/overleaf-sync.yml`
- Add an `overleaf` git remote locally
- Commit and push the workflow to GitHub

### Step 3 — Add GitHub secrets (manual, user must do this)

Navigate to `https://github.com/OWNER/REPO/settings/secrets/actions` and add:

| Secret name | Value |
|---|---|
| `OVERLEAF_PROJECT_ID` | the project ID |
| `OVERLEAF_GIT_TOKEN` | the Overleaf git token |

### Step 4 — Trigger first sync

Make any small commit and push to trigger the first GitHub Action run:

```bash
git add . && git commit -m "chore: trigger initial Overleaf sync" && git push
```

Watch the Action at `https://github.com/OWNER/REPO/actions`. Refresh Overleaf to confirm changes arrived.

---

## Daily workflow (every session)

```bash
# 1. Pull before editing (gets any changes made in Overleaf)
git pull

# 2. Edit .tex files

# 3. Commit and push (auto-syncs to Overleaf via GitHub Action)
git add sections/file.tex
git commit -m "docs: ..."
git push
```

**Refresh the Overleaf browser tab** after ~30 seconds to see the pushed changes.

---

## How the sync works

| Event | What happens |
|---|---|
| `git push` to GitHub | GitHub Action immediately pushes commits to `git.overleaf.com` |
| Hourly schedule | GitHub Action fetches Overleaf changes and merges into GitHub `main` |
| Manual trigger | Actions tab → "Sync with Overleaf" → Run workflow |
| Conflict | Action creates a `overleaf-sync-conflict-*` branch for manual resolution |

---

## Security reminders

- Never commit the Overleaf Git token to any file
- If the token is ever exposed (e.g., shown in chat), regenerate it immediately:
  Overleaf → Account Settings → Git Integration → regenerate
- Update the `OVERLEAF_GIT_TOKEN` GitHub secret after regenerating

---

## References

- `templates/overleaf-sync.yml` — GitHub Actions workflow template
- `scripts/setup.py` — One-time setup script
- `references/troubleshooting.md` — Common failure modes and fixes
