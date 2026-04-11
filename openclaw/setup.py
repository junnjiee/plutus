#!/usr/bin/env python3
"""
openclaw/setup.py — Install finance-agent skills and mtool into OpenClaw.

Usage:
    python openclaw/setup.py
    uv run python openclaw/setup.py
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_SRC = REPO_ROOT / ".agents" / "skills"
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", Path.home() / ".openclaw"))
OPENCLAW_SKILLS_DIR = OPENCLAW_HOME / "skills"
OPENCLAW_CONFIG = OPENCLAW_HOME / "openclaw.json"

# OpenClaw metadata per skill: emoji for the Skills UI
SKILL_META = {
    "fa-onboard": {"emoji": "🚀"},
    "fa-net-worth": {"emoji": "💰"},
    "fa-analyze-cashflow": {"emoji": "📊"},
    "fa-liability-tracker": {"emoji": "📋"},
}

ADAPTER_NOTE = """\
> **OpenClaw adapter note:** When instructions refer to "the data directory", use
> the value of `FINANCE_AGENT_DATA_DIR` (injected via OpenClaw's skill entry config).
> Use `mtool` directly — it is installed globally. No `uv sync` step is needed.
> If the user is messaging via a chat app (Telegram, WhatsApp, Signal, iMessage, etc.),
> use no markdown formatting and no markdown tables. Use emojis where appropriate.
"""


# ---------------------------------------------------------------------------
# Skill generation
# ---------------------------------------------------------------------------


def build_openclaw_metadata(skill_name: str) -> str:
    """
    Return a single-line JSON string for the `metadata:` frontmatter field.
    OpenClaw requires the metadata value to be a single-line JSON object.
    """
    meta = SKILL_META.get(skill_name, {"emoji": "💰"})
    openclaw_obj = {
        "emoji": meta["emoji"],
        "requires": {"bins": ["uv"]},
        "install": [
            {
                "id": "brew-uv",
                "kind": "brew",
                "formula": "uv",
                "bins": ["uv"],
                "label": "Install uv (brew)",
            }
        ],
    }
    return json.dumps({"openclaw": openclaw_obj}, separators=(",", ":"))


def transform(content: str, skill_name: str) -> str:
    """
    Given the raw source SKILL.md, produce an OpenClaw-flavored version by:
      1. Appending a single-line JSON `metadata:` field to the frontmatter.
      2. Inserting an adapter note at the start of the body.
      3. Replacing venv-relative tool paths with their global equivalents.
      4. Rewriting `uv sync` references to fit the global-install model.
    """
    lines = content.splitlines()

    delimiters = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delimiters) < 2:
        return content  # not standard frontmatter, return unchanged

    fm_start, fm_end = delimiters[0], delimiters[1]
    frontmatter = lines[fm_start + 1 : fm_end]
    body = lines[fm_end + 1 :]

    # 1. Append OpenClaw metadata as a single-line JSON value
    metadata_line = f"metadata: {build_openclaw_metadata(skill_name)}"
    new_frontmatter = ["---"] + frontmatter + [metadata_line] + ["---"]

    # 2. Prepend the adapter note to the body
    adapter_lines = ["", *ADAPTER_NOTE.splitlines(), ""]
    new_body = adapter_lines + body

    # 3 & 4. Fix tool paths and uv sync references
    result = "\n".join(new_frontmatter + new_body)

    result = result.replace(".venv/bin/mtool", "mtool")
    result = result.replace(".venv/bin/python", "python3")

    # Pattern A: "prepare/ensure [the] [project] environment [prep word] `uv sync`"
    result = re.sub(
        r"(?:prepare|ensure)\s+(?:the\s+)?(?:project\s+)?"
        r"environment\s+\w+\s+`uv sync`",
        "ensure `mtool` is installed (run `python openclaw/setup.py` from the finance-agent repo)",
        result,
    )
    # Pattern B: "... environment with `uv sync` and use" (trailing conjunction)
    result = re.sub(
        r"(?:prepare|ensure)\s+(?:the\s+)?(?:\w+\s+)?environment\s+with\s+`uv sync`\s+and\s+use",
        "use",
        result,
    )
    # Pattern C: "If [the] environment is not ready[...], run `uv sync` [first]"
    result = re.sub(
        r"If (?:the )?environment is not ready[^,]*,?\s+run `uv sync`\s*\w*",
        "mtool is installed globally — no environment activation needed",
        result,
    )
    # Pattern D: any remaining standalone "run `uv sync`" reference
    result = re.sub(
        r"run `uv sync`",
        "ensure `mtool` is installed globally",
        result,
    )

    return result


# ---------------------------------------------------------------------------
# Installation steps
# ---------------------------------------------------------------------------


def install_mtool() -> bool:
    print("\nInstalling mtool globally via uv tool...")
    result = subprocess.run(
        ["uv", "tool", "install", "--reinstall", str(REPO_ROOT)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  FAILED:\n{result.stderr.strip()}")
        return False
    print("  OK  mtool")
    return True


def install_skills():
    print(f"\nGenerating and installing skills to {OPENCLAW_SKILLS_DIR} ...")
    OPENCLAW_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if not skill_dir.is_dir():
            continue
        source = skill_dir / "SKILL.md"
        if not source.exists():
            continue

        skill_name = skill_dir.name
        generated = transform(source.read_text(), skill_name)

        dest_dir = OPENCLAW_SKILLS_DIR / skill_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "SKILL.md"
        action = "updated" if dest.exists() else "installed"
        dest.write_text(generated)
        print(f"  {action}  /{skill_name}")


def _load_config() -> dict:
    """
    Read ~/.openclaw/openclaw.json, stripping JSON5 line comments and trailing
    commas before parsing.

    Returns an empty dict if the file is missing. If the file exists but cannot
    be parsed (e.g., it uses unsupported JSON5 features), backs it up to
    openclaw.json.bak and returns an empty dict rather than silently discarding
    existing user config without a trace.
    """
    if not OPENCLAW_CONFIG.exists():
        return {}
    raw = OPENCLAW_CONFIG.read_text()
    # Strip // line comments (JSON5 feature not supported by stdlib json)
    raw = re.sub(r"//[^\n]*", "", raw)
    # Strip trailing commas before ] or } (another JSON5 extension)
    raw = re.sub(r",(\s*[}\]])", r"\1", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        bak = OPENCLAW_CONFIG.with_suffix(".json.bak")
        OPENCLAW_CONFIG.replace(bak)
        print(
            f"  WARNING: Could not parse {OPENCLAW_CONFIG.name} — backed up to {bak.name}"
        )
        return {}


def configure_openclaw(data_dir: str):
    """
    Upsert finance-agent skill entries in ~/.openclaw/openclaw.json.

    For each skill, this sets:
        skills.entries.<skill-name>.env.FINANCE_AGENT_DATA_DIR = data_dir

    OpenClaw injects `env` values into the agent context, so the skills can
    resolve `data/` paths without hard-coding anything in the SKILL.md files.
    """
    OPENCLAW_HOME.mkdir(parents=True, exist_ok=True)
    is_new = not OPENCLAW_CONFIG.exists()

    config = _load_config()

    skills_cfg = config.setdefault("skills", {})
    entries = skills_cfg.setdefault("entries", {})

    skill_names = [
        d.name
        for d in sorted(SKILLS_SRC.iterdir())
        if d.is_dir() and (d / "SKILL.md").exists()
    ]

    for skill_name in skill_names:
        entry = entries.setdefault(skill_name, {})
        entry.setdefault("env", {})["FINANCE_AGENT_DATA_DIR"] = data_dir

    OPENCLAW_CONFIG.write_text(json.dumps(config, indent=2) + "\n")
    action = "installed" if is_new else "updated"
    print(f"\n  {action}  {OPENCLAW_CONFIG}")
    print(f"           FINANCE_AGENT_DATA_DIR → {data_dir}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Install finance-agent skills into OpenClaw.")
    parser.add_argument("--data-dir", dest="data_dir", default=None, help="Path to the finance-agent data directory (skips interactive prompt)")
    args = parser.parse_args()

    print("finance-agent → OpenClaw setup")
    print("=" * 40)

    if not SKILLS_SRC.exists():
        print(f"ERROR: skills directory not found at {SKILLS_SRC}")
        sys.exit(1)

    if args.data_dir:
        data_dir = str(Path(args.data_dir).expanduser().resolve())
    else:
        default_data = os.environ.get(
            "FINANCE_AGENT_DATA_DIR",
            str(Path.home() / ".config" / "finance_agent" / "data"),
        )
        raw = input(f"\nData directory path [{default_data}]: ").strip()
        data_dir = str(Path(raw or default_data).expanduser().resolve())

    ok = install_mtool()
    if not ok:
        print("\nWARNING: mtool install failed. Skills were not installed.")
        sys.exit(1)

    install_skills()
    configure_openclaw(data_dir)

    print("\nDone. Skills available in OpenClaw:")
    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            print(f"  /{skill_dir.name}")
    print(
        "\nStart OpenClaw from any directory and invoke skills with /skill-name.\n"
        "The data directory is pre-configured via FINANCE_AGENT_DATA_DIR."
    )


if __name__ == "__main__":
    main()
