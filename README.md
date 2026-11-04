# Structures of Learning

A research map for developing abstractions and formal mathematics to understand systems that learn .

My motivation is to contribute to theoretical work that aims to _explain_ the behavior of learning systems through _useful_ mathematical abstractions. The goal is for these abstractions to become not only descriptive and prescriptive, but eventually _predictive_: to lead to falsifiable predictions that can either provide new insight into deep learning or force us to refine the abstractions themselves, bringing them into closer alignment with the phenomena they are meant to describe.

The repository develops this map through questions, mathematical constructions, literature notes, and experiments. It is intentionally a work in progress: questions may be incomplete and informal, conjectures and mathematics may be wrong, and the structure of the map itself will change as my understanding changes. I personally see this as a middle-ground between an informal idea and a complete paper.

# Literature & Resources

See [`literature/README.md`](literature/README.md).

To copy a paper's bibliographic metadata from personal Obsidian notes into a
project relevance note, see the [literature import setup](https://github.com/IsidorManning/structures-of-learning/blob/main/docs/literature-workflow.md).
GitHub publication generates a literature index grouped by topic and subtopic.

# Reading the repository

- [`main`](https://github.com/IsidorManning/structures-of-learning/tree/main) is the public, GitHub-friendly research map. Edit ordinary Markdown and code here directly.
- [`source`](https://github.com/IsidorManning/structures-of-learning/tree/source) is the Obsidian source. It intentionally contains relative Obsidian wikilinks. 

Obsidian edits go through `source` so wikilinks can be converted. Ordinary
Markdown and code edits can go directly to `main`. GitHub Actions reconciles
both directions, preserving existing wikilinks in `source` where changes merge
cleanly. New Markdown links from `main` remain Markdown links in Obsidian.

## Publication pipeline for Obsidian

The vault remains unchanged on the local machine. Its branch is still named `main`, but repository-local Git configuration maps it to the remote `source` branch:

1. Write in Obsidian using `[[wikilinks]]`, aliases, headings, and embeds.
2. Commit with an ordinary, meaningful message.
3. Run plain `git push`. Local `main` is sent to remote `source`.
4. GitHub Actions fetches the latest `source` and `main` on a temporary runner.
5. Direct edits on `main` are merged back into `source`; source changes are rendered and merged into `main`.
6. The literature index is rebuilt from the combined project notes, and both snapshots are validated.
7. Both branch heads are pushed atomically. A conflicting passage or a concurrent edit stops the update rather than overwriting work.

Only files returned by `git ls-files` are copied. Ignored and untracked vault files are never part of the rendered output.

The public and source commit hashes differ because their Markdown trees differ.
Publication commits carry a `Source-Commit` trailer; mirrored main commits carry
a `Public-Commit` trailer. Replayed commits retain the writer's author, authored
date, subject, and body. GitHub Actions is the committer. Cleanup and index-only
maintenance commits use the bot as author.

### Configure an Obsidian checkout

Run this once in each local clone used as an Obsidian vault:

```bash
bash scripts/configure-obsidian-git.sh
```

It configures only this repository:

```text
local main  --git push-->  origin/source
local main  <--git pull--  origin/source
origin/source  <--GitHub Actions-->  origin/main
```

Afterward, the normal loop is unchanged:

```bash
git add .
git commit -m "Connect geometric and logical priors"
git push
```

Use argument-free `git push` in this Obsidian checkout. An explicit
`git push origin main` bypasses its mapping and sends unconverted Obsidian files
to the public branch. To work directly on `main`, use GitHub's editor or a
separate normal checkout tracking `origin/main`.

After synchronization, pull before starting your next edit or push. Source can
now receive automated commits containing direct main edits. If you already have
local commits, merge the incoming source history without rewriting published
history, resolve any local conflict, then push normally.

### Literature index

Edit each paper's `topic` and optional `subtopic` properties to organize the
literature README. Only the region between the `literature-index:start` and
`literature-index:end` comments is generated. The surrounding introduction and
any historical manual index stay editable. Notes without topics appear under
Uncategorized. The generated region is excluded from branch merges and rebuilt
from the final combined collection on `main`.

### Preview and conflict recovery

With the Python dependencies installed, preview synchronization without moving
any local or remote branch refs:

```bash
git fetch origin main source
python scripts/synchronize_research.py
```

The command creates temporary worktrees and Git objects; it never checks out,
resets, stages, or commits files in your active vault. Git 2.38 or newer is
required for three-way tree merging. Add `--push` only when you intend to publish
the prepared result to both remote branches.

If synchronization fails, open the failed Actions run. Its summary and
`research-sync-report` artifact identify conflicting paths and the incoming
commit. Reconcile the conflicting edits on the appropriate editing branch and
push again. Do not merge the whole rendered branch into the Obsidian branch or
force-push to clear a conflict. A concurrency rejection needs a fresh run against
the latest heads; the workflow can be rerun manually.

Pull requests run validation only. Pushes to either branch and manual runs
perform synchronization. All validation happens before the atomic push; bot
pushes do not need to trigger a second workflow.

### Supported Obsidian links

| Obsidian source | GitHub rendering |
|---|---|
| `[[note]]` | Link to the unique `note.md` in the repository |
| `[[../path/note]]` | Relative link to `../path/note.md` |
| `[[note|label]]` | Markdown link with `label` as its text |
| `[[note#Heading|label]]` | Link to the target's GitHub heading anchor |
| `![[image.png|alt text]]` | Markdown image embed |
| `[[paper.pdf|label]]` | Markdown link to the PDF |

Wikilinks in YAML frontmatter are rejected. Research relations belong in the visible `## Relations` section so they work in Obsidian and become readable on GitHub.

## Validation

Publication stops on missing or ambiguous targets, missing headings, links outside the repository, wikilinks in YAML, and duplicate `id` or `citekey` values. Run the same checks manually, without changing any files, with:

```bash
python scripts/export_notes.py --source . --check
```

Both wikilinks and ordinary inline Markdown links to local files and headings
are checked. External web links are left intact. Final source and public
snapshots must pass all checks; repaired duplicate metadata in intermediate
historical commits does not block replay.

Automation code and tests are maintained on GitHub's main branch. The source
branch needs only the hidden workflow dispatcher; it does not need local
dependencies or build scripts to publish notes. Infrastructure paths are
excluded from content synchronization.

The public root README and literature README are maintained on `main` as well.
Their publication updates do not rewrite your Obsidian index files. The earlier
manual literature index is preserved in `docs/literature-index-before-automation.md`.

