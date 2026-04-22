from __future__ import annotations

import json
import os

import typer

from mtool.constants import DEFAULT_DATA_DIR, GLOBAL_CONFIG
from mtool.harness import hermes

app = typer.Typer(
    help="Install finance-agent skills into a harness.",
    invoke_without_command=True,
)


def _get_data_dir() -> str:
    return os.environ.get("FINANCE_AGENT_DATA_DIR", DEFAULT_DATA_DIR)


def _load_config() -> dict:
    if not GLOBAL_CONFIG.exists():
        return {}
    return json.loads(GLOBAL_CONFIG.read_text())


def _save_config(harnesses: list[str]):
    GLOBAL_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    config = _load_config()
    config["harnesses"] = harnesses
    GLOBAL_CONFIG.write_text(json.dumps(config, indent=2))


def _run_saved():
    """Re-run skill installation using saved config (called by mtool update)."""
    config = _load_config()
    if not config:
        print("No saved config found. Run 'mtool setup' first.")
        raise typer.Exit(1)

    data_dir = _get_data_dir()
    print(f"Re-installing skills (data dir: {data_dir})")

    if "hermes" in config.get("harnesses", []):
        hermes.install(data_dir)


@app.command("hermes")
def cmd_hermes():
    """Install finance-agent skills into Hermes Agent."""
    hermes.install(_get_data_dir())

    harnesses = list(set(_load_config().get("harnesses", [])) | {"hermes"})
    _save_config(harnesses)


@app.callback()
def cmd_setup(
    ctx: typer.Context, saved: bool = typer.Option(False, "--saved", hidden=True)
):
    """Install finance-agent skills. Run without arguments for interactive setup."""
    if ctx.invoked_subcommand is not None:
        return

    if saved:
        _run_saved()
        return

    print("finance-agent setup")
    print("=" * 40)

    # For now, only hermes is supported
    hermes.install(_get_data_dir())
    _save_config(["hermes"])
