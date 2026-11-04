#!/usr/bin/env python3
"""Build a portable literature README from project notes, never from a personal vault."""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
from urllib.parse import quote

import yaml

START = "<!-- literature-index:start -->"
END = "<!-- literature-index:end -->"


def label(value: object) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip()
    return re.sub(r"([\\`*_{}\[\]<>#])", r"\\\1", text)


def build_index(folder: Path) -> str:
    groups: dict[str, dict[str, list[tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    keys: dict[str, Path] = {}
    for path in sorted(folder.rglob("*.md")):
        if path.name.casefold() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\s*\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
        if not match:
            continue
        data = yaml.safe_load(match[1])
        if not isinstance(data, dict) or data.get("type") != "literature":
            continue
        key = data.get("citekey")
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"{path}: missing citekey")
        if key in keys:
            raise ValueError(f"duplicate citekey {key!r}: {keys[key]} and {path}")
        keys[key] = path
        heading = re.search(r"^#\s+(.+)$", text[match.end():], re.MULTILINE)
        title = data.get("title") or (heading[1] if heading else None)
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"{path}: missing title")
        authors = data.get("authors", [])
        if isinstance(authors, str):
            authors = [authors]
        if not isinstance(authors, list) or any(not isinstance(author, str) or not author.strip() for author in authors):
            raise ValueError(f"{path}: authors must be names or a list of names")
        first = authors[0] if authors else "Unknown author"
        surname = first.split(",")[0] if "," in first else first.split()[-1]
        author = surname + (" et al." if len(authors) > 1 else "")
        topic, subtopic = data.get("topic") or "Uncategorized", data.get("subtopic") or ""
        if not isinstance(topic, str) or not isinstance(subtopic, str):
            raise ValueError(f"{path}: topic and subtopic must be text")
        destination = quote(path.relative_to(folder).as_posix(), safe="/._-~")
        entry = f"- [{label(author)} ({label(data.get('year') or 'n.d.')}) — {label(title)}]({destination})"
        groups[topic.strip() or "Uncategorized"][subtopic.strip()].append((title.casefold(), entry))
    lines = [START, "<!-- Edit paper topic/subtopic metadata to update this index. -->", ""]
    for topic in sorted(groups, key=str.casefold):
        lines.extend([f"## {label(topic)}", ""])
        for subtopic in sorted(groups[topic], key=str.casefold):
            if subtopic:
                lines.extend([f"### {label(subtopic)}", ""])
            lines.extend(entry for _, entry in sorted(groups[topic][subtopic]))
            lines.append("")
    if not groups:
        lines.extend(["No literature notes yet.", ""])
    lines.append(END)
    return "\n".join(lines)


def update_readme(folder: Path) -> None:
    generated = build_index(folder)
    path = folder / "README.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Literature\n\n"
    if START in existing or END in existing:
        if existing.count(START) != 1 or existing.count(END) != 1 or existing.index(START) > existing.index(END):
            raise ValueError(f"{path}: invalid literature index markers")
        result = existing[:existing.index(START)] + generated + existing[existing.index(END) + len(END):]
    else:
        # Preserve historical, manually curated indexes; never replace them silently.
        result = existing.rstrip() + "\n\n" + generated + "\n"
    path.write_text(result, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--literature", type=Path, default=Path("literature"))
    update_readme(parser.parse_args().literature)

