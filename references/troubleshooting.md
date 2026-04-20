# Troubleshooting

## GitHub Action fails immediately

**Check:** `https://github.com/OWNER/REPO/actions` → click the failed run → expand the failing step.

**Common causes:**

| Symptom | Cause | Fix |
|---|---|---|
| `Context access might be invalid: OVERLEAF_PROJECT_ID` | Secret not added | Add both secrets at Settings → Secrets → Actions |
| `Authentication failed` | Wrong token or expired | Regenerate token in Overleaf, update GitHub secret |
| `remote: Repository not found` | Wrong project ID | Check URL: `https://www.overleaf.com/project/[ID]` |
| `Merge conflict detected` | Simultaneous edits | Pull the `overleaf-sync-conflict-*` branch, resolve, push |

## Changes not appearing in Overleaf after push

1. Check that the GitHub Action completed (green checkmark in Actions tab)
2. **Refresh the Overleaf browser tab** — Overleaf does not auto-refresh
3. If Action is green but changes are missing, check that the push step reached `git push overleaf HEAD:master`

## Overleaf changes not appearing in GitHub

- Wait up to 1 hour for the scheduled pull
- Or trigger manually: Actions tab → "Sync with Overleaf" → Run workflow

## Local `git pull` shows nothing but Overleaf has changes

The hourly Action commits Overleaf changes back to `origin/main`. Run `git pull` after the Action completes.

## `overleaf` remote not configured locally

After cloning the repo on a new machine, re-add the remote:

```bash
git remote add overleaf https://git.overleaf.com/PROJECT_ID
```

## Token expired / rotated

1. Regenerate at Overleaf → Account Settings → Git Integration
2. Update GitHub secret: repo → Settings → Secrets → `OVERLEAF_GIT_TOKEN` → Update
3. No changes needed locally — the remote URL does not contain the token
