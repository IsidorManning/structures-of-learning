#!/usr/bin/env bash
set -euo pipefail

repository_root="$(git rev-parse --show-toplevel)"
current_branch="$(git -C "$repository_root" branch --show-current)"

if [[ "$current_branch" != "main" ]]; then
  echo "Expected the local Obsidian branch to be named 'main'; found '$current_branch'." >&2
  exit 1
fi

if ! git -C "$repository_root" remote get-url origin >/dev/null 2>&1; then
  echo "This repository does not have an 'origin' remote." >&2
  exit 1
fi

git -C "$repository_root" config remote.origin.push refs/heads/main:refs/heads/source
git -C "$repository_root" config branch.main.remote origin
git -C "$repository_root" config branch.main.merge refs/heads/source
git -C "$repository_root" config push.default upstream

echo "Configured this checkout:"
echo "  local main -> git push -> origin/source"
echo "  origin/source -> git pull -> local main"
echo
echo "GitHub Actions publishes the converted result to origin/main."
echo "Use plain 'git push'; do not explicitly run 'git push origin main'."
