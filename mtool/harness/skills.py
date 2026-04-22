from __future__ import annotations

from importlib.resources import files
from pathlib import Path


def iter_skills() -> list[tuple[str, str]]:
    """Return sorted list of (skill_name, SKILL.md content) from bundled package data."""
    root = files("mtool.skills")
    results = []
    for entry in root.iterdir():
        if entry.is_dir():
            content = (entry / "SKILL.md").read_text(encoding="utf-8")
            results.append((entry.name, content))
    return sorted(results)


def split_frontmatter(content: str) -> tuple[list[str], list[str]]:
    """Split SKILL.md into (frontmatter_lines, body_lines)."""
    lines = content.splitlines()
    delimiters = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delimiters) != 2:
        raise ValueError(
            f"Expected 2 frontmatter delimiters (---), found {len(delimiters)}"
        )
    fm_start, fm_end = delimiters[0], delimiters[1]
    return lines[fm_start + 1 : fm_end], lines[fm_end + 1 :]


def write_skill(dest: Path, content: str) -> str:
    """Write skill file. Returns 'installed', 'updated', or 'unchanged'."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        dest.write_text(content)
        return "installed"
    if dest.read_text() == content:
        return "unchanged"
    dest.write_text(content)
    return "updated"
