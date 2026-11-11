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
from urllib.parse import quote, unquote, urlsplit

from note_format import clean_markdown, START, END, server_owned


WIKILINK_RE = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r'!?\[[^\]\n]*\]\((?:<([^>\n]*)>|([^\s)\n]+))(?:[ \t]+["\'][^\n]*?["\'])?\)')
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
FRONTMATTER_FIELD_RE = re.compile(r"^(id|citekey):[ \t]*(.+?)[ \t]*$", re.MULTILINE)
IMAGE_EXTENSIONS = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


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


def escaped(text: str, position: int) -> bool:
    """Whether a delimiter is preceded by an odd number of backslashes."""
    start = position
    while start and text[start - 1] == "\\":
        start -= 1
    return (position - start) % 2 == 1


def math_end(line: str, delimiter: str, start: int) -> int:
    for match in re.finditer(re.escape(delimiter), line[start:]):
        position = start + match.start()
        if escaped(line, position):
            continue
        if delimiter == "$" and (
            position == 0 or line[position - 1].isspace()
            or line[position - 1] == "$"
            or (position + 1 < len(line) and (line[position + 1].isdigit() or line[position + 1] == "$"))
        ):
            continue
        return position
    return -1


def render_line_segments(
    line: str,
    transform,
    in_comment: bool,
    math_delimiter: str | None = None,
    following_lines: str = "",
) -> tuple[str, bool, str | None]:
    """Apply transform outside code, comments, and TeX math; retain display state."""
    result: list[str] = []
    cursor = 0
    while cursor < len(line):
        if in_comment or math_delimiter:
            closing = "-->" if in_comment else math_delimiter
            end = line.find(closing, cursor) if in_comment else math_end(line, closing, cursor)
            if end < 0:
                result.append(line[cursor:])
                break
            result.append(line[cursor:end + len(closing)])
            cursor = end + len(closing)
            in_comment, math_delimiter = False, None
            continue
        token = None
        for match in re.finditer(r"<!--|`+|\$\$|\$|\\\(|\\\[", line[cursor:]):
            position = cursor + match.start()
            marker = match.group()
            if escaped(line, position):
                continue
            if marker == "$":
                # An unmatched dollar/currency amount must not hide real links.
                if position + 1 == len(line) or line[position + 1].isspace():
                    continue
                if math_end(line, "$", position + 1) < 0:
                    continue
            if marker in {"$$", r"\(", r"\["}:
                closing = {r"\(": r"\)", r"\[": r"\]"}.get(marker, marker)
                if math_end(line + following_lines, closing, position + len(marker)) < 0:
                    continue
            token = (position, marker)
            break
        if token is None:
            result.append(transform(line[cursor:]))
            break
        position, marker = token
        result.append(transform(line[cursor:position]))
        result.append(marker)
        cursor = position + len(marker)
        if marker == "<!--":
            in_comment = True
        elif marker.startswith("`"):
            end = line.find(marker, cursor)
            if end < 0:
                result.append(line[cursor:])
                break
            result.append(line[cursor:end + len(marker)])
            cursor = end + len(marker)
        else:
            math_delimiter = {r"\(": r"\)", r"\[": r"\]"}.get(marker, marker)
    return "".join(result), in_comment, math_delimiter


def render_markdown(index: RepositoryIndex, path: PurePosixPath) -> tuple[str, list[Diagnostic]]:
    frontmatter = index.frontmatters[path]
    body = index.bodies[path]
    diagnostics: list[Diagnostic] = []
    if "[[" in frontmatter:
        diagnostics.append(Diagnostic(path, 1, "wikilinks are not allowed in YAML frontmatter; move relations into the body"))

    output_lines: list[str] = []
    fence: str | None = None
    in_comment = False
    in_generated_index = False
    math_delimiter: str | None = None
    if str(path) == "literature/README.md":
        clean_markdown(body, strip_index=True)  # Validate the marker pair.
    body_line = index.body_start_lines[path]
    remaining_body = body
    for offset, line in enumerate(body.splitlines(keepends=True)):
        line_number = body_line + offset
        remaining_body = remaining_body[len(line):]
        if str(path) == "literature/README.md" and fence is None:
            if line.strip() == START:
                in_generated_index = True
            if in_generated_index:
                output_lines.append(line)
                if line.strip() == END:
                    in_generated_index = False
                continue
        fence_match = FENCE_RE.match(line) if not math_delimiter and not in_comment else None
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
            for link in MARKDOWN_LINK_RE.finditer(segment):
                destination = link.group(1) if link.group(1) is not None else link.group(2)
                parts = urlsplit(destination)
                if parts.scheme or parts.netloc:
                    continue
                target = normalise_relative(path, unquote(parts.path)) if parts.path else path
                if target is None or target not in index.paths:
                    diagnostics.append(Diagnostic(path, line_number, f"Markdown target does not exist: {destination}"))
                elif parts.fragment and target in index.headings:
                    if unquote(parts.fragment) not in index.headings[target][1]:
                        diagnostics.append(Diagnostic(path, line_number, f"Markdown heading does not exist: {destination}"))

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

        rendered_line, in_comment, math_delimiter = render_line_segments(
            line, transform, in_comment, math_delimiter, remaining_body
        )
        output_lines.append(rendered_line)

    rendered_body = "".join(output_lines)
    rendered = clean_markdown(frontmatter + rendered_body)
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


def export_repository(source: Path, output: Path | None = None, *, build_index: bool = True,
                      check_metadata: bool = True, notes_only: bool = False) -> int:
    source = source.resolve()
    paths = tracked_files(source)
    if notes_only:
        paths = [path for path in paths if not server_owned(str(path))]
    index = RepositoryIndex(source, paths)
    rendered_files: dict[PurePosixPath, str] = {}
    diagnostics = validate_metadata(index) if check_metadata else []
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
    # Build from the exported snapshot: CI has no access to the personal vault.
    if build_index and (output / "literature").is_dir():
        from build_literature_index import update_readme

        update_readme(output / "literature")
    return len(paths)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("."), help="source Git repository")
    parser.add_argument("--output", type=Path, help="directory for the rendered repository")
    parser.add_argument("--check", action="store_true", help="validate only; write no files")
    parser.add_argument("--notes-only", action="store_true", help="validate/export research content without GitHub-owned infrastructure and indexes")
    args = parser.parse_args(argv)
    if not args.check and args.output is None:
        parser.error("--output is required unless --check is used")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        count = export_repository(args.source, None if args.check else args.output, notes_only=args.notes_only)
    except (ExportError, OSError, subprocess.CalledProcessError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    action = "Validated" if args.check else "Rendered"
    print(f"{action} {count} tracked files successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

