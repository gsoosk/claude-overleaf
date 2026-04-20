# Troubleshooting

## "Cannot push to Overleaf - merge conflict detected"

**Root cause:** Overleaf had commits that weren't in GitHub when the Action ran. The old workflow aborted instead of resolving.

**Fixed in v2.1+:** The Action now uses `-X ours` when merging Overleaf changes before pushing. Conflicts are auto-resolved in favor of GitHub (Claude's edits win). The push never blocks.

**If you still see this on an older workflow:** The `.github/workflows/overleaf-sync.yml` in your repo is outdated. Re-run the setup script to install the latest template:

```bash
python3 ~/.claude/skills/overleaf-sync/scripts/setup.py /path/to/repo \
  --overleaf-id PROJECT_ID \
  --commit
```

**Preventive fix (Claude session start):** Always run the three-step pull before editing:

```bash
git pull
git fetch overleaf
git merge overleaf/master --no-edit --allow-unrelated-histories 2>/dev/null || true
git push
```

This merges Overleaf's state locally first, so the subsequent push is always a fast-forward — conflicts never reach the Action.

---

## GitHub Action fails immediately

**Check:** `https://github.com/OWNER/REPO/actions` → click the failed run → expand the failing step.

| Symptom | Cause | Fix |
|---|---|---|
| `Context access might be invalid: OVERLEAF_PROJECT_ID` | Secret not added | Add both secrets at Settings → Secrets → Actions |
| `Authentication failed` | Wrong token or expired | Regenerate token in Overleaf, update GitHub secret |
| `remote: Repository not found` | Wrong project ID | Check URL: `https://www.overleaf.com/project/[ID]` |
| `Push to Overleaf failed` | Token lacks push access | Verify token in Overleaf Account Settings → Git Integration |

---

## Changes not appearing in Overleaf after push

1. Check the GitHub Action completed (green checkmark in Actions tab)
2. **Refresh the Overleaf browser tab** — Overleaf does not auto-refresh
3. If Action is green but changes are missing, confirm the push step shows `git push overleaf HEAD:master`

---

## Overleaf changes not appearing in GitHub

- Wait up to 1 hour for the scheduled pull
- Or trigger manually: Actions tab → "Sync with Overleaf" → Run workflow
- Or run locally: `git fetch overleaf && git merge overleaf/master --no-edit && git push`

---

## `overleaf` remote not configured locally

After cloning the repo on a new machine, re-add the remote:

```bash
git remote add overleaf https://git.overleaf.com/PROJECT_ID
```

---

## Token expired / rotated

1. Regenerate at Overleaf → Account Settings → Git Integration
2. Update GitHub secret: repo → Settings → Secrets → `OVERLEAF_GIT_TOKEN` → Update
3. No local changes needed — the remote URL does not contain the token
