# Structures of Learning

A research map for developing mathematical structures of learning.

## Reading the repository

- [`main`](https://github.com/IsidorManning/structures-of-learning/tree/main) is the canonical Obsidian source. It intentionally contains Obsidian wikilinks.
- [`rendered`](https://github.com/IsidorManning/structures-of-learning/tree/rendered) is the generated GitHub-friendly mirror. Its wikilinks are ordinary Markdown links.

Do not edit `rendered` directly. Every push to `main` rebuilds and replaces it.

## Publication pipeline

The vault remains unchanged on the local machine:

1. Write in Obsidian using `[[wikilinks]]`, aliases, headings, and embeds.
2. Commit and push to `main` as usual.
3. GitHub Actions checks out the repository on a temporary runner.
4. `scripts/export_notes.py` validates every tracked wikilink and writes a converted mirror to `.build/rendered` on that runner.
5. If validation succeeds, the action force-publishes that mirror as the `rendered` branch.

Only files returned by `git ls-files` are copied. Ignored and untracked vault files are never part of the rendered output.

## Supported Obsidian links

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

The publication stops on missing or ambiguous targets, missing headings, links outside the repository, wikilinks in YAML, and duplicate `id` or `citekey` values. Run the same checks manually, without changing any files, with:

```bash
python scripts/export_notes.py --source . --check
```

# Theories & Mathematics

# Themes

# Literature & Resources

See [`literature/README.md`](literature/README.md).
