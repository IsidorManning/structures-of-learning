#!/usr/bin/env python3
"""Replay source commits as rendered commits on GitHub's public branch.

The source and public histories necessarily have different commit hashes because
their Markdown trees differ. This publisher preserves each source commit's
author, authored date, subject, and body, and adds a Source-Commit trailer so a
later run knows exactly where publication last stopped.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from export_notes import ExportError, export_repository


SOURCE_TRAILER = "Source-Commit"
SOURCE_TRAILER_RE = re.compile(r"^Source-Commit: ([0-9a-f]{40,64})$", re.MULTILINE)


def git(repository: Path, *arguments: str, capture: bool = True, env: dict[str, str] | None = None) -> str:
    process = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        env=env,
    )
    return process.stdout if capture else ""


def latest_source_marker(public_repository: Path) -> str | None:
    message = git(public_repository, "log", "-1", "--format=%B")
    matches = SOURCE_TRAILER_RE.findall(message)
    return matches[-1] if matches else None


def source_commits(source_repository: Path, start: str, end: str) -> list[str]:
    output = git(source_repository, "rev-list", "--reverse", "--first-parent", f"{start}..{end}")
    return [line for line in output.splitlines() if line]


def copy_rendered_tree(rendered: Path, public: Path) -> None:
    for child in public.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    for child in rendered.iterdir():
        destination = public / child.name
        if child.is_dir() and not child.is_symlink():
            shutil.copytree(child, destination, symlinks=True)
        elif child.is_symlink():
            destination.symlink_to(os.readlink(child))
        else:
            shutil.copy2(child, destination)


def commit_metadata(source_repository: Path, commit: str) -> tuple[str, str, str, str]:
    record = git(
        source_repository,
        "show",
        "-s",
        "--format=%an%x00%ae%x00%aI%x00%B",
        commit,
    )
    name, email, authored_date, message = record.split("\0", 3)
    return name, email, authored_date, message.rstrip("\n")


def message_with_source_trailer(message: str, source_commit: str) -> str:
    cleaned = SOURCE_TRAILER_RE.sub("", message).rstrip()
    return f"{cleaned}\n\n{SOURCE_TRAILER}: {source_commit}\n"


def prepare_public_worktree(source_repository: Path, public_ref: str, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    git(source_repository, "worktree", "add", "--detach", str(destination), public_ref, capture=False)


def current_checkout(repository: Path) -> str:
    symbolic = subprocess.run(
        ["git", "-C", str(repository), "symbolic-ref", "--quiet", "--short", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
    )
    if symbolic.returncode == 0:
        return symbolic.stdout.strip()
    return git(repository, "rev-parse", "HEAD").strip()


def publish(
    source_repository: Path,
    source_ref: str,
    public_ref: str,
    public_worktree: Path,
    rendered_directory: Path,
) -> tuple[int, str]:
    source_repository = source_repository.resolve()
    public_worktree = public_worktree.resolve()
    rendered_directory = rendered_directory.resolve()
    prepare_public_worktree(source_repository, public_ref, public_worktree)

    marker = latest_source_marker(public_worktree)
    if marker is None:
        marker = git(source_repository, "merge-base", public_ref, source_ref).strip()
        if not marker:
            raise ValueError(f"{public_ref} and {source_ref} have no common ancestor")
    ancestor_check = subprocess.run(
        ["git", "-C", str(source_repository), "merge-base", "--is-ancestor", marker, source_ref]
    )
    if ancestor_check.returncode != 0:
        raise ValueError(
            f"published source commit {marker} is not an ancestor of {source_ref}; "
            "the source history was probably rewritten"
        )

    commits = source_commits(source_repository, marker, source_ref)
    if not commits:
        return 0, git(public_worktree, "rev-parse", "HEAD").strip()

    original_checkout = current_checkout(source_repository)
    try:
        for source_commit in commits:
            git(source_repository, "checkout", "--detach", "--force", source_commit, capture=False)
            export_repository(source_repository, rendered_directory)
            copy_rendered_tree(rendered_directory, public_worktree)

            name, email, authored_date, message = commit_metadata(source_repository, source_commit)
            final_message = message_with_source_trailer(message, source_commit)
            environment = os.environ.copy()
            environment.update(
                {
                    "GIT_AUTHOR_NAME": name,
                    "GIT_AUTHOR_EMAIL": email,
                    "GIT_AUTHOR_DATE": authored_date,
                    "GIT_COMMITTER_NAME": "github-actions[bot]",
                    "GIT_COMMITTER_EMAIL": "41898282+github-actions[bot]@users.noreply.github.com",
                }
            )
            git(public_worktree, "add", "--all", capture=False)
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as message_file:
                message_file.write(final_message)
                message_path = Path(message_file.name)
            try:
                git(
                    public_worktree,
                    "commit",
                    "--allow-empty",
                    "--file",
                    str(message_path),
                    capture=False,
                    env=environment,
                )
            finally:
                message_path.unlink(missing_ok=True)
    finally:
        git(source_repository, "checkout", "--detach", "--force", original_checkout, capture=False)

    return len(commits), git(public_worktree, "rev-parse", "HEAD").strip()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("."))
    parser.add_argument("--source-ref", default="HEAD")
    parser.add_argument("--public-ref", default="origin/main")
    parser.add_argument("--public-worktree", type=Path, required=True)
    parser.add_argument("--rendered-directory", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        count, head = publish(
            args.source,
            args.source_ref,
            args.public_ref,
            args.public_worktree,
            args.rendered_directory,
        )
    except (ExportError, OSError, subprocess.CalledProcessError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Prepared {count} rendered commit(s); public HEAD is {head}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
