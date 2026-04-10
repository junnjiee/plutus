#!/usr/bin/env python3
"""
hermes/setup.py — Install finance-agent skills and mtool into Hermes Agent.

Usage:
    python hermes/setup.py
    uv run python hermes/setup.py
"""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_SRC = REPO_ROOT / ".agents" / "skills"
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
HERMES_SKILLS_DIR = HERMES_HOME / "skills" / "finance_agent"
HERMES_CONFIG = HERMES_HOME / "config.yaml"

SKILL_META = {
    "fa-onboard": {
        "tags": ["finance", "personal-finance", "setup", "onboarding"],
        "related_skills": ["fa-net-worth", "fa-analyze-cashflow", "fa-liability-tracker"],
    },
    "fa-net-worth": {
        "tags": ["finance", "personal-finance", "net-worth", "portfolio"],
        "related_skills": ["fa-onboard", "fa-analyze-cashflow", "fa-liability-tracker"],
    },
    "fa-analyze-cashflow": {
        "tags": ["finance", "personal-finance", "cashflow", "runway", "savings"],
        "related_skills": ["fa-onboard", "fa-net-worth", "fa-liability-tracker"],
    },
    "fa-liability-tracker": {
        "tags": ["finance", "personal-finance", "liabilities", "subscriptions"],
        "related_skills": ["fa-onboard", "fa-analyze-cashflow", "fa-net-worth"],
    },
}

ADAPTER_NOTE = """\
> **Hermes adapter note:** All `data/` path references below should be resolved
> using the `finance_agent.data_dir` value from the skill config injected above.
> Use `mtool` directly — it is installed globally. No `uv sync` step is needed.
"""


# ---------------------------------------------------------------------------
# Skill generation
# ---------------------------------------------------------------------------

def build_extra_frontmatter(skill_name: str, data_dir: str) -> str:
    meta = SKILL_META.get(skill_name, {"tags": ["finance"], "related_skills": []})
    tags = "[" + ", ".join(f'"{t}"' for t in meta["tags"]) + "]"
    related = "[" + ", ".join(f'"{s}"' for s in meta["related_skills"]) + "]"
    return (
        f"version: 1.0.0\n"
        f"author: finance-agent\n"
        f"license: MIT\n"
        f"prerequisites:\n"
        f"  commands: [mtool]\n"
        f"metadata:\n"
        f"  hermes:\n"
        f"    tags: {tags}\n"
        f"    related_skills: {related}\n"
        f"    config:\n"
        f"      - key: finance_agent.data_dir\n"
        f"        description: Absolute path to the finance-agent data directory\n"
        f"        default: \"{data_dir}\"\n"
        f"        prompt: Where is your finance-agent data directory?\n"
    )


def transform(content: str, skill_name: str, data_dir: str) -> str:
    """
    Given the raw source SKILL.md, produce a Hermes-flavored version by:
      1. Injecting extra YAML fields before the closing --- of the frontmatter.
      2. Inserting an adapter note at the start of the body.
      3. Replacing venv-relative tool paths with their global equivalents.
    """
    lines = content.splitlines()

    # Find the two --- delimiter positions
    delimiters = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delimiters) < 2:
        return content  # not standard frontmatter, return unchanged

    fm_start, fm_end = delimiters[0], delimiters[1]
    frontmatter = lines[fm_start + 1 : fm_end]
    body = lines[fm_end + 1 :]

    # 1. Build the new frontmatter block
    extra = build_extra_frontmatter(skill_name, data_dir).splitlines()
    new_frontmatter = ["---"] + frontmatter + extra + ["---"]

    # 2. Prepend the adapter note to the body (after any leading blank lines)
    adapter_lines = ["", *ADAPTER_NOTE.splitlines(), ""]
    new_body = adapter_lines + body

    # 3. Fix venv-relative tool calls
    result = "\n".join(new_frontmatter + new_body)
    result = result.replace(".venv/bin/mtool", "mtool")
    result = result.replace(".venv/bin/python", "python3")
    result = result.replace(
        "prepare the project environment with `uv sync`",
        "ensure `mtool` is installed (run `python hermes/setup.py` from the finance-agent repo)",
    )
    result = result.replace(
        "ensure the project environment is ready with `uv sync`",
        "ensure `mtool` is installed (run `python hermes/setup.py` from the finance-agent repo)",
    )
    result = result.replace(
        "If the environment is not ready yet, run `uv sync` first",
        "mtool is installed globally — no environment activation needed",
    )
    result = result.replace(
        "prepare the environment with `uv sync` and use",
        "use",
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


def install_skills(data_dir: str):
    print(f"\nGenerating and installing skills to {HERMES_SKILLS_DIR} ...")
    HERMES_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if not skill_dir.is_dir():
            continue
        source = skill_dir / "SKILL.md"
        if not source.exists():
            continue

        skill_name = skill_dir.name
        generated = transform(source.read_text(), skill_name, data_dir)

        dest_dir = HERMES_SKILLS_DIR / skill_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "SKILL.md"
        action = "updated" if dest.exists() else "installed"
        dest.write_text(generated)
        print(f"  {action}  /{skill_name}")


def configure_hermes(data_dir: str):
    """Write or update finance_agent.data_dir in ~/.hermes/config.yaml."""
    import re

    HERMES_HOME.mkdir(parents=True, exist_ok=True)
    quoted_dir = f'"{data_dir}"'

    # Used when the file does not exist or has no skills: key at all.
    new_block = (
        "# finance-agent skill configuration (added by hermes/setup.py)\n"
        "skills:\n"
        "  config:\n"
        "    finance_agent:\n"
        f"      data_dir: {quoted_dir}\n"
    )

    if not HERMES_CONFIG.exists():
        HERMES_CONFIG.write_text(new_block)
        print(f"\n  installed  {HERMES_CONFIG}")
        return

    existing = HERMES_CONFIG.read_text()

    # Case: finance_agent block already exists → update data_dir value in place.
    if "finance_agent" in existing:
        updated = re.sub(
            r"(finance_agent:\s*\n\s*data_dir:\s*).*",
            f"\\1{quoted_dir}",
            existing,
        )
        HERMES_CONFIG.write_text(updated)
        print(f"\n  updated    finance_agent.data_dir → {data_dir}")
        return

    # Case: skills: key exists but no finance_agent block → insert under it.
    if re.search(r"^skills\s*:", existing, re.MULTILINE):
        finance_agent_block = (
            "  config:\n"
            "    finance_agent:\n"
            f"      data_dir: {quoted_dir}\n"
        )
        updated = re.sub(
            r"(^skills\s*:\s*\n)",
            r"\1" + finance_agent_block,
            existing,
            count=1,
            flags=re.MULTILINE,
        )
        HERMES_CONFIG.write_text(updated)
        print(f"\n  installed  finance_agent.data_dir → {data_dir}")
        return

    # Case: no skills: key at all → append the full block.
    with open(HERMES_CONFIG, "a") as f:
        separator = "\n" if existing and not existing.endswith("\n") else ""
        f.write(f"{separator}\n{new_block}")
    print(f"\n  installed  finance_agent.data_dir → {data_dir}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("finance-agent → Hermes Agent setup")
    print("=" * 40)

    if not SKILLS_SRC.exists():
        print(f"ERROR: skills directory not found at {SKILLS_SRC}")
        sys.exit(1)

    default_data = str(REPO_ROOT / "data")
    raw = input(f"\nData directory path [{default_data}]: ").strip()
    data_dir = raw or default_data

    ok = install_mtool()
    if not ok:
        print("\nWARNING: mtool install failed. Skills were not installed.")
        sys.exit(1)

    install_skills(data_dir)
    configure_hermes(data_dir)

    print("\nDone. Skills available in Hermes:")
    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            print(f"  /{skill_dir.name}")
    print(
        "\nStart Hermes from any directory and invoke skills with /skill-name.\n"
        "The data directory is pre-configured — Hermes will use it automatically."
    )


if __name__ == "__main__":
    main()
