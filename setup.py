"""
setup.py — Interactive setup for finance-agent.

Usage:
    bash setup.sh           # initial setup
    bash setup.sh --update  # reinstall mtool + skills using saved config
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import pyperclip
import questionary

REPO_ROOT = Path(__file__).parent.resolve()
GITHUB_REPO = "git+https://github.com/junnjiee/finance-agent.git"
DEFAULT_DATA_DIR = str(Path.home() / ".config" / "finance_agent" / "data")
SETUP_CONFIG = REPO_ROOT / "setup.json"

HARNESS_CHOICE = "Coding harnesses (Claude Code, Codex, Opencode, etc.)"


def tilde(path) -> str:
    p = Path(path)
    try:
        return f"~/{p.relative_to(Path.home())}"
    except ValueError:
        return str(p)


OPENCLAW_CHOICE = "OpenClaw"
HERMES_CHOICE = "Hermes Agent"


def install_mtool() -> bool:
    print("\nInstalling mtool globally via uv tool...")
    result = subprocess.run(
        ["uv", "tool", "install", "--reinstall", GITHUB_REPO],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  FAILED:\n{result.stderr.strip()}")
        return False
    print("  OK  mtool")
    return True


def prompt_data_dir() -> str:
    raw = input(
        f"\nData directory path (leave blank to use default: {tilde(DEFAULT_DATA_DIR)}): "
    ).strip()
    return str(Path(raw or DEFAULT_DATA_DIR).expanduser())


def show_env_export(data_dir: str):
    export_line = f'export FINANCE_AGENT_DATA_DIR="{data_dir}"'
    print("\n  Add this to your shell profile (~/.zshrc, ~/.bashrc, etc.):")
    print(f"\n    {export_line}\n")

    input("  Press Enter to copy to clipboard...")
    pyperclip.copy(export_line)
    print("  Copied.")


def prompt_harnesses() -> list[str]:
    choices = [HARNESS_CHOICE, OPENCLAW_CHOICE, HERMES_CHOICE]
    selected = questionary.checkbox(
        "Where will you use finance-agent? (space to select, enter to confirm)",
        choices=choices,
    ).ask()
    return selected or []


GLOBAL_CONFIG = Path.home() / ".config" / "finance_agent" / "mtool.json"


def save_global_config():
    GLOBAL_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    GLOBAL_CONFIG.write_text(json.dumps({"repo_root": str(REPO_ROOT)}, indent=2))


def save_config(data_dir: str, selected: list[str]):
    SETUP_CONFIG.write_text(
        json.dumps({"data_dir": data_dir, "harnesses": selected}, indent=2)
    )


def load_config() -> dict:
    if not SETUP_CONFIG.exists():
        print("No saved setup config found. Run setup first: bash setup.sh")
        sys.exit(1)
    return json.loads(SETUP_CONFIG.read_text())


def run_subscript(script: Path, data_dir: str):
    cmd = [sys.executable, str(script), "--data-dir", data_dir]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\n  WARNING: {script.name} exited with code {result.returncode}")


def run_harnesses(data_dir: str, selected: list[str]):
    if HARNESS_CHOICE in selected:
        print(
            f"Coding harnesses: open your agentic harness in the finance_agent project directory ({tilde(REPO_ROOT)})."
        )
        print(f"  Data directory: {tilde(data_dir)}")

    if OPENCLAW_CHOICE in selected:
        openclaw_home = Path(os.environ.get("OPENCLAW_HOME", Path.home() / ".openclaw"))
        if openclaw_home.exists():
            print("\nRunning OpenClaw setup...")
            run_subscript(REPO_ROOT / "openclaw" / "setup.py", data_dir)
        else:
            print(
                f"\nSkipping OpenClaw: {tilde(openclaw_home)} not found. Install OpenClaw first."
            )

    if HERMES_CHOICE in selected:
        hermes_home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
        if hermes_home.exists():
            print("\nRunning Hermes setup...")
            run_subscript(REPO_ROOT / "hermes" / "setup.py", data_dir)
        else:
            print(
                f"\nSkipping Hermes: {tilde(hermes_home)} not found. Install Hermes Agent first."
            )


def main():
    parser = argparse.ArgumentParser(description="finance-agent setup")
    parser.add_argument(
        "--update",
        action="store_true",
        help="Reinstall mtool and skills using saved config",
    )
    args = parser.parse_args()

    print("finance-agent setup")
    print("=" * 40)

    if not REPO_ROOT.joinpath(".agents", "skills").exists():
        print(
            f"ERROR: skills directory not found at {tilde(REPO_ROOT / '.agents' / 'skills')}"
        )
        sys.exit(1)

    if args.update:
        config = load_config()
        data_dir = config["data_dir"]
        selected = config["harnesses"]
        print(f"\nUsing saved config: {tilde(SETUP_CONFIG)}")
        print(f"  Data directory : {tilde(data_dir)}")
        print(f"  Harnesses      : {', '.join(selected) or 'none'}")
    else:
        # 1. Install mtool
        if not install_mtool():
            print("\nSetup cannot continue without mtool.")
            sys.exit(1)

        # 2. Data directory
        data_dir = prompt_data_dir()

        # 3. Env var instructions (only when non-default)
        if data_dir != str(Path(DEFAULT_DATA_DIR).expanduser()):
            show_env_export(data_dir)

        # 4. Harness selection
        selected = prompt_harnesses()
        if not selected:
            print("\nNothing selected — nothing else to do.")
            print("Run this script again any time to update your setup.")
            return

        save_config(data_dir, selected)
        save_global_config()

    print()

    if args.update:
        if not install_mtool():
            print("\nUpdate failed: could not reinstall mtool.")
            sys.exit(1)

    run_harnesses(data_dir, selected)
    print("\nDone.")


if __name__ == "__main__":
    main()
