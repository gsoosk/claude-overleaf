#!/usr/bin/env python3
"""
Overleaf sync setup for GitHub repositories.
Adds GitHub Action workflow for bidirectional sync with Overleaf.
Adapted from https://github.com/feamster/overleaf-sync
"""

import sys
import shutil
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True, check=False
    )
    if check and result.returncode != 0:
        print(f"Error: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result


def main():
    parser = argparse.ArgumentParser(description="Set up Overleaf sync for a GitHub repository")
    parser.add_argument("repo_path", help="Path to the repository")
    parser.add_argument("--overleaf-id", required=True, help="Overleaf project ID")
    parser.add_argument("--commit", action="store_true", help="Commit and push the workflow file")
    args = parser.parse_args()

    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists() or not (repo_path / ".git").exists():
        print(f"Error: {repo_path} is not a git repository")
        sys.exit(1)

    print(f"Setting up Overleaf sync for: {repo_path.name}")

    # Template lives at ../templates/overleaf-sync.yml relative to this script
    script_dir = Path(__file__).parent
    workflow_template = script_dir.parent / "templates" / "overleaf-sync.yml"

    if not workflow_template.exists():
        print(f"Error: Template not found at {workflow_template}")
        sys.exit(1)

    # Create .github/workflows and copy template
    workflows_dir = repo_path / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(workflow_template, workflows_dir / "overleaf-sync.yml")
    print("✓ Created .github/workflows/overleaf-sync.yml")

    # Parse GitHub remote for secrets URL
    result = run_command("git remote get-url origin", cwd=repo_path, check=False)
    if result.returncode == 0:
        origin_url = result.stdout.strip()
        if "github.com" in origin_url:
            part = origin_url.replace("https://github.com/", "").replace(".git", "")
            if ":" in part:
                part = part.split(":")[-1].replace(".git", "")
            owner, repo_name = part.split("/", 1)
            secrets_url = f"https://github.com/{owner}/{repo_name}/settings/secrets/actions"

            print(f"""
{'='*60}
NEXT STEPS — Add GitHub Secrets
{'='*60}
1. Go to: {secrets_url}

2. Add two secrets:

   OVERLEAF_PROJECT_ID = {args.overleaf_id}

   OVERLEAF_GIT_TOKEN  = (Overleaf > Account Settings > Git Integration)
{'='*60}
""")

    # Add Overleaf git remote locally if not present
    existing_remotes = run_command("git remote", cwd=repo_path, check=False).stdout
    if "overleaf" not in existing_remotes.split():
        run_command(
            f'git remote add overleaf "https://git.overleaf.com/{args.overleaf_id}"',
            cwd=repo_path
        )
        print("✓ Added local 'overleaf' git remote")
    else:
        print("✓ 'overleaf' remote already exists")

    if args.commit:
        print("Committing and pushing workflow...")
        run_command("git add .github/workflows/overleaf-sync.yml", cwd=repo_path)
        run_command('git commit -m "chore: add Overleaf sync GitHub Action workflow"', cwd=repo_path)
        run_command("git push", cwd=repo_path)
        print("✓ Pushed to GitHub")

    print("\n✓ Setup complete!")
    print("Once secrets are added, every git push will sync to Overleaf automatically.")
    print("Overleaf → GitHub syncs every hour via the scheduled workflow.")
    print("\nRefresh the Overleaf browser tab to see incoming changes.")


if __name__ == "__main__":
    main()
