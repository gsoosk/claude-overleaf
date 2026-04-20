---
description: Set up bidirectional sync between the current repo and an Overleaf project, then start editing. Claude handles all git plumbing automatically.
---

# /overleaf-sync

Activate the overleaf-sync skill for the current repository. Claude will check whether sync is already configured, run first-time setup if needed (asking only for the Overleaf Project ID and Git Token), and then be ready to write and push `.tex` files to Overleaf.

## Instructions

1. **Check if sync is already configured**
   - Run `git remote -v | grep overleaf`
   - If the `overleaf` remote exists and `.github/workflows/overleaf-sync.yml` is present → sync is ready, skip to step 4
   - Otherwise → run first-time setup below

2. **First-time setup (Claude does this automatically)**
   - Ask the user for:
     - **Overleaf Project ID** — from `https://www.overleaf.com/project/[PROJECT_ID]`
     - **Overleaf Git Token** — from Overleaf → Account Settings → Git Integration
   - Run the setup script:
     ```bash
     python3 ~/.claude/skills/overleaf-sync/scripts/setup.py . \
       --overleaf-id PROJECT_ID \
       --commit
     ```
   - Instruct the user to add two GitHub secrets at `https://github.com/OWNER/REPO/settings/secrets/actions`:
     - `OVERLEAF_PROJECT_ID` = the project ID
     - `OVERLEAF_GIT_TOKEN` = the git token
   - Wait for confirmation that secrets are added before proceeding

3. **Sync state before editing**
   ```bash
   git pull
   git fetch overleaf
   git merge overleaf/master --no-edit --allow-unrelated-histories 2>/dev/null || true
   git push
   ```

4. **Confirm ready**
   - Report the current branch, last commit, and which `.tex` files exist
   - Ask the user what they would like to write or edit
