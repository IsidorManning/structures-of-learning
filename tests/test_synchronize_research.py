from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from publish_rendered import (git, publish_head, publication_pair, SyncConflict,
                              worktree, rendered_tree, normalized_tree)
from synchronize_research import synchronize, push


class SynchronizeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        subprocess.run(["git", "init", "-q", "--initial-branch=main", str(self.repo)], check=True)
        git(self.repo, "config", "user.name", "Research Author")
        git(self.repo, "config", "user.email", "author@example.com")
        (self.repo / "note.md").write_text("# Note\n\nOriginal claim.\n\n" + "Separate paragraph.\n\n" * 8, encoding="utf-8")
        (self.repo / "target.md").write_text("# Target\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "Initial research")
        git(self.repo, "branch", "source")
        self.edit("source", {"links.md": "# Links\n\nSee [[target|target]].\n"}, "Add Obsidian links")
        _, published = publish_head(self.repo, "source", "main")
        git(self.repo, "update-ref", "refs/heads/main", published)

    def tearDown(self):
        self.temporary.cleanup()

    def edit(self, branch, changes, message="Research edit"):
        with worktree(self.repo, branch) as checkout:
            for name, content in changes.items():
                path = checkout / name
                if content is None:
                    path.unlink()
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
            git(checkout, "add", "--all")
            git(checkout, "commit", "-qm", message)
            head = git(checkout, "rev-parse", "HEAD").strip()
        git(self.repo, "update-ref", f"refs/heads/{branch}", head)
        return head

    def content(self, ref, path):
        return git(self.repo, "show", f"{ref}:{path}")

    def accept(self, source, main):
        git(self.repo, "update-ref", "refs/heads/source", source)
        git(self.repo, "update-ref", "refs/heads/main", main)

    def test_direct_main_and_source_edits_survive_roundtrip_without_loops(self):
        main_commit = self.edit("main", {"main-only.md": "# Main contribution\n"}, "Markdown contribution")
        self.edit("source", {"source-only.md": "# Source contribution\n\n[[target]]\n"})
        (self.repo / "private-untracked.md").write_text("Private scratch work", encoding="utf-8")
        (self.repo / "note.md").write_text("Uncommitted local work", encoding="utf-8")
        original_head = git(self.repo, "rev-parse", "HEAD")
        original_status = git(self.repo, "status", "--porcelain")
        source, main = synchronize(self.repo, "source", "main")
        for name in ["main-only.md", "source-only.md"]:
            self.assertIn("contribution", self.content(source, name))
            self.assertIn("contribution", self.content(main, name))
        self.assertIn("[[target|target]]", self.content(source, "links.md"))
        self.assertIn("[target](target.md)", self.content(main, "links.md"))
        self.assertIn(f"Public-Commit: {main_commit}", git(self.repo, "log", "--format=%B", source))
        self.assertEqual(original_head, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(original_status, git(self.repo, "status", "--porcelain"))
        self.assertEqual("Uncommitted local work", (self.repo / "note.md").read_text())
        self.assertNotIn("private-untracked.md", git(self.repo, "ls-tree", "-r", "--name-only", main))
        self.accept(source, main)
        self.assertEqual((source, main), synchronize(self.repo, "source", "main"))

    def test_delete_modify_conflict_does_not_erase_research(self):
        self.edit("source", {"note.md": "# Note\n\nNew research claim.\n"})
        self.edit("main", {"note.md": None})
        refs = git(self.repo, "show-ref")
        with self.assertRaisesRegex(SyncConflict, "note.md"):
            synchronize(self.repo, "source", "main")
        self.assertEqual(refs, git(self.repo, "show-ref"))

    def test_generated_index_edit_is_rebuilt_without_becoming_source_prose(self):
        self.edit("source", {"literature/README.md": "# Literature\n\nHandwritten introduction.\n\n"})
        source, main = synchronize(self.repo, "source", "main")
        self.accept(source, main)
        text = self.content("main", "literature/README.md").replace("No literature notes yet.", "Stale generated content.")
        self.edit("main", {"literature/README.md": text})
        new_source, new_main = synchronize(self.repo, "source", "main")
        self.assertEqual(source, new_source)
        self.assertIn("Handwritten introduction.", self.content(new_main, "literature/README.md"))
        self.assertNotIn("Stale generated content.", self.content(new_main, "literature/README.md"))
        self.accept(new_source, new_main)
        self.assertEqual((new_source, new_main), synchronize(self.repo, "source", "main"))

    def test_independent_changes_in_same_note_preserve_wikilinks(self):
        text = self.content("source", "note.md")
        self.edit("source", {"note.md": text + "\nSee [[target]].\n"})
        self.edit("main", {"note.md": text.replace("Original claim.", "Corrected claim.")})
        source, main = synchronize(self.repo, "source", "main")
        self.assertIn("Corrected claim.", self.content(source, "note.md"))
        self.assertIn("[[target]]", self.content(source, "note.md"))
        self.assertIn("[target](target.md)", self.content(main, "note.md"))

    def test_conflicting_claims_leave_refs_and_checkout_unchanged(self):
        text = self.content("source", "note.md")
        self.edit("source", {"note.md": text.replace("Original claim.", "Source claim.")})
        self.edit("main", {"note.md": text.replace("Original claim.", "Main claim.")})
        refs = git(self.repo, "show-ref")
        status = git(self.repo, "status", "--porcelain")
        with self.assertRaisesRegex(SyncConflict, "note.md"):
            synchronize(self.repo, "source", "main")
        self.assertEqual(refs, git(self.repo, "show-ref"))
        self.assertEqual(status, git(self.repo, "status", "--porcelain"))

    def test_forward_publication_preserves_direct_main_edit_and_finds_older_marker(self):
        published_source = git(self.repo, "rev-parse", "source").strip()
        self.edit("main", {"main-only.md": "# Main\n"})
        self.edit("source", {"source-only.md": "# Source\n"})
        self.assertEqual(publication_pair(self.repo, "main")[1], published_source)
        _, head = publish_head(self.repo, "source", "main")
        self.assertEqual(self.content(head, "main-only.md"), "# Main\n")

    def test_legacy_manual_merge_wikilinks_are_converted_on_main(self):
        self.edit("main", {"legacy.md": "# Legacy\n\n[[target]]\n"})
        source, main = synchronize(self.repo, "source", "main")
        self.assertIn("[target](target.md)", self.content(source, "legacy.md"))
        self.assertIn("[target](target.md)", self.content(main, "legacy.md"))
        self.accept(source, main)
        self.assertEqual((source, main), synchronize(self.repo, "source", "main"))

    def test_format_only_main_merge_does_not_conflict_with_newer_source_link(self):
        published_source = git(self.repo, "rev-parse", "source").strip()
        self.edit("main", {"links.md": "# Links\n\nSee [target](target.md)."},
                  f"Legacy publication\n\nSource-Commit: {published_source}")
        self.edit("main", {"links.md": "# Links\n\nSee [[target|target]].\n"})
        self.edit("source", {"new.md": "# New target\n", "links.md": "# Links\n\nSee [[new|new target]].\n"})
        source, main = synchronize(self.repo, "source", "main")
        self.assertIn("[[new|new target]]", self.content(source, "links.md"))
        self.assertIn("[new target](new.md)", self.content(main, "links.md"))

    def test_renames_deletions_and_binary_files_are_preserved(self):
        text = self.content("source", "note.md")
        self.edit("main", {"note.md": None, "renamed.md": text, "image.bin": b"\x00\x01\xff"})
        source, main = synchronize(self.repo, "source", "main")
        for ref in [source, main]:
            files = git(self.repo, "ls-tree", "-r", "--name-only", ref).splitlines()
            self.assertNotIn("note.md", files)
            self.assertIn("renamed.md", files)
            self.assertIn("image.bin", files)
        self.accept(source, main)
        self.edit("source", {"renamed.md": None})
        source, main = synchronize(self.repo, "source", "main")
        self.assertNotIn("renamed.md", git(self.repo, "ls-tree", "-r", "--name-only", main))

    def test_index_is_rebuilt_from_combined_collection(self):
        def paper(key):
            return f'---\ntype: literature\ncitekey: {key}\ntitle: Paper {key}\ntopic: Categories\nsubtopic: Learning\n---\n'
        self.edit("source", {"literature/source.md": paper("Source")})
        self.edit("main", {"literature/main.md": paper("Main")})
        source, main = synchronize(self.repo, "source", "main")
        index = self.content(main, "literature/README.md")
        self.assertIn("Paper Source", index)
        self.assertIn("Paper Main", index)
        self.assertIn("### Learning", index)
        self.accept(source, main)
        self.assertEqual((source, main), synchronize(self.repo, "source", "main"))

    def test_deleting_paper_on_main_rebuilds_stale_index(self):
        paper = '---\ntype: literature\ncitekey: DeleteMe\ntitle: Delete me\n---\n'
        self.edit("source", {"literature/paper.md": paper})
        source, main = synchronize(self.repo, "source", "main")
        self.accept(source, main)
        self.edit("main", {"literature/paper.md": None})
        # The workflow's initial validation must tolerate the now-stale derived link.
        from export_notes import export_repository
        with worktree(self.repo, "main") as checkout:
            export_repository(checkout)
        source, main = synchronize(self.repo, "source", "main")
        self.assertNotIn("Delete me", self.content(main, "literature/README.md"))

    def test_atomic_push_rejects_concurrent_edit_without_updating_other_branch(self):
        remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        git(self.repo, "remote", "add", "origin", str(remote))
        push(self.repo, "origin", "source", "main")
        old_source = git(remote, "rev-parse", "source")
        self.edit("source", {"incoming.md": "# Source\n"})
        source, main = synchronize(self.repo, "source", "main")
        concurrent = self.edit("main", {"concurrent.md": "# Concurrent\n"})
        git(self.repo, "push", "origin", "main:main")
        with self.assertRaises(subprocess.CalledProcessError):
            push(self.repo, "origin", source, main)
        self.assertEqual(old_source, git(remote, "rev-parse", "source"))
        self.assertEqual(concurrent, git(remote, "rev-parse", "main").strip())

    def test_repaired_metadata_in_history_can_publish_but_final_duplicates_fail(self):
        note = "---\nid: Duplicate\n---\n# Note\n"
        self.edit("source", {"first.md": note, "second.md": note})
        refs = git(self.repo, "show-ref")
        with self.assertRaisesRegex(Exception, "duplicate id"):
            synchronize(self.repo, "source", "main")
        self.assertEqual(refs, git(self.repo, "show-ref"))
        self.edit("source", {"second.md": note.replace("Duplicate", "Distinct")})
        source, main = synchronize(self.repo, "source", "main")
        self.assertIn("Distinct", self.content(main, "second.md"))
        self.assertEqual(rendered_tree(self.repo, source), normalized_tree(self.repo, main))

    def test_server_code_stays_on_main_and_source_only_push_does_not_change_source(self):
        self.edit("main", {"scripts/server.txt": "new server", "tests/server.txt": "server tests"})
        original = self.edit("source", {"scripts/server.txt": "old server", "new-note.md": "# New note\n"})
        source, main = synchronize(self.repo, "source", "main")
        self.assertEqual(original, source)
        self.assertEqual("new server", self.content(main, "scripts/server.txt"))
        self.assertEqual("old server", self.content(source, "scripts/server.txt"))
        self.assertNotIn("tests/server.txt", git(self.repo, "ls-tree", "-r", "--name-only", source))

