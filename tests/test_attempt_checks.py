import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parent.parent


class AttemptCheckSelectionTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name) / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        shutil.copy2(SOURCE_ROOT / "scripts" / "run_attempt_checks.py", self.repo / "scripts")
        self.make_runner("old-attempt", "old runner")
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("config", "user.email", "runner-tests@openmaths.invalid")
        self.git("config", "user.name", "OpenMaths runner tests")
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

    def make_runner(self, attempt, message):
        runner = self.repo / "problems" / "test-problem" / "attempts" / attempt / "code" / "run.sh"
        runner.parent.mkdir(parents=True)
        runner.write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\n" f"echo '{message}'\n",
            encoding="utf-8",
        )

    def run_checks(self, *args):
        return subprocess.run(
            [sys.executable, "scripts/run_attempt_checks.py", *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
        )

    def test_base_selects_only_changed_attempt_runner(self):
        self.make_runner("new-attempt", "new runner")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "new attempt")

        result = self.run_checks("--base", self.base)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("new runner", result.stdout)
        self.assertNotIn("old runner", result.stdout)

    def test_no_base_runs_full_historical_suite(self):
        self.make_runner("new-attempt", "new runner")

        result = self.run_checks()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("old runner", result.stdout)
        self.assertIn("new runner", result.stdout)


if __name__ == "__main__":
    unittest.main()
