#!/usr/bin/env python3
"""Render an Obsidian repository as GitHub-compatible Markdown.

Only files reported by ``git ls-files`` are exported. Source files are never
modified: the rendered repository is written to a separate output directory.
"""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import quote


WIKILINK_RE = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
FRONTMATTER_FIELD_RE = re.compile(r"^(id|citekey):[ \t]*(.+?)[ \t]*$", re.MULTILINE)
IMAGE_EXTENSIONS = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
NOTICE = "<!-- Generated from the Obsidian source on main. Do not edit this branch directly. -->"


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: PurePosixPath
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


class ExportError(Exception):
    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = sorted(diagnostics)
        super().__init__("\n".join(map(str, self.diagnostics)))


def tracked_files(source: Path) -> list[PurePosixPath]:
    process = subprocess.run(
        ["git", "-C", str(source), "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return [PurePosixPath(os.fsdecode(item)) for item in process.stdout.split(b"\0") if item]


def split_frontmatter(text: str) -> tuple[str, str, int]:
    """Return frontmatter, body, and the body's one-based starting line."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text, 1
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[: index + 1]), "".join(lines[index + 1 :]), index + 2
    return "", text, 1


def strip_heading_markup(value: str) -> str:
    value = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[*_~`]", "", value)
    return value.strip()


def github_slug(value: str) -> str:
    value = strip_heading_markup(value).casefold()
    characters: list[str] = []
    for character in value:
        category = unicodedata.category(character)
        if character in {"-", "_"} or character.isspace() or category[0] in {"L", "N", "M"}:
            characters.append(character)
    return re.sub(r"\s+", "-", "".join(characters)).strip("-")


def heading_index(body: str) -> tuple[dict[str, str], set[str]]:
    by_name: dict[str, str] = {}
    slugs: set[str] = set()
    slug_counts: Counter[str] = Counter()
    fence: str | None = None
    for line in body.splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            continue
        if fence is not None:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        name = strip_heading_markup(match.group(2))
        base_slug = github_slug(name)
        occurrence = slug_counts[base_slug]
        slug_counts[base_slug] += 1
        slug = base_slug if occurrence == 0 else f"{base_slug}-{occurrence}"
        by_name.setdefault(name.casefold(), slug)
        slugs.add(slug)
    return by_name, slugs


def normalise_relative(source: PurePosixPath, target: str) -> PurePosixPath | None:
    if target.startswith("/"):
        candidate = posixpath.normpath(target.lstrip("/"))
    else:
        candidate = posixpath.normpath(str(source.parent / target))
    if candidate in {"", ".", ".."} or candidate.startswith("../"):
        return None
    return PurePosixPath(candidate)


class RepositoryIndex:
    def __init__(self, root: Path, paths: list[PurePosixPath]):
        self.root = root
        self.paths = set(paths)
        self.markdown_paths = {path for path in paths if path.suffix.casefold() in {".md", ".markdown"}}
        self.by_stem: dict[str, list[PurePosixPath]] = defaultdict(list)
        self.headings: dict[PurePosixPath, tuple[dict[str, str], set[str]]] = {}
        self.frontmatters: dict[PurePosixPath, str] = {}
        self.bodies: dict[PurePosixPath, str] = {}
        self.body_start_lines: dict[PurePosixPath, int] = {}
        for path in sorted(self.markdown_paths):
            self.by_stem[path.stem.casefold()].append(path)
            text = (root / path).read_text(encoding="utf-8")
            frontmatter, body, body_line = split_frontmatter(text)
            self.frontmatters[path] = frontmatter
            self.bodies[path] = body
            self.body_start_lines[path] = body_line
            self.headings[path] = heading_index(body)

    def resolve(self, source: PurePosixPath, raw_target: str) -> tuple[PurePosixPath | None, str | None]:
        target = raw_target.strip().replace("\\", "/")
        if not target:
            return source, None
        if "://" in target:
            return None, "external URLs must use normal Markdown link syntax"

        is_path = "/" in target or target.startswith(".") or PurePosixPath(target).suffix != ""
        if is_path:
            candidate = normalise_relative(source, target)
            if candidate is None:
                return None, "link points outside the repository"
            candidates = [candidate]
            if not candidate.suffix:
                candidates.extend([candidate.with_suffix(".md"), candidate / "README.md"])
            for resolved in candidates:
                if resolved in self.paths:
                    return resolved, None
            return None, f"target does not exist: {target}"

        matches = self.by_stem.get(target.casefold(), [])
        if len(matches) == 1:
            return matches[0], None
        if not matches:
            return None, f"target does not exist: {target}"
        options = ", ".join(map(str, matches))
        return None, f"ambiguous basename {target!r}; use a path ({options})"


def markdown_destination(source: PurePosixPath, target: PurePosixPath, fragment: str | None) -> str:
    relative = posixpath.relpath(str(target), str(source.parent))
    encoded = quote(relative, safe="/._-~")
    return encoded + (f"#{fragment}" if fragment else "")


def default_label(target: PurePosixPath, heading: str | None) -> str:
    return heading or target.stem


def render_link(
    index: RepositoryIndex,
    source: PurePosixPath,
    embedded: bool,
    payload: str,
) -> tuple[str | None, str | None]:
    left, separator, alias = payload.partition("|")
    target_text, heading_separator, heading = left.partition("#")
    target, error = index.resolve(source, target_text)
    if error or target is None:
        return None, error
    if "^" in heading:
        return None, "Obsidian block references are not supported"

    fragment: str | None = None
    if heading_separator:
        heading_name = heading.strip()
        if not heading_name:
            return None, "empty heading reference"
        headings_by_name, slugs = index.headings.get(target, ({}, set()))
        fragment = headings_by_name.get(heading_name.casefold())
        if fragment is None:
            requested_slug = github_slug(heading_name)
            if requested_slug in slugs:
                fragment = requested_slug
            else:
                return None, f"heading does not exist in {target}: {heading_name}"

    label = alias.strip() if separator else default_label(target, heading.strip() or None)
    if not label:
        label = default_label(target, heading.strip() or None)
    destination = markdown_destination(source, target, fragment)
    if embedded and target.suffix.casefold() in IMAGE_EXTENSIONS:
        return f"![{label}]({destination})", None
    return f"[{label}]({destination})", None


def render_line_segments(
    line: str,
    transform,
    in_comment: bool,
) -> tuple[str, bool]:
    """Apply transform outside inline code and HTML comments."""
    result: list[str] = []
    cursor = 0
    code_delimiter: str | None = None
    while cursor < len(line):
        if in_comment:
            end = line.find("-->", cursor)
            if end < 0:
                result.append(line[cursor:])
                return "".join(result), True
            result.append(line[cursor : end + 3])
            cursor = end + 3
            in_comment = False
            continue
        if code_delimiter is not None:
            end = line.find(code_delimiter, cursor)
            if end < 0:
                result.append(line[cursor:])
                return "".join(result), in_comment
            result.append(line[cursor : end + len(code_delimiter)])
            cursor = end + len(code_delimiter)
            code_delimiter = None
            continue
        comment = line.find("<!--", cursor)
        tick = line.find("`", cursor)
        candidates = [(position, kind) for position, kind in ((comment, "comment"), (tick, "code")) if position >= 0]
        if not candidates:
            result.append(transform(line[cursor:]))
            break
        position, kind = min(candidates)
        result.append(transform(line[cursor:position]))
        if kind == "comment":
            in_comment = True
            result.append("<!--")
            cursor = position + 4
        else:
            end = position
            while end < len(line) and line[end] == "`":
                end += 1
            code_delimiter = line[position:end]
            result.append(code_delimiter)
            cursor = end
    return "".join(result), in_comment


def render_markdown(index: RepositoryIndex, path: PurePosixPath) -> tuple[str, list[Diagnostic]]:
    frontmatter = index.frontmatters[path]
    body = index.bodies[path]
    diagnostics: list[Diagnostic] = []
    if "[[" in frontmatter:
        diagnostics.append(Diagnostic(path, 1, "wikilinks are not allowed in YAML frontmatter; move relations into the body"))

    output_lines: list[str] = []
    fence: str | None = None
    in_comment = False
    body_line = index.body_start_lines[path]
    for offset, line in enumerate(body.splitlines(keepends=True)):
        line_number = body_line + offset
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            output_lines.append(line)
            continue
        if fence is not None:
            output_lines.append(line)
            continue

        def transform(segment: str) -> str:
            def replace(match: re.Match[str]) -> str:
                rendered, error = render_link(index, path, bool(match.group(1)), match.group(2))
                if error:
                    column_prefix = line[: line.find(segment)] + segment[: match.start()]
                    column = len(column_prefix) + 1
                    diagnostics.append(Diagnostic(path, line_number, f"column {column}: {error}"))
                    return match.group(0)
                assert rendered is not None
                return rendered

            return WIKILINK_RE.sub(replace, segment)

        rendered_line, in_comment = render_line_segments(line, transform, in_comment)
        output_lines.append(rendered_line)

    rendered_body = "".join(output_lines)
    if frontmatter:
        separator = "" if frontmatter.endswith("\n\n") else "\n"
        rendered = frontmatter + separator + NOTICE + "\n\n" + rendered_body.lstrip("\n")
    else:
        rendered = NOTICE + "\n\n" + rendered_body
    return rendered, diagnostics


def validate_metadata(index: RepositoryIndex) -> list[Diagnostic]:
    occurrences: dict[tuple[str, str], list[PurePosixPath]] = defaultdict(list)
    for path, frontmatter in index.frontmatters.items():
        for match in FRONTMATTER_FIELD_RE.finditer(frontmatter):
            value = match.group(2).strip().strip("\"'")
            if value:
                occurrences[(match.group(1), value)].append(path)
    diagnostics: list[Diagnostic] = []
    for (field, value), paths in occurrences.items():
        if len(paths) > 1:
            joined = ", ".join(map(str, paths))
            for path in paths:
                diagnostics.append(Diagnostic(path, 1, f"duplicate {field} {value!r}: {joined}"))
    return diagnostics


def export_repository(source: Path, output: Path | None = None) -> int:
    source = source.resolve()
    paths = tracked_files(source)
    index = RepositoryIndex(source, paths)
    rendered_files: dict[PurePosixPath, str] = {}
    diagnostics = validate_metadata(index)
    for path in sorted(index.markdown_paths):
        rendered, file_diagnostics = render_markdown(index, path)
        rendered_files[path] = rendered
        diagnostics.extend(file_diagnostics)
    if diagnostics:
        raise ExportError(diagnostics)

    if output is None:
        return len(paths)
    output = output.resolve()
    if output == source or output == source.parent:
        raise ValueError("output must not replace the source repository or its parent")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for path in paths:
        destination = output / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if path in rendered_files:
            destination.write_text(rendered_files[path], encoding="utf-8")
        else:
            shutil.copy2(source / path, destination)
    return len(paths)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("."), help="source Git repository")
    parser.add_argument("--output", type=Path, help="directory for the rendered repository")
    parser.add_argument("--check", action="store_true", help="validate only; write no files")
    args = parser.parse_args(argv)
    if not args.check and args.output is None:
        parser.error("--output is required unless --check is used")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        count = export_repository(args.source, None if args.check else args.output)
    except (ExportError, OSError, subprocess.CalledProcessError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    action = "Validated" if args.check else "Rendered"
    print(f"{action} {count} tracked files successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
