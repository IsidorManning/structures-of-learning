from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from export_notes import ExportError, export_repository  # noqa: E402
from note_format import LEGACY_NOTICE


class ExportNotesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "source"
        self.output = Path(self.temporary.name) / "rendered"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def add(self, path: str, content: str | bytes) -> None:
        destination = self.repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            destination.write_bytes(content)
        else:
            destination.write_text(content, encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", "--", path], check=True)

    def test_converts_relative_basename_heading_and_pdf_links(self) -> None:
        self.add("literature/paper.md", "# A Paper\n\n## Main Result\n")
        self.add("papers/draft.pdf", b"%PDF-example")
        self.add(
            "threads/topic/questions/question.md",
            "---\nid: Q-1\ntype: question\n---\n\n"
            "[[../../../literature/paper|Paper]]\n"
            "[[paper#Main Result|result]]\n"
            "[[../../../papers/draft.pdf|draft]]\n",
        )

        export_repository(self.repo, self.output)

        rendered = (self.output / "threads/topic/questions/question.md").read_text()
        self.assertIn("[Paper](../../../literature/paper.md)", rendered)
        self.assertIn("[result](../../../literature/paper.md#main-result)", rendered)
        self.assertIn("[draft](../../../papers/draft.pdf)", rendered)
        self.assertEqual((self.output / "papers/draft.pdf").read_bytes(), b"%PDF-example")

    def test_preserves_frontmatter_fenced_code_inline_code_and_comments(self) -> None:
        self.add("target.md", "# Target\n")
        self.add(
            "source.md",
            "---\nid: Q-2\n---\n\n[[target]]\n\n"
            "```md\n[[not-a-link]]\n```\n"
            "`[[also-not-a-link]]`\n"
            "<!-- [[comment-link]] -->\n",
        )

        export_repository(self.repo, self.output)

        rendered = (self.output / "source.md").read_text()
        self.assertTrue(rendered.startswith("---\nid: Q-2\n---\n"))
        self.assertIn("[target](target.md)", rendered)
        self.assertIn("```md\n[[not-a-link]]\n```", rendered)
        self.assertIn("`[[also-not-a-link]]`", rendered)
        self.assertIn("<!-- [[comment-link]] -->", rendered)

    def test_converts_image_embed(self) -> None:
        self.add("assets/diagram.png", b"png")
        self.add("notes/note.md", "![[../assets/diagram.png|Diagram]]\n")

        export_repository(self.repo, self.output)

        self.assertIn("![Diagram](../assets/diagram.png)", (self.output / "notes/note.md").read_text())

    def test_drops_legacy_banner_without_adding_a_new_one(self) -> None:
        self.add("note.md", "---\nid: Q-clean\n---\n\n" + LEGACY_NOTICE + "\n\n# Note\n")
        export_repository(self.repo, self.output)
        rendered = (self.output / "note.md").read_text()
        self.assertNotIn(LEGACY_NOTICE, rendered)
        self.assertEqual("---\nid: Q-clean\n---\n\n# Note\n", rendered)

    def test_rendering_normalizes_a_missing_final_newline(self) -> None:
        self.add("note.md", "# Note")
        export_repository(self.repo, self.output)
        self.assertEqual("# Note\n", (self.output / "note.md").read_text())

    def test_validates_normal_markdown_links_and_ignores_code(self) -> None:
        self.add("target space.md", "# Target\n\n## Result\n")
        self.add("note.md", "[Result](target%20space.md#result)\n`[Example](missing.md)`\n[Web](https://example.org)\n")
        export_repository(self.repo, self.output)
        self.add("note.md", "[Missing](missing.md)\n[Wrong heading](target%20space.md#wrong)\n")
        with self.assertRaises(ExportError) as context:
            export_repository(self.repo, self.output)
        self.assertIn("Markdown target does not exist", str(context.exception))
        self.assertIn("Markdown heading does not exist", str(context.exception))

    def test_exports_only_git_tracked_files(self) -> None:
        self.add("public.md", "# Public\n")
        private = self.repo / "private.md"
        private.write_text("# Private\n", encoding="utf-8")

        export_repository(self.repo, self.output)

        self.assertTrue((self.output / "public.md").exists())
        self.assertFalse((self.output / "private.md").exists())

    def test_reports_missing_ambiguous_and_frontmatter_links(self) -> None:
        self.add("a/shared.md", "# A\n")
        self.add("b/shared.md", "# B\n")
        self.add("source.md", "---\nparent: \"[[a/shared]]\"\n---\n[[missing]]\n[[shared]]\n")

        with self.assertRaises(ExportError) as context:
            export_repository(self.repo, self.output)

        message = str(context.exception)
        self.assertIn("wikilinks are not allowed in YAML frontmatter", message)
        self.assertIn("target does not exist: missing", message)
        self.assertIn("ambiguous basename 'shared'", message)
        self.assertFalse(self.output.exists())

    def test_reports_duplicate_ids_and_missing_headings(self) -> None:
        self.add("one.md", "---\nid: duplicate\n---\n# One\n")
        self.add("two.md", "---\nid: duplicate\n---\n[[one#Unknown]]\n")

        with self.assertRaises(ExportError) as context:
            export_repository(self.repo, self.output)

        message = str(context.exception)
        self.assertIn("duplicate id 'duplicate'", message)
        self.assertIn("heading does not exist in one.md: Unknown", message)


if __name__ == "__main__":
    unittest.main()

