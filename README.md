# Structures of Learning

A research map for questioning, understanding, and developing mathematical structures of deep learning (and potentially of systems that learn more generally).

My motivation is to contribute to theoretical work that aims to _explain_ the behavior of learning systems through _useful_ mathematical abstractions. The goal is for these abstractions to become not only descriptive and prescriptive, but eventually _predictive_: to lead to falsifiable predictions that can either provide new insight into deep learning or force us to refine the abstractions themselves, bringing them into closer alignment with the phenomena they are meant to describe.

The repository develops this map through questions, mathematical constructions, literature notes, and experiments. It is intentionally a work in progress: questions may be incomplete and informal, conjectures and mathematics may be wrong, and the structure of the map itself will change as my understanding changes.

# Theories & Mathematics
Currently, the theories mostly being explored in this project are Categorical Deep Learning (CDL) and Neuroalgebriac Geometry.

# Literature & Resources

See [`literature/README.md`](literature/README.md).

# Reading the repository

- [`main`](https://github.com/IsidorManning/structures-of-learning/tree/main) is the public, GitHub-friendly research map. It is generated automatically.
- [`source`](https://github.com/IsidorManning/structures-of-learning/tree/source) is the Obsidian source. It intentionally contains relative Obsidian wikilinks.

I write in Obsidian, so I do not edit the remote `main` branch directly. Instead, changes belong in the Obsidian source and are published automatically.

## Publication pipeline for Obsidian

The vault remains unchanged on the local machine. Its branch is still named `main`, but repository-local Git configuration maps it to the remote `source` branch:

1. Write in Obsidian using `[[wikilinks]]`, aliases, headings, and embeds.
2. Commit with an ordinary, meaningful message.
3. Run plain `git push`. Local `main` is sent to remote `source`.
4. GitHub Actions checks out the repository on a temporary runner.
5. `scripts/export_notes.py` validates every tracked wikilink and creates a converted snapshot.
6. `scripts/publish_rendered.py` commits that snapshot to remote `main`, preserving the source commit's author, authored date, subject, and body.

Only files returned by `git ls-files` are copied. Ignored and untracked vault files are never part of the rendered output.

The public and source commit hashes differ because their Markdown trees differ. Generated commits carry a `Source-Commit` trailer for synchronization, while retaining the human-written commit message. GitHub Actions appears as the committer; the original writer remains the author.

### Configure an Obsidian checkout

Run this once in each local clone used as an Obsidian vault:

```bash
bash scripts/configure-obsidian-git.sh
```

It configures only this repository:

```text
local main  --git push-->  origin/source
local main  <--git pull--  origin/source
origin/source  --GitHub Actions-->  origin/main
```

Afterward, the normal loop is unchanged:

```bash
git add .
git commit -m "Connect geometric and logical priors"
git push
```

Use argument-free `git push`. An explicit `git push origin main` bypasses the repository's mapping and targets the generated public branch.

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
