#!/usr/bin/env python3
"""Merge rendered source changes into main without replacing independent edits.

All checkouts are disposable worktrees. The caller's checkout and branch refs
are never changed. synchronize_research coordinates both directions.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from export_notes import ExportError, export_repository
from note_format import clean_markdown, server_owned

SOURCE_TRAILER_RE = re.compile(r"^Source-Commit: ([0-9a-f]{40,64})$", re.MULTILINE)
BOT = {"GIT_AUTHOR_NAME": "github-actions[bot]",
       "GIT_AUTHOR_EMAIL": "41898282+github-actions[bot]@users.noreply.github.com",
       "GIT_COMMITTER_NAME": "github-actions[bot]",
       "GIT_COMMITTER_EMAIL": "41898282+github-actions[bot]@users.noreply.github.com"}


def git(repository: Path, *arguments: str, input: str | None = None,
        env: dict[str, str] | None = None) -> str:
    result = subprocess.run(["git", "-C", str(repository), *arguments], check=True,
                            input=input, text=True, encoding="utf-8", stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=env)
    return result.stdout


def publication_pair(repository: Path, ref: str = "HEAD") -> tuple[str, str] | None:
    # Direct main commits need not carry a marker; search first-parent history.
    records = git(repository, "log", "--first-parent", "--format=%H%x00%B%x00", ref).split("\0")
    for index in range(0, len(records) - 1, 2):
        matches = SOURCE_TRAILER_RE.findall(records[index + 1])
        if matches:
            return records[index].strip(), matches[-1]
    return None


def latest_source_marker(public_repository: Path) -> str | None:
    pair = publication_pair(public_repository)
    return pair[1] if pair else None


def source_commits(repository: Path, start: str, end: str) -> list[str]:
    return git(repository, "rev-list", "--reverse", "--first-parent", f"{start}..{end}").splitlines()


@contextmanager
def worktree(repository: Path, ref: str):
    with tempfile.TemporaryDirectory(prefix="research-sync-") as temporary:
        path = Path(temporary) / "checkout"
        git(repository, "worktree", "add", "--detach", str(path), ref)
        try:
            yield path
        finally:
            git(repository, "worktree", "remove", "--force", str(path))


def directory_tree(repository: Path, directory: Path, base: str | None = None) -> str:
    with tempfile.TemporaryDirectory(prefix="research-index-") as temporary:
        environment = os.environ.copy()
        environment["GIT_INDEX_FILE"] = str(Path(temporary) / "index")
        gitdir = git(repository, "rev-parse", "--absolute-git-dir").strip()
        arguments = ["git", f"--git-dir={gitdir}", f"--work-tree={directory}"]
        if base is None and (directory / ".git").exists():
            base = git(directory, "rev-parse", "HEAD").strip()
        for command in [["read-tree", base] if base else ["read-tree", "--empty"], ["add", "--all", "--force"]]:
            subprocess.run(arguments + command, cwd=directory, env=environment,
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return subprocess.run(arguments + ["write-tree"], cwd=directory, env=environment,
                              check=True, text=True, stdout=subprocess.PIPE).stdout.strip()


def normalized_tree(repository: Path, ref: str) -> str:
    with tempfile.TemporaryDirectory(prefix="research-index-") as temporary:
        environment = os.environ.copy()
        environment["GIT_INDEX_FILE"] = str(Path(temporary) / "index")
        git(repository, "read-tree", ref, env=environment)
        markdown = []
        for record in git(repository, "ls-tree", "-rz", "--full-tree", ref).split("\0"):
            if not record:
                continue
            header, path = record.split("\t", 1)
            mode, kind, oid = header.split()
            if kind != "blob" or mode not in {"100644", "100755"} or Path(path).suffix.lower() not in {".md", ".markdown"}:
                continue
            markdown.append((mode, oid, path))
        # Batch reads keep synchronization practical for a vault with many notes.
        data = subprocess.run(["git", "-C", str(repository), "cat-file", "--batch"],
                              input="".join(oid + "\n" for _, oid, _ in markdown).encode(),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
        cursor = 0
        updates = []
        for mode, oid, path in markdown:
            end = data.index(b"\n", cursor)
            header = data[cursor:end].split()
            if len(header) != 3 or header[1] != b"blob":
                raise ValueError(f"Cannot read Markdown blob {oid}")
            size = int(header[2])
            raw = data[end + 1:end + 1 + size]
            cursor = end + size + 2
            original = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
            cleaned = clean_markdown(original, strip_index=path == "literature/README.md")
            if cleaned.encode("utf-8") != raw:
                blob = git(repository, "hash-object", "-w", "--stdin", input=cleaned).strip()
                updates.append(f"{mode} {blob}\t{path}\0")
        if updates:
            git(repository, "update-index", "-z", "--index-info", input="".join(updates), env=environment)
        return git(repository, "write-tree", env=environment).strip()


def rendered_tree(repository: Path, ref: str) -> str:
    with worktree(repository, ref) as checkout, tempfile.TemporaryDirectory(prefix="research-render-") as temporary:
        output = Path(temporary) / "rendered"
        # Intermediate historical metadata may have been repaired by a later
        # commit. Final source/public snapshots are validated strictly below.
        export_repository(checkout, output, build_index=False, check_metadata=False, notes_only=True)
        return normalized_tree(repository, directory_tree(repository, output, ref))


def tree_entries(repository: Path, ref: str) -> dict[str, tuple[str, str]]:
    entries = {}
    for record in git(repository, "ls-tree", "-rz", "--full-tree", ref).split("\0"):
        if record:
            header, path = record.split("\t", 1)
            mode, _kind, oid = header.split()
            entries[path] = (mode, oid)
    return entries


def research_tree(repository: Path, ref: str) -> str:
    tree = normalized_tree(repository, ref)
    entries = tree_entries(repository, tree)
    remove = [path for path in entries if server_owned(path)]
    scaffold = entries.get("literature/README.md")
    if scaffold and git(repository, "cat-file", "blob", scaffold[1]).strip() == "# Literature":
        remove.append("literature/README.md")
    with tempfile.TemporaryDirectory(prefix="research-policy-") as temporary:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(Path(temporary) / "index")
        git(repository, "read-tree", tree, env=env)
        if remove:
            git(repository, "update-index", "--force-remove", "--", *remove, env=env)
        return git(repository, "write-tree", env=env).strip()


def apply_research(repository: Path, target: str, incoming: str, before: str | None = None) -> str:
    """Keep server files on their own branch; update only changed notes in source."""
    old = tree_entries(repository, target if before is None else before)
    new = tree_entries(repository, incoming)
    paths = {path for path in old.keys() | new.keys() if not server_owned(path)}
    if before is not None:
        paths = {path for path in paths if old.get(path) != new.get(path)}
    with tempfile.TemporaryDirectory(prefix="research-policy-") as temporary:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(Path(temporary) / "index")
        git(repository, "read-tree", target, env=env)
        updates = []
        for path in sorted(paths):
            if before is None and path == "literature/README.md" and path not in new:
                body = git(repository, "cat-file", "blob", old[path][1])
                if clean_markdown(body, strip_index=True).strip() == "# Literature":
                    continue  # Keep the public index scaffold after the last paper is deleted.
            if path in new:
                mode, oid = new[path]
                updates.append(f"{mode} {oid}\t{path}\0")
            else:
                git(repository, "update-index", "--force-remove", "--", path, env=env)
        if updates:
            git(repository, "update-index", "-z", "--index-info", input="".join(updates), env=env)
        return git(repository, "write-tree", env=env).strip()


def commit_tree(repository: Path, tree: str, parents: list[str], message: str,
                original: str | None = None) -> str:
    environment = os.environ.copy()
    environment.update(BOT)
    if original:
        name, email, date = git(repository, "show", "-s", "--format=%an%x00%ae%x00%aI", original).strip().split("\0")
        environment.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_AUTHOR_DATE=date)
    arguments = ["commit-tree", tree]
    for parent in parents:
        arguments.extend(["-p", parent])
    return git(repository, *arguments, input=message + "\n", env=environment).strip()


class SyncConflict(ValueError):
    pass


def merge_trees(repository: Path, base: str, ours: str, theirs: str, context: str) -> str:
    if ours == theirs or base == theirs:
        return ours
    if base == ours:
        return theirs
    ancestor = commit_tree(repository, base, [], "Temporary merge base")
    left = commit_tree(repository, ours, [ancestor], "Temporary current tree")
    right = commit_tree(repository, theirs, [ancestor], "Temporary incoming tree")
    result = subprocess.run(["git", "-C", str(repository), "merge-tree", "--write-tree", "--name-only", left, right],
                            text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        if result.returncode != 1:
            raise ValueError(f"Git could not merge {context}: {result.stderr}")
        raise SyncConflict(f"Conflict while {context}. No branch refs were changed.\n{result.stdout.partition(chr(10))[2]}")
    return result.stdout.splitlines()[0]


def with_index(repository: Path, tree: str) -> str:
    from build_literature_index import update_readme

    commit = commit_tree(repository, tree, [], "Temporary index input")
    with worktree(repository, commit) as checkout:
        if (checkout / "literature").is_dir():
            update_readme(checkout / "literature")
        return directory_tree(repository, checkout)


def message_with_source_trailer(message: str, source_commit: str) -> str:
    return f"{SOURCE_TRAILER_RE.sub('', message).rstrip()}\n\nSource-Commit: {source_commit}\n"


def publish_head(repository: Path, source_ref: str, public_ref: str) -> tuple[int, str]:
    source_head = git(repository, "rev-parse", source_ref).strip()
    public_head = git(repository, "rev-parse", public_ref).strip()
    with worktree(repository, source_head) as checkout:
        export_repository(checkout, notes_only=True)
    pair = publication_pair(repository, public_head)
    marker = pair[1] if pair else git(repository, "merge-base", public_head, source_head).strip()
    git(repository, "merge-base", "--is-ancestor", marker, source_head)
    previous = research_tree(repository, rendered_tree(repository, marker))
    # Older manual source merges can have left wikilinks on main. Convert those
    # too, retaining all of main's independent content before merging new deltas.
    current = research_tree(repository, rendered_tree(repository, public_head))
    commits = source_commits(repository, marker, source_head)
    for source_commit in commits:
        incoming = research_tree(repository, rendered_tree(repository, source_commit))
        current = merge_trees(repository, previous, current, incoming, f"publishing source {source_commit}")
        tree = with_index(repository, apply_research(repository, public_head, current))
        message = git(repository, "show", "-s", "--format=%B", source_commit)
        public_head = commit_tree(repository, tree, [public_head], message_with_source_trailer(message, source_commit), source_commit)
        previous = incoming
    # Also handles one-time banner cleanup and index refresh without new source commits.
    final = with_index(repository, apply_research(repository, public_head, current))
    if final != git(repository, "rev-parse", f"{public_head}^{{tree}}").strip():
        public_head = commit_tree(repository, final, [public_head],
                                  message_with_source_trailer("Refresh research publication", source_head))
    with worktree(repository, public_head) as checkout:
        export_repository(checkout)
    return len(commits), public_head


def publish(source_repository: Path, source_ref: str, public_ref: str,
            public_worktree: Path, rendered_directory: Path) -> tuple[int, str]:
    """Compatibility entry point: prepare a new public worktree, never move refs."""
    count, head = publish_head(source_repository.resolve(), source_ref, public_ref)
    if public_worktree.exists():
        raise ValueError("public worktree must be a new directory")
    public_worktree.parent.mkdir(parents=True, exist_ok=True)
    git(source_repository, "worktree", "add", "--detach", str(public_worktree.resolve()), head)
    return count, head


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("."))
    parser.add_argument("--source-ref", default="HEAD")
    parser.add_argument("--public-ref", default="origin/main")
    parser.add_argument("--public-worktree", type=Path, required=True)
    parser.add_argument("--rendered-directory", type=Path, required=True)
    args = parser.parse_args()
    try:
        count, head = publish(args.source, args.source_ref, args.public_ref, args.public_worktree, args.rendered_directory)
    except (ExportError, OSError, subprocess.CalledProcessError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Prepared {count} rendered commit(s); public HEAD is {head}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

