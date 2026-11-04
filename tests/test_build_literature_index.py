from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_literature_index import build_index, update_readme
from export_notes import export_repository
import subprocess


class LiteratureIndexTests(unittest.TestCase):
    def test_groups_metadata_and_preserves_manual_content_idempotently(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "paper space.md").write_text('---\ntype: literature\ncitekey: X\nauthors: ["Example, Alice", "Bob Other"]\nyear: 2026\ntopic: Categories\nsubtopic: Differentiation\n---\n# A Paper\n', encoding="utf-8")
            (root / "README.md").write_text("# Literature\n\nMy curated introduction.\n", encoding="utf-8")
            update_readme(root)
            result = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("My curated introduction.", result)
            self.assertIn("## Categories\n\n### Differentiation", result)
            self.assertIn("Example et al. (2026)", result)
            self.assertIn("paper%20space.md", result)
            update_readme(root)
            self.assertEqual(result, (root / "README.md").read_text(encoding="utf-8"))

    def test_missing_topics_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            text = '---\ntype: literature\ncitekey: X\n---\n# Paper\n'
            (root / "one.md").write_text(text, encoding="utf-8")
            self.assertIn("## Uncategorized", build_index(root))
            (root / "two.md").write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate citekey"):
                build_index(root)

    def test_export_builds_index_without_modifying_source_or_including_untracked_notes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            folder = root / "literature"
            folder.mkdir()
            (folder / "README.md").write_text("# Literature\n", encoding="utf-8")
            (folder / "paper.md").write_text('---\ntype: literature\ncitekey: X\ntitle: Public paper\n---\n', encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            (folder / "private.md").write_text('---\ntype: literature\ncitekey: Private\ntitle: Private paper\n---\n', encoding="utf-8")
            output = root.parent / "output"
            export_repository(root, output)
            result = (output / "literature/README.md").read_text(encoding="utf-8")
            self.assertIn("Public paper", result)
            self.assertNotIn("Private paper", result)
            self.assertEqual("# Literature\n", (folder / "README.md").read_text(encoding="utf-8"))

