"""CLI wrapper for mtool update command."""

from __future__ import annotations

import subprocess
import sys

import typer

from mtool.constants import GITHUB_REPO


def update():
    """Pull the latest version from GitHub and refresh skills."""
    print("Updating mtool...")
    result = subprocess.run(
        [sys.executable, "-m", "uv", "pip", "install", "--upgrade", GITHUB_REPO],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Failed to update mtool:\n{result.stderr}")
        raise typer.Exit(1)

    print("Refreshing skills...")
    result = subprocess.run(["mtool", "setup", "--saved"])
    if result.returncode != 0:
        print("Skill refresh failed.")
        raise typer.Exit(1)

    print("Done.")
