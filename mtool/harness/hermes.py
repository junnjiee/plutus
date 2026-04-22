"""Hermes Agent harness — transform and install finance-agent skills."""

from __future__ import annotations

import os
import re
from pathlib import Path

from mtool.constants import ADAPTER_NOTE, HERMES_META
from mtool.harness.skills import iter_skills, split_frontmatter, write_skill


def _extra_frontmatter(skill_name: str, data_dir: str) -> str:
    if skill_name not in HERMES_META:
        raise ValueError(f"Unknown skill: {skill_name}")
    meta = HERMES_META[skill_name]
    tags = "[" + ", ".join(f'"{t}"' for t in meta["tags"]) + "]"
    related = "[" + ", ".join(f'"{s}"' for s in meta["related_skills"]) + "]"
    return (
        f"version: 0.7.0\n"
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
        f'        default: "{data_dir}"\n'
        f"        prompt: Where is your finance-agent data directory?\n"
    )


def _transform(content: str, skill_name: str, data_dir: str) -> str:
    """Inject Hermes frontmatter and adapter note into a SKILL.md."""
    frontmatter, body = split_frontmatter(content)
    extra = _extra_frontmatter(skill_name, data_dir).splitlines()
    new_fm = ["---"] + frontmatter + extra + ["---"]
    new_body = ["", *ADAPTER_NOTE.splitlines(), ""] + body
    return "\n".join(new_fm + new_body)


def _configure(data_dir: str, hermes_home: Path):
    """Update ~/.hermes/config.yaml with finance_agent.data_dir."""
    config_path = hermes_home / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Hermes config not found at {config_path}")

    existing = config_path.read_text()
    quoted = f'"{data_dir}"'

    if "finance_agent" in existing:
        updated = re.sub(
            r"(finance_agent:\s*\n\s*data_dir:\s*).*",
            f"\\1{quoted}",
            existing,
        )
        if updated != existing:
            config_path.write_text(updated)
            print(f"  updated    finance_agent.data_dir → {data_dir}")
    else:
        fa_block = f"  config:\n    finance_agent:\n      data_dir: {quoted}\n"
        # Try inserting under existing config: key
        updated = re.sub(
            r"(^  config\s*:[ \t]*\n)",
            r"\1" + f"    finance_agent:\n      data_dir: {quoted}\n",
            existing,
            count=1,
            flags=re.MULTILINE,
        )
        # If no config: key, inject it under skills:
        if updated == existing:
            updated = re.sub(
                r"(^skills\s*:[ \t]*\n)",
                r"\1" + fa_block,
                existing,
                count=1,
                flags=re.MULTILINE,
            )
        if updated == existing:
            raise RuntimeError(
                f"Could not inject finance_agent config into {config_path}. "
                "Expected a 'skills:' section."
            )
        config_path.write_text(updated)
        print(f"  installed  finance_agent.data_dir → {data_dir}")


def install(data_dir: str, hermes_home: Path | None = None):
    """Transform and install all skills into Hermes."""
    if hermes_home is None:
        hermes_home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))

    if not hermes_home.exists():
        print(f"Hermes not found at {hermes_home}. Install Hermes Agent first.")
        return False

    skills_dir = hermes_home / "skills" / "finance_agent"
    print(f"\nInstalling skills to {skills_dir} ...")

    installed, updated, unchanged = [], [], []
    for skill_name, content in iter_skills():
        transformed = _transform(content, skill_name, data_dir)
        dest = skills_dir / skill_name / "SKILL.md"
        result = write_skill(dest, transformed)
        if result == "installed":
            installed.append(skill_name)
        elif result == "updated":
            updated.append(skill_name)
        else:
            unchanged.append(skill_name)

    _configure(data_dir, hermes_home)

    print(f"new skills: {installed}")
    print(f"updated skills: {updated}")
    return True
