from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from publish_rendered import publish  # noqa: E402


class PublishRenderedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repository"
        subprocess.run(["git", "init", "-q", "--initial-branch=main", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test Committer"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "committer@example.com"], check=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, path: str, content: str) -> None:
        destination = self.repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    def commit(self, message: str, author_name: str, author_email: str, date: str) -> str:
        subprocess.run(["git", "-C", str(self.repo), "add", "--all"], check=True)
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_AUTHOR_NAME": author_name,
                "GIT_AUTHOR_EMAIL": author_email,
                "GIT_AUTHOR_DATE": date,
                "GIT_COMMITTER_DATE": date,
            }
        )
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-q", "-m", message],
            check=True,
            env=environment,
        )
        return subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()

    def test_replays_source_commit_with_rendered_tree_and_original_metadata(self) -> None:
        self.write("target.md", "# Target\n")
        self.write("note.md", "# Note\n")
        self.commit("Initial research map", "Initial Author", "initial@example.com", "2026-08-26T10:00:00+00:00")
        subprocess.run(["git", "-C", str(self.repo), "branch", "source"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "switch", "-q", "source"], check=True)

        self.write("note.md", "# Note\n\nSee [[target|the target]].\n")
        first_source_commit = self.commit(
            "Connect the research notes\n\nExplain the relationship.",
            "Isidor Example",
            "isidor@example.com",
            "2026-08-27T20:15:00+00:00",
        )
        self.write("target.md", "# Target\n\nA concise summary.\n")
        source_commit = self.commit(
            "Summarize the target note",
            "Isidor Example",
            "isidor@example.com",
            "2026-08-27T21:00:00+00:00",
        )

        count, public_head = publish(
            self.repo,
            "source",
            "main",
            self.root / "public",
            self.root / "rendered",
        )

        self.assertEqual(count, 2)
        self.assertIn("[the target](target.md)", (self.root / "public/note.md").read_text())
        metadata = subprocess.run(
            ["git", "-C", str(self.root / "public"), "show", "-s", "--format=%an%x00%ae%x00%aI%x00%B", public_head],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        name, email, date, message = metadata.split("\0", 3)
        self.assertEqual(name, "Isidor Example")
        self.assertEqual(email, "isidor@example.com")
        self.assertEqual(date, "2026-08-27T21:00:00Z")
        self.assertTrue(message.startswith("Summarize the target note"))
        self.assertIn(f"Source-Commit: {source_commit}", message)
        self.assertNotEqual(public_head, source_commit)
        subjects = subprocess.run(
            ["git", "-C", str(self.root / "public"), "log", "-2", "--format=%s"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.splitlines()
        self.assertEqual(subjects, ["Summarize the target note", "Connect the research notes"])
        first_public_message = subprocess.run(
            ["git", "-C", str(self.root / "public"), "show", "-s", "--format=%B", "HEAD^"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        self.assertIn("Explain the relationship.", first_public_message)
        self.assertIn(f"Source-Commit: {first_source_commit}", first_public_message)

    def test_configures_plain_push_to_remote_source(self) -> None:
        subprocess.run(["git", "-C", str(self.repo), "remote", "add", "origin", "https://example.invalid/repo.git"], check=True)
        subprocess.run(
            ["bash", str(ROOT / "scripts/configure-obsidian-git.sh")],
            cwd=self.repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )

        def config(key: str) -> str:
            return subprocess.run(
                ["git", "-C", str(self.repo), "config", "--get", key],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()

        self.assertEqual(config("remote.origin.push"), "refs/heads/main:refs/heads/source")
        self.assertEqual(config("branch.main.merge"), "refs/heads/source")
        self.assertEqual(config("push.default"), "upstream")


if __name__ == "__main__":
    unittest.main()
