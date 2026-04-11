import json
import subprocess
import sys
from pathlib import Path

import typer

from mtool import expenses

app = typer.Typer()
app.add_typer(expenses.app, name="expenses")

# market imports yfinance/pandas which are heavy — skip them for `mtool update`
# so the update command starts up fast without loading unused dependencies
if len(sys.argv) < 2 or sys.argv[1] != "update":
    from mtool import market

    app.add_typer(market.app, name="market")

GLOBAL_CONFIG = Path.home() / ".config" / "finance_agent" / "mtool.json"


# do not push this to remote repo
@app.command()
def dev_mode():
    """If you are seeing this, you are in development environment."""


@app.command()
def update():
    """Pull the latest changes from GitHub and refresh skills."""
    if not GLOBAL_CONFIG.exists():
        print("No setup config found. Run setup first: bash setup.sh")
        raise typer.Exit(1)

    repo_root = Path(json.loads(GLOBAL_CONFIG.read_text())["repo_root"])
    if not repo_root.exists():
        print(f"Repo not found at {repo_root}. Re-run bash setup.sh to reconfigure.")
        raise typer.Exit(1)

    # Check for uncommitted changes
    status = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    has_changes = bool(status.stdout.strip())

    if has_changes:
        print("Stashing local changes...")
        stash = subprocess.run(
            ["git", "-C", str(repo_root), "stash"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if stash.returncode != 0:
            print("Failed to stash changes.")
            raise typer.Exit(1)

    print("Pulling latest changes from GitHub...")
    result = subprocess.run(
        ["git", "-C", str(repo_root), "pull"],
        capture_output=True,
        text=True,
    )
    pull_failed = result.returncode != 0
    already_up_to_date = "Already up to date." in result.stdout

    if has_changes:
        print("Restoring stashed changes...")
        subprocess.run(
            ["git", "-C", str(repo_root), "stash", "pop"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    if pull_failed:
        print("git pull failed.")
        raise typer.Exit(1)

    if already_up_to_date:
        print("Already up to date.")

    print("\nReinstalling mtool and refreshing skills...")
    result = subprocess.run(
        [sys.executable, str(repo_root / "setup.py"), "--update"],
    )
    if result.returncode != 0:
        print("Setup refresh failed.")
        raise typer.Exit(1)

    print("Done.")


if __name__ == "__main__":
    app()
