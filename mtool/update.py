"""CLI wrapper for mtool update command."""

from __future__ import annotations

import shutil
import subprocess

import typer

from mtool.constants import GITHUB_REPO


def update():
    """Pull the latest version from GitHub and refresh skills."""
    uv = shutil.which("uv")
    if uv is None:
        print("uv not found. Install uv first: https://docs.astral.sh/uv/")
        raise typer.Exit(1)

    print("Updating mtool...")
    result = subprocess.run(
        [uv, "tool", "upgrade", "finance_agent"],
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
