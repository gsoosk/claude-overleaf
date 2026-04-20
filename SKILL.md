---
name: overleaf-sync
description: This skill should be used when the user wants Claude to write, edit, or co-author LaTeX files on an Overleaf project. Triggers on phrases like "edit my Overleaf paper", "write the introduction for my paper", "help me write my LaTeX paper", "co-author my Overleaf project", "I want you to edit my tex files", or any request to write/modify content in a paper that lives on Overleaf. Claude handles all git pull/push/sync automatically — the user only needs to provide the repo and describe what they want written.
version: 2.0.0
---

# Claude as Overleaf Co-author

Claude edits `.tex` files in a repo that is synced to Overleaf. The user describes what they want written; Claude handles all git plumbing (pull, commit, push) so changes appear in Overleaf automatically.

---

## Role boundaries

**Claude does:**
- `git pull` before every edit session — always, without being asked
- Read existing `.tex` files to understand current content and style
- Write or edit `.tex` content as instructed
- `git add` + `git commit` + `git push` after every edit — always, without being asked
- Run first-time setup if the repo is not yet synced to Overleaf

**Claude does not:**
- Ask the user to pull or push manually
- Compile or render PDFs
- Manage Overleaf's built-in GitHub Sync premium feature (uses Git integration instead)
- Store or commit secrets

---

## Session start — always do this first

```bash
# 1. Pull GitHub changes
git pull

# 2. Also fetch and merge any direct Overleaf edits (prevents push conflicts)
git fetch overleaf
git merge overleaf/master --no-edit --allow-unrelated-histories 2>/dev/null || true

# 3. Push the merged state back so GitHub and Overleaf are in sync before editing
git push
```

This three-step pull **prevents the most common conflict**: Overleaf has changes Claude hasn't seen, so the GitHub Action can't push back. By merging Overleaf changes locally first, the subsequent push is always a fast-forward.

Check that the `overleaf` remote exists:

```bash
git remote -v | grep overleaf
```

If missing, the repo is not yet bridged. Run first-time setup (see below).

---

## Edit workflow — every time Claude makes changes

```bash
# 1. Pull latest (may include collaborator or Overleaf edits)
git pull

# 2. Read the target .tex file(s) before editing
# 3. Make the edit

# 4. Stage, commit, push
git add <changed files>
git commit -m "docs(<section>): <what changed>"
git push
```

Changes appear in Overleaf within ~30 seconds. The user only needs to **refresh the Overleaf browser tab**.

---

## First-time setup (if repo is not yet bridged)

Two paths depending on what the user provides:

### Path A — User has a GitHub repo already synced to Overleaf

Ask the user for:
- **Overleaf Project ID** — from `https://www.overleaf.com/project/[PROJECT_ID]`
- **Overleaf Git Token** — Overleaf → Account Settings → Git Integration

Then run:

```bash
python3 ~/.claude/skills/overleaf-sync/scripts/setup.py /path/to/repo \
  --overleaf-id PROJECT_ID \
  --commit
```

Then ask the user to add two GitHub secrets at `https://github.com/OWNER/REPO/settings/secrets/actions`:

| Secret | Value |
|---|---|
| `OVERLEAF_PROJECT_ID` | the project ID |
| `OVERLEAF_GIT_TOKEN` | the Overleaf git token |

### Path B — User only has an Overleaf project (no GitHub repo yet)

1. Create a new GitHub repo
2. Clone it locally
3. Add Overleaf as a remote and pull the initial content:

```bash
git remote add overleaf https://git.overleaf.com/PROJECT_ID
git pull overleaf master --allow-unrelated-histories
git push origin main
```

4. Then follow Path A to install the GitHub Actions workflow.

---

## How the sync works

| Event | Effect |
|---|---|
| `git push` to GitHub | GitHub Action pushes commits to Overleaf within ~30 seconds |
| Hourly schedule | GitHub Action pulls Overleaf edits back to GitHub |
| Manual trigger | GitHub → Actions tab → "Sync with Overleaf" → Run workflow |
| Conflict on push | Auto-resolved with `-X ours` — GitHub (Claude) edits win |
| Conflict on hourly pull | Auto-resolved with `-X theirs` — Overleaf edits win |

---

## Security

- Never commit the Overleaf Git token to any file
- If a token is shown in conversation, remind the user to regenerate it immediately:
  Overleaf → Account Settings → Git Integration → regenerate → update GitHub secret

---

## References

- `scripts/setup.py` — First-time setup script
- `templates/overleaf-sync.yml` — GitHub Actions workflow template
- `references/troubleshooting.md` — Failure modes and fixes
