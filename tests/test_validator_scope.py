import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ATTEMPT = (
    SOURCE_ROOT
    / "problems"
    / "erdos-straus"
    / "attempts"
    / "2026-08-24-baseline-witness-harness-k7f2"
)


class ValidatorScopeTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name) / "repo"
        shutil.copytree(
            SOURCE_ROOT,
            self.repo,
            ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"),
        )
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("config", "user.email", "scope-tests@openmaths.invalid")
        self.git("config", "user.name", "OpenMaths scope tests")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "base")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def tearDown(self):
        self.tempdir.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=True,
        )

    def commit_changes(self):
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "test change")

    def add_attempt(self, attempt_id, status="exploration"):
        target = (
            self.repo
            / "problems"
            / "erdos-straus"
            / "attempts"
            / attempt_id
        )
        shutil.copytree(SOURCE_ATTEMPT, target)
        metadata = target / "attempt.yaml"
        text = metadata.read_text(encoding="utf-8")
        text = text.replace(SOURCE_ATTEMPT.name, attempt_id)
        text = text.replace("status: exploration", f"status: {status}")
        metadata.write_text(text, encoding="utf-8")
        return target

    def validate(self):
        return subprocess.run(
            [sys.executable, "scripts/validate.py", "--base", self.base],
            cwd=self.repo,
            capture_output=True,
            text=True,
        )

    def assert_invalid(self, expected):
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(expected, result.stderr)

    def test_project_pr_without_attempt_changes_is_allowed(self):
        readme = self.repo / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        self.commit_changes()
        self.assertEqual(self.validate().returncode, 0)

    def test_one_new_exploration_attempt_is_allowed(self):
        self.add_attempt("2026-08-24-scope-test-a1b2")
        self.commit_changes()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_attempt_pr_cannot_change_readme(self):
        self.add_attempt("2026-08-24-scope-test-a1b2")
        readme = self.repo / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nout of scope\n", encoding="utf-8")
        self.commit_changes()
        self.assert_invalid("attempt PRs may change only")

    def test_attempt_pr_cannot_add_two_attempts(self):
        self.add_attempt("2026-08-24-scope-test-a1b2")
        self.add_attempt("2026-08-24-scope-test-c3d4")
        self.commit_changes()
        self.assert_invalid("an attempt PR may add one")

    def test_new_attempt_must_start_at_exploration(self):
        self.add_attempt("2026-08-24-scope-test-a1b2", status="candidate")
        self.commit_changes()
        self.assert_invalid("new attempts must use claim.status 'exploration'")

    def test_existing_attempt_content_is_append_only(self):
        writeup = (
            self.repo
            / "problems"
            / "erdos-straus"
            / "attempts"
            / SOURCE_ATTEMPT.name
            / "WRITEUP.md"
        )
        writeup.write_text(writeup.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        self.commit_changes()
        self.assert_invalid("existing attempts are append-only")

    def test_steward_can_update_only_existing_attempt_metadata(self):
        metadata = (
            self.repo
            / "problems"
            / "erdos-straus"
            / "attempts"
            / SOURCE_ATTEMPT.name
            / "attempt.yaml"
        )
        text = metadata.read_text(encoding="utf-8")
        metadata.write_text(text.replace("status: exploration", "status: candidate"), encoding="utf-8")
        self.commit_changes()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
