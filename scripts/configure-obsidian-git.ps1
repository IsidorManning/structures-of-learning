$ErrorActionPreference = "Stop"

$repositoryRoot = (git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) {
    throw "Run this script inside the structures-of-learning Git repository."
}

$currentBranch = (git -C $repositoryRoot branch --show-current).Trim()
if ($currentBranch -ne "main") {
    throw "Expected the local Obsidian branch to be named 'main'; found '$currentBranch'."
}

git -C $repositoryRoot remote get-url origin | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "This repository does not have an 'origin' remote."
}

git -C $repositoryRoot config remote.origin.push refs/heads/main:refs/heads/source
git -C $repositoryRoot config branch.main.remote origin
git -C $repositoryRoot config branch.main.merge refs/heads/source
git -C $repositoryRoot config push.default upstream

if ($LASTEXITCODE -ne 0) {
    throw "Git configuration failed."
}

Write-Host "Configured this checkout:"
Write-Host "  local main -> git push -> origin/source"
Write-Host "  origin/source -> git pull -> local main"
Write-Host ""
Write-Host "GitHub Actions publishes the converted result to origin/main."
Write-Host "Use plain 'git push'; do not explicitly run 'git push origin main'."
