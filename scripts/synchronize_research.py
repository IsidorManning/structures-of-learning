#!/usr/bin/env python3
"""Reconcile source and main in temporary worktrees; optionally push both atomically."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from export_notes import ExportError, export_repository
from publish_rendered import (commit_tree, git, merge_trees, normalized_tree,
                              publication_pair, publish_head, rendered_tree, source_commits, worktree,
                              research_tree, apply_research)


def synchronize(repository: Path, source_ref: str, public_ref: str) -> tuple[str, str]:
    source = git(repository, "rev-parse", source_ref).strip()
    public = git(repository, "rev-parse", public_ref).strip()
    pair = publication_pair(repository, public)
    if pair:
        baseline, published_source = pair
        git(repository, "merge-base", "--is-ancestor", published_source, source)
    else:
        baseline = git(repository, "merge-base", source, public).strip()
    # Mirror only main's outstanding changes, not its complete rendered tree.
    # Compare main in rendered form. Historical manual source merges may have
    # changed link spelling alone; those must not become incoming prose edits.
    previous = research_tree(repository, rendered_tree(repository, baseline))
    current = research_tree(repository, source)
    for incoming_commit in source_commits(repository, baseline, public):
        incoming = research_tree(repository, rendered_tree(repository, incoming_commit))
        merged = merge_trees(repository, previous, current, incoming,
                             f"bringing main {incoming_commit} into source")
        if merged != current:
            message = git(repository, "show", "-s", "--format=%B", incoming_commit).rstrip()
            source = commit_tree(repository, apply_research(repository, source, merged, current), [source],
                                 f"{message}\n\nPublic-Commit: {incoming_commit}", incoming_commit)
        current, previous = merged, incoming
    with worktree(repository, source) as checkout:
        export_repository(checkout, notes_only=True)
    _, main = publish_head(repository, source, public)
    with worktree(repository, main) as checkout:
        export_repository(checkout)
    rendered = research_tree(repository, rendered_tree(repository, source))
    public_tree = research_tree(repository, main)
    if rendered != public_tree:
        details = git(repository, "diff", "--stat", rendered, public_tree)
        raise ValueError(f"Source and main did not converge after rendering; no refs were changed\n{details}")
    return source, main


def push(repository: Path, remote: str, source: str, main: str) -> None:
    # A concurrent edit to either branch rejects the complete update; no force pushes.
    git(repository, "push", "--atomic", remote,
        f"{source}:refs/heads/source", f"{main}:refs/heads/main")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--source-ref", default="origin/source")
    parser.add_argument("--public-ref", default="origin/main")
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--remote", default="origin")
    args = parser.parse_args()
    try:
        source, public = synchronize(args.repository.resolve(), args.source_ref, args.public_ref)
        if args.push:
            push(args.repository, args.remote, source, public)
    except (ExportError, OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"Synchronization stopped: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr, file=sys.stderr)
        return 1
    print(f"Source HEAD: {source}\nMain HEAD: {public}")
    print("Published both branches atomically." if args.push else "Preview only; branch refs were not changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

